from flask import Flask, request, jsonify, render_template
from obrada_teksta.analizator import (
    analiziraj_email,
    ucitaj_sve_primere,
    ucitaj_teske_primere,
)
from fazi.zakljucivanje import pokreni_fis
from fazi.skupovi import IZLAZNI_SKUPOVI_DEFINICIJE
import os

app = Flask(
    __name__,
    template_folder="veb/sabloni",
    static_folder="veb/static",
)

@app.context_processor
def cache_busting():
    def verzija_fajla(putanja):
        try:
            puna_putanja = os.path.join(app.static_folder, putanja)
            return int(os.path.getmtime(puna_putanja))
        except OSError:
            return 0
    return dict(verzija_fajla=verzija_fajla)

@app.route("/")
def index():
    return render_template("dashboard.html")


@app.route("/primeri-svi")
def primeri_svi():
    jezik = request.args.get("jezik", "en")
    lista = ucitaj_sve_primere(jezik)
    return jsonify({"primeri": lista})


@app.route("/primeri-teski")
def primeri_teski():
    jezik = request.args.get("jezik", "en")
    lista = ucitaj_teske_primere(jezik)
    return jsonify({"primeri": lista})


@app.route("/skupovi")
def skupovi():
    return jsonify({
        "univerzum": {"min": 0, "max": 100, "korak": 1},
        "skupovi": [
            {
                "ime": ime,
                "naziv": definicija["naziv"],
                "tip": definicija["tip"],
                "params": list(definicija["params"]),
                "kategorija": definicija["kategorija"],
            }
            for ime, definicija in IZLAZNI_SKUPOVI_DEFINICIJE.items()
        ],
    })


@app.route("/analiziraj", methods=["POST"])
def analiziraj():
    nacin_recnika = "kombinovano"
    if request.is_json:
        podaci = request.get_json()
        tekst_emaila = podaci.get("tekst", "")
        nacin_recnika = podaci.get("recnik", "kombinovano")
    else:
        tekst_emaila = request.form.get("tekst", "")
        nacin_recnika = request.form.get("recnik", "kombinovano")

    if nacin_recnika not in ("rucni", "nauceni", "kombinovano"):
        nacin_recnika = "kombinovano"

    if not tekst_emaila.strip():
        return jsonify({"greska": "Tekst emaila je prazan."}), 400

    ulazi = analiziraj_email(tekst_emaila, nacin_recnik=nacin_recnika)

    rezultat_fis = pokreni_fis(
        ulazi["kljucne_reci"],
        ulazi["broj_linkova"],
        ulazi["caps_procenat"],
        ulazi["interpunkcija"],
    )

    rezultat = {
        "tekst":         tekst_emaila,
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
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port) 