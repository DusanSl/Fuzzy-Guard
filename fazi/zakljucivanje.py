import skfuzzy as fuzz

from fazi.pravila import (
    fuzzifikuj,
    kontroler_spam_score,
    sastavi_pravila,
)
from fazi.defazifikacija import defazifikuj
from fazi.skupovi import x_spam_score, izlazni_skupovi, KATEGORIJA_PO_SKUPU


def pokreni_fis(
    val_kljucne:       float,
    val_linkova:       float,
    val_caps:          float,
    val_interpunkcija: float,
) -> dict:

    mu = fuzzifikuj(val_kljucne, val_linkova, val_caps, val_interpunkcija)

    agregirani_skup, alfe = kontroler_spam_score(mu)

    spam_score = defazifikuj(agregirani_skup)

    if max(alfe.values()) == 0:
        # Nijedno pravilo nije aktivirano. Pravila bi trebalo da pokrivaju ceo
        # univerzum (testira se), pa je ovo samo zastita. Odsustvo dokaza nije
        # dokaz odsustva: takav email ide na proveru, nikako u LEGITIMAN.
        return {"spam_score": 47.0, "kategorija": "SUMNJIVO", "aktivna_pravila": []}

    # Kategoriju izvodimo iz istog broja koji se prikazuje korisniku: gledamo
    # kojoj izlaznoj skupini defazifikovana vrednost najvise pripada. Time su
    # broj i oznaka po definiciji saglasni.
    clanstva = {
        ime: float(fuzz.interp_membership(x_spam_score, skup, spam_score))
        for ime, skup in izlazni_skupovi.items()
    }
    najjaci_skup = max(clanstva, key=clanstva.get)

    # Najjaca aktivna pravila, za prikaz "zasto" u interfejsu i odbranu.
    aktivna_pravila = [
        {"pravilo": naziv, "jacina": round(float(jacina), 3), "kategorija": kategorija}
        for naziv, jacina, _, kategorija in sastavi_pravila(mu)
        if float(jacina) > 0.05
    ]
    aktivna_pravila.sort(key=lambda stavka: stavka["jacina"], reverse=True)

    return {
        "spam_score": spam_score,
        "kategorija": KATEGORIJA_PO_SKUPU[najjaci_skup],
        "aktivna_pravila": aktivna_pravila[:6],
    }
