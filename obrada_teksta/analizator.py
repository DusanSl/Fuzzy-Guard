import html
import json
import os
import re
from pathlib import Path
from typing import Optional

from obrada_teksta.podudaranje import pronadji_poklapanja

PUTANJA_PRIMERI = Path(__file__).parent.parent / "primeri.txt"
PUTANJA_RECNICI = Path(__file__).parent.parent / "podaci"

# Naučeni rečnici po jeziku. Runtime koristi njih; ručni rečnik postoji samo
# u neuronska_mreza/legacy_recnik.py za evaluacioni baseline.
RECNICI_PO_JEZIKU = {
    "en": PUTANJA_RECNICI / "recnik_naucen_en.json",
    "sr": PUTANJA_RECNICI / "recnik_naucen_sr.json",
}

# en         - samo engleski naučeni rečnik
# sr         - samo srpski naučeni rečnik
# kombinovano - oba (podrazumevano)
VALIDNI_RECNICI = ("en", "sr", "kombinovano")
NACIN_RECNIKA = os.environ.get("FUZZY_GUARD_RECNIK", "kombinovano").strip().lower()

_RECNICI_KEŠ = {}

# --- normalizacija teksta -------------------------------------------------

_UZORAK_LINKA = re.compile(r"(?i)\b(?:https?://|hxxps?://|www\.)[^\s<>\"']+")
_UZORAK_HREF = re.compile(r"(?i)href\s*=\s*[\"']([^\"']+)[\"']")
_UZORAK_SKRIPT = re.compile(r"(?is)<(script|style)\b.*?</\1>")
_UZORAK_TAG = re.compile(r"(?s)<[^>]+>")
_UZORAK_CAPS = re.compile(r"\b[A-Z\u010c\u0106\u0160\u017d\u0110]{3,}\b")
_UZORAK_INTERPUNKCIJA = re.compile(r"[!?]+")


def _ocisti_html(tekst: str) -> str:
    """Dekodira entitete i uklanja HTML, ostavljajući vidljivi tekst."""
    tekst = html.unescape(tekst)
    tekst = _UZORAK_SKRIPT.sub(" ", tekst)
    tekst = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</li>|</tr>|</h[1-6]>", " ", tekst)
    tekst = _UZORAK_TAG.sub(" ", tekst)
    return re.sub(r"\s+", " ", tekst).strip()


def _izvuci_linkove(tekst: str) -> list:
    """Vraća jedinstvene linkove iz teksta i iz href atributa."""
    kandidati = _UZORAK_HREF.findall(tekst) + _UZORAK_LINKA.findall(tekst)
    ocisceni = []
    for link in kandidati:
        link = html.unescape(link).strip().rstrip(".,;:!?)]}>\"'")
        if not link:
            continue
        link = re.sub(r"(?i)^hxxp", "http", link)
        if link.lower().startswith("www."):
            link = "http://" + link
        ocisceni.append(link.lower())
    return list(dict.fromkeys(ocisceni))


# --- naučeni rečnici ------------------------------------------------------

def ucitaj_nauceni_recnik(jezik: str = "en") -> dict:
    """Učitava naučeni rečnik za jezik. Vraća {} ako ga nema.

    Keš se osvežava kada se fajl promeni (mtime), pa retreniranje rečnika ne
    zahteva restart servera.
    """
    putanja = RECNICI_PO_JEZIKU.get(jezik)
    if putanja is None:
        return {}

    try:
        vreme = putanja.stat().st_mtime
    except OSError:
        _RECNICI_KEŠ.pop(jezik, None)
        return {}

    keširan = _RECNICI_KEŠ.get(jezik)
    if keširan and keširan[0] == vreme:
        return keširan[1]

    try:
        podaci = json.loads(putanja.read_text(encoding="utf-8"))
        recnik = {
            termin: float(tezina)
            for termin, tezina in podaci.get("tezine", {}).items()
        }
    except (OSError, ValueError, AttributeError):
        recnik = {}

    _RECNICI_KEŠ[jezik] = (vreme, recnik)
    return recnik


def _termini_za_nacin(nacin_recnik: str, legacy_recnik=None) -> list:
    """Vraća listu (termin, tezina, izvor) za izabrani rečnik."""
    if nacin_recnik == "legacy":
        if legacy_recnik is None:
            from neuronska_mreza.legacy_recnik import termini as legacy_termini
            legacy_recnik = dict(
                (termin, tezina) for termin, tezina, _ in legacy_termini()
            )
        return [(termin, tezina, "rucni") for termin, tezina in legacy_recnik.items()]

    jezici = ("en", "sr") if nacin_recnik == "kombinovano" else (nacin_recnik,)
    termini = []
    for jezik in jezici:
        for termin, tezina in ucitaj_nauceni_recnik(jezik).items():
            termini.append((termin, tezina, jezik))
    return termini


def _izracunaj_kljucne_reci(tekst: str, nacin_recnik: str, legacy_recnik=None):
    """Vraća (evidencija 0-10, lista najjačih pogodaka za objašnjenje)."""
    return pronadji_poklapanja(
        tekst, _termini_za_nacin(nacin_recnik, legacy_recnik)
    )


# --- analiza --------------------------------------------------------------

def analiziraj_email(
    tekst: str,
    nacin_recnik: Optional[str] = None,
    legacy_recnik=None,
) -> dict:
    vidljivi_tekst = _ocisti_html(tekst)

    broj_kljucnih_reci, pogodjene_reci = _izracunaj_kljucne_reci(
        vidljivi_tekst,
        (nacin_recnik or NACIN_RECNIKA),
        legacy_recnik=legacy_recnik,
    )

    pronadjeni_linkovi = _izvuci_linkove(tekst)
    broj_linkova = min(len(pronadjeni_linkovi), 10)

    tekst_bez_linkova = _UZORAK_LINKA.sub(" ", vidljivi_tekst)

    sva_slova = [karakter for karakter in tekst_bez_linkova if karakter.isalpha()]
    if sva_slova:
        velika_slova = sum(1 for karakter in sva_slova if karakter.isupper())
        caps_procenat = (velika_slova / len(sva_slova)) * 100
    else:
        caps_procenat = 0.0

    broj_uzvika = tekst_bez_linkova.count('!')
    broj_upitnika = tekst_bez_linkova.count('?')
    ukupno_karaktera = len(tekst_bez_linkova.replace(' ', ''))
    if ukupno_karaktera > 0:
        interpunkcija = round(((broj_uzvika + broj_upitnika) / ukupno_karaktera) * 100, 2)
    else:
        interpunkcija = 0.0

    oznake = [
        {
            "tip": "link",
            "pozicije": [
                list(poklapanje.span())
                for poklapanje in _UZORAK_LINKA.finditer(vidljivi_tekst)
            ][:50],
        },
        {
            "tip": "caps",
            "pozicije": [
                list(poklapanje.span())
                for poklapanje in _UZORAK_CAPS.finditer(vidljivi_tekst)
            ][:50],
        },
        {
            "tip": "interpunkcija",
            "pozicije": [
                list(poklapanje.span())
                for poklapanje in _UZORAK_INTERPUNKCIJA.finditer(vidljivi_tekst)
            ][:50],
        },
    ]

    return {
        "kljucne_reci":  float(broj_kljucnih_reci),
        "broj_linkova":  float(broj_linkova),
        "caps_procenat": round(caps_procenat, 2),
        "interpunkcija": float(interpunkcija),
        "pokrivene_reci": pogodjene_reci,
        "oznake": oznake,
        "vidljivi_tekst": vidljivi_tekst,
    }


def _izdvoji_metapodatke(linije: list) -> tuple:
    posaljilac = tema = kategorija = ""
    ostatak = []

    for linija in linije:
        if not ostatak:
            if linija.startswith("From:"):
                posaljilac = linija[5:].strip()
                continue
            if linija.startswith("Subject:"):
                tema = linija[8:].strip()
                continue
            if linija.startswith("Category:"):
                kategorija = linija[9:].strip()
                continue
        ostatak.append(linija)

    return posaljilac, tema, kategorija, "\n".join(ostatak).strip()


def _ucitaj_primere(jezik: str = "en") -> list:
    if not PUTANJA_PRIMERI.exists():
        return []

    try:
        sadrzaj = PUTANJA_PRIMERI.read_text(encoding="utf-8")
        blokovi = [b.strip() for b in sadrzaj.split("---") if b.strip()]

        primeri_en = []
        primeri_sr = []

        for blok in blokovi:
            linije = blok.split("\n")
            if len(linije) < 2:
                continue
            tag = linije[0].strip().lower()

            posaljilac, tema, kategorija, tekst = _izdvoji_metapodatke(linije[1:])
            if not tekst:
                continue

            zapis = {
                "posaljilac": posaljilac,
                "tema": tema,
                "kategorija": kategorija,
                "tekst": tekst,
            }

            if tag.startswith("[en]"):
                primeri_en.append(zapis)
            elif tag.startswith("[sr]"):
                primeri_sr.append(zapis)

        return primeri_sr if jezik == "sr" else primeri_en
    except Exception:
        return []


def ucitaj_sve_primere(jezik: str = "en") -> list:
    return _ucitaj_primere(jezik)
