"""Regresioni testovi za fazi sistem.

Pokretanje iz korena projekta:

    python -m pytest
"""

from pathlib import Path

import skfuzzy as fuzz

from obrada_teksta.analizator import analiziraj_email
from obrada_teksta import analizator
from obrada_teksta.analizator import (
    SPAM_RECNIK_RECI,
    _izracunaj_kljucne_reci,
    ucitaj_nauceni_recnik,
    ucitaj_teske_primere,
)
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


def test_srpski_recnik_je_sacuvan():
    """Rucni (srpski) recnik je baseline bez neuronske mreze i ne sme da nestane."""
    for rec in ("besplatno", "nagrada", "klikni", "čestitamo", "osvojio"):
        assert rec in SPAM_RECNIK_RECI


def test_nauceni_recnik_se_ucitava():
    recnik = ucitaj_nauceni_recnik()
    assert isinstance(recnik, dict)
    assert len(recnik) > 0
    assert all(tezina > 0 for tezina in recnik.values())


def test_kombinovani_recnik_ne_broji_isti_termin_dvaput():
    # "free" postoji u rucnom recniku, pa se naucena verzija preskace
    assert _izracunaj_kljucne_reci("free", "rucni")[0] == 1.0
    assert _izracunaj_kljucne_reci("free", "kombinovano")[0] == 1.0


def test_nauceni_recnik_dodaje_nove_termine():
    recnik = ucitaj_nauceni_recnik()
    rucni = set(SPAM_RECNIK_RECI)
    novi = next((termin for termin in recnik if termin not in rucni and " " not in termin), None)
    assert novi is not None, "nauceni recnik ne sadrzi nijedan nov termin"
    assert _izracunaj_kljucne_reci(novi, "nauceni")[0] > 0


def test_rucni_recnik_radi_bez_naucenog(monkeypatch):
    """Ako nema naucenog recnika, sistem mora da radi kao pre neuronske mreze."""
    monkeypatch.setattr(analizator, "_NAUCENI_RECNIK", {})
    assert _izracunaj_kljucne_reci("free", "kombinovano")[0] == 1.0
    assert _izracunaj_kljucne_reci("free prize", "kombinovano")[0] == 3.0


def test_html_se_uklanja_pre_analize():
    obican = analiziraj_email("WIN a FREE prize now")
    html = analiziraj_email("<html><body><p>WIN a <b>FREE</b> prize now</p></body></html>")
    assert obican["kljucne_reci"] == html["kljucne_reci"]
    assert obican["caps_procenat"] == html["caps_procenat"]


def test_leet_speak_se_prepoznaje():
    assert analiziraj_email("FR33 pr1ze")["kljucne_reci"] >= 2


def test_homoglifi_se_prepoznaju():
    assert analiziraj_email("Fr\u0435\u0435 prize")["kljucne_reci"] >= 2


def test_www_i_hxxp_linkovi_se_broje():
    assert analiziraj_email("visit www.example.com and hxxp://evil.net")["broj_linkova"] == 2


def test_link_iz_href_atributa():
    assert analiziraj_email('<a href="http://x.com">click</a>')["broj_linkova"] == 1


def test_api_vraca_objasnjenje():
    from main import app
    klijent = app.test_client()
    odgovor = klijent.post(
        "/analiziraj", json={"tekst": "You WON a FREE prize, click here now"}
    ).get_json()
    assert "objasnjenje" in odgovor
    assert odgovor["objasnjenje"]["pokrivene_reci"]
    assert "aktivna_pravila" in odgovor["objasnjenje"]


def test_teski_primeri_postoje():
    assert len(ucitaj_teske_primere("sr")) >= 5
    assert len(ucitaj_teske_primere("en")) >= 3


def test_teski_srpski_primeri_nemaju_rucne_kljucne_reci():
    """Teski primeri su namerno bez ijedne reci iz rucnog recnika."""
    for tekst in ucitaj_teske_primere("sr"):
        ulazi = analiziraj_email(tekst, nacin_recnik="rucni")
        assert ulazi["kljucne_reci"] == 0.0, tekst


def test_obican_ucitavac_ne_vraca_teske_primere():
    from obrada_teksta.analizator import ucitaj_sve_primere
    normalni = set(ucitaj_sve_primere("en")) | set(ucitaj_sve_primere("sr"))
    teski = set(ucitaj_teske_primere("en")) | set(ucitaj_teske_primere("sr"))
    assert teski
    assert normalni.isdisjoint(teski)


def test_objasnjenje_sadrzi_ulaze_pozicije_i_uslove():
    from main import app
    klijent = app.test_client()
    odgovor = klijent.post(
        "/analiziraj", json={"tekst": "You WON a FREE prize, click here now"}
    ).get_json()
    objasnjenje = odgovor["objasnjenje"]

    assert objasnjenje["tekst"]
    assert set(objasnjenje["ulazi"]) == {
        "kljucne_reci", "broj_linkova", "caps_procenat", "interpunkcija"
    }
    assert objasnjenje["pokrivene_reci"]
    prvo = objasnjenje["pokrivene_reci"][0]
    assert prvo["pozicije"]
    pocetak, kraj = prvo["pozicije"][0]
    assert objasnjenje["tekst"][pocetak:kraj].lower() == prvo["rec"]

    assert objasnjenje["aktivna_pravila"]
    assert objasnjenje["aktivna_pravila"][0]["uslov_sr"]
    assert objasnjenje["aktivna_pravila"][0]["uslov_en"]


def test_svako_pravilo_ima_opis():
    from fazi.pravila import OPISI_PRAVILA, sastavi_pravila
    mu = fuzzifikuj(5, 1, 20, 10)
    for naziv, _, _, _ in sastavi_pravila(mu):
        assert naziv in OPISI_PRAVILA
        assert OPISI_PRAVILA[naziv]["sr"]
        assert OPISI_PRAVILA[naziv]["en"]


def test_skupovi_endpoint_vraca_sest_skupova():
    from main import app
    podaci = app.test_client().get("/skupovi").get_json()
    assert len(podaci["skupovi"]) == 6
    for skup in podaci["skupovi"]:
        assert skup["tip"] in ("trimf", "trapmf")
        assert len(skup["params"]) in (3, 4)
        assert skup["kategorija"] in ("LEGITIMAN", "SUMNJIVO", "SPAM")
        assert skup["naziv"]


def test_dashboard_ima_nove_elemente():
    from main import app
    html = app.test_client().get("/").get_data(as_text=True)
    for element in ("spektar", "verdict-sadrzaj", "tab-sadrzaj", "tema-dugme", "istorija"):
        assert element in html






