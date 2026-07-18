import numpy as np
from fazi.skupovi import (
    x_kljucne_reci,  kljucne_zanemarljive, kljucne_zastupljene, kljucne_dominantne,
    x_broj_linkova,  linkovi_minimalni,    linkovi_umereni,     linkovi_brojni,
    x_caps_procenat, caps_uobicajen,       caps_poviseni,       caps_blago_povisen, caps_agresivan,
    x_interpunkcija, interpunkcija_retka,  interpunkcija_blago, interpunkcija_umerena, interpunkcija_agresivna,
    score_legitiman, score_legitiman_energicno, score_sumnjiv, score_spam,
    stepen_pripadnosti,
)


def fuzzifikuj(
    val_kljucne:     float,
    val_linkovi:     float,
    val_caps:        float,
    val_interpunkcija: float,
) -> dict:
    return {
        "kljucne_reci": {
            "zanemarljive": stepen_pripadnosti(x_kljucne_reci, kljucne_zanemarljive, val_kljucne),
            "zastupljene":  stepen_pripadnosti(x_kljucne_reci, kljucne_zastupljene,  val_kljucne),
            "dominantne":   stepen_pripadnosti(x_kljucne_reci, kljucne_dominantne,   val_kljucne),
        },
        "broj_linkova": {
            "minimalni": stepen_pripadnosti(x_broj_linkova, linkovi_minimalni, val_linkovi),
            "umereni":   stepen_pripadnosti(x_broj_linkova, linkovi_umereni,   val_linkovi),
            "brojni":    stepen_pripadnosti(x_broj_linkova, linkovi_brojni,    val_linkovi),
        },
        "caps_procenat": {
            "uobicajen": stepen_pripadnosti(x_caps_procenat, caps_uobicajen, val_caps),
            "poviseni":  stepen_pripadnosti(x_caps_procenat, caps_poviseni,  val_caps),
            "blago":     stepen_pripadnosti(x_caps_procenat, caps_blago_povisen, val_caps),
            "agresivan": stepen_pripadnosti(x_caps_procenat, caps_agresivan, val_caps),
        },
        "interpunkcija": {
            "retka":     stepen_pripadnosti(x_interpunkcija, interpunkcija_retka,     val_interpunkcija),
            "blago":     stepen_pripadnosti(x_interpunkcija, interpunkcija_blago,     val_interpunkcija),
            "umerena":   stepen_pripadnosti(x_interpunkcija, interpunkcija_umerena,   val_interpunkcija),
            "agresivna": stepen_pripadnosti(x_interpunkcija, interpunkcija_agresivna, val_interpunkcija),
        },
    }


def kontroler_spam_score(mu: dict):
    kljucne = mu["kljucne_reci"]
    linkovi = mu["broj_linkova"]
    caps    = mu["caps_procenat"]
    inter   = mu["interpunkcija"]

    aktivacije = []
    alfa_legitiman = []
    alfa_sumnjiv   = []
    alfa_spam      = []

    # LEGITIMATE
    p01 = min(kljucne["zanemarljive"], linkovi["minimalni"], caps["uobicajen"], inter["retka"])
    aktivacije.append(np.fmin(p01, score_legitiman))
    alfa_legitiman.append(p01)

    # LEGITIMATE_ENERGETIC
    p02 = min(caps["blago"], kljucne["zanemarljive"], linkovi["minimalni"])
    aktivacije.append(np.fmin(p02, score_legitiman_energicno))
    alfa_legitiman.append(p02)
    p03 = min(inter["blago"], kljucne["zanemarljive"], linkovi["minimalni"])
    aktivacije.append(np.fmin(p03, score_legitiman_energicno))
    alfa_legitiman.append(p03)

    # SUSPICIOUS
    p04 = min(kljucne["zastupljene"], linkovi["umereni"], caps["poviseni"], inter["umerena"])
    aktivacije.append(np.fmin(p04, score_sumnjiv))
    alfa_sumnjiv.append(p04)
    p05 = min(kljucne["zastupljene"], linkovi["minimalni"])
    aktivacije.append(np.fmin(p05, score_sumnjiv))
    alfa_sumnjiv.append(p05)
    p06 = min(
        np.fmax(kljucne["zanemarljive"], kljucne["zastupljene"]),
        linkovi["umereni"],
        caps["uobicajen"],
        inter["retka"],
    )
    aktivacije.append(np.fmin(p06, score_sumnjiv))
    alfa_sumnjiv.append(p06)
    p07 = min(kljucne["dominantne"], caps["uobicajen"])
    aktivacije.append(np.fmin(p07, score_sumnjiv))
    alfa_sumnjiv.append(p07)
    p08 = min(caps["agresivan"], kljucne["zanemarljive"], linkovi["minimalni"])
    aktivacije.append(np.fmin(p08, score_sumnjiv))
    alfa_sumnjiv.append(p08)
    p09 = min(inter["agresivna"], kljucne["zanemarljive"], linkovi["minimalni"])
    aktivacije.append(np.fmin(p09, score_sumnjiv))
    alfa_sumnjiv.append(p09)

    # SPAM
    p10 = np.fmax(kljucne["dominantne"], linkovi["brojni"])
    aktivacije.append(np.fmin(p10, score_spam))
    alfa_spam.append(p10)
    p11 = min(kljucne["zastupljene"], np.fmax(caps["agresivan"], inter["agresivna"]))
    aktivacije.append(np.fmin(p11, score_spam))
    alfa_spam.append(p11)
    p12 = min(linkovi["umereni"], np.fmax(caps["agresivan"], inter["agresivna"]))
    aktivacije.append(np.fmin(p12, score_spam))
    alfa_spam.append(p12)
    p13 = kljucne["dominantne"]
    aktivacije.append(np.fmin(p13, score_spam))
    alfa_spam.append(p13)
    p14 = min(
        np.fmax(kljucne["zastupljene"], kljucne["dominantne"]),
        np.fmax(linkovi["umereni"], linkovi["brojni"]),
        np.fmax(caps["poviseni"], caps["agresivan"])
    )
    aktivacije.append(np.fmin(p14, score_spam))
    alfa_spam.append(p14)

    agregirani_skup = np.fmax.reduce(aktivacije)
    alfe = {
        "LEGITIMAN": max(alfa_legitiman),
        "SUMNJIVO":  max(alfa_sumnjiv),
        "SPAM":      max(alfa_spam),
    }
    return agregirani_skup, alfe