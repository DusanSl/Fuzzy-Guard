import numpy as np
from fazi.skupovi import (
    x_kljucne_reci,  kljucne_zanemarljive, kljucne_zastupljene, kljucne_dominantne,
    x_broj_linkova,  linkovi_minimalni,    linkovi_umereni,     linkovi_brojni,
    x_caps_procenat, caps_uobicajen,       caps_poviseni,       caps_blago_povisen, caps_agresivan,
    x_interpunkcija, interpunkcija_retka,  interpunkcija_blago, interpunkcija_umerena, interpunkcija_agresivna,
    x_nn_pouzdanje,  nn_nisko,             nn_srednje,          nn_visoko,
    score_legitiman, score_legitiman_energicno, score_blago_sumnjiv,
    score_sumnjiv, score_visoko_sumnjiv, score_spam,
    stepen_pripadnosti,
)


def fuzzifikuj(
    val_kljucne:       float,
    val_linkovi:       float,
    val_caps:          float,
    val_interpunkcija: float,
    val_nn:            float,
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
        "nn_pouzdanje": {
            "nisko":   stepen_pripadnosti(x_nn_pouzdanje, nn_nisko,   val_nn),
            "srednje": stepen_pripadnosti(x_nn_pouzdanje, nn_srednje, val_nn),
            "visoko":  stepen_pripadnosti(x_nn_pouzdanje, nn_visoko,  val_nn),
        },
    }


def sastavi_pravila(mu: dict) -> list:
    """Vraca listu pravila kao (naziv, jacina, izlazni skup, kategorija).

    Pravila su numerisana u jednom neprekinutom nizu p01, p02, ... p17.
    Suffiks (p03a, p06a) sme da nosi samo pravilo koje je bliska varijanta
    prethodnog; nikad ne sme da napravi prazninu u numeraciji.

    Neuro-fazi blok (n01-n02) je odvojen prefiksom ``n`` da bi se lako
    izdvojio u ablaciji. Nijedno ``n`` pravilo ne vodi u SPAM: mreza je
    potvrda ili ublažavanje, nikad jedini dokaz.

    Jacina je fazi AND (min) / OR (max) nad stepenima pripadnosti.
    """
    kljucne_reci  = mu["kljucne_reci"]
    broj_linkova  = mu["broj_linkova"]
    caps_procenat = mu["caps_procenat"]
    interpunkcija = mu["interpunkcija"]
    nn_pouzdanje  = mu["nn_pouzdanje"]

    return [
        # --- LEGITIMNO ---------------------------------------------------
        # p01 — zanemarljive reci, minimalni linkovi, uobicajena slova, retka interpunkcija
        ("p01", min(kljucne_reci["zanemarljive"], broj_linkova["minimalni"],
                    caps_procenat["uobicajen"], interpunkcija["retka"]),
         score_legitiman, "LEGITIMAN"),

        # p02 — blago povisena slova, zanemarljive reci, minimalni linkovi
        ("p02", min(caps_procenat["blago"], kljucne_reci["zanemarljive"],
                    broj_linkova["minimalni"]),
         score_legitiman_energicno, "LEGITIMAN"),

        # p03 — blaga interpunkcija, zanemarljive reci, minimalni linkovi
        ("p03", min(interpunkcija["blago"], kljucne_reci["zanemarljive"],
                    broj_linkova["minimalni"]),
         score_legitiman_energicno, "LEGITIMAN"),

        # p03a — varijanta p03: umerena interpunkcija umesto blage
        ("p03a", min(interpunkcija["umerena"], kljucne_reci["zanemarljive"],
                     broj_linkova["minimalni"]),
         score_legitiman_energicno, "LEGITIMAN"),

        # --- BLAGO SUMNJIVO ----------------------------------------------
        # p04 — zanemarljive reci, umereni linkovi, uobicajena slova, retka interpunkcija
        ("p04", min(kljucne_reci["zanemarljive"], broj_linkova["umereni"],
                    caps_procenat["uobicajen"], interpunkcija["retka"]),
         score_blago_sumnjiv, "SUMNJIVO"),

        # --- SUMNJIVO ----------------------------------------------------
        # p05 — zastupljene reci, minimalni linkovi
        ("p05", min(kljucne_reci["zastupljene"], broj_linkova["minimalni"]),
         score_sumnjiv, "SUMNJIVO"),

        # p06 — zastupljene reci, umereni linkovi, uobicajena slova, retka interpunkcija
        ("p06", min(kljucne_reci["zastupljene"], broj_linkova["umereni"],
                    caps_procenat["uobicajen"], interpunkcija["retka"]),
         score_sumnjiv, "SUMNJIVO"),

        # p06a — varijanta p06 bez uslova na velika slova i interpunkciju
        ("p06a", min(kljucne_reci["zastupljene"], broj_linkova["umereni"]),
         score_sumnjiv, "SUMNJIVO"),

        # p07 — umereni/brojni linkovi, povisena/blaga/agresivna slova, zanemarljive reci
        ("p07", min(max(broj_linkova["umereni"], broj_linkova["brojni"]),
                    max(caps_procenat["poviseni"], caps_procenat["blago"],
                        caps_procenat["agresivan"]),
                    kljucne_reci["zanemarljive"]),
         score_sumnjiv, "SUMNJIVO"),

        # p08 — umereni/brojni linkovi, umerena/blaga/agresivna interpunkcija, zanemarljive reci
        ("p08", min(max(broj_linkova["umereni"], broj_linkova["brojni"]),
                    max(interpunkcija["umerena"], interpunkcija["blago"],
                        interpunkcija["agresivna"]),
                    kljucne_reci["zanemarljive"]),
         score_sumnjiv, "SUMNJIVO"),

        # --- VISOKO SUMNJIVO ---------------------------------------------
        # p09 — zastupljene reci, umereni linkovi, povisena slova, umerena interpunkcija
        ("p09", min(kljucne_reci["zastupljene"], broj_linkova["umereni"],
                    caps_procenat["poviseni"], interpunkcija["umerena"]),
         score_visoko_sumnjiv, "SUMNJIVO"),

        # p10 — dominantne reci, umereni linkovi, uobicajena slova, retka interpunkcija
        ("p10", min(kljucne_reci["dominantne"], broj_linkova["umereni"],
                    caps_procenat["uobicajen"], interpunkcija["retka"]),
         score_visoko_sumnjiv, "SUMNJIVO"),

        # p11 — dominantne reci, uobicajena slova
        ("p11", min(kljucne_reci["dominantne"], caps_procenat["uobicajen"]),
         score_visoko_sumnjiv, "SUMNJIVO"),

        # p12 — agresivna slova, zanemarljive reci, minimalni linkovi
        ("p12", min(caps_procenat["agresivan"], kljucne_reci["zanemarljive"],
                    broj_linkova["minimalni"]),
         score_visoko_sumnjiv, "SUMNJIVO"),

        # p13 — agresivna interpunkcija, zanemarljive reci, minimalni linkovi
        ("p13", min(interpunkcija["agresivna"], kljucne_reci["zanemarljive"],
                    broj_linkova["minimalni"]),
         score_visoko_sumnjiv, "SUMNJIVO"),

        # --- SPAM --------------------------------------------------------
        # p14 — dominantne reci ili brojni linkovi
        ("p14", max(kljucne_reci["dominantne"], broj_linkova["brojni"]),
         score_spam, "SPAM"),

        # p15 — zastupljene reci i (agresivna slova ili agresivna interpunkcija)
        ("p15", min(kljucne_reci["zastupljene"],
                    max(caps_procenat["agresivan"], interpunkcija["agresivna"])),
         score_spam, "SPAM"),

        # p16 — umereni linkovi i (agresivna slova ili agresivna interpunkcija)
        ("p16", min(broj_linkova["umereni"],
                    max(caps_procenat["agresivan"], interpunkcija["agresivna"])),
         score_spam, "SPAM"),

        # p17 — (zastupljene ili dominantne) reci, (umereni ili brojni) linkovi,
        #        (povisena ili blaga ili agresivna) slova
        ("p17", min(max(kljucne_reci["zastupljene"], kljucne_reci["dominantne"]),
                    max(broj_linkova["umereni"], broj_linkova["brojni"]),
                    max(caps_procenat["poviseni"], caps_procenat["blago"],
                        caps_procenat["agresivan"])),
         score_spam, "SPAM"),

        # --- NEURO-FAZI POTVRDA ------------------------------------------
        # Mreza nikad nije jedini uslov. Ako je visoko sigurna, moze samo da
        # podigne sumnju na "visoko sumnjivo" uz dokaz iz teksta. Ako je nisko
        # sigurna, moze da ublazi "samo mnogo linkova" obrazac, ali linkovi i
        # dalje moraju biti brojni. Nijedno n pravilo ne vodi u SPAM.
        # n01 — mreza visoko + (zastupljene ili dominantne) reci
        ("n01", min(nn_pouzdanje["visoko"],
                    max(kljucne_reci["zastupljene"], kljucne_reci["dominantne"])),
         score_visoko_sumnjiv, "SUMNJIVO"),

        # n02 — mreza nisko + brojni linkovi: mreza kaze da obrazac nije spam,
        # pa linkovi sami ne smeju da drze ocenu u spam opsegu.
        ("n02", min(nn_pouzdanje["nisko"], broj_linkova["brojni"]),
         score_blago_sumnjiv, "SUMNJIVO"),
    ]


def kontroler_spam_score(mu: dict):
    pravila = sastavi_pravila(mu)

    aktivacije = [np.fmin(jacina, izlazni_skup) for _, jacina, izlazni_skup, _ in pravila]
    agregirani_skup = np.fmax.reduce(aktivacije)

    alfe = {"LEGITIMAN": 0.0, "SUMNJIVO": 0.0, "SPAM": 0.0}
    for _, jacina, _, kategorija in pravila:
        alfe[kategorija] = max(alfe[kategorija], float(jacina))

    return agregirani_skup, alfe


# Kratki, citljivi uslovi za svako pravilo (za panel "Zasto" u interfejsu).
OPISI_PRAVILA = {
    "p01": {
        "sr": "zanemarljive reči + minimalni linkovi + uobičajena velika slova + retka interpunkcija",
        "en": "negligible keywords + minimal links + normal caps + sparse punctuation",
    },
    "p02": {
        "sr": "blago povišena velika slova + zanemarljive reči + minimalni linkovi",
        "en": "mildly elevated caps + negligible keywords + minimal links",
    },
    "p03": {
        "sr": "blaga interpunkcija + zanemarljive reči + minimalni linkovi",
        "en": "mild punctuation + negligible keywords + minimal links",
    },
    "p03a": {
        "sr": "umerena interpunkcija + zanemarljive reči + minimalni linkovi",
        "en": "moderate punctuation + negligible keywords + minimal links",
    },
    "p04": {
        "sr": "zanemarljive reči + umereni linkovi + uobičajena velika slova + retka interpunkcija",
        "en": "negligible keywords + moderate links + normal caps + sparse punctuation",
    },
    "p05": {
        "sr": "zastupljene reči + minimalni linkovi",
        "en": "present keywords + minimal links",
    },
    "p06": {
        "sr": "zastupljene reči + umereni linkovi + uobičajena velika slova + retka interpunkcija",
        "en": "present keywords + moderate links + normal caps + sparse punctuation",
    },
    "p06a": {
        "sr": "zastupljene reči + umereni linkovi",
        "en": "present keywords + moderate links",
    },
    "p07": {
        "sr": "umereni/brojni linkovi + povišena/blaga/agresivna velika slova + zanemarljive reči",
        "en": "moderate/numerous links + elevated/mild/aggressive caps + negligible keywords",
    },
    "p08": {
        "sr": "umereni/brojni linkovi + umerena/blaga/agresivna interpunkcija + zanemarljive reči",
        "en": "moderate/numerous links + moderate/mild/aggressive punctuation + negligible keywords",
    },
    "p09": {
        "sr": "zastupljene reči + umereni linkovi + povišena velika slova + umerena interpunkcija",
        "en": "present keywords + moderate links + elevated caps + moderate punctuation",
    },
    "p10": {
        "sr": "dominantne reči + umereni linkovi + uobičajena velika slova + retka interpunkcija",
        "en": "dominant keywords + moderate links + normal caps + sparse punctuation",
    },
    "p11": {
        "sr": "dominantne reči + uobičajena velika slova",
        "en": "dominant keywords + normal caps",
    },
    "p12": {
        "sr": "agresivna velika slova + zanemarljive reči + minimalni linkovi",
        "en": "aggressive caps + negligible keywords + minimal links",
    },
    "p13": {
        "sr": "agresivna interpunkcija + zanemarljive reči + minimalni linkovi",
        "en": "aggressive punctuation + negligible keywords + minimal links",
    },
    "p14": {
        "sr": "dominantne reči ILI brojni linkovi",
        "en": "dominant keywords OR numerous links",
    },
    "p15": {
        "sr": "zastupljene reči + (agresivna velika slova ILI agresivna interpunkcija)",
        "en": "present keywords + (aggressive caps OR aggressive punctuation)",
    },
    "p16": {
        "sr": "umereni linkovi + (agresivna velika slova ILI agresivna interpunkcija)",
        "en": "moderate links + (aggressive caps OR aggressive punctuation)",
    },
    "p17": {
        "sr": "(zastupljene ili dominantne) reči + (umereni ili brojni) linkovi + (povišena, blaga ili agresivna) velika slova",
        "en": "(present or dominant) keywords + (moderate or numerous) links + (elevated, mild or aggressive) caps",
    },
    "n01": {
        "sr": "mreža visoko + (zastupljene ili dominantne) reči",
        "en": "network high + (present or dominant) keywords",
    },
    "n02": {
        "sr": "mreža nisko + brojni linkovi",
        "en": "network low + numerous links",
    },
}
