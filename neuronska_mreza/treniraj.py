"""Poređenje neuronske mreže i neuro-fazi sistema.

Mreža ima dve uloge:

1. **Runtime:** njen izlaz je peti fazi ulaz ``nn_pouzdanje`` (0-100).
   Pravila ``n01``-``n02`` koriste ga kao potvrdu; konačnu ocenu i dalje daje
   Mamdani + centroid. Nijedno ``n`` pravilo ne vodi u SPAM samo na osnovu
   mreže.
2. **Evaluacija:** isti MLP se poredi sa čistim fazi sistemom (bez ``n``
   pravila) i sa hibridom. Oba modela dobijaju iste četiri karakteristike:

    kljucne_reci, broj_linkova, caps_procenat, interpunkcija

Podela podataka je u dva koraka i to je namerno:

- **test** (25%, ``random_state=42``) se dodiruje samo jednom, na kraju, za
  tabelu rezultata;
- **interna validacija** (20% trening skupa, ``random_state=7``) služi samo za
  ablaciju ``n`` pravila. Rezultat ablacije se ispisuje i ulazi u README. Baza
  pravila se ne menja automatski: ``n01`` je zadržan namerno, a razlog i cena
  su u README-u, u odeljku "Validation and Limitations".

Pragovi na kojima se porede modeli su različiti po prirodi, pa se ovde ispisuju:

- MLP odlučuje na ``predict_proba >= 0.50``;
- fazi sistem odlučuje kroz kategoriju ``SPAM``, koju daje najviša pripadnost u
  izlaznim skupovima (prag nije ručno biran, izlazi iz ``fazi/skupovi.py``).

Jabuka i narandža se ne porede po pragu, nego po F1, odzivu i AUC na istoj
podeli i istim karakteristikama.

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
    average_precision_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
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

# Podela na test je fiksna i ista kao u README-u. Menja se samo ako se menja
# cela evaluacija, nikad da bi rezultat izgledao bolje.
TEST_SIZE = 0.25
SEME_TESTA = 42

# Interna validacija služi samo za izbor ``n`` pravila. Ne ulazi u test.
INTERNA_VALIDACIJA = 0.20
SEME_INTERNE_VALIDACIJE = 7

# Prag MLP-a za klasifikacionu tabelu. Fazi sistem nema ovakav prag: on
# odlučuje kroz kategoriju izlaznog skupa. Videti docstring na vrhu.
PRAG_MREZE = 0.50

# Kandidati za ablaciju. Redosled je od najprostijeg ka najsloženijem, pa se
# kod izjednačenog F1 bira prostiji skup (manje pravila).
KANDIDATI_NN_PRAVILA = ((), ("n01",), ("n02",), ("n01", "n02"))
PODRAZUMEVANA_NN_PRAVILA = ("n01", "n02")

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


def napravi_mrezu() -> MLPClassifier:
    """Ista arhitektura i isti hiperparametri za svaki rečnik i korpus."""
    return MLPClassifier(
        hidden_layer_sizes=(16, 8),
        activation="relu",
        max_iter=800,
        early_stopping=True,
        random_state=42,
    )


def oznacen_naziv(nn_pravila) -> str:
    return " + ".join(nn_pravila) if nn_pravila else "bez n pravila"


def fazi_rezultati(X: np.ndarray, verovatnoce, nn_pravila) -> list:
    """Pokreće fazi sistem za svaki red i vraća listu rezultata.

    ``verovatnoce`` je niz po redovima ili jedan broj (npr. neutralno 50).
    """
    if np.isscalar(verovatnoce):
        verovatnoce = np.full(len(X), float(verovatnoce))
    return [
        pokreni_fis(
            float(red[0]),
            float(red[1]),
            float(red[2]),
            float(red[3]),
            float(verovatnoca),
            nn_pravila=nn_pravila,
        )
        for red, verovatnoca in zip(X, verovatnoce)
    ]


def skorovi_i_oznake(rezultati: list) -> tuple:
    """Vraća (spam_score 0-100, 1/0) iz rezultata fazi sistema.

    Ocena se koristi za AUC (rangiranje), a kategorija za klasifikacionu
    tabelu. Kategorija se izvodi iz iste ocene, pa su oba prikaza saglasna.
    """
    skorovi = np.array([rezultat["spam_score"] for rezultat in rezultati], dtype=float)
    oznake = np.array(
        [1 if rezultat["kategorija"] == "SPAM" else 0 for rezultat in rezultati],
        dtype=int,
    )
    return skorovi, oznake


def broj_aktiviranja(X: np.ndarray, verovatnoce, nn_pravila) -> dict:
    """Koliko puta je svako pravilo prešlo prag aktivacije na datom skupu.

    ``pokreni_fis`` vraća samo šest najjačih pravila (za UI), pa se ovde
    fuzzifikacija ponavlja da bi brojanje obuhvatilo sva pravila.
    """
    from fazi.pravila import fuzzifikuj, sastavi_pravila

    brojaci = {}
    for red, verovatnoca in zip(X, verovatnoce):
        mu = fuzzifikuj(
            float(red[0]), float(red[1]), float(red[2]), float(red[3]),
            float(verovatnoca),
        )
        for naziv, jacina, _, _ in sastavi_pravila(mu, nn_pravila):
            if float(jacina) > 0.05:
                brojaci[naziv] = brojaci.get(naziv, 0) + 1
    return brojaci


def metrike(istinite, predvidjene) -> dict:
    return {
        "tacnost": accuracy_score(istinite, predvidjene),
        "preciznost": precision_score(istinite, predvidjene, zero_division=0),
        "odziv": recall_score(istinite, predvidjene, zero_division=0),
        "f1": f1_score(istinite, predvidjene, zero_division=0),
    }


def izaberi_nn_pravila(tekstovi: list, oznake: np.ndarray, nacin_recnik: str) -> tuple:
    """Ablacija ``n`` pravila na internoj validaciji trening skupa.

    Vraća skup sa najboljim AUC-om. To je **predlog ablacije**, ne automatska
    izmena baze: ``main`` zadržava pun skup pravila (vidi README, "Validation
    and Limitations"). Test skup se ovde ne dodiruje. Mreža za ablaciju se
    trenira samo na unutrašnjem trening delu, da validacija ostane čista.
    """
    indeksi = np.arange(len(oznake))
    indeksi_train, _ = train_test_split(
        indeksi,
        test_size=TEST_SIZE,
        random_state=SEME_TESTA,
        stratify=oznake,
    )
    y_train = oznake[indeksi_train]
    tekst_train = [tekstovi[i] for i in indeksi_train]

    indeksi_unutra, indeksi_valid = train_test_split(
        np.arange(len(y_train)),
        test_size=INTERNA_VALIDACIJA,
        random_state=SEME_INTERNE_VALIDACIJE,
        stratify=y_train,
    )

    X_unutra = izvuci_karakteristike(
        [tekst_train[i] for i in indeksi_unutra], nacin_recnik
    )
    X_valid = izvuci_karakteristike(
        [tekst_train[i] for i in indeksi_valid], nacin_recnik
    )
    y_valid = y_train[indeksi_valid]

    skaliraj = StandardScaler().fit(X_unutra)
    mreza = napravi_mrezu()
    mreza.fit(skaliraj.transform(X_unutra), y_train[indeksi_unutra])
    verovatnoce_valid = mreza.predict_proba(skaliraj.transform(X_valid))[:, 1] * 100.0

    print(f"\n--- Izbor n pravila na internoj validaciji (recnik: {nacin_recnik}) ---")
    print(f"Validacija: {len(y_valid)} primera | spam: {int(y_valid.sum())}")
    print(f"{'skup n pravila':22s} {'AUC':>7s} {'F1':>7s} {'preciznost':>11s} {'odziv':>7s}")

    # Kriterijum je AUC defazifikovane ocene, a ne F1 kategorije. Razlog je
    # definisan output skupovima: n01 vodi u ``visoko_sumnjiv`` (nije SPAM), pa
    # metrika koja gleda samo kategoriju SPAM ne moze da vidi njegov efekat.
    # Ocena je ono sto sistem vraca i prikazuje, pa se pravila biraju po
    # kvalitetu rangiranja; kod izjednacenog AUC-a odlucuju F1 i jednostavnost.
    izabrano = KANDIDATI_NN_PRAVILA[0]
    najbolji_auc = -1.0
    najbolji_f1 = -1.0
    for kandidat in KANDIDATI_NN_PRAVILA:
        skorovi, predvidjene = skorovi_i_oznake(
            fazi_rezultati(X_valid, verovatnoce_valid, kandidat)
        )
        auc = roc_auc_score(y_valid, skorovi)
        m = metrike(y_valid, predvidjene)
        print(
            f"{oznacen_naziv(kandidat):22s} {auc:7.4f} {m['f1']:7.3f} "
            f"{m['preciznost']:11.3f} {m['odziv']:7.3f}"
        )
        bolji = auc > najbolji_auc or (auc == najbolji_auc and m["f1"] > najbolji_f1)
        if bolji:
            najbolji_auc = auc
            najbolji_f1 = m["f1"]
            izabrano = kandidat

    print(
        f"Izabrano: {oznacen_naziv(izabrano)} "
        f"(interna validacija AUC {najbolji_auc:.4f}, F1 {najbolji_f1:.3f})"
    )
    return izabrano


def obradi_korpus(
    naziv: str,
    putanja: Path,
    rezimi: tuple,
    izbor_nn_pravila: tuple,
    sacuvaj_model: bool = False,
):
    if not putanja.exists():
        print(f"\n[preskoceno] {naziv}: nema fajla {putanja}")
        return

    print(f"\n================ {naziv} ================")
    tekstovi, oznake = ucitaj_podatke(putanja)

    indeksi = np.arange(len(oznake))
    indeksi_train, indeksi_test = train_test_split(
        indeksi, test_size=TEST_SIZE, random_state=SEME_TESTA, stratify=oznake
    )
    y_train, y_test = oznake[indeksi_train], oznake[indeksi_test]
    tekst_train = [tekstovi[i] for i in indeksi_train]
    tekst_test = [tekstovi[i] for i in indeksi_test]

    print(f"Trening: {len(y_train)} primera | Test: {len(y_test)} primera | "
          f"spam u testu: {int(y_test.sum())}")
    print(f"n pravila u bazi: {oznacen_naziv(izbor_nn_pravila)}")
    print(f"Pragovi: MLP predict_proba >= {PRAG_MREZE:.2f} | "
          "fazi kategorija SPAM (izlazni skupovi)")

    rezultati = {}
    sacuvani = []
    for nacin in rezimi:
        X_train = izvuci_karakteristike(tekst_train, nacin)
        X_test = izvuci_karakteristike(tekst_test, nacin)

        skaliraj = StandardScaler().fit(X_train)
        mreza = napravi_mrezu()
        mreza.fit(skaliraj.transform(X_train), y_train)

        verovatnoce = mreza.predict_proba(skaliraj.transform(X_test))[:, 1] * 100.0
        pred_mreze = (verovatnoce >= PRAG_MREZE * 100.0).astype(int)

        # Čist fazi sistem: n pravila su isključena, pa peti ulaz ne utiče.
        skorovi_fazi, pred_fazi = skorovi_i_oznake(
            fazi_rezultati(X_test, NEUTRALNO_NN, ())
        )

        # Hibrid: mrežin izlaz je peti fazi ulaz, a baza sadrži ``n`` pravila
        # koja je pozivalac fiksirao. ``legacy`` nema runtime model, pa hibrid
        # ostaje neutralan i jednak je čistom fazi sistemu.
        if nacin == "legacy" or not izbor_nn_pravila:
            skorovi_hibrid, pred_hibrid = skorovi_fazi, pred_fazi
        else:
            skorovi_hibrid, pred_hibrid = skorovi_i_oznake(
                fazi_rezultati(X_test, verovatnoce, izbor_nn_pravila)
            )

        brojaci_n = None
        if nacin == "kombinovano":
            brojaci_n = broj_aktiviranja(X_test, verovatnoce, ("n01", "n02"))

        rezultati[nacin] = {
            "mreza": metrike(y_test, pred_mreze),
            "fazi": metrike(y_test, pred_fazi),
            "hibrid": metrike(y_test, pred_hibrid),
            "pred_fazi": pred_fazi,
            "pred_hibrid": pred_hibrid,
            "skorovi_fazi": skorovi_fazi,
            "skorovi_hibrid": skorovi_hibrid,
            "brojaci_n": brojaci_n,
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
        # AUC i PR-AUC traže kontinuiranu ocenu, ne kategoriju. Koristi se
        # spam_score 0-100; oba sistema se rangiraju na isti način.
        print("\nSkor-level metrike (kombinovano, test):")
        print(f"{'sistem':14s} {'AUC':>7s} {'PR-AUC':>8s} {'F1':>7s} "
              f"{'preciznost':>11s} {'odziv':>7s}")
        for naziv_sistema, kljuc_skora, kljuc_metrika in (
            ("Fazi", "skorovi_fazi", "fazi"),
            ("Neuro-fazi", "skorovi_hibrid", "hibrid"),
        ):
            skorovi = rezultati["kombinovano"][kljuc_skora]
            m = rezultati["kombinovano"][kljuc_metrika]
            print(
                f"{naziv_sistema:14s} {roc_auc_score(y_test, skorovi):7.4f} "
                f"{average_precision_score(y_test, skorovi):8.4f} "
                f"{m['f1']:7.4f} {m['preciznost']:11.4f} {m['odziv']:7.4f}"
            )

        for naziv, kljuc in (("fazi", "fazi"), ("neuro-fazi", "hibrid")):
            print(f"\nMatrica konfuzije {naziv} sistema (kombinovano):")
            print(confusion_matrix(y_test, rezultati["kombinovano"][f"pred_{kljuc}"]))
            print(classification_report(
                y_test, rezultati["kombinovano"][f"pred_{kljuc}"],
                target_names=["ham", "spam"], digits=3,
            ))

        brojaci_n = rezultati["kombinovano"]["brojaci_n"]
        if brojaci_n is not None:
            delovi = [
                f"{naziv}: {brojaci_n.get(naziv, 0)}"
                for naziv in ("n01", "n02")
            ]
            print(f"\nAktiviranja n pravila na testu (prag 0.05): {', '.join(delovi)}")

    if sacuvani:
        for putanja_modela in sacuvani:
            print(f"Model sacuvan u {putanja_modela}")


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

    # Ablacija se radi jednom, na primarnom korpusu, i važi za sve redove
    # ispod: svi modeli dele istu bazu pravila, što je uslov za pošteno
    # poređenje. Njen rezultat se prikazuje, ali baza se ne menja automatski.
    baza_pravila = PODRAZUMEVANA_NN_PRAVILA
    putanja_primarnog = KORPUSI["email"][1]
    if putanja_primarnog.exists():
        nacin_za_izbor = "kombinovano" if "kombinovano" in rezimi else rezimi[0]
        tekstovi_primarni, oznake_primarne = ucitaj_podatke(putanja_primarnog)
        izbor_ablacije = izaberi_nn_pravila(
            tekstovi_primarni, oznake_primarne, nacin_za_izbor
        )
        if tuple(izbor_ablacije) != tuple(baza_pravila):
            print(
                f"\nNapomena: ablacija predlaže {oznacen_naziv(izbor_ablacije)}, "
                f"a baza zadržava {oznacen_naziv(baza_pravila)}. "
                "n01 ne menja odluku o SPAM-u, samo podiže sumnju; zadržan je "
                "radi uloge potvrde. Vidi README, Validation and Limitations."
            )
    else:
        print(
            f"\n[upozorenje] nema {putanja_primarnog}; "
            f"koristi se podrazumevani skup {oznacen_naziv(baza_pravila)}"
        )

    for kljuc, (naziv, putanja) in korpusi:
        # model se cuva samo za primarni (engleski email) korpus
        obradi_korpus(
            naziv, putanja, rezimi, baza_pravila, sacuvaj_model=(kljuc == "email")
        )


if __name__ == "__main__":
    main()
