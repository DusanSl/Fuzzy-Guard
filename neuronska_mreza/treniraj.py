"""Poređenje neuronske mreže i neuro-fazi sistema.

Mreža ima dve uloge:

1. **Runtime:** njen izlaz je peti fazi ulaz ``nn_pouzdanje`` (0-100).
   Pravila ``n01``-``n03`` koriste ga kao potvrdu; konačnu ocenu i dalje daje
   Mamdani + centroid. Nijedno ``n`` pravilo ne vodi u SPAM samo na osnovu
   mreže.
2. **Evaluacija:** isti MLP se poredi sa čistim fazi sistemom (bez ``n``
   pravila) i sa hibridom. Oba modela dobijaju iste četiri karakteristike:

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

Modeli za runtime se čuvaju u ``podaci/model_nn_<recnik>.joblib``. Model se
odbija ako se rečnik promeni (hash u metapodacima).

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
from neuronska_mreza.predikcija import KARAKTERISTIKE, sacuvaj_model as sacuvaj_model_na_disk
from obrada_teksta.analizator import analiziraj_email

KOREN = Path(__file__).parent.parent
KORPUSI = {
    "email": ("SpamAssassin (emailovi)", KOREN / "podaci" / "spamassassin.tsv"),
    "sr": ("SpamAssassin na srpskom (hibridni korpus)", KOREN / "podaci" / "sr_spamassassin.tsv"),
    "sms": ("SMS Spam Collection", KOREN / "podaci" / "SMSSpamCollection.tsv"),
}

REZIMI = ("legacy", "en", "sr", "kombinovano")
NEUTRALNO_NN = 50.0

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


def fazi_predikcija(red: np.ndarray, val_nn: float) -> int:
    """1 ako fazi sistem kaže SPAM, inače 0 (SUMNJIVO se računa kao ham)."""
    rezultat = pokreni_fis(
        float(red[0]),
        float(red[1]),
        float(red[2]),
        float(red[3]),
        float(val_nn),
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
    sacuvani = []
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

        verovatnoce = mreza.predict_proba(skaliraj.transform(X_test))[:, 1] * 100.0
        pred_mreze = (verovatnoce >= 50.0).astype(int)

        # Čist fazi sistem: nn ulaz je neutralan, pa se n pravila ne aktiviraju.
        pred_fazi = np.array([fazi_predikcija(red, NEUTRALNO_NN) for red in X_test])
        # Hibrid: mrežin izlaz je peti fazi ulaz. Za ``legacy`` nema runtime
        # modela, pa hibrid ostaje neutralan i jednak čistom fazi sistemu.
        verovatnoce_hibrid = (
            np.full_like(verovatnoce, NEUTRALNO_NN)
            if nacin == "legacy" else verovatnoce
        )
        pred_hibrid = np.array([
            fazi_predikcija(red, verovatnoca)
            for red, verovatnoca in zip(X_test, verovatnoce_hibrid)
        ])

        rezultati[nacin] = {
            "mreza": metrike(y_test, pred_mreze),
            "fazi": metrike(y_test, pred_fazi),
            "hibrid": metrike(y_test, pred_hibrid),
            "pred_fazi": pred_fazi,
            "pred_hibrid": pred_hibrid,
        }

        if sacuvaj_model and nacin in ("en", "sr", "kombinovano"):
            sacuvani.append(sacuvaj_model_na_disk(nacin, skaliraj, mreza))

    print(f"\n{'model':26s} {'recnik':13s} {'tacnost':>8s} {'preciznost':>11s} "
          f"{'odziv':>7s} {'F1':>7s}")
    for nacin in rezimi:
        for naziv_modela, kljuc in (
            ("Neuronska mreza (MLP)", "mreza"),
            ("Fazi (4 ulaza)", "fazi"),
            ("Neuro-fazi (5 ulaza)", "hibrid"),
        ):
            m = rezultati[nacin][kljuc]
            print(f"{naziv_modela:26s} {nacin:13s} {m['tacnost']:8.3f} "
                  f"{m['preciznost']:11.3f} {m['odziv']:7.3f} {m['f1']:7.3f}")

    if "kombinovano" in rezultati:
        for naziv, kljuc in (("fazi", "fazi"), ("neuro-fazi", "hibrid")):
            pred = rezultati["kombinovano"][f"pred_{kljuc}"]
            print(f"\nMatrica konfuzije {naziv} sistema (kombinovano):")
            print(confusion_matrix(y_test, pred))
            print(classification_report(y_test, pred, target_names=["ham", "spam"], digits=3))

    if sacuvani:
        for putanja in sacuvani:
            print(f"Model sacuvan u {putanja}")


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
