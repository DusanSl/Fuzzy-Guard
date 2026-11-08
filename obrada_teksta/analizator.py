import re
import random
import json
import os
from pathlib import Path
from typing import Optional

SPAM_RECNIK_RECI = [
    # Engleski
    "win", "winner", "won", "free", "click", "offer", "prize",
    "congratulations", "claim", "cash", "bonus", "reward", "rewards",
    "urgent", "limited", "exclusive", "guarantee", "guaranteed", "deal",
    "cheap", "discount", "income", "profit", "rich", "million", "dollar",
    "dollars", "money", "selected", "opportunity",
    "account", "verify", "unusual", "eligible", "refund", "confirm",
    "update", "settings", "subscription", "expire", "expires", "renew",
    "approved", "loan", "jackpot", "unlimited", "access",

    # Srpski
    "pobedi", "pobednik", "pobedniku", "pobednika",
    "osvojio", "osvojili", "osvojite", "osvoji",
    "besplatno", "besplatnu", "besplatni", "besplatna", "besplatne", "besplatan",
    "klikni", "kliknite", "kliknete",
    "ponuda", "ponude", "ponudu",
    "nagrada", "nagradu", "nagrade", "nagradi",
    "čestitamo", "čestitam",
    "preuzmi", "preuzmite", "preuzmete", "preuzimite",
    "gotovina", "gotovinu", "gotovine",
    "hitno", "hitna", "hitni", "hitne",
    "ograničeno", "ograničena", "ograničenu", "ograničene", "ograničeni",
    "neograničeno", "neograničena", "neograničenu", "neograničene", "neograničeni",
    "ekskluzivno", "ekskluzivna", "ekskluzivnu", "ekskluzivne", "ekskluzivni",
    "garantovano", "garantovana", "garantujemo", "garantovanu",
    "jeftino", "jeftina", "jeftine", "jeftini", "jeftinu",
    "popust", "popusta", "popustu", "popustom",
    "novac", "novca", "novcem", "novcu",
    "prihod", "prihoda", "prihode", "prihodom",
    "zarada", "zaradu", "zarade", "zaradite", "zaraditi",
    "bogat", "bogata", "bogati", "bogatstvo",
    "milion", "miliona", "milione", "milionima",
    "dolar", "dolara", "dolare", "dolarima",
    "dinar", "dinara", "dinare", "dinarima",
    "izabran", "izabrana", "izabrani", "izabrano", "izabrane",
    "prilika", "prilike", "priliku", "prilikama",
    "pogodba", "pogodbe", "pogodbu",
    "nalog", "naloga", "nalogu",
    "verifikuj", "verifikujte", "verifikuje",
    "aktivnost", "aktivnosti",
    "potvrdite", "potvrdi", "potvrdite",
    "povraćaj", "povraćaja",
    "ažuriranje", "ažurirajte", "ažurirate",
    "podešavanja", "podešavanje",
    "pretplata", "pretplatu", "pretplate",
    "ističe", "ističu",
    "obnovite", "obnovi", "obnova",
    "pristup", "pristupa",
    "kredit", "kredita",
    "odobren", "odobrena", "odobreno",
    "keš",
    "naplatite", "naplati",
    "dobitnik", "dobitnica", "dobitnika",
    "džekpot", "džekpota",
]

SPAM_RECNIK_FRAZE = [
    "buy now", "act now", "order now", "click here", "limited time",
    "limited offer", "free prize", "you won", "you have won",
    "claim now", "claim your", "get rich", "make money",
    "gift card", "get paid", "lose access",

    "kupi sad", "deluj odmah", "naruči odmah", "klikni ovde",
    "ograničena ponuda", "besplatna nagrada", "osvojio si", "preuzmi nagradu",
    "reaguj odmah",
]

PUTANJA_PRIMERI = Path(__file__).parent.parent / "primeri.txt"
PUTANJA_RECNIK = Path(__file__).parent.parent / "podaci" / "recnik_naucen.json"

# rucni     - samo lista odrzavana rukom (ponasanje pre uvodjenja mreze)
# nauceni   - samo recnik koji je naucila neuronska mreza
# kombinovano - rucni + nauceni (podrazumevano)
NACIN_RECNIKA = os.environ.get("FUZZY_GUARD_RECNIK", "kombinovano").strip().lower()

_NAUCENI_RECNIK = None


def ucitaj_nauceni_recnik() -> dict:
    """Ucitava recnik koji je izvozila neuronska mreza. Vraca {} ako ga nema."""
    global _NAUCENI_RECNIK
    if _NAUCENI_RECNIK is not None:
        return _NAUCENI_RECNIK
    try:
        podaci = json.loads(PUTANJA_RECNIK.read_text(encoding="utf-8"))
        _NAUCENI_RECNIK = {
            termin: float(tezina) for termin, tezina in podaci.get("tezine", {}).items()
        }
    except (OSError, ValueError):
        _NAUCENI_RECNIK = {}
    return _NAUCENI_RECNIK


def _izracunaj_kljucne_reci(tekst_mali: str, nacin_recnik: str) -> float:
    evidencija = 0.0

    if nacin_recnik in ("rucni", "kombinovano"):
        for rec in SPAM_RECNIK_RECI:
            uzorak = r"\b" + re.escape(rec) + r"\b"
            evidencija += len(re.findall(uzorak, tekst_mali))
        for fraza in SPAM_RECNIK_FRAZE:
            evidencija += len(re.findall(re.escape(fraza), tekst_mali))

    if nacin_recnik in ("nauceni", "kombinovano"):
        rucni_termini = set(SPAM_RECNIK_RECI) | set(SPAM_RECNIK_FRAZE)
        for termin, tezina in ucitaj_nauceni_recnik().items():
            if nacin_recnik == "kombinovano" and termin in rucni_termini:
                continue  # ne broji dvaput isti termin
            if " " in termin:
                broj = len(re.findall(re.escape(termin), tekst_mali))
            else:
                broj = len(re.findall(r"\b" + re.escape(termin) + r"\b", tekst_mali))
            evidencija += broj * tezina

    return min(evidencija, 10.0)



def analiziraj_email(tekst: str, nacin_recnik: Optional[str] = None) -> dict:
    tekst_bez_linkova = re.sub(r'https?://\S+', '', tekst)
    tekst_mali = tekst_bez_linkova.lower()

    broj_kljucnih_reci = _izracunaj_kljucne_reci(
        tekst_mali, (nacin_recnik or NACIN_RECNIKA)
    )

    pronadjeni_linkovi = re.findall(r'https?://\S+', tekst)
    broj_linkova = min(len(pronadjeni_linkovi), 10)

    sva_slova = [karakter for karakter in tekst if karakter.isalpha()]
    if sva_slova:
        velika_slova = sum(1 for karakter in sva_slova if karakter.isupper())
        caps_procenat = (velika_slova / len(sva_slova)) * 100
    else:
        caps_procenat = 0.0

    broj_uzvika = tekst.count('!')
    broj_upitnika = tekst.count('?')
    ukupno_karaktera = len(tekst_bez_linkova.replace(' ', ''))
    if ukupno_karaktera > 0:
        interpunkcija = round(((broj_uzvika + broj_upitnika) / ukupno_karaktera) * 100, 2)
    else:
        interpunkcija = 0.0

    return {
        "kljucne_reci":  float(broj_kljucnih_reci),
        "broj_linkova":  float(broj_linkova),
        "caps_procenat": round(caps_procenat, 2),
        "interpunkcija": float(interpunkcija),
    }


def ucitaj_sve_primere(jezik: str = "en") -> list:
    if not PUTANJA_PRIMERI.exists():
        return []

    try:
        sadrzaj = PUTANJA_PRIMERI.read_text(encoding="utf-8")
        blokovi = [b.strip() for b in sadrzaj.split("---") if b.strip()]

        primeri_en = []
        primeri_sr = []

        for blok in blokovi:
            linije = blok.split("\n", 1)
            if len(linije) < 2:
                continue
            tag = linije[0].strip().lower()
            tekst = linije[1].strip()

            if tag == "[en]":
                primeri_en.append(tekst)
            elif tag == "[sr]":
                primeri_sr.append(tekst)

        return primeri_sr if jezik == "sr" else primeri_en
    except Exception:
        return []