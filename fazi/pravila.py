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
    val_kljucne:       float,
    val_linkovi:       float,
    val_caps:          float,
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
            "uobicajen": stepen_pripadnosti(x_caps_procenat, caps_uobicajen,       val_caps),
            "poviseni":  stepen_pripadnosti(x_caps_procenat, caps_poviseni,        val_caps),
            "blago":     stepen_pripadnosti(x_caps_procenat, caps_blago_povisen,   val_caps),
            "agresivan": stepen_pripadnosti(x_caps_procenat, caps_agresivan,       val_caps),
        },
        "interpunkcija": {
            "retka":     stepen_pripadnosti(x_interpunkcija, interpunkcija_retka,     val_interpunkcija),
            "blago":     stepen_pripadnosti(x_interpunkcija, interpunkcija_blago,     val_interpunkcija),
            "umerena":   stepen_pripadnosti(x_interpunkcija, interpunkcija_umerena,   val_interpunkcija),
            "agresivna": stepen_pripadnosti(x_interpunkcija, interpunkcija_agresivna, val_interpunkcija),
        },
    }


def sastavi_pravila(mu: dict) -> list:
    """Vraca listu pravila kao (naziv, jacina, izlazni skup, kategorija).

    Jacina je fazi AND (min) / OR (max) nad stepenima pripadnosti.
    """
    kljucne_reci  = mu["kljucne_reci"]
    broj_linkova  = mu["broj_linkova"]
    caps_procenat = mu["caps_procenat"]
    interpunkcija = mu["interpunkcija"]

    return [
        # LEGITIMNO
        ("p01", min(kljucne_reci["zanemarljive"], broj_linkova["minimalni"],
                    caps_procenat["uobicajen"], interpunkcija["retka"]),
         score_legitiman, "LEGITIMAN"),
        ("p02", min(caps_procenat["blago"], kljucne_reci["zanemarljive"],
                    broj_linkova["minimalni"]),
         score_legitiman_energicno, "LEGITIMAN"),
        ("p03", min(interpunkcija["blago"], kljucne_reci["zanemarljive"],
                    broj_linkova["minimalni"]),
         score_legitiman_energicno, "LEGITIMAN"),
        # Bez kljucnih reci i bez linkova, umerena interpunkcija je jedini
        # signal i nije dovoljna za sumnju (pokriva tacke koje su ranije
        # ostajale bez ijednog aktivnog pravila).
        ("p03b", min(interpunkcija["umerena"], kljucne_reci["zanemarljive"],
                     broj_linkova["minimalni"]),
         score_legitiman_energicno, "LEGITIMAN"),

        # BLAGO SUMNJIVO - cist tekst sa jednim do dva linka
        ("p06a", min(kljucne_reci["zanemarljive"], broj_linkova["umereni"],
                     caps_procenat["uobicajen"], interpunkcija["retka"]),
         score_blago_sumnjiv, "SUMNJIVO"),

        # SUMNJIVO - prisutne kljucne reci, ostalo je jos uobicajeno
        ("p05", min(kljucne_reci["zastupljene"], broj_linkova["minimalni"]),
         score_sumnjiv, "SUMNJIVO"),
        ("p06b", min(kljucne_reci["zastupljene"], broj_linkova["umereni"],
                     caps_procenat["uobicajen"], interpunkcija["retka"]),
         score_sumnjiv, "SUMNJIVO"),
        ("p10", min(max(broj_linkova["umereni"], broj_linkova["brojni"]),
                    max(caps_procenat["poviseni"], caps_procenat["blago"],
                        caps_procenat["agresivan"]),
                    kljucne_reci["zanemarljive"]),
         score_sumnjiv, "SUMNJIVO"),
        ("p11", min(max(broj_linkova["umereni"], broj_linkova["brojni"]),
                    max(interpunkcija["umerena"], interpunkcija["blago"],
                        interpunkcija["agresivna"]),
                    kljucne_reci["zanemarljive"]),
         score_sumnjiv, "SUMNJIVO"),
        # Prisutne kljucne reci + umereni linkovi. Pokriva tacke koje su
        # ranije ostajale bez pravila jer je p11 zahtevalo zanemarljive reci.
        ("p17", min(kljucne_reci["zastupljene"], broj_linkova["umereni"]),
         score_sumnjiv, "SUMNJIVO"),

        # VISOKO SUMNJIVO - jedan jak signal ili cetiri umerena istovremeno
        ("p04", min(kljucne_reci["zastupljene"], broj_linkova["umereni"],
                    caps_procenat["poviseni"], interpunkcija["umerena"]),
         score_visoko_sumnjiv, "SUMNJIVO"),
        ("p06c", min(kljucne_reci["dominantne"], broj_linkova["umereni"],
                     caps_procenat["uobicajen"], interpunkcija["retka"]),
         score_visoko_sumnjiv, "SUMNJIVO"),
        ("p07", min(kljucne_reci["dominantne"], caps_procenat["uobicajen"]),
         score_visoko_sumnjiv, "SUMNJIVO"),
        ("p08", min(caps_procenat["agresivan"], kljucne_reci["zanemarljive"],
                    broj_linkova["minimalni"]),
         score_visoko_sumnjiv, "SUMNJIVO"),
        ("p09", min(interpunkcija["agresivna"], kljucne_reci["zanemarljive"],
                    broj_linkova["minimalni"]),
         score_visoko_sumnjiv, "SUMNJIVO"),

        # SPAM
        # p15 ("dominantne reci -> SPAM") je uklonjeno: p12 ga u potpunosti
        # pokriva preko max(...), pa nije dodavalo informaciju.
        ("p12", max(kljucne_reci["dominantne"], broj_linkova["brojni"]),
         score_spam, "SPAM"),
        ("p13", min(kljucne_reci["zastupljene"],
                    max(caps_procenat["agresivan"], interpunkcija["agresivna"])),
         score_spam, "SPAM"),
        ("p14", min(broj_linkova["umereni"],
                    max(caps_procenat["agresivan"], interpunkcija["agresivna"])),
         score_spam, "SPAM"),
        # p16 mora da ukljuci i blago_povisen: bez njega je opseg 35-45%
        # velikih slova ostajao nepokriven i skor je padao sa ~87 na 47.
        ("p16", min(max(kljucne_reci["zastupljene"], kljucne_reci["dominantne"]),
                    max(broj_linkova["umereni"], broj_linkova["brojni"]),
                    max(caps_procenat["poviseni"], caps_procenat["blago"],
                        caps_procenat["agresivan"])),
         score_spam, "SPAM"),
    ]


def kontroler_spam_score(mu: dict):
    pravila = sastavi_pravila(mu)

    aktivacije = [np.fmin(jacina, izlazni_skup) for _, jacina, izlazni_skup, _ in pravila]
    agregirani_skup = np.fmax.reduce(aktivacije)

    alfe = {"LEGITIMAN": 0.0, "SUMNJIVO": 0.0, "SPAM": 0.0}
    for _, jacina, _, kategorija in pravila:
        alfe[kategorija] = max(alfe[kategorija], float(jacina))

    return agregirani_skup, alfe
