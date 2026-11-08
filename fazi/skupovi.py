"""Univerzumi i fazi skupovi za Fuzzy Guard.

Svi skupovi su trouglasti (``trimf``) ili trapezoidni (``trapmf``), kako se
radi na kursu. Kod "losih" skupova desno rame se nalazi na kraju univerzuma,
pa pripadnost raste sve do maksimuma umesto da se rano zasiti. Zasiceno rame
brise informaciju: sa starim ``linkovi_brojni [2, 4, 10, 10]`` cetiri linka i
deset linkova daju istu pripadnost.
"""

import numpy as np
import skfuzzy as fuzz

x_kljucne_reci  = np.arange(0, 11, 1)
x_broj_linkova  = np.arange(0, 11, 1)
x_caps_procenat = np.arange(0, 101, 1)
x_interpunkcija = np.arange(0, 101, 1)

x_spam_score    = np.arange(0, 101, 1)

# --- Kljucne reci (0-10) -------------------------------------------------
kljucne_zanemarljive = fuzz.trapmf(x_kljucne_reci, [0, 0, 1, 3])
# Temе prebaceno sa 4 na 3: sa simetricnim [1, 4, 7] tri i pet kljucnih reci
# daju istu pripadnost 0.667, pa sistem ne moze da ih razlikuje.
kljucne_zastupljene  = fuzz.trimf (x_kljucne_reci, [1, 3, 7])
kljucne_dominantne   = fuzz.trapmf(x_kljucne_reci, [5, 8, 10, 10])

# --- Broj linkova (0-10) -------------------------------------------------
linkovi_minimalni = fuzz.trapmf(x_broj_linkova, [0, 0, 0, 1])
linkovi_umereni   = fuzz.trimf (x_broj_linkova, [0, 1, 3])
linkovi_brojni    = fuzz.trapmf(x_broj_linkova, [2, 8, 10, 10])

# --- Procenat velikih slova (0-100%) -------------------------------------
caps_uobicajen = fuzz.trapmf(x_caps_procenat, [0, 0, 1, 12])
caps_poviseni  = fuzz.trimf (x_caps_procenat, [7, 16, 32])
caps_blago_povisen = fuzz.trimf(x_caps_procenat, [10, 25, 65])
# Donja granica 45: legitimni primeri imaju do ~6% velikih slova, spam 26-60%.
caps_agresivan = fuzz.trapmf(x_caps_procenat, [45, 85, 100, 100])

# --- Interpunkcija (0-100%) ----------------------------------------------
interpunkcija_retka = fuzz.trapmf(x_interpunkcija, [0, 0, 2, 5])
interpunkcija_blago = fuzz.trimf (x_interpunkcija, [2, 5, 10])
interpunkcija_umerena   = fuzz.trimf (x_interpunkcija, [6, 12, 25])
# Najveca izmerena vrednost na uzorcima je ~14%. "Agresivna" zato mora da
# pocne tek na 14 i da ima prostora iznad toga; ranije je dostizala 1.0 vec
# na 14, pa je obican email sa par uzvika glasio kao maksimalno agresivan.
interpunkcija_agresivna = fuzz.trapmf(x_interpunkcija, [14, 40, 100, 100])

# --- Izlaz: spam skor (0-100) --------------------------------------------
# Sest stepenovanih izlaznih skupova. Trouglovi nisu idealno simetricni: kod
# savrseno simetricnog trougla teziste ne zavisi od jacine aktivacije, pa bi
# svako pravilo koje se aktivira dalo isti skor bez obzira na stepen.
# Definicije izlaznih skupova. Jedan izvor istine — iz ovoga se grade i numpy
# skupovi i /skupovi endpoint koji front-end koristi da nacrta spektar.
IZLAZNI_SKUPOVI_DEFINICIJE = {
    "legitiman": {
        "tip": "trapmf", "params": (0, 0, 8, 20),
        "kategorija": "LEGITIMAN", "naziv": "legitiman",
    },
    "energicno": {
        "tip": "trimf", "params": (10, 13, 22),
        "kategorija": "LEGITIMAN", "naziv": "legitiman energično",
    },
    "blago_sumnjiv": {
        "tip": "trimf", "params": (24, 30, 42),
        "kategorija": "SUMNJIVO", "naziv": "blago sumnjiv",
    },
    "sumnjiv": {
        "tip": "trimf", "params": (38, 44, 58),
        "kategorija": "SUMNJIVO", "naziv": "sumnjiv",
    },
    "visoko_sumnjiv": {
        "tip": "trimf", "params": (54, 60, 74),
        "kategorija": "SUMNJIVO", "naziv": "visoko sumnjiv",
    },
    "spam": {
        "tip": "trapmf", "params": (72, 88, 100, 100),
        "kategorija": "SPAM", "naziv": "spam",
    },
}


def _napravi_izlazni_skup(definicija):
    return getattr(fuzz, definicija["tip"])(x_spam_score, list(definicija["params"]))


score_legitiman           = _napravi_izlazni_skup(IZLAZNI_SKUPOVI_DEFINICIJE["legitiman"])
score_legitiman_energicno = _napravi_izlazni_skup(IZLAZNI_SKUPOVI_DEFINICIJE["energicno"])
score_blago_sumnjiv       = _napravi_izlazni_skup(IZLAZNI_SKUPOVI_DEFINICIJE["blago_sumnjiv"])
score_sumnjiv             = _napravi_izlazni_skup(IZLAZNI_SKUPOVI_DEFINICIJE["sumnjiv"])
score_visoko_sumnjiv      = _napravi_izlazni_skup(IZLAZNI_SKUPOVI_DEFINICIJE["visoko_sumnjiv"])
score_spam                = _napravi_izlazni_skup(IZLAZNI_SKUPOVI_DEFINICIJE["spam"])

izlazni_skupovi = {
    ime: _napravi_izlazni_skup(definicija)
    for ime, definicija in IZLAZNI_SKUPOVI_DEFINICIJE.items()
}

KATEGORIJA_PO_SKUPU = {
    ime: definicija["kategorija"]
    for ime, definicija in IZLAZNI_SKUPOVI_DEFINICIJE.items()
}


def stepen_pripadnosti(x_univerzum, funkcija_pripadnosti, vrednost: float) -> float:
    return float(fuzz.interp_membership(x_univerzum, funkcija_pripadnosti, vrednost))
