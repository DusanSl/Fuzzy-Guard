"""Pronalaženje spam termina u tekstu bez dvostrukog brojanja.

Stari pristup je za svaki termin pokretao poseban regularni izraz nad celim
tekstom. Dve posledice su bile važne:

1. fraza i njene pojedinačne reči su se brojale odvojeno ("free prize" je
   nosilo 3.0 umesto 2.0), pa je kratak spam lako dolazio do maksimalne
   evidencije;
2. pozicije su se računale nad normalizovanim tekstom, pa su se pomerala
   osvetljenja kod znakova čija promena veličine menja dužinu stringa.

Ovaj modul radi nad tokenima. Svaki token pamti svoju originalnu poziciju, a
normalizacija se radi po tokenu, tako da pozicije uvek odgovaraju vidljivom
tekstu. Posle pronalaženja, biraju se nepoklopljena poklapanja: najduže prvo,
pa teže. Time fraza potiskuje svoje delove umesto da se sabira sa njima.
"""

import re
from typing import Iterable, NamedTuple

# Ćirilica koja izgleda kao latinica menja se samo u tokenima koji mešaju
# pisma. Tako "frее" (sa ćiriličnim e) postaje "free", a pravi ćirilični
# tekst ostaje netaknut.
_CIRILICA_U_LATINICU = str.maketrans({
    "а": "a", "е": "e", "о": "o", "р": "p", "с": "c", "х": "x",
    "у": "y", "к": "k", "м": "m", "т": "t", "н": "h", "в": "b",
    "А": "a", "Е": "e", "О": "o", "Р": "p", "С": "c", "Х": "x",
    "У": "y", "К": "k", "М": "m", "Т": "t", "Н": "h", "В": "b",
})

# Leetspeak: "fr33", "v1agra", "c0ngratulat10ns". Primenjuje se samo na tokene
# koji sadrže bar jedno latinično slovo, da se čisti brojevi ne bi kvarili.
_LEET = str.maketrans({
    "0": "o", "1": "i", "3": "e", "4": "a", "5": "s",
    "7": "t", "8": "b", "9": "g", "@": "a", "$": "s",
})

_UZORAK_TOKENA = re.compile(r"\w+", re.UNICODE)
# Fraza ne sme da pređe granicu rečenice ("...click. Here is...").
_GRANICA_RECENICE = re.compile(r"[.!?]")


class Token(NamedTuple):
    pocetak: int
    kraj: int
    original: str
    normalizovan: str


def normalizuj_token(token: str) -> str:
    token = token.lower()
    ima_latinicu = any("a" <= znak <= "z" for znak in token)
    ima_cirilicu = any("\u0400" <= znak <= "\u04ff" for znak in token)

    if ima_latinicu and ima_cirilicu:
        token = token.translate(_CIRILICA_U_LATINICU)
    if any("a" <= znak <= "z" for znak in token):
        token = token.translate(_LEET)
    return token


def tokenizuj(tekst: str) -> list:
    return [
        Token(poklapanje.start(), poklapanje.end(), poklapanje.group(0),
              normalizuj_token(poklapanje.group(0)))
        for poklapanje in _UZORAK_TOKENA.finditer(tekst)
    ]


def _terminski_indeks(termini: Iterable) -> dict:
    """Mapira tuple normalizovanih tokena u (termin, tezina, izvor)."""
    indeks = {}
    for termin, tezina, izvor in termini:
        kljuc = tuple(normalizuj_token(deo) for deo in _UZORAK_TOKENA.findall(termin))
        if not kljuc:
            continue
        postojeci = indeks.get(kljuc)
        if postojeci is None or tezina > postojeci[1]:
            indeks[kljuc] = (termin, tezina, izvor)
    return indeks


def pronadji_poklapanja(tekst: str, termini: Iterable) -> tuple:
    """Vraća (evidencija 0-10, lista pogodaka za objašnjenje).

    ``termini`` je iterabil od (termin, tezina, izvor). Evidencija je zbir
    težina prihvaćenih, nepoklopljenih poklapanja.
    """
    tokeni = tokenizuj(tekst)
    indeks = _terminski_indeks(termini)
    if not tokeni or not indeks:
        return 0.0, []

    najveca_duzina = max(len(kljuc) for kljuc in indeks)
    kandidati = []

    for pocetak in range(len(tokeni)):
        for duzina in range(min(najveca_duzina, len(tokeni) - pocetak), 0, -1):
            kljuc = tuple(token.normalizovan for token in tokeni[pocetak:pocetak + duzina])
            pogodak = indeks.get(kljuc)
            if pogodak is None:
                continue
            if duzina > 1:
                prelazi_recenicu = any(
                    _GRANICA_RECENICE.search(tekst[tokeni[i].kraj:tokeni[i + 1].pocetak])
                    for i in range(pocetak, pocetak + duzina - 1)
                )
                if prelazi_recenicu:
                    continue
            termin, tezina, izvor = pogodak
            kandidati.append({
                "pocetak": pocetak,
                "kraj": pocetak + duzina,
                "duzina": duzina,
                "tezina": tezina,
                "termin": termin,
                "izvor": izvor,
            })
            break

    # Najduže poklapanje ima prioritet; kod iste dužine teže.
    kandidati.sort(key=lambda stavka: (-stavka["duzina"], -stavka["tezina"], stavka["pocetak"]))

    zauzeti = [False] * len(tokeni)
    prihvaceni = []
    for kandidat in kandidati:
        pocetak, kraj = kandidat["pocetak"], kandidat["kraj"]
        if any(zauzeti[pocetak:kraj]):
            continue
        for indeks_tokena in range(pocetak, kraj):
            zauzeti[indeks_tokena] = True
        prihvaceni.append(kandidat)

    evidencija = 0.0
    grupisani = {}
    for kandidat in prihvaceni:
        evidencija += kandidat["tezina"]
        kljuc = (kandidat["termin"], kandidat["izvor"])
        zapis = grupisani.setdefault(kljuc, {
            "rec": kandidat["termin"],
            "broj": 0,
            "tezina": kandidat["tezina"],
            "izvor": kandidat["izvor"],
            "pozicije": [],
        })
        zapis["broj"] += 1
        if len(zapis["pozicije"]) < 10:
            zapis["pozicije"].append([
                tokeni[kandidat["pocetak"]].pocetak,
                tokeni[kandidat["kraj"] - 1].kraj,
            ])

    pogodjene = sorted(
        grupisani.values(),
        key=lambda stavka: stavka["broj"] * stavka["tezina"],
        reverse=True,
    )
    return min(evidencija, 10.0), pogodjene
