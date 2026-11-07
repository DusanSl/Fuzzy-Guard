import numpy as np
from fazi.skupovi import (
    x_kljucne_reci,  kljucne_zanemarljive, kljucne_zastupljene, kljucne_dominantne,
    x_broj_linkova,  linkovi_minimalni,    linkovi_umereni,     linkovi_brojni,
    x_caps_procenat, caps_uobicajen,       caps_poviseni,       caps_blago_povisen, caps_agresivan,
    x_interpunkcija, interpunkcija_retka,  interpunkcija_blago, interpunkcija_umerena, interpunkcija_agresivna,
    score_legitiman, score_legitiman_energicno, score_blago_sumnjiv,
    score_sumnjiv, score_visoko_sumnjiv, score_spam,
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
    k = mu["kljucne_reci"]
    l = mu["broj_linkova"]
    c = mu["caps_procenat"]
    i = mu["interpunkcija"]

    # (naziv, jacina, izlazni skup, kategorija)
    # Jacina je fuzzy AND (min) / OR (max) nad stepenima pripadnosti.
    pravila = [
        # LEGITIMNO
        ("p01", min(k["zanemarljive"], l["minimalni"], c["uobicajen"], i["retka"]),
         score_legitiman, "LEGITIMAN"),
        ("p02", min(c["blago"], k["zanemarljive"], l["minimalni"]),
         score_legitiman_energicno, "LEGITIMAN"),
        ("p03", min(i["blago"], k["zanemarljive"], l["minimalni"]),
         score_legitiman_energicno, "LEGITIMAN"),

        # BLAGO SUMNJIVO - cist tekst sa jednim do dva linka
        ("p06a", min(k["zanemarljive"], l["umereni"], c["uobicajen"], i["retka"]),
         score_blago_sumnjiv, "SUMNJIVO"),

        # SUMNJIVO - prisutne kljucne reci, ostalo je jos uobicajeno
        ("p05",  min(k["zastupljene"], l["minimalni"]),
         score_sumnjiv, "SUMNJIVO"),
        ("p06b", min(k["zastupljene"], l["umereni"], c["uobicajen"], i["retka"]),
         score_sumnjiv, "SUMNJIVO"),
        ("p10",  min(max(l["umereni"], l["brojni"]), max(c["poviseni"], c["blago"]), k["zanemarljive"]),
         score_sumnjiv, "SUMNJIVO"),
        ("p11",  min(max(l["umereni"], l["brojni"]), max(i["umerena"], i["blago"]), k["zanemarljive"]),
         score_sumnjiv, "SUMNJIVO"),
        # VISOKO SUMNJIVO - jedan jak signal ili cetiri umerena istovremeno
        ("p04",  min(k["zastupljene"], l["umereni"], c["poviseni"], i["umerena"]),
         score_visoko_sumnjiv, "SUMNJIVO"),
        ("p06c", min(k["dominantne"], l["umereni"], c["uobicajen"], i["retka"]),
         score_visoko_sumnjiv, "SUMNJIVO"),
        ("p07",  min(k["dominantne"], c["uobicajen"]),
         score_visoko_sumnjiv, "SUMNJIVO"),
        ("p08",  min(c["agresivan"], k["zanemarljive"], l["minimalni"]),
         score_visoko_sumnjiv, "SUMNJIVO"),
        ("p09",  min(i["agresivna"], k["zanemarljive"], l["minimalni"]),
         score_visoko_sumnjiv, "SUMNJIVO"),

        # SPAM
        ("p12", np.fmax(k["dominantne"], l["brojni"]), score_spam, "SPAM"),
        ("p13", min(k["zastupljene"], np.fmax(c["agresivan"], i["agresivna"])),
         score_spam, "SPAM"),
        ("p14", min(l["umereni"], np.fmax(c["agresivan"], i["agresivna"])),
         score_spam, "SPAM"),
        ("p15", k["dominantne"], score_spam, "SPAM"),
        ("p16", min(max(k["zastupljene"], k["dominantne"]),
                    max(l["umereni"], l["brojni"]),
                    max(c["poviseni"], c["agresivan"])),
         score_spam, "SPAM"),
    ]

    aktivacije = [np.fmin(jacina, skup) for _, jacina, skup, _ in pravila]
    agregirani_skup = np.fmax.reduce(aktivacije)

    alfe = {"LEGITIMAN": 0.0, "SUMNJIVO": 0.0, "SPAM": 0.0}
    for _, jacina, _, kategorija in pravila:
        alfe[kategorija] = max(alfe[kategorija], float(jacina))

    return agregirani_skup, alfe
