from pathlib import Path

from flask import Flask, jsonify, render_template, request
from werkzeug.exceptions import HTTPException

from obrada_teksta.analizator import (
    VALIDNI_RECNICI,
    analiziraj_email,
    ucitaj_sve_primere,
)
from fazi.skupovi import IZLAZNI_SKUPOVI_DEFINICIJE, ULAZNI_SKUPOVI_DEFINICIJE
from fazi.zakljucivanje import pokreni_fis

KOREN = Path(__file__).parent
MAKS_DUŽINA_ZAHTEVA = 256 * 1024
MAKS_ANALIZIRANIH_ZNAKOVA = 50_000

app = Flask(
    __name__,
    template_folder=str(KOREN / "veb" / "sabloni"),
    static_folder=str(KOREN / "veb" / "static"),
)
app.config["MAX_CONTENT_LENGTH"] = MAKS_DUŽINA_ZAHTEVA


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
    nacin_recnika = "kombinovano"
    if request.is_json:
        podaci = request.get_json(silent=True) or {}
    else:
        podaci = request.form

    tekst_emaila = podaci.get("tekst", "")
    nacin_recnika = podaci.get("recnik", "kombinovano")

    if not isinstance(tekst_emaila, str):
        return jsonify({"greska": "Tekst emaila mora biti string."}), 400
    if nacin_recnika not in VALIDNI_RECNICI:
        nacin_recnika = "kombinovano"

    tekst_emaila = tekst_emaila.strip()
    if not tekst_emaila:
        return jsonify({"greska": "Tekst emaila je prazan."}), 400

    skraceno = len(tekst_emaila) > MAKS_ANALIZIRANIH_ZNAKOVA
    analizirani_tekst = tekst_emaila[:MAKS_ANALIZIRANIH_ZNAKOVA]

    ulazi = analiziraj_email(analizirani_tekst, nacin_recnik=nacin_recnika)

    rezultat_fis = pokreni_fis(
        ulazi["kljucne_reci"],
        ulazi["broj_linkova"],
        ulazi["caps_procenat"],
        ulazi["interpunkcija"],
    )

    rezultat = {
        "tekst":         analizirani_tekst,
        "skraceno":      skraceno,
        "kljucne_reci":  ulazi["kljucne_reci"],
        "broj_linkova":  ulazi["broj_linkova"],
        "caps_procenat": ulazi["caps_procenat"],
        "interpunkcija": ulazi["interpunkcija"],
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
