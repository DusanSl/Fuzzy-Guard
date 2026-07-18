import re
import random
from pathlib import Path

SPAM_RECNIK_RECI = [
    "win", "winner", "won", "free", "click", "offer", "prize",
    "congratulations", "claim", "cash", "bonus", "reward",
    "urgent", "limited", "exclusive", "guarantee", "deal",
    "cheap", "discount", "income", "profit", "rich", "million", "dollar",
    "money", "selected", "opportunity",

    "pobedi", "pobednik", "pobedniku", "pobednika",
    "osvojio", "osvojili", "osvojite", "osvoji",
    "besplatno", "besplatnu", "besplatni", "besplatna", "besplatne",
    "klikni", "kliknite", "kliknete",
    "ponuda", "ponude", "ponudu",
    "nagrada", "nagradu", "nagrade", "nagradi",
    "čestitamo", "čestitamo", "čestitamo",
    "preuzmi", "preuzmite", "preuzmete", "preuzimite",
    "gotovina", "gotovinu", "gotovine",
    "hitno", "hitna", "hitni", "hitne",
    "ograničeno", "ograničena", "ograničenu", "ograničene", "ograničeni",
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
    "izabran", "izabrana", "izabrani", "izabrano", "izabrane",
    "prilika", "prilike", "priliku", "prilikama",
    "pogodba", "pogodbe", "pogodbu",
]

SPAM_RECNIK_FRAZE = [
    "buy now", "act now", "order now", "click here", "limited time",
    "limited offer", "free prize", "you won", "you have won",
    "claim now", "claim your", "get rich", "make money",

    "kupi sad", "deluj odmah", "naruči odmah", "klikni ovde",
    "ograničena ponuda", "besplatna nagrada", "osvojio si", "preuzmi nagradu",
]

PUTANJA_PRIMERI = Path(__file__).parent.parent / "primeri.txt"


def analiziraj_email(tekst: str) -> dict:
    tekst_mali = tekst.lower()

    broj_kljucnih_reci = 0
    for rec in SPAM_RECNIK_RECI:
        uzorak = r'\b' + re.escape(rec) + r'\b'
        broj_kljucnih_reci += len(re.findall(uzorak, tekst_mali))
    for fraza in SPAM_RECNIK_FRAZE:
        uzorak = re.escape(fraza)
        broj_kljucnih_reci += len(re.findall(uzorak, tekst_mali))
    broj_kljucnih_reci = min(broj_kljucnih_reci, 10)

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
    tekst_bez_linkova = re.sub(r'https?://\S+', '', tekst)
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


def ucitaj_random_primer() -> str:

    if not PUTANJA_PRIMERI.exists():
        return f"Greška: Fajl nije pronađen na lokaciji {PUTANJA_PRIMERI}"

    try:
        sadrzaj = PUTANJA_PRIMERI.read_text(encoding="utf-8")
        primeri = [p.strip() for p in sadrzaj.split("---") if p.strip()]

        if not primeri:
            return "Fajl je prazan ili nema separatora ---"

        return random.choice(primeri)
    except Exception as e:
        return f"Greška pri čitanju fajla: {str(e)}"