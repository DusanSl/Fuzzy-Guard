"""Ručni rečnik — samo za evaluaciju, ne za rad aplikacije.

Ovaj modul čuva staru ručnu listu termina kako bi se tabela "pre / posle
neuronske mreže" mogla ponovo da izračuna. Aplikacija ga ne uvozi; runtime
koristi isključivo naučene rečnike iz ``podaci/recnik_naucen_en.json`` i
``podaci/recnik_naucen_sr.json``.
"""

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


def termini():
    """Vraća listu (termin, tezina, izvor) za evaluacioni baseline."""
    return [(rec, 1.0, "rucni") for rec in SPAM_RECNIK_RECI + SPAM_RECNIK_FRAZE]
