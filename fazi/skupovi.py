import numpy as np
import skfuzzy as fuzz

x_kljucne_reci  = np.arange(0, 11, 1)
x_broj_linkova  = np.arange(0, 11, 1)
x_caps_procenat = np.arange(0, 101, 1)
x_interpunkcija = np.arange(0, 101, 1)

x_spam_score    = np.arange(0, 101, 1)

kljucne_zanemarljive = fuzz.trapmf(x_kljucne_reci, [0, 0, 1, 3])
kljucne_zastupljene  = fuzz.trimf (x_kljucne_reci, [1, 4, 7])
kljucne_dominantne   = fuzz.trapmf(x_kljucne_reci, [5, 7, 10, 10])

linkovi_minimalni = fuzz.trapmf(x_broj_linkova, [0, 0, 0, 1])
linkovi_umereni   = fuzz.trimf (x_broj_linkova, [0, 1, 3])
linkovi_brojni    = fuzz.trapmf(x_broj_linkova, [2, 4, 10, 10])

caps_uobicajen = fuzz.trapmf(x_caps_procenat, [0, 0, 1, 10])
caps_poviseni  = fuzz.trimf (x_caps_procenat, [7, 18, 35])
caps_blago_povisen = fuzz.trimf(x_caps_procenat, [10, 35, 60])
caps_agresivan = fuzz.trapmf(x_caps_procenat, [60, 85, 100, 100])

interpunkcija_retka = fuzz.trapmf(x_interpunkcija, [0, 0, 2, 5])
interpunkcija_blago = fuzz.trimf(x_interpunkcija, [3, 15, 30])
interpunkcija_umerena   = fuzz.trimf (x_interpunkcija, [8, 15, 25])
interpunkcija_agresivna = fuzz.trapmf(x_interpunkcija, [15, 25, 100, 100])

score_legitiman = fuzz.trapmf(x_spam_score, [0, 0, 8, 20])
score_legitiman_energicno = fuzz.trimf(x_spam_score, [10, 15, 20])
score_sumnjiv = fuzz.trimf (x_spam_score, [20, 40, 65])
score_spam    = fuzz.trapmf(x_spam_score, [55, 75, 100, 100])


def stepen_pripadnosti(x_universe, mf, vrednost: float) -> float:
    return float(fuzz.interp_membership(x_universe, mf, vrednost))