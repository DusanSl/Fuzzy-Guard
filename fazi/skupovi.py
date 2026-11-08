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
score_legitiman           = fuzz.trapmf(x_spam_score, [0, 0, 8, 20])
score_legitiman_energicno = fuzz.trimf (x_spam_score, [10, 13, 22])
score_blago_sumnjiv       = fuzz.trimf (x_spam_score, [24, 30, 42])
score_sumnjiv             = fuzz.trimf (x_spam_score, [38, 44, 58])
score_visoko_sumnjiv      = fuzz.trimf (x_spam_score, [54, 60, 74])
score_spam                = fuzz.trapmf(x_spam_score, [72, 88, 100, 100])

# Imena izlaznih skupova -> lingvisticka kategorija koja se prikazuje korisniku.
izlazni_skupovi = {
    "legitiman":      score_legitiman,
    "energicno":      score_legitiman_energicno,
    "blago_sumnjiv":  score_blago_sumnjiv,
    "sumnjiv":        score_sumnjiv,
    "visoko_sumnjiv": score_visoko_sumnjiv,
    "spam":           score_spam,
}

KATEGORIJA_PO_SKUPU = {
    "legitiman":      "LEGITIMAN",
    "energicno":      "LEGITIMAN",
    "blago_sumnjiv":  "SUMNJIVO",
    "sumnjiv":        "SUMNJIVO",
    "visoko_sumnjiv": "SUMNJIVO",
    "spam":           "SPAM",
}


def stepen_pripadnosti(x_univerzum, funkcija_pripadnosti, vrednost: float) -> float:
    return float(fuzz.interp_membership(x_univerzum, funkcija_pripadnosti, vrednost))
