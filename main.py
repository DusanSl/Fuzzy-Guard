from collections import defaultdict, deque
from pathlib import Path
from threading import Lock
from time import monotonic

from flask import Flask, jsonify, render_template, request
from werkzeug.exceptions import HTTPException

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
MAKS_ANALIZIRANIH_ZNAKOVA = 50_000

# Šabloni dodaju ?v=<mtime> na CSS i JS, pa statika može dugo da se kešira:
# novi sadržaj uvek dobija novi URL.
KEŠIRANJE_STATIKE_SEKUNDI = 365 * 24 * 60 * 60

BEZBEDNOSNA_ZAGLAVLJA = {
    "X-Content-Type-Options": "nosniff",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "X-Frame-Options": "DENY",
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

# Jednostavan klizni prozor po IP adresi. Dovoljno za javni demo i zaštitu od
# slučajnog ili namernog spamovanja skupog /analiziraj endpointa.
GRANICA_ZAHTEVA = 120
PROZOR_ZAHTEVA = 60.0
_zahtevi_po_ip = defaultdict(deque)
_zahtevi_lock = Lock()


def _dozvoli_zahtev(ip_adresa: str) -> bool:
    sada = monotonic()
    with _zahtevi_lock:
        red = _zahtevi_po_ip[ip_adresa]
        while red and sada - red[0] > PROZOR_ZAHTEVA:
            red.popleft()
        if len(red) >= GRANICA_ZAHTEVA:
            return False
        red.append(sada)
        if len(_zahtevi_po_ip) > 2000:
            for kljuc in [k for k, v in _zahtevi_po_ip.items() if not v]:
                _zahtevi_po_ip.pop(kljuc, None)
        return True


@app.after_request
def bezbednosna_zaglavlja(odgovor):
    for ime, vrednost in BEZBEDNOSNA_ZAGLAVLJA.items():
        odgovor.headers.setdefault(ime, vrednost)
    if request.endpoint != "static":
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


@app.errorhandler(HTTPException)
def http_greska(greska):
    return jsonify({"greska": greska.description}), greska.code


@app.errorhandler(Exception)
def neocekivana_greska(greska):
    app.logger.exception("Neočekivana greška pri obradi zahteva")
    return jsonify({"greska": "Došlo je do interne greške."}), 500


@app.route("/")
def index():
    return render_template("dashboard.html")


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

    nacin_recnika = "auto"
    if request.is_json:
        podaci = request.get_json(silent=True) or {}
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
        # teksta je na ulazu od 50.000 znakova pravilo odgovor većim za ~50 KB.
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
    import os

    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="127.0.0.1", port=port)
