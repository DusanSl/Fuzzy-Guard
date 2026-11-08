"""Neuronska mreza za detekciju spama.

Ovaj modul je namerno odvojen od fazi sistema. Mreza NE ucestvuje u izracunavanju
``spam_score`` — sluzi kao drugo misljenje i kao poredjenje za odbranu projekta.

Mreza koristi iste cetiri ulazne karakteristike kao fazi sistem, tako da je
poredjenje fer:

    kljucne_reci, broj_linkova, caps_procenat, interpunkcija

Korpusi:
- ``podaci/spamassassin.tsv`` — 3000 emailova (500 spama). Primarni korpus,
  jer je projekat filter za email.
- ``podaci/SMSSpamCollection.tsv`` — 5574 SMS poruka (747 spama). Sekundarni
  korpus; pokazuje da iste karakteristike slabije rade van email domena.
"""

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


def izvuci_karakteristike(tekstovi: list) -> np.ndarray:
    redovi = []
    for tekst in tekstovi:
        ulazi = analiziraj_email(tekst)
        redovi.append([ulazi[ime] for ime in KARAKTERISTIKE])
    return np.array(redovi, dtype=float)


def fazi_predikcija(tekst: str) -> int:
    """1 ako fazi sistem kaze SPAM, inace 0 (SUMNJIVO se racuna kao ham)."""
    ulazi = analiziraj_email(tekst)
    rezultat = pokreni_fis(
        ulazi["kljucne_reci"],
        ulazi["broj_linkova"],
        ulazi["caps_procenat"],
        ulazi["interpunkcija"],
    )
    return 1 if rezultat["kategorija"] == "SPAM" else 0


def pisi_metrike(naziv: str, istinite, predvidjene) -> dict:
    print(f"\n--- {naziv} ---")
    print(classification_report(istinite, predvidjene, target_names=["ham", "spam"], digits=3))
    print("matrica konfuzije:")
    print(confusion_matrix(istinite, predvidjene))
    return {
        "tacnost": accuracy_score(istinite, predvidjene),
        "preciznost": precision_score(istinite, predvidjene, zero_division=0),
        "odziv": recall_score(istinite, predvidjene, zero_division=0),
        "f1": f1_score(istinite, predvidjene, zero_division=0),
    }


def obradi_korpus(naziv: str, putanja: Path, sacuvaj_model: bool = False) -> dict:
    if not putanja.exists():
        print(f"\n[preskoceno] {naziv}: nema fajla {putanja}")
        return {}

    print(f"\n================ {naziv} ================")
    tekstovi, oznake = ucitaj_podatke(putanja)
    X = izvuci_karakteristike(tekstovi)

    X_train, X_test, y_train, y_test, tekst_train, tekst_test = train_test_split(
        X, oznake, tekstovi,
        test_size=0.25,
        random_state=42,
        stratify=oznake,
    )

    skaliraj = StandardScaler().fit(X_train)
    mreza = MLPClassifier(
        hidden_layer_sizes=(16, 8),
        activation="relu",
        max_iter=800,
        early_stopping=True,
        random_state=42,
    )
    mreza.fit(skaliraj.transform(X_train), y_train)

    mreza_pred = mreza.predict(skaliraj.transform(X_test))
    fazi_pred = np.array([fazi_predikcija(tekst) for tekst in tekst_test])

    print(f"Trening: {len(y_train)} primera | Test: {len(y_test)} primera | "
          f"spam u testu: {int(y_test.sum())}")

    metrike_mreze = pisi_metrike("Neuronska mreza (MLP)", y_test, mreza_pred)
    metrike_fazi = pisi_metrike("Fazi sistem (Mamdani)", y_test, fazi_pred)

    print("\nPoredjenje:")
    print(f"{'model':22s} {'tacnost':>8s} {'preciznost':>11s} {'odziv':>7s} {'F1':>7s}")
    for ime, metrike in (("Neuronska mreza", metrike_mreze), ("Fazi sistem", metrike_fazi)):
        print(f"{ime:22s} {metrike['tacnost']:8.3f} {metrike['preciznost']:11.3f} "
              f"{metrike['odziv']:7.3f} {metrike['f1']:7.3f}")

    if sacuvaj_model:
        import joblib
        joblib.dump({"skaliraj": skaliraj, "mreza": mreza}, PUTANJA_MODEL)
        print(f"\nModel sacuvan u {PUTANJA_MODEL}")

    return {"mreza": metrike_mreze, "fazi": metrike_fazi}


def treniraj():
    for indeks, (naziv, putanja) in enumerate(KORPUSI):
        obradi_korpus(naziv, putanja, sacuvaj_model=(indeks == 0))


if __name__ == "__main__":
    treniraj()
