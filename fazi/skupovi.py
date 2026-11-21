"""Univerzumi i fazi skupovi za Fuzzy Guard.

Svi skupovi su trouglasti (``trimf``) ili trapezoidni (``trapmf``), kako se
radi na kursu. Numpy skupovi se grade direktno ispod, a
``ULAZNI_SKUPOVI_DEFINICIJE`` / ``IZLAZNI_SKUPOVI_DEFINICIJE`` služe endpointu
``GET /skupovi`` za crtanje u interfejsu.

Kod "loših" skupova desno rame se nalazi na kraju univerzuma, pa pripadnost
raste sve do maksimuma umesto da se rano zasiti. Zasićeno rame briše
informaciju: sa starim ``linkovi_brojni [2, 4, 10, 10]`` četiri linka i
deset linkova daju istu pripadnost.

``energicno`` je trougao ``[10, 13, 22]``, a ``blago_sumnjiv`` počinje na 22.
Na samoj vrednosti 22 oba imaju pripadnost nula; za taj jedan granični slučaj
``pokreni_fis`` ima eksplicitni fallback na ``SUMNJIVO``.
"""

import numpy as np
import skfuzzy as fuzz

x_kljucne_reci  = np.arange(0, 11, 1)
x_broj_linkova  = np.arange(0, 11, 1)
x_caps_procenat = np.arange(0, 101, 1)
x_interpunkcija = np.arange(0, 101, 1)
x_nn_pouzdanje  = np.arange(0, 101, 1)

x_spam_score    = np.arange(0, 101, 1)

UNIVERZUMI = {
    "kljucne_reci":  x_kljucne_reci,
    "broj_linkova":  x_broj_linkova,
    "caps_procenat": x_caps_procenat,
    "interpunkcija": x_interpunkcija,
    "nn_pouzdanje":  x_nn_pouzdanje,
}

# --- Ulazni skupovi -------------------------------------------------------
# Jedan izvor istine za numpy skupove i za crtanje u interfejsu.
# Kategorija opisuje smer signala (LEGITIMAN / SUMNJIVO / SPAM) i koristi se
# samo za boju u spektru.
ULAZNI_SKUPOVI_DEFINICIJE = {
    "kljucne_reci": {
        # Rame drži punu pripadnost do 1: jedan slab pogodak još nije dokaz.
        # Desno rame pada na nulu tek na 3, gde ``zastupljene`` dostiže punu
        # pripadnost, pa dva skupa nisu istovremeno na jedinici.
        "kljucne_zanemarljive": {
            "tip": "trapmf", "params": (0, 0, 1, 3),
            "kategorija": "LEGITIMAN", "naziv": "zanemarljive",
        },
        # Temе prebačeno sa 4 na 3: sa simetričnim [1, 4, 7] tri i pet
        # ključnih reči daju istu pripadnost 0.667, pa sistem ne može da ih
        # razlikuje.
        "kljucne_zastupljene": {
            "tip": "trimf", "params": (1, 3, 7),
            "kategorija": "SUMNJIVO", "naziv": "zastupljene",
        },
        # Evidencija je u ``podudaranje.py`` ograničena na 10 (``min(..., 10.0)``),
        # pa desno rame mora da stoji na kraju univerzuma: sa ramenom [5, 8, 8, 10]
        # bi osam i deset pogodaka dalo istu pripadnost.
        "kljucne_dominantne": {
            "tip": "trapmf", "params": (5, 8, 10, 10),
            "kategorija": "SPAM", "naziv": "dominantne",
        },
    },
    "broj_linkova": {
        # Nula linkova je puno "minimalno"; jedan link već gasi pripadnost.
        # Kalibrisano na uzorku iz ``primeri.txt``: legitimni primeri imaju 0-1
        # link, pa dva linka više ne smeju da se proglase minimalnim.
        "linkovi_minimalni": {
            "tip": "trapmf", "params": (0, 0, 0, 1),
            "kategorija": "LEGITIMAN", "naziv": "minimalni",
        },
        # Tri linka su pun "umeren" signal (trapez se drži na 1 do 3), a
        # "brojni" počinje na 3. Ranije je tri linka davalo samo 0.167, pa
        # kratak spam sa tri linka nije mogao da aktivira spam pravila.
        "linkovi_umereni": {
            "tip": "trapmf", "params": (0, 1, 3, 5),
            "kategorija": "SUMNJIVO", "naziv": "umereni",
        },
        # Broj linkova se u ``analizator.py`` seče na 10 (``min(len, 10)``), pa
        # desno rame stoji na kraju univerzuma iz istog razloga kao kod
        # ``kljucne_dominantne``: osam i deset linkova ne smeju da se stope.
        "linkovi_brojni": {
            "tip": "trapmf", "params": (3, 8, 10, 10),
            "kategorija": "SPAM", "naziv": "brojni",
        },
    },
    "caps_procenat": {
        # Legitimni uzorci imaju do ~6% velikih slova (veliko slovo na početku
        # rečenice, skraćenice), pa je 12% sigurna gornja granica "uobičajenog".
        # Iznad 12 ostaje samo ``caps_agresivan``, koji traži jasan dokaz.
        "caps_uobicajen": {
            "tip": "trapmf", "params": (0, 0, 1, 12),
            "kategorija": "LEGITIMAN", "naziv": "uobičajen",
        },
        # Prelazni skup između uobičajenog (12) i agresivnog (45). Temе 16 je
        # blizu izmerenog proseka spam primera, a levo rame na 7 se preklapa sa
        # ``caps_uobicajen`` da između 12 i 16 ne postoji mrtav pojas.
        "caps_poviseni": {
            "tip": "trimf", "params": (7, 16, 32),
            "kategorija": "SUMNJIVO", "naziv": "povišeni",
        },
        # Široki most preko opsega 22-44%. Bez njega bi skok sa 32 na 45 ostao
        # nepokriven i podizanje caps-a bi moglo da snizi ocenu (regresija 6).
        "caps_blago_povisen": {
            "tip": "trimf", "params": (10, 25, 65),
            "kategorija": "SUMNJIVO", "naziv": "blago povišen",
        },
        # Donja granica 45: legitimni primeri imaju do ~6% velikih slova,
        # spam 26-60%.
        "caps_agresivan": {
            "tip": "trapmf", "params": (45, 85, 100, 100),
            "kategorija": "SPAM", "naziv": "agresivan",
        },
    },
    "interpunkcija": {
        # Običan tekst retko prelazi 2% znakova "!" i "?"; pet procenata je
        # prva granica na kojoj se priča može nazvati naglašenom.
        "interpunkcija_retka": {
            "tip": "trapmf", "params": (0, 0, 2, 5),
            "kategorija": "LEGITIMAN", "naziv": "retka",
        },
        # Prelazni skup: temе 5 je polazna tačka merenja, a 10 spaja sa
        # ``interpunkcija_umerena`` (koja počinje na 6) bez praznog pojasa.
        "interpunkcija_blago": {
            "tip": "trimf", "params": (2, 5, 10),
            "kategorija": "SUMNJIVO", "naziv": "blaga",
        },
        # Umerena interpunkcija je prelaz ka agresivnoj. Temе 12 je blizu gornje
        # izmerene granice na uzorku (~14%), a desno rame ide do 25 da skup ne
        # padne na nulu pre nego što ``interpunkcija_agresivna`` preuzme na 14.
        "interpunkcija_umerena": {
            "tip": "trimf", "params": (6, 12, 25),
            "kategorija": "SUMNJIVO", "naziv": "umerena",
        },
        # Najveća izmerena vrednost na uzorcima je ~14%. "Agresivna" zato
        # mora da počne tek na 14; ranije je dostizala 1.0 već na 14.
        "interpunkcija_agresivna": {
            "tip": "trapmf", "params": (14, 40, 100, 100),
            "kategorija": "SPAM", "naziv": "agresivna",
        },
    },
    # Peti ulaz je izlaz neuronske mreže, ne merenje iz teksta. Mreža daje
    # verovatnoću spama 0–100 za iste četiri karakteristike. Skupovi su namerno
    # široki: samo vrlo sigurna mreža ulazi u "potvrđuje spam", pa mreža ostaje
    # potvrda, a ne glavni izvor odluke.
    "nn_pouzdanje": {
        # Ispod 30 mreza je sigurna da nije spam. Na neutralnom 50 pripadnost
        # pada na nulu, pa neutralan ulaz ne moze da aktivira nijedno n pravilo.
        "nn_iskljucuje_spam": {
            "tip": "trapmf", "params": (0, 0, 30, 50),
            "kategorija": "LEGITIMAN", "naziv": "isključuje spam",
        },
        # Temе je neutralno 50: tu mreza ne kaze nista ni u jednu stranu.
        "nn_sumnja_na_spam": {
            "tip": "trimf", "params": (30, 50, 70),
            "kategorija": "SUMNJIVO", "naziv": "sumnja na spam",
        },
        # Potvrda pocinje tek na 55, a puna je od 75. Time samo vrlo sigurna
        # mreza ulazi u "potvrdjuje spam" i ne moze da zameni dokaz iz teksta.
        "nn_potvrdjuje_spam": {
            "tip": "trapmf", "params": (55, 75, 100, 100),
            "kategorija": "SPAM", "naziv": "potvrđuje spam",
        },
    },
}


# --- Izlaz: spam skor (0-100) --------------------------------------------
# Šest stepenovanih izlaznih skupova. Trouglovi nisu idealno simetrični: kod
# savršeno simetričnog trougla težište ne zavisi od jačine aktivacije, pa bi
# svako pravilo koje se aktivira dalo isti skor bez obzira na stepen.
IZLAZNI_SKUPOVI_DEFINICIJE = {
    # Puno legitiman do 8; prelaz traje do 20, gde ``energicno`` već radi.
    "legitiman": {
        "tip": "trapmf", "params": (0, 0, 8, 20),
        "kategorija": "LEGITIMAN", "naziv": "legitiman",
    },
    # Vrh na 13: ispod 10 nije "energično", a na 22 predaje ``blago_sumnjiv``.
    "energicno": {
        "tip": "trimf", "params": (10, 13, 22),
        "kategorija": "LEGITIMAN", "naziv": "legitiman energično",
    },
    # Počinje tačno gde ``energicno`` staje (22), vrh na 30.
    "blago_sumnjiv": {
        "tip": "trimf", "params": (22, 30, 42),
        "kategorija": "SUMNJIVO", "naziv": "blago sumnjiv",
    },
    # Vrh na 44; preklapa se sa susedima da nijedna ocena ne ostane bez skupa.
    "sumnjiv": {
        "tip": "trimf", "params": (38, 44, 58),
        "kategorija": "SUMNJIVO", "naziv": "sumnjiv",
    },
    # Vrh na 60; desno rame (74) spaja se sa ``spam`` (počinje na 72).
    "visoko_sumnjiv": {
        "tip": "trimf", "params": (54, 60, 74),
        "kategorija": "SUMNJIVO", "naziv": "visoko sumnjiv",
    },
    # Počinje na 72, puno od 88; desno rame stoji na kraju univerzuma (100).
    "spam": {
        "tip": "trapmf", "params": (72, 88, 100, 100),
        "kategorija": "SPAM", "naziv": "spam",
    },
}


kljucne_zanemarljive = fuzz.trapmf(x_kljucne_reci, [0, 0, 1, 3])
kljucne_zastupljene  = fuzz.trimf (x_kljucne_reci, [1, 3, 7])
kljucne_dominantne   = fuzz.trapmf(x_kljucne_reci, [5, 8, 10, 10])

linkovi_minimalni = fuzz.trapmf(x_broj_linkova, [0, 0, 0, 1])
linkovi_umereni   = fuzz.trapmf(x_broj_linkova, [0, 1, 3, 5])
linkovi_brojni    = fuzz.trapmf(x_broj_linkova, [3, 8, 10, 10])

caps_uobicajen      = fuzz.trapmf(x_caps_procenat, [0, 0, 1, 12])
caps_poviseni       = fuzz.trimf (x_caps_procenat, [7, 16, 32])
caps_blago_povisen  = fuzz.trimf (x_caps_procenat, [10, 25, 65])
caps_agresivan      = fuzz.trapmf(x_caps_procenat, [45, 85, 100, 100])

interpunkcija_retka     = fuzz.trapmf(x_interpunkcija, [0, 0, 2, 5])
interpunkcija_blago     = fuzz.trimf (x_interpunkcija, [2, 5, 10])
interpunkcija_umerena   = fuzz.trimf (x_interpunkcija, [6, 12, 25])
interpunkcija_agresivna = fuzz.trapmf(x_interpunkcija, [14, 40, 100, 100])

nn_iskljucuje_spam = fuzz.trapmf(x_nn_pouzdanje, [0, 0, 30, 50])
nn_sumnja_na_spam  = fuzz.trimf (x_nn_pouzdanje, [30, 50, 70])
nn_potvrdjuje_spam = fuzz.trapmf(x_nn_pouzdanje, [55, 75, 100, 100])


score_legitiman           = fuzz.trapmf(x_spam_score, [0, 0, 8, 20])
score_legitiman_energicno = fuzz.trimf (x_spam_score, [10, 13, 22])
score_blago_sumnjiv       = fuzz.trimf (x_spam_score, [22, 30, 42])
score_sumnjiv             = fuzz.trimf (x_spam_score, [38, 44, 58])
score_visoko_sumnjiv      = fuzz.trimf (x_spam_score, [54, 60, 74])
score_spam                = fuzz.trapmf(x_spam_score, [72, 88, 100, 100])

izlazni_skupovi = {
    "legitiman": score_legitiman,
    "energicno": score_legitiman_energicno,
    "blago_sumnjiv": score_blago_sumnjiv,
    "sumnjiv": score_sumnjiv,
    "visoko_sumnjiv": score_visoko_sumnjiv,
    "spam": score_spam,
}

KATEGORIJA_PO_SKUPU = {
    ime: definicija["kategorija"]
    for ime, definicija in IZLAZNI_SKUPOVI_DEFINICIJE.items()
}


def stepen_pripadnosti(x_univerzum, funkcija_pripadnosti, vrednost: float) -> float:
    return float(fuzz.interp_membership(x_univerzum, funkcija_pripadnosti, vrednost))
