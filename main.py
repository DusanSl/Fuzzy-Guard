import gzip
import os
from collections import OrderedDict, deque
from pathlib import Path
from threading import Lock
from time import monotonic

from flask import Flask, Response, jsonify, render_template, request, url_for
from werkzeug.exceptions import HTTPException
from werkzeug.middleware.proxy_fix import ProxyFix

from obrada_teksta.analizator import (
    VALIDNI_RECNICI,
    analiziraj_email,
    ucitaj_sve_primere,
)
from fazi.skupovi import IZLAZNI_SKUPOVI_DEFINICIJE, ULAZNI_SKUPOVI_DEFINICIJE
from fazi.zakljucivanje import pokreni_fis
from neuronska_mreza.predikcija import pouzdanje_nn

KOREN = Path(__file__).parent
MAKS_DUŽINA_ZAHTEVA = 256 * 1024
MAKS_ANALIZIRANIH_ZNAKOVA = 10_000

# Šabloni dodaju ?v=<mtime> na CSS i JS, pa statika može dugo da se kešira:
# novi sadržaj uvek dobija novi URL.
KEŠIRANJE_STATIKE_SEKUNDI = 365 * 24 * 60 * 60

BEZBEDNOSNA_ZAGLAVLJA = {
    "X-Content-Type-Options": "nosniff",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "X-Frame-Options": "DENY",
    # Aplikacija ne koristi kameru, mikrofon, lokaciju ni plaćanje.
    "Permissions-Policy": "camera=(), microphone=(), geolocation=(), payment=(), usb=()",
    # Sprečava da druga strana otvori aplikaciju u prozoru i komunicira sa njom.
    "Cross-Origin-Opener-Policy": "same-origin",
    "Cross-Origin-Resource-Policy": "same-origin",
    "Content-Security-Policy": (
        "default-src 'self'; base-uri 'none'; object-src 'none'; "
        "frame-ancestors 'none'; form-action 'self'; connect-src 'self'; "
        "img-src 'self' data:; font-src 'self'; "
        # engine.js upisuje style atribute (širine traka), pa je
        # 'unsafe-inline' potreban samo za stilove. Skripte ostaju 'self'.
        "style-src 'self' 'unsafe-inline'; script-src 'self'"
    ),
}

app = Flask(
    __name__,
    template_folder=str(KOREN / "veb" / "sabloni"),
    static_folder=str(KOREN / "veb" / "static"),
)
app.config["MAX_CONTENT_LENGTH"] = MAKS_DUŽINA_ZAHTEVA
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = KEŠIRANJE_STATIKE_SEKUNDI

# Broj slojeva obrnutog proksija ispred aplikacije. Podrazumevano 0: tada se
# X-Forwarded-* ignorišu, pa klijent ne može da lažira svoju IP adresu i zaobiđe
# ograničenje zahteva. Na hostingu iza proksija postaviti na broj slojeva:
#
#     FUZZY_GUARD_PROXY_SLOJEVI=1
#
# Bez toga bi svi posetioci delili jednu IP adresu, a HSTS se ne bi slao.
PROXY_SLOJEVI = int(os.environ.get("FUZZY_GUARD_PROXY_SLOJEVI", "0"))
if PROXY_SLOJEVI > 0:
    app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=PROXY_SLOJEVI, x_proto=PROXY_SLOJEVI
    )

# Gzip se primenjuje samo na tekstualne odgovore. Ispod ovog praga kompresija
# troši više bajtova na zaglavlja nego što uštedi.
MAKS_NEKOMPRESOVANO = 512
TIPOVI_ZA_KOMPRESIJU = frozenset({
    "text/html",
    "text/css",
    "text/plain",
    "text/javascript",
    "application/javascript",
    "application/json",
    "application/xml",
    "image/svg+xml",
})

# Jednostavan klizni prozor po IP adresi. Dovoljno za javni demo i zaštitu od
# slučajnog ili namernog spamovanja skupog /analiziraj endpointa. Granice se
# mogu podesiti bez izmene koda:
#
#     FUZZY_GUARD_GRANICA_ZAHTEVA=120
#     FUZZY_GUARD_PROZOR_ZAHTEVA=60
GRANICA_ZAHTEVA = int(os.environ.get("FUZZY_GUARD_GRANICA_ZAHTEVA", "120"))
PROZOR_ZAHTEVA = float(os.environ.get("FUZZY_GUARD_PROZOR_ZAHTEVA", "60"))
# Gornja granica broja IP korpi. Bez nje bi mreža jednokratnih klijenata
# trajno punila rečnik, jer se prazne korpe brišu samo kad ista IP ponovo dođe.
MAKS_IP_KORPI = 2000
_zahtevi_po_ip = OrderedDict()
_zahtevi_lock = Lock()


def _dozvoli_zahtev(ip_adresa: str) -> bool:
    sada = monotonic()
    with _zahtevi_lock:
        red = _zahtevi_po_ip.get(ip_adresa)
        if red is None:
            red = deque()
            _zahtevi_po_ip[ip_adresa] = red
        else:
            # LRU: aktivan klijent ide na kraj, pa se najstariji brišu prvi.
            _zahtevi_po_ip.move_to_end(ip_adresa)

        while red and sada - red[0] > PROZOR_ZAHTEVA:
            red.popleft()
        if len(red) >= GRANICA_ZAHTEVA:
            return False

        red.append(sada)
        while len(_zahtevi_po_ip) > MAKS_IP_KORPI:
            _zahtevi_po_ip.popitem(last=False)
        return True


@app.after_request
def bezbednosna_zaglavlja(odgovor):
    for ime, vrednost in BEZBEDNOSNA_ZAGLAVLJA.items():
        odgovor.headers.setdefault(ime, vrednost)
    if request.is_secure:
        odgovor.headers.setdefault(
            "Strict-Transport-Security", "max-age=31536000; includeSubDomains"
        )
    if request.endpoint == "static":
        # Šabloni dodaju ?v=<mtime>, pa se ime fajla menja sa sadržajem.
        odgovor.headers["Cache-Control"] = "public, max-age=31536000, immutable"
    else:
        # Odgovor može da sadrži tekst emaila, pa ga posrednici ne smeju da
        # čuvaju u kešu.
        odgovor.headers["Cache-Control"] = "no-store"
    return odgovor


@app.context_processor
def cache_busting():
    def verzija_fajla(putanja):
        try:
            puna_putanja = Path(app.static_folder) / putanja
            return int(puna_putanja.stat().st_mtime)
        except OSError:
            return 0
    return dict(verzija_fajla=verzija_fajla)


def _treba_kompresiju(odgovor) -> bool:
    if not 200 <= odgovor.status_code < 300:
        return False
    if odgovor.headers.get("Content-Encoding"):
        return False
    if (odgovor.mimetype or "").lower() not in TIPOVI_ZA_KOMPRESIJU:
        return False
    # ``no-transform`` zabranjuje posrednicima da menjaju telo odgovora.
    return "no-transform" not in odgovor.headers.get("Cache-Control", "")


@app.after_request
def kompresuj_odgovor(odgovor):
    """Gzip za tekstualne odgovore, uključujući statiku.

    Waitress ne kompresuje sam, a HTML, CSS i JS su najveći prenos na prvom
    učitavanju. ``Vary`` se postavlja i kada klijent ne šalje ``Accept-Encoding``,
    da keš ne bi servirao gzip verziju klijentu koji je ne razume.
    """
    if not _treba_kompresiju(odgovor):
        return odgovor

    odgovor.headers["Vary"] = "Accept-Encoding"

    if "gzip" not in request.accept_encodings:
        return odgovor

    # Statika se šalje u passthrough režimu; telo mora prvo da se pročita.
    if odgovor.direct_passthrough:
        odgovor.direct_passthrough = False
    podaci = odgovor.get_data()
    if len(podaci) < MAKS_NEKOMPRESOVANO:
        return odgovor

    kompresovano = gzip.compress(podaci, compresslevel=6)
    if len(kompresovano) >= len(podaci):
        return odgovor

    odgovor.set_data(kompresovano)
    odgovor.headers["Content-Encoding"] = "gzip"
    # ETag je izračunat za nekompresovano telo, pa više ne važi. Keširanje
    # statike ionako nosi ``immutable`` i verziju u URL-u.
    odgovor.headers.pop("ETag", None)
    return odgovor


@app.errorhandler(HTTPException)
def http_greska(greska):
    # Pregledač koji je otvorio pogrešan URL treba HTML stranicu. API klijenti
    # ne šalju ``Accept: text/html``, pa za njih odgovor ostaje JSON.
    if request.method in ("GET", "HEAD") and (
        request.accept_mimetypes.best == "text/html"
    ):
        return render_template(
            "greska.html", kod=greska.code
        ), greska.code
    return jsonify({"greska": greska.description}), greska.code


@app.errorhandler(Exception)
def neocekivana_greska(greska):
    app.logger.exception("Neočekivana greška pri obradi zahteva")
    return jsonify({"greska": "Došlo je do interne greške."}), 500


@app.route("/")
def index():
    return render_template("dashboard.html", maks_znakova=MAKS_ANALIZIRANIH_ZNAKOVA)


@app.route("/healthz")
def healthz():
    """Brza provera da proces odgovara. Ne dira rečnike ni model."""
    return jsonify({"status": "ok"})


@app.route("/robots.txt")
def robots():
    linije = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /analiziraj",
        "Disallow: /primeri-svi",
        f"Sitemap: {url_for('sitemap', _external=True)}",
        "",
    ]
    return Response("\n".join(linije), mimetype="text/plain")


@app.route("/sitemap.xml")
def sitemap():
    url = url_for("index", _external=True)
    return Response(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"  <url><loc>{url}</loc><changefreq>monthly</changefreq></url>\n"
        "</urlset>\n",
        mimetype="application/xml",
    )


@app.route("/primeri-svi")
def primeri_svi():
    jezik = request.args.get("jezik", "en")
    lista = ucitaj_sve_primere(jezik)
    return jsonify({"primeri": lista})


def _definicije_za_json(definicije: dict) -> list:
    return [
        {
            "ime": ime,
            "naziv": definicija["naziv"],
            "tip": definicija["tip"],
            "params": list(definicija["params"]),
            "kategorija": definicija["kategorija"],
        }
        for ime, definicija in definicije.items()
    ]


@app.route("/skupovi")
def skupovi():
    izlazi = _definicije_za_json(IZLAZNI_SKUPOVI_DEFINICIJE)
    return jsonify({
        "univerzum": {"min": 0, "max": 100, "korak": 1},
        "ulazi": {
            ime: _definicije_za_json(definicije)
            for ime, definicije in ULAZNI_SKUPOVI_DEFINICIJE.items()
        },
        "izlazi": izlazi,
        # Zadržano zbog starijih klijenata/testova.
        "skupovi": izlazi,
    })


@app.route("/analiziraj", methods=["POST"])
def analiziraj():
    if not _dozvoli_zahtev(request.remote_addr or "nepoznat"):
        odgovor = jsonify({"greska": "Previše zahteva. Pokušajte ponovo kasnije."})
        odgovor.status_code = 429
        odgovor.headers["Retry-After"] = str(int(PROZOR_ZAHTEVA))
        return odgovor

    if request.is_json:
        podaci = request.get_json(silent=True)
        if not isinstance(podaci, dict):
            return jsonify({"greska": "Telo zahteva mora biti JSON objekat."}), 400
    else:
        podaci = request.form

    tekst_emaila = podaci.get("tekst", "")
    nacin_recnika = podaci.get("recnik", "auto")

    if not isinstance(tekst_emaila, str):
        return jsonify({"greska": "Tekst emaila mora biti string."}), 400
    if nacin_recnika not in VALIDNI_RECNICI:
        nacin_recnika = "auto"

    tekst_emaila = tekst_emaila.strip()
    if not tekst_emaila:
        return jsonify({"greska": "Tekst emaila je prazan."}), 400

    skraceno = len(tekst_emaila) > MAKS_ANALIZIRANIH_ZNAKOVA
    analizirani_tekst = tekst_emaila[:MAKS_ANALIZIRANIH_ZNAKOVA]

    ulazi = analiziraj_email(analizirani_tekst, nacin_recnik=nacin_recnika)

    # Mreža dobija iste četiri karakteristike i vraća samo peti ulaz. Ako
    # model ne postoji ili ne odgovara rečniku, vrednost je neutralna 50 i
    # sistem se ponaša kao čist fazi sistem.
    nn_pouzdanje = pouzdanje_nn(ulazi, ulazi.get("recnik", nacin_recnika))

    rezultat_fis = pokreni_fis(
        ulazi["kljucne_reci"],
        ulazi["broj_linkova"],
        ulazi["caps_procenat"],
        ulazi["interpunkcija"],
        nn_pouzdanje,
    )

    rezultat = {
        # Vidljivi tekst se šalje samo u objasnjenje.tekst; duplo slanje celog
        # teksta je na ulazu od 10.000 znakova pravilo odgovor većim za ~10 KB.
        "skraceno":      skraceno,
        "recnik":        ulazi.get("recnik", nacin_recnika),
        "kljucne_reci":  ulazi["kljucne_reci"],
        "broj_linkova":  ulazi["broj_linkova"],
        "caps_procenat": ulazi["caps_procenat"],
        "interpunkcija": ulazi["interpunkcija"],
        "nn_pouzdanje":  round(nn_pouzdanje, 2),
        "spam_score":    round(rezultat_fis["spam_score"], 2),
        "kategorija":    rezultat_fis["kategorija"],
        "objasnjenje": {
            "tekst":           ulazi.get("vidljivi_tekst", ""),
            "pokrivene_reci":  ulazi.get("pokrivene_reci", []),
            "oznake":          ulazi.get("oznake", []),
            "aktivna_pravila": rezultat_fis.get("aktivna_pravila", []),
            "ulazi":           rezultat_fis.get("ulazi", {}),
        },
    }

    return jsonify(rezultat)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="127.0.0.1", port=port)
