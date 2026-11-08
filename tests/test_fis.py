"""Regresioni testovi za fazi sistem.

Pokretanje iz korena projekta:

    python -m pytest
"""

from pathlib import Path

import skfuzzy as fuzz

from obrada_teksta.analizator import analiziraj_email
from fazi.pravila import fuzzifikuj, sastavi_pravila
from fazi.zakljucivanje import pokreni_fis
from fazi.skupovi import x_spam_score, izlazni_skupovi, KATEGORIJA_PO_SKUPU

PUTANJA_PRIMERI = Path(__file__).parent.parent / "primeri.txt"


def ucitaj_primere() -> list:
    sadrzaj = PUTANJA_PRIMERI.read_text(encoding="utf-8")
    blokovi = [blok.strip() for blok in sadrzaj.split("---") if blok.strip()]
    return [blok.split("\n", 1)[1] for blok in blokovi]


def analiziraj_tekst(tekst: str) -> dict:
    ulazi = analiziraj_email(tekst)
    return pokreni_fis(
        ulazi["kljucne_reci"],
        ulazi["broj_linkova"],
        ulazi["caps_procenat"],
        ulazi["interpunkcija"],
    )


def izracunaj_kategoriju(spam_score: float) -> str:
    clanstva = {
        ime: float(fuzz.interp_membership(x_spam_score, skup, spam_score))
        for ime, skup in izlazni_skupovi.items()
    }
    return KATEGORIJA_PO_SKUPU[max(clanstva, key=clanstva.get)]


def test_pokrivenost_celog_univerzuma():
    """Nijedna kombinacija ulaza ne sme da ostavi nijedno pravilo neaktivno."""
    for kljucne_reci in range(0, 11):
        for broj_linkova in range(0, 11):
            for caps_procenat in range(0, 101, 10):
                for interpunkcija in range(0, 101, 10):
                    mu = fuzzifikuj(kljucne_reci, broj_linkova, caps_procenat, interpunkcija)
                    jacine = [jacina for _, jacina, _, _ in sastavi_pravila(mu)]
                    assert max(jacine) > 0.0, (
                        "nijedno pravilo nije aktivno za",
                        kljucne_reci, broj_linkova, caps_procenat, interpunkcija,
                    )


def test_kategorija_je_saglasna_sa_skorom():
    for tekst in ucitaj_primere():
        rezultat = analiziraj_tekst(tekst)
        assert rezultat["kategorija"] == izracunaj_kategoriju(rezultat["spam_score"])


def test_skor_ostaje_u_opsegu():
    for tekst in ucitaj_primere():
        rezultat = analiziraj_tekst(tekst)
        assert 0.0 <= rezultat["spam_score"] <= 100.0


def test_rupa_izmedju_35_i_45_procenata_velikih_slova():
    """Nekad je skok sa 30% na 40% velikih slova obarao skor sa ~87 na 47."""
    na_trideset = pokreni_fis(3, 1, 30, 0)
    na_cetrdeset = pokreni_fis(3, 1, 40, 0)
    assert abs(na_trideset["spam_score"] - na_cetrdeset["spam_score"]) < 10


def test_ocigledan_spam_je_spam():
    rezultat = analiziraj_tekst(
        "CONGRATULATIONS!!! You WON a FREE prize! Click here: http://fakesite.com "
        "to CLAIM NOW!!! Click http://bonus.com and http://reward.net NOW!!!"
    )
    assert rezultat["kategorija"] == "SPAM"
    assert rezultat["spam_score"] >= 80


def test_obican_email_je_legitiman():
    rezultat = analiziraj_tekst(
        "Hi, just wanted to confirm our meeting tomorrow at 3pm. "
        "Let me know if that works for you."
    )
    assert rezultat["kategorija"] == "LEGITIMAN"
    assert rezultat["spam_score"] < 20


def test_interpunkcija_ne_okida_agresivno_previse_rano():
    """12% interpunkcije nekad je davalo 'agresivnu' pripadnost 0.67."""
    rezultat = pokreni_fis(0, 0, 30, 12)
    assert rezultat["kategorija"] == "LEGITIMAN"
    assert rezultat["spam_score"] < 25


def test_primeri_daju_dovoljno_razlicitih_skorova():
    skorovi = {round(analiziraj_tekst(tekst)["spam_score"], 2) for tekst in ucitaj_primere()}
    assert len(skorovi) >= 25
