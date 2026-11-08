"""Evaluacija fazi sistema na ručno označenim primerima iz ``primeri.txt``.

Ovo nije benchmark: 96 primera je malo i kategorije su ručno korigovane.
Skript služi da se pošteno prikaže ponašanje na realnom srpskom tekstu, za
razliku od mašinski prevedenog korpusa.

Kategorije: ``legitiman`` -> ham, ``prevara`` -> spam, ``sumnjiv`` se preskače
jer nije binarna oznaka.

Pokretanje::

    python -m neuronska_mreza.evaluiraj_sr
"""

from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score

from fazi.zakljucivanje import pokreni_fis
from obrada_teksta.analizator import analiziraj_email, ucitaj_sve_primere

REZIMI = ("en", "sr", "kombinovano")


def main():
    for jezik_primera in ("sr", "en"):
        primeri = ucitaj_sve_primere(jezik_primera)
        oznaceni = [
            (primer, 1 if primer["kategorija"] == "prevara" else 0)
            for primer in primeri
            if primer["kategorija"] in ("legitiman", "prevara")
        ]
        if not oznaceni:
            continue

        istinite = [oznaka for _, oznaka in oznaceni]
        print(f"\n=== primeri.txt ({jezik_primera}) — {len(oznaceni)} primera, "
              f"{sum(istinite)} spama ===")

        for nacin in REZIMI:
            predvidjene = []
            for primer, _ in oznaceni:
                ulazi = analiziraj_email(primer["tekst"], nacin_recnik=nacin)
                rezultat = pokreni_fis(
                    ulazi["kljucne_reci"],
                    ulazi["broj_linkova"],
                    ulazi["caps_procenat"],
                    ulazi["interpunkcija"],
                )
                predvidjene.append(1 if rezultat["kategorija"] == "SPAM" else 0)

            print(
                f"  {nacin:13s} tacnost={accuracy_score(istinite, predvidjene):.3f} "
                f"preciznost={precision_score(istinite, predvidjene, zero_division=0):.3f} "
                f"odziv={recall_score(istinite, predvidjene, zero_division=0):.3f} "
                f"F1={f1_score(istinite, predvidjene, zero_division=0):.3f}"
            )
            print(f"  {'':13s} matrica={confusion_matrix(istinite, predvidjene).tolist()}")


if __name__ == "__main__":
    main()
