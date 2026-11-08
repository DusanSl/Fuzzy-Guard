"""Poredjenje neuronske mreze i fazi sistema.

Mreza NE ucestvuje u izracunavanju ``spam_score`` — sluzi kao drugo misljenje i
kao poredjenje za odbranu projekta. Oba modela dobijaju iste cetiri ulazne
karakteristike, tako da je poredjenje fer:

    kljucne_reci, broj_linkova, caps_procenat, interpunkcija

Za ``kljucne_reci`` postoje tri rezima (vidi ``obrada_teksta/analizator.py``):

    rucni        - samo lista odrzavana rukom
    nauceni      - samo recnik koji je naucila mreza
    kombinovano  - rucni + nauceni (podrazumevano)

Korpusi:
- ``podaci/spamassassin.tsv`` — 3000 emailova (500 spama). Primarni korpus.
- ``podaci/SMSSpamCollection.tsv`` — 5574 SMS poruka (747 spama). Sekundarni
  korpus; pokazuje da iste karakteristike slabije rade van email domena.

Pokretanje:

    python -m neuronska_mreza.treniraj
    python -m neuronska_mreza.treniraj --recnik svi
"""

import argparse
from pathlib import Path

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

from obrada_teksta.analizator import analiziraj_email
from fazi.zakljucivanje import pokreni_fis

KOREN = Path(__file__).parent.parent
KORPUSI = (
    ("SpamAssassin (emailovi)", KOREN / "podaci" / "spamassassin.tsv"),
    ("SMS Spam Collection", KOREN / "podaci" / "SMSSpamCollection.tsv"),
)
PUTANJA_MODEL = Path(__file__).parent / "model.joblib"

KARAKTERISTIKE = ("kljucne_reci", "broj_linkova", "caps_procenat", "interpunkcija")
REZIMI = ("rucni", "nauceni", "kombinovano")


def ucitaj_podatke(putanja: Path):
    """Vraca (tekstovi, oznake) gde je oznaka 1 za spam, 0 za ham."""
    tekstovi, oznake = [], []
    for linija in putanja.read_text(encoding="utf-8").splitlines():
        if "\t" not in linija:
            continue
        oznaka, tekst = linija.split("\t", 1)
        oznake.append(1 if oznaka.strip() == "spam" else 0)
        tekstovi.append(tekst)
    return tekstovi, np.array(oznake)


def izvuci_karakteristike(tekstovi: list, nacin_recnik: str) -> np.ndarray:
    redovi = []
    for tekst in tekstovi:
        ulazi = analiziraj_email(tekst, nacin_recnik=nacin_recnik)
        redovi.append([ulazi[ime] for ime in KARAKTERISTIKE])
    return np.array(redovi, dtype=float)


def fazi_predikcija(tekst: str, nacin_recnik: str) -> int:
    """1 ako fazi sistem kaze SPAM, inace 0 (SUMNJIVO se racuna kao ham)."""
    ulazi = analiziraj_email(tekst, nacin_recnik=nacin_recnik)
    rezultat = pokreni_fis(
        ulazi["kljucne_reci"],
        ulazi["broj_linkova"],
        ulazi["caps_procenat"],
        ulazi["interpunkcija"],
    )
    return 1 if rezultat["kategorija"] == "SPAM" else 0


def metrike(istinite, predvidjene) -> dict:
    return {
        "tacnost": accuracy_score(istinite, predvidjene),
        "preciznost": precision_score(istinite, predvidjene, zero_division=0),
        "odziv": recall_score(istinite, predvidjene, zero_division=0),
        "f1": f1_score(istinite, predvidjene, zero_division=0),
    }


def obradi_korpus(naziv: str, putanja: Path, rezimi: tuple, sacuvaj_model: bool = False):
    if not putanja.exists():
        print(f"\n[preskoceno] {naziv}: nema fajla {putanja}")
        return

    print(f"\n================ {naziv} ================")
    tekstovi, oznake = ucitaj_podatke(putanja)

    indeksi = np.arange(len(oznake))
    indeksi_train, indeksi_test = train_test_split(
        indeksi, test_size=0.25, random_state=42, stratify=oznake
    )
    y_train, y_test = oznake[indeksi_train], oznake[indeksi_test]
    tekst_train = [tekstovi[i] for i in indeksi_train]
    tekst_test = [tekstovi[i] for i in indeksi_test]

    print(f"Trening: {len(y_train)} primera | Test: {len(y_test)} primera | "
          f"spam u testu: {int(y_test.sum())}")

    rezultati = {}
    for nacin in rezimi:
        X_train = izvuci_karakteristike(tekst_train, nacin)
        X_test = izvuci_karakteristike(tekst_test, nacin)

        skaliraj = StandardScaler().fit(X_train)
        mreza = MLPClassifier(
            hidden_layer_sizes=(16, 8),
            activation="relu",
            max_iter=800,
            early_stopping=True,
            random_state=42,
        )
        mreza.fit(skaliraj.transform(X_train), y_train)
        metrike_mreze = metrike(y_test, mreza.predict(skaliraj.transform(X_test)))

        fazi_pred = np.array([fazi_predikcija(tekst, nacin) for tekst in tekst_test])
        metrike_fazi = metrike(y_test, fazi_pred)

        rezultati[nacin] = (metrike_mreze, metrike_fazi, fazi_pred)

        if sacuvaj_model and nacin == "kombinovano":
            import joblib
            joblib.dump({"skaliraj": skaliraj, "mreza": mreza}, PUTANJA_MODEL)

    print(f"\n{'model':26s} {'recnik':13s} {'tacnost':>8s} {'preciznost':>11s} "
          f"{'odziv':>7s} {'F1':>7s}")
    for nacin in rezimi:
        metrike_mreze, metrike_fazi, _ = rezultati[nacin]
        for naziv_modela, m in (("Neuronska mreza (MLP)", metrike_mreze),
                                ("Fazi sistem (Mamdani)", metrike_fazi)):
            print(f"{naziv_modela:26s} {nacin:13s} {m['tacnost']:8.3f} "
                  f"{m['preciznost']:11.3f} {m['odziv']:7.3f} {m['f1']:7.3f}")

    if "kombinovano" in rezultati:
        _, _, fazi_pred = rezultati["kombinovano"]
        print("\nMatrica konfuzije fazi sistema (kombinovano):")
        print(confusion_matrix(y_test, fazi_pred))
        print(classification_report(y_test, fazi_pred, target_names=["ham", "spam"], digits=3))

    if sacuvaj_model:
        print(f"Model sacuvan u {PUTANJA_MODEL}")


def main():
    parser = argparse.ArgumentParser(description="Poredjenje MLP i fazi sistema.")
    parser.add_argument(
        "--recnik", choices=(*REZIMI, "svi"), default="kombinovano",
        help="koji recnik koristi ulaz 'kljucne_reci'",
    )
    parser.add_argument(
        "--korpus", choices=("svi", "email", "sms"), default="svi",
        help="koji korpus evaluirati",
    )
    argumenti = parser.parse_args()

    rezimi = REZIMI if argumenti.recnik == "svi" else (argumenti.recnik,)
    korpusi = KORPUSI
    if argumenti.korpus == "email":
        korpusi = KORPUSI[:1]
    elif argumenti.korpus == "sms":
        korpusi = KORPUSI[1:]

    for naziv, putanja in korpusi:
        # model se cuva samo za primarni (email) korpus, da --korpus sms
        # ne bi pregazio istrenirani email model
        obradi_korpus(naziv, putanja, rezimi, sacuvaj_model=(putanja == KORPUSI[0][1]))


if __name__ == "__main__":
    main()
