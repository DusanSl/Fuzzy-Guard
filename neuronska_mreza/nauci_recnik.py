"""Ucenje spam recnika iz oznacenih podataka.

Neuronska mreza (jedan neuron / linearni klasifikator) se trenira na TF-IDF
predstavkama teksta, a njeni koeficijenti se izvoze kao tezine reci i fraza.
Dobijeni recnik se posle koristi pri izracunavanju ulaza ``kljucne_reci``.

Recnici se cuvaju odvojeno po jeziku (``recnik_naucen_en.json`` i
``recnik_naucen_sr.json``); spajanje se radi u ``obrada_teksta/analizator.py``.

Pokretanje:

    python -m neuronska_mreza.nauci_recnik --jezik en
    python -m neuronska_mreza.nauci_recnik --jezik sr
    python -m neuronska_mreza.nauci_recnik --jezik en --top 40
"""

import argparse
import json
import re
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, f1_score
from sklearn.model_selection import train_test_split

KOREN = Path(__file__).parent.parent
PUTANJA_PODACI = KOREN / "podaci" / "spamassassin.tsv"
PUTANJA_SR_PODACI = KOREN / "podaci" / "sr_spamassassin.tsv"
RECNICI_PO_JEZIKU = {
    "en": KOREN / "podaci" / "recnik_naucen_en.json",
    "sr": KOREN / "podaci" / "recnik_naucen_sr.json",
}

# Težine se skaliraju u ovaj opseg da budu uporedive sa starim ručnim
# rečnikom, gde je svaka pogođena reč nosila težinu 1.0.
TEZINA_MIN = 0.5
TEZINA_MAX = 2.0
BROJ_TERMINA = 400
# Termin mora biti bar 2x češći u spamu nego u hamu. Prag je izabran na
# validacionom delu trening skupa (75/25 unutar treninga), ne na testu.
MIN_ODNOS = 2.0
MIN_SPAM_DOKUMENATA = 10

DOZVOLJEN_TERMIN = re.compile(r"^[A-Za-zČĆŠŽĐčćšžđ][A-Za-zČĆŠŽĐčćšžđ' -]*$")

# Opšte poslovne reči koje u SpamAssassin korpusu nekad prođu 2x filter, ali
# same po sebi nisu spam signal. Bez ovoga "Thanks for your reply, I will
# visit the office" dobija dva pogotka i ulazi u SUMNJIVO.
GENERICNE_RECI = {
    "visit", "reply", "contact", "receive", "center", "information",
    "business", "service", "message", "please", "thanks", "regards",
}

# HTML/MIME i strukturni artefakti korpusa. Bez ovoga bi mreza naucila da su
# "font", "href" i "align" spam reci, sto je posledica toga kako je korpus
# sacuvan, a ne spam signal.
ARTEFAKTI = {
    "font", "fonts", "font-family", "href", "align", "width", "height",
    "color", "bgcolor", "border", "body", "html", "head", "div", "span",
    "style", "class", "size", "arial", "helvetica", "verdana", "times",
    "roman", "rgb", "px", "pt", "mime", "content", "transfer", "encoding",
    "br", "td", "tr", "table", "img", "src", "alt", "mailto", "http",
    "https", "www", "com", "org", "net", "bnq", "btamail", "adclick",
    "charset", "iso", "utf", "boundary", "multipart", "quoted", "printable",
    "nbsp", "amp", "quot", "apos", "bold", "italic", "underline", "valign",
    "colspan", "rowspan", "padding", "margin", "cellpadding", "cellspacing",
    "btnsubmit", "bordercolor", "bordercolordark", "bordercolorlight",
}



def ucitaj_podatke(putanja: Path):
    tekstovi, oznake = [], []
    for linija in putanja.read_text(encoding="utf-8").splitlines():
        if "\t" not in linija:
            continue
        oznaka, tekst = linija.split("\t", 1)
        oznake.append(1 if oznaka.strip() == "spam" else 0)
        tekstovi.append(tekst)
    return tekstovi, np.array(oznake)


def je_koristan_termin(termin: str) -> bool:
    if len(termin) < 3 or len(termin) > 20:
        return False
    delovi = termin.split()
    if any(deo in ARTEFAKTI for deo in delovi):
        return False
    if not DOZVOLJEN_TERMIN.match(termin):
        return False
    if any(deo in termin for deo in ("http", "www", "txt")):
        return False
    # "cccccc", "aaaa" i slicni ostaci HTML stilova nisu reci
    if len(set(termin.replace(" ", ""))) == 1:
        return False
    if re.search(r"(.)\1{3,}", termin):
        return False
    return True


def skaliraj_tezine(koeficijenti: np.ndarray) -> np.ndarray:
    najmanji = float(np.min(koeficijenti))
    najveci = float(np.max(koeficijenti))
    if najveci == najmanji:
        return np.full_like(koeficijenti, (TEZINA_MIN + TEZINA_MAX) / 2)
    return TEZINA_MIN + (koeficijenti - najmanji) * (TEZINA_MAX - TEZINA_MIN) / (najveci - najmanji)


def nauci(korpus: Path, broj_termina: int, top: int, jezik: str = "en") -> dict:
    tekstovi, oznake = ucitaj_podatke(korpus)
    X_train, X_test, y_train, y_test = train_test_split(
        tekstovi, oznake, test_size=0.25, random_state=42, stratify=oznake
    )

    vektorizator = TfidfVectorizer(
        ngram_range=(1, 2),
        min_df=3,
        max_features=20_000,
        sublinear_tf=True,
        strip_accents="unicode" if jezik == "en" else None,
        lowercase=True,
        stop_words="english" if jezik == "en" else None,
    )
    X_train_tfidf = vektorizator.fit_transform(X_train)
    X_test_tfidf = vektorizator.transform(X_test)
    imena = np.array(vektorizator.get_feature_names_out())

    # Koliko dokumenata sadrzi termin u spam i u ham skupu. Termin koji je
    # podjednako cest u oba nije spam signal, bez obzira na koeficijent.
    prisutan = (X_train_tfidf > 0)
    df_spam = np.asarray(prisutan[y_train == 1].sum(axis=0)).ravel()
    df_ham = np.asarray(prisutan[y_train == 0].sum(axis=0)).ravel()

    # Jedan neuron sa logistickom aktivacijom = najmanja moguca neuronska mreza.
    mreza = LogisticRegression(max_iter=1000, class_weight="balanced", solver="liblinear")
    mreza.fit(X_train_tfidf, y_train)

    predikcija = mreza.predict(X_test_tfidf)
    print("Klasifikator recnika na test skupu:")
    print(classification_report(y_test, predikcija, target_names=["ham", "spam"], digits=3))
    print(f"F1 (spam): {f1_score(y_test, predikcija):.3f}")

    koeficijenti = mreza.coef_[0]

    pozitivni = []
    for i, (ime, koef) in enumerate(zip(imena, koeficijenti)):
        if koef <= 0 or not je_koristan_termin(ime):
            continue
        if ime in GENERICNE_RECI:
            continue
        # termin mora biti bar 2x cesci u spamu i pojaviti se u bar 10 spamova
        if df_spam[i] < MIN_SPAM_DOKUMENATA or (df_spam[i] + 1) / (df_ham[i] + 1) < MIN_ODNOS:
            continue
        pozitivni.append((ime, koef))

    pozitivni.sort(key=lambda par: par[1], reverse=True)
    pozitivni = pozitivni[:broj_termina]

    if not pozitivni:
        raise SystemExit("Nije pronadjen nijedan pozitivan termin; proveri korpus.")

    termini = [ime for ime, _ in pozitivni]
    tezine = skaliraj_tezine(np.array([koef for _, koef in pozitivni]))

    recnik = {
        "verzija": 2,
        "jezik": jezik,
        "izvor": korpus.name,
        "broj_termina": len(termini),
        "tezine": {termin: round(float(tezina), 4) for termin, tezina in zip(termini, tezine)},
    }

    print(f"\nNauceno termina: {len(termini)}")
    print(f"Top {top} naucenih spam termina:")
    for termin, tezina in list(recnik["tezine"].items())[:top]:
        print(f"  {tezina:4.2f}  {termin}")

    if jezik == "en":
        from neuronska_mreza.legacy_recnik import SPAM_RECNIK_FRAZE, SPAM_RECNIK_RECI

        rucni = set(SPAM_RECNIK_RECI) | set(SPAM_RECNIK_FRAZE)
        nauceni_jednorecni = {t for t in termini if " " not in t}
        presek = sorted(nauceni_jednorecni & rucni)
        print(f"\nPreklapanje sa starim rucnim recnikom: {len(presek)} / {len(nauceni_jednorecni)}")
        print("  zajednicki:", ", ".join(presek[:20]) if presek else "(nema)")
        novi = sorted(nauceni_jednorecni - rucni)
        print("  novi kod mreze:", ", ".join(novi[:20]) if novi else "(nema)")

    return recnik


def main():
    parser = argparse.ArgumentParser(description="Uci spam recnik iz oznacenih podataka.")
    parser.add_argument("--korpus", type=Path)
    parser.add_argument("--jezik", choices=("en", "sr"), default="en")
    parser.add_argument("--broj-termina", type=int, default=BROJ_TERMINA)
    parser.add_argument("--top", type=int, default=30)
    argumenti = parser.parse_args()

    korpus = argumenti.korpus
    if korpus is None:
        korpus = PUTANJA_PODACI if argumenti.jezik == "en" else PUTANJA_SR_PODACI

    izlaz = RECNICI_PO_JEZIKU[argumenti.jezik]
    recnik = nauci(korpus, argumenti.broj_termina, argumenti.top, argumenti.jezik)
    izlaz.write_text(
        json.dumps(recnik, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\nSacuvano u {izlaz}")


if __name__ == "__main__":
    main()
