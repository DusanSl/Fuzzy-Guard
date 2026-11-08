import re
import random
import json
import os
import html
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

# --- normalizacija teksta -------------------------------------------------

# Cirilica koja izgleda kao latinica (homoglifi) menja se samo u tokenima koji
# mesaju pisma. Tako "frее" (sa cirilicnim e) postaje "free", a pravi cirilicni
# tekst ostaje netaknut.
_CIRILICA_U_LATINICU = str.maketrans({
    "а": "a", "е": "e", "о": "o", "р": "p", "с": "c", "х": "x",
    "у": "y", "к": "k", "м": "m", "т": "t", "н": "h", "в": "b",
    "А": "a", "Е": "e", "О": "o", "Р": "p", "С": "c", "Х": "x",
    "У": "y", "К": "k", "М": "m", "Т": "t", "Н": "h", "В": "b",
})

# Leetspeak: "fr33", "v1agra", "c0ngratulat10ns". Primenjuje se samo na tokene
# koji sadrze bar jedno latinicno slovo, da se cisti brojevi ne bi kvarili.
_LEET = str.maketrans({
    "0": "o", "1": "i", "3": "e", "4": "a", "5": "s",
    "7": "t", "8": "b", "9": "g", "@": "a", "$": "s",
})

_UZORAK_LINKA = re.compile(r"(?i)\b(?:https?://|hxxps?://|www\.)[^\s<>\"']+")
_UZORAK_HREF = re.compile(r"(?i)href\s*=\s*[\"']([^\"']+)[\"']")
_UZORAK_SKRIPT = re.compile(r"(?is)<(script|style)\b.*?</\1>")
_UZORAK_TAG = re.compile(r"(?s)<[^>]+>")


def _ocisti_html(tekst: str) -> str:
    """Dekodira entitete i uklanja HTML, ostavljajuci vidljivi tekst."""
    tekst = html.unescape(tekst)
    tekst = _UZORAK_SKRIPT.sub(" ", tekst)
    tekst = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</li>|</tr>|</h[1-6]>", " ", tekst)
    tekst = _UZORAK_TAG.sub(" ", tekst)
    return re.sub(r"\s+", " ", tekst).strip()


def _normalizuj_za_mecovanje(tekst: str) -> str:
    delovi = []
    for token in re.split(r"(\W+)", tekst.lower()):
        if not token or not any(znak.isalnum() for znak in token):
            delovi.append(token)
            continue

        ima_latinicu = any("a" <= znak <= "z" for znak in token)
        ima_cirilicu = any("\u0400" <= znak <= "\u04ff" for znak in token)

        if ima_latinicu and ima_cirilicu:
            token = token.translate(_CIRILICA_U_LATINICU)
        if any("a" <= znak <= "z" for znak in token):
            token = token.translate(_LEET)

        delovi.append(token)
    return "".join(delovi)


def _izvuci_linkove(tekst: str) -> list:
    """Vraca jedinstvene linkove iz teksta i iz href atributa."""
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


# Uzorci se kompajliraju jednom; ranije se 271 nauceni izraz ponovo kompajlirao
# pri svakom zahtevu.
_RUCNI_UZORCI = [
    (re.compile(r"\b" + re.escape(rec) + r"\b"), rec, 1.0)
    for rec in SPAM_RECNIK_RECI
] + [
    (re.compile(re.escape(fraza)), fraza, 1.0)
    for fraza in SPAM_RECNIK_FRAZE
]
_RUCNI_TERMINI = set(SPAM_RECNIK_RECI) | set(SPAM_RECNIK_FRAZE)

_NAUCENI_UZORCI = None
_NAUCENI_IZVOR = None


def _nauceni_uzorci() -> list:
    global _NAUCENI_UZORCI, _NAUCENI_IZVOR
    recnik = ucitaj_nauceni_recnik()
    if _NAUCENI_IZVOR is not recnik:
        uzorci = []
        for termin, tezina in recnik.items():
            if " " in termin:
                uzorak = re.compile(re.escape(termin))
            else:
                uzorak = re.compile(r"\b" + re.escape(termin) + r"\b")
            uzorci.append((uzorak, termin, tezina))
        _NAUCENI_UZORCI = uzorci
        _NAUCENI_IZVOR = recnik
    return _NAUCENI_UZORCI



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


def _izracunaj_kljucne_reci(tekst_za_mecovanje: str, nacin_recnik: str):
    """Vraca (evidencija 0-10, lista najjacih pogodaka za objasnjenje)."""
    evidencija = 0.0
    pogodjene = []

    if nacin_recnik in ("rucni", "kombinovano"):
        for uzorak, termin, tezina in _RUCNI_UZORCI:
            broj = len(uzorak.findall(tekst_za_mecovanje))
            if broj:
                evidencija += broj * tezina
                pogodjene.append(
                    {"rec": termin, "broj": broj, "tezina": tezina, "izvor": "rucni"}
                )

    if nacin_recnik in ("nauceni", "kombinovano"):
        for uzorak, termin, tezina in _nauceni_uzorci():
            if nacin_recnik == "kombinovano" and termin in _RUCNI_TERMINI:
                continue  # ne broji dvaput isti termin
            broj = len(uzorak.findall(tekst_za_mecovanje))
            if broj:
                evidencija += broj * tezina
                pogodjene.append(
                    {"rec": termin, "broj": broj, "tezina": tezina, "izvor": "nauceni"}
                )

    pogodjene.sort(key=lambda stavka: stavka["broj"] * stavka["tezina"], reverse=True)
    return min(evidencija, 10.0), pogodjene[:8]


def analiziraj_email(tekst: str, nacin_recnik: Optional[str] = None) -> dict:
    vidljivi_tekst = _ocisti_html(tekst)
    tekst_za_mecovanje = _normalizuj_za_mecovanje(vidljivi_tekst)

    broj_kljucnih_reci, pogodjene_reci = _izracunaj_kljucne_reci(
        tekst_za_mecovanje, (nacin_recnik or NACIN_RECNIKA)
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

    return {
        "kljucne_reci":  float(broj_kljucnih_reci),
        "broj_linkova":  float(broj_linkova),
        "caps_procenat": round(caps_procenat, 2),
        "interpunkcija": float(interpunkcija),
        "pokrivene_reci": pogodjene_reci,
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