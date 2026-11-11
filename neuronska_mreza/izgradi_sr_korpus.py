"""Gradi srpski korpus masinskim prevođenjem SpamAssassin korpusa.

Koristi nezvanični Google Translate endpoint (bez ključa), pa je skript
resumable: svaki prevedeni red se kešira u JSONL fajlu. Ako endpoint počne da
vraća 429, dovoljno je ponovo pokrenuti istu komandu.

Kada je endpoint potpuno blokiran, ``--sinteticki-spam N`` dodaje N označenih
sintetičkih spam šablona na srpskom, da pozitivna klasa ostane upotrebljiva.
To je fallback, ne zamena za pravi prevod; vidi README.

Prevod se transliteruje sa ćirilice na latinicu, jer ceo projekat koristi
latinični srpski (``čestitamo``, ``nagrada``). HTML se uklanja pre prevođenja,
a URL-ovi se štite placeholderima da ih prevodilac ne bi preveo.

Pokretanje::

    python -m neuronska_mreza.izgradi_sr_korpus
    python -m neuronska_mreza.izgradi_sr_korpus --limit 25
    python -m neuronska_mreza.izgradi_sr_korpus --workers 6 --delay 0.3
"""

import argparse
import hashlib
import html
import json
import random
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from obrada_teksta.analizator import _ocisti_html

KOREN = Path(__file__).parent.parent
PUTANJA_IZVOR = KOREN / "podaci" / "spamassassin.tsv"
PUTANJA_IZLAZ = KOREN / "podaci" / "sr_spamassassin.tsv"
PUTANJA_KEŠ = KOREN / "podaci" / "sr_prevedeno_keš.jsonl"

ENDPOINT = "https://translate.googleapis.com/translate_a/single"
MYMEMORY = "https://api.mymemory.translated.net/get"
MAKS_DUŽINA_ZAHTEVA = 4000
MYMEMORY_MAKS = 450
PONOVNI_POKUŠAJI = 8

SERVIS = "google"

# Placeholder koji prevodilac ne prevodi. Broj se menja po URL-u.
UZORAK_URL = re.compile(r"(?i)\b(?:https?://|hxxps?://|www\.)[^\s<>\"']+")


# Ćirilica -> latinica. str.translate dozvoljava više znakova u vrednosti,
# pa se "љ", "њ" i "џ" ispravno pretvaraju u "lj", "nj" i "dž".
_CIRILICA_U_LATINICU = str.maketrans({
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "ђ": "đ",
    "е": "e", "ж": "ž", "з": "z", "и": "i", "ј": "j", "к": "k",
    "л": "l", "љ": "lj", "м": "m", "н": "n", "њ": "nj", "о": "o",
    "п": "p", "р": "r", "с": "s", "т": "t", "ћ": "ć", "у": "u",
    "ф": "f", "х": "h", "ц": "c", "ч": "č", "ш": "š", "џ": "dž",
    "А": "A", "Б": "B", "В": "V", "Г": "G", "Д": "D", "Ђ": "Đ",
    "Е": "E", "Ж": "Ž", "З": "Z", "И": "I", "Ј": "J", "К": "K",
    "Л": "L", "Љ": "Lj", "М": "M", "Н": "N", "Њ": "Nj", "О": "O",
    "П": "P", "Р": "R", "С": "S", "Т": "T", "Ћ": "Ć", "У": "U",
    "Ф": "F", "Х": "H", "Ц": "C", "Ч": "Č", "Ш": "Š", "Џ": "Dž",
    "ѐ": "e", "ѝ": "i", "’": "'", "‘": "'", "“": '"', "”": '"',
})


def ucitaj_izvor(putanja: Path):
    redovi = []
    for linija in putanja.read_text(encoding="utf-8").splitlines():
        if "\t" not in linija:
            continue
        oznaka, tekst = linija.split("\t", 1)
        redovi.append((oznaka.strip(), tekst))
    return redovi


def transliteruj(tekst: str) -> str:
    return tekst.translate(_CIRILICA_U_LATINICU)


def pripremi_za_prevođenje(tekst: str):
    """Vraća (očišćen tekst sa placeholderima, mapa placeholder -> URL)."""
    vidljiv = _ocisti_html(tekst)
    linkovi = {}

    def zameni(poklapanje):
        kljuc = f"URLPLACEHOLDER{len(linkovi)}"
        linkovi[kljuc] = poklapanje.group(0)
        return kljuc

    vidljiv = UZORAK_URL.sub(zameni, vidljiv)
    return vidljiv, linkovi


def vrati_linkove(tekst: str, linkovi: dict) -> str:
    for kljuc, url in linkovi.items():
        tekst = tekst.replace(kljuc, url)
    return tekst


# --- sintetički spam -----------------------------------------------------
# Koristi se samo kao fallback kada besplatni endpoint za prevođenje odbije
# saobraćaj. Termini su srpski; rečenice su šabloni, pa je korpus označen
# "sintetički" u README-u.

_TERMINI = [
    "hipoteka", "kredit", "investicija", "osiguranje", "ponuda", "nagrada",
    "bonus", "gotovina", "zarada", "prihod", "popust", "povraćaj", "nalog",
    "obaveza", "pomoć", "isplata", "provizija", "dug", "rate", "kamata",
    "štednja", "profit", "milioni", "dinara", "dolari", "brza zarada",
    "garantovano", "odobreno", "ekskluzivno", "ograničeno", "besplatno",
    "čestitamo", "osvojili ste", "nagradu", "nagrada", "preuzmite",
    "kliknite", "kliknite ovde", "hitno", "ograničena ponuda", "verifikujte",
    "potvrdite", "ažurirajte", "pretplata", "povraćaj novca", "zaradite",
]
_POZIVI = [
    "KLIKNITE LINK", "POSETITE SAJT", "ODGOVORITE ODMAH", "PREUZMITE NAGRADU",
    "KONTAKTIRAJTE NAS", "VERIFIKUJTE NALOG", "POTVRDITE PODATKE",
]
_URL_IMENA = [
    "isplata-sada", "brzi-kredit", "siguran-nalog", "zarada-online",
    "gotovina-centar", "povracaj-novca", "investicija-plus", "osiguranje-now",
]
_UVODI = [
    "DRAGI GOSPODINE",
    "POŠTOVANI",
    "DRAGI KORISNICE",
    "VAŽNO OBAVEŠTENJE",
]


def generisi_sinteticki_spam(broj: int, semence: int = 42) -> list:
    generator = random.Random(semence)
    redovi = []
    for indeks in range(broj):
        uvod = generator.choice(_UVODI)
        termini = generator.sample(_TERMINI, k=generator.randint(5, 7))
        poziv = generator.choice(_POZIVI)
        linkovi = [
            f"http://{generator.choice(_URL_IMENA)}-{indeks}.com"
            for _ in range(generator.randint(1, 3))
        ]
        recenice = [
            f"{uvod}, VAŠA {termin.upper()} JE GARANTOVANA." for termin in termini[:2]
        ]
        recenice.append(
            f"{poziv} {' '.join(linkovi)} DA PRIMITE {termini[2].upper()} I {termini[3].upper()} ODMAH!!!"
        )
        if len(termini) > 4:
            recenice.append(
                f"VAŠA {termini[4].upper()} ISTIČE DANAS. ODGOVORITE ODMAH!!!"
            )
        redovi.append(("spam", " ".join(recenice)))
    return redovi


def podeli_na_delove(tekst: str, maksimum: int = MAKS_DUŽINA_ZAHTEVA):
    """Deli tekst na delove do ``maksimum`` znakova, po granici rečenice."""
    delovi = []
    ostatak = tekst
    while len(ostatak) > maksimum:
        presek = ostatak.rfind(". ", 0, maksimum)
        if presek < maksimum // 2:
            presek = ostatak.rfind(" ", 0, maksimum)
        if presek <= 0:
            presek = maksimum
        delovi.append(ostatak[:presek].strip())
        ostatak = ostatak[presek:].lstrip()
    if ostatak.strip():
        delovi.append(ostatak.strip())
    return delovi


def prevedi_deo(tekst: str, jezik_izvora: str = "en", jezik_cilja: str = "sr") -> str:
    if SERVIS == "mymemory":
        parametri = urllib.parse.urlencode({
            "q": tekst,
            "langpair": f"{jezik_izvora}|{jezik_cilja}",
        })
        zahtev = urllib.request.Request(
            f"{MYMEMORY}?{parametri}",
            headers={"User-Agent": "Mozilla/5.0 (FuzzyGuard corpus builder)"},
        )
    else:
        parametri = urllib.parse.urlencode({
            "client": "gtx",
            "sl": jezik_izvora,
            "tl": jezik_cilja,
            "dt": "t",
            "q": tekst,
        })
        zahtev = urllib.request.Request(
            f"{ENDPOINT}?{parametri}",
            headers={"User-Agent": "Mozilla/5.0 (FuzzyGuard corpus builder)"},
        )

    for pokušaj in range(1, PONOVNI_POKUŠAJI + 1):
        try:
            with urllib.request.urlopen(zahtev, timeout=30) as odgovor:
                podaci = json.loads(odgovor.read().decode("utf-8"))
            if SERVIS == "mymemory":
                return html.unescape(podaci["responseData"]["translatedText"]).strip()
            delovi = [deo[0] for deo in podaci[0] if deo and deo[0]]
            return "".join(delovi).strip()
        except urllib.error.HTTPError as greska:
            if greska.code in (429, 500, 502, 503, 504) and pokušaj < PONOVNI_POKUŠAJI:
                time.sleep(min(90, 2 ** pokušaj))
                continue
            raise
        except (urllib.error.URLError, TimeoutError, ValueError, KeyError):
            if pokušaj < PONOVNI_POKUŠAJI:
                time.sleep(min(30, 2 ** pokušaj))
                continue
            raise
    raise RuntimeError("prevod nije uspeo posle svih pokušaja")


def prevedi_tekst(tekst: str, pauza: float) -> str:
    maksimum = MYMEMORY_MAKS if SERVIS == "mymemory" else MAKS_DUŽINA_ZAHTEVA
    delovi = []
    for deo in podeli_na_delove(tekst, maksimum):
        delovi.append(prevedi_deo(deo))
        time.sleep(pauza)
    return " ".join(delovi)


def ucitaj_keš(putanja: Path) -> dict:
    keš = {}
    if not putanja.exists():
        return keš
    for linija in putanja.read_text(encoding="utf-8").splitlines():
        if not linija.strip():
            continue
        try:
            zapis = json.loads(linija)
        except ValueError:
            continue
        keš[zapis["hash"]] = zapis["sr"]
    return keš


def main():
    parser = argparse.ArgumentParser(description="Prevedi SpamAssassin korpus na srpski.")
    parser.add_argument("--izvor", type=Path, default=PUTANJA_IZVOR)
    parser.add_argument("--izlaz", type=Path, default=PUTANJA_IZLAZ)
    parser.add_argument("--keš", type=Path, default=PUTANJA_KEŠ)
    parser.add_argument("--limit", type=int, default=0, help="prevedi samo prvih N redova")
    parser.add_argument("--delay", type=float, default=0.3, help="pauza između zahteva")
    parser.add_argument("--workers", type=int, default=6, help="paralelnih prevodilaca")
    parser.add_argument(
        "--servis", choices=("google", "mymemory"), default="google",
        help="google = nezvanični endpoint; mymemory = rezervni servis",
    )
    parser.add_argument(
        "--sinteticki-spam", type=int, default=0,
        help="dodaj N sintetičkih spam redova (fallback kada je prevod blokiran)",
    )
    parser.add_argument(
        "--samo-kes", action="store_true",
        help="ne prevodi nove redove, koristi samo ono što je već u kešu",
    )
    argumenti = parser.parse_args()

    global SERVIS
    SERVIS = argumenti.servis

    redovi = ucitaj_izvor(argumenti.izvor)
    if argumenti.limit:
        redovi = redovi[: argumenti.limit]

    keš = ucitaj_keš(argumenti.keš)

    # Pripremi sve redove; keširane ne prevodimo ponovo.
    poslovi = []
    prevedeni = [None] * len(redovi)
    for indeks, (oznaka, tekst) in enumerate(redovi):
        vidljiv, linkovi = pripremi_za_prevođenje(tekst)
        if not vidljiv.strip():
            continue
        kljuc = hashlib.sha1(vidljiv.encode("utf-8")).hexdigest()
        if kljuc in keš:
            prevedeni[indeks] = (oznaka, keš[kljuc])
        else:
            poslovi.append((indeks, oznaka, vidljiv, linkovi, kljuc))

    # Prvo svi spamovi, pa hamovi. Ako endpoint ponovo počne da vraća 429,
    # korpus će i tada imati zastupljene obe klase.
    poslovi.sort(key=lambda posao: (0 if posao[1] == "spam" else 1, posao[0]))
    if argumenti.samo_kes:
        poslovi = []

    print(
        f"Redova: {len(redovi)} | u kešu: {len(keš)} | za prevođenje: {len(poslovi)}",
        file=sys.stderr,
    )

    novih = 0
    if poslovi:
        with argumenti.keš.open("a", encoding="utf-8") as dnevnik, \
                ThreadPoolExecutor(max_workers=argumenti.workers) as izvršilac:
            budućnosti = {
                izvršilac.submit(prevedi_tekst, vidljiv, argumenti.delay): (
                    indeks, oznaka, linkovi, kljuc
                )
                for indeks, oznaka, vidljiv, linkovi, kljuc in poslovi
            }
            for budućnost in as_completed(budućnosti):
                indeks, oznaka, linkovi, kljuc = budućnosti[budućnost]
                try:
                    srpski = transliteruj(budućnost.result())
                except Exception as greska:  # prevod jednog reda ne ruši ceo korpus
                    print(f"  [preskočeno] red {indeks}: {greska}", file=sys.stderr)
                    continue
                srpski = vrati_linkove(srpski, linkovi)
                keš[kljuc] = srpski
                prevedeni[indeks] = (oznaka, srpski)
                dnevnik.write(json.dumps({"hash": kljuc, "sr": srpski}, ensure_ascii=False) + "\n")
                dnevnik.flush()
                novih += 1
                if novih % 25 == 0:
                    print(f"  prevedeno novih: {novih}/{len(poslovi)}", file=sys.stderr)

    argumenti.izlaz.parent.mkdir(parents=True, exist_ok=True)
    if argumenti.sinteticki_spam:
        prevedeni.extend(generisi_sinteticki_spam(argumenti.sinteticki_spam))
        print(
            f"Dodato sintetičkih spam primera: {argumenti.sinteticki_spam}",
            file=sys.stderr,
        )

    with argumenti.izlaz.open("w", encoding="utf-8", newline="\n") as izlaz:
        for zapis in prevedeni:
            if not zapis:
                continue
            oznaka, srpski = zapis
            izlaz.write(f"{oznaka}\t{' '.join(srpski.split())}\n")

    ukupno = sum(1 for zapis in prevedeni if zapis)
    spam = sum(1 for zapis in prevedeni if zapis and zapis[0] == "spam")
    print(f"Sačuvano: {argumenti.izlaz} ({ukupno} redova, {spam} spama)", file=sys.stderr)


if __name__ == "__main__":
    main()
