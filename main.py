from flask import Flask, request, jsonify, render_template
from obrada_teksta.analizator import analiziraj_email, ucitaj_sve_primere
from fazi.zakljucivanje import pokreni_fis
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


@app.route("/analiziraj", methods=["POST"])
def analiziraj():
    if request.is_json:
        podaci = request.get_json()
        tekst_emaila = podaci.get("tekst", "")
    else:
        tekst_emaila = request.form.get("tekst", "")

    if not tekst_emaila.strip():
        return jsonify({"greska": "Tekst emaila je prazan."}), 400

    ulazi = analiziraj_email(tekst_emaila)

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
    }

    return jsonify(rezultat)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port) 