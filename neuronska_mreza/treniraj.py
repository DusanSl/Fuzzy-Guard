"""Poređenje neuronske mreže i fazi sistema.

Mreža NE učestvuje u izračunavanju ``spam_score`` — služi kao drugo mišljenje i
kao poređenje za odbranu projekta. Oba modela dobijaju iste četiri ulazne
karakteristike, tako da je poređenje fer:

    kljucne_reci, broj_linkova, caps_procenat, interpunkcija

Rečnici:

    legacy       - stari ručni rečnik (samo za tabelu "pre / posle mreže")
    en           - naučeni engleski rečnik
    sr           - naučeni srpski rečnik (korpus preveden mašinski)
    kombinovano  - en + sr (podrazumevano u aplikaciji)

Korpusi:
- ``podaci/spamassassin.tsv`` — 3000 engleskih emailova (500 spama).
- ``podaci/sr_spamassassin.tsv`` — isti korpus mašinski preveden na srpski.
- ``podaci/SMSSpamCollection.tsv`` — 5574 SMS poruka (747 spama).

Pokretanje::

    python -m neuronska_mreza.treniraj
    python -m neuronska_mreza.treniraj --recnik svi
    python -m neuronska_mreza.treniraj --korpus sr --recnik sr
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

from fazi.zakljucivanje import pokreni_fis
from neuronska_mreza.legacy_recnik import termini as legacy_termini
from obrada_teksta.analizator import analiziraj_email

KOREN = Path(__file__).parent.parent
KORPUSI = {
    "email": ("SpamAssassin (emailovi)", KOREN / "podaci" / "spamassassin.tsv"),
    "sr": ("SpamAssassin na srpskom (hibridni korpus)", KOREN / "podaci" / "sr_spamassassin.tsv"),
    "sms": ("SMS Spam Collection", KOREN / "podaci" / "SMSSpamCollection.tsv"),
}
PUTANJA_MODEL = Path(__file__).parent / "model.joblib"

KARAKTERISTIKE = ("kljucne_reci", "broj_linkova", "caps_procenat", "interpunkcija")
REZIMI = ("legacy", "en", "sr", "kombinovano")

_LEGACY_RECNIK = dict((termin, tezina) for termin, tezina, _ in legacy_termini())


def ucitaj_podatke(putanja: Path):
    """Vraća (tekstovi, oznake) gde je oznaka 1 za spam, 0 za ham."""
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
        ulazi = analiziraj_email(
            tekst,
            nacin_recnik=nacin_recnik,
            legacy_recnik=_LEGACY_RECNIK if nacin_recnik == "legacy" else None,
        )
        redovi.append([ulazi[ime] for ime in KARAKTERISTIKE])
    return np.array(redovi, dtype=float)


def fazi_predikcija(tekst: str, nacin_recnik: str) -> int:
    """1 ako fazi sistem kaže SPAM, inače 0 (SUMNJIVO se računa kao ham)."""
    ulazi = analiziraj_email(
        tekst,
        nacin_recnik=nacin_recnik,
        legacy_recnik=_LEGACY_RECNIK if nacin_recnik == "legacy" else None,
    )
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
    parser = argparse.ArgumentParser(description="Poređenje MLP i fazi sistema.")
    parser.add_argument(
        "--recnik", choices=(*REZIMI, "svi"), default="kombinovano",
        help="koji rečnik koristi ulaz 'kljucne_reci'",
    )
    parser.add_argument(
        "--korpus", choices=(*KORPUSI, "svi"), default="svi",
        help="koji korpus evaluirati",
    )
    argumenti = parser.parse_args()

    rezimi = REZIMI if argumenti.recnik == "svi" else (argumenti.recnik,)
    if argumenti.korpus == "svi":
        korpusi = list(KORPUSI.items())
    else:
        korpusi = [(argumenti.korpus, KORPUSI[argumenti.korpus])]

    for kljuc, (naziv, putanja) in korpusi:
        # model se cuva samo za primarni (engleski email) korpus
        obradi_korpus(naziv, putanja, rezimi, sacuvaj_model=(kljuc == "email"))


if __name__ == "__main__":
    main()
