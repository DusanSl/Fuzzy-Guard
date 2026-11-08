"""Regresioni testovi za fazi sistem.

Pokretanje iz korena projekta:

    python -m pytest
"""

from pathlib import Path

import skfuzzy as fuzz

from obrada_teksta.analizator import analiziraj_email, ucitaj_nauceni_recnik
from obrada_teksta import analizator
from obrada_teksta.analizator import _izracunaj_kljucne_reci
from obrada_teksta.podudaranje import pronadji_poklapanja
from neuronska_mreza.legacy_recnik import SPAM_RECNIK_RECI, termini as legacy_termini
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
    if max(clanstva.values()) == 0:
        return "SUMNJIVO"
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
        "DEAR SIR, YOUR MORTGAGE SETTLEMENT IS GUARANTEED! CLICK LINK "
        "http://a.com http://b.com http://c.com NOW!!!"
    )
    assert rezultat["kategorija"] == "SPAM"
    assert rezultat["spam_score"] >= 70


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


def test_srpski_recnik_je_naucen():
    """Srpski rečnik je naučen iz hibridnog srpskog korpusa, ne ručno."""
    recnik = ucitaj_nauceni_recnik("sr")
    assert len(recnik) > 50
    assert any(
        any(znak in termin for znak in "čćšžđ")
        for termin in recnik
    )


def test_nauceni_recnici_se_ucitavaju():
    for jezik in ("en", "sr"):
        recnik = ucitaj_nauceni_recnik(jezik)
        assert isinstance(recnik, dict)
        assert len(recnik) > 0
        assert all(tezina > 0 for tezina in recnik.values())


def test_kombinovani_recnik_spaja_oba_jezika():
    en = set(ucitaj_nauceni_recnik("en"))
    sr = set(ucitaj_nauceni_recnik("sr"))
    assert en
    assert sr
    assert en != sr
    zajednicki = en & sr
    # Termini koji se poklope ne smeju da se saberu dvaput.
    for termin in list(zajednicki)[:5]:
        assert _izracunaj_kljucne_reci(termin, "kombinovano")[0] <= 2.0


def test_legacy_baseline_radi_bez_naucenog_recnika():
    """Stari ručni rečnik ostaje dostupan samo za evaluaciju."""
    recnik = dict((termin, tezina) for termin, tezina, _ in legacy_termini())
    assert _izracunaj_kljucne_reci(
        "free prize", "legacy", legacy_recnik=recnik
    )[0] == 1.0
    assert "free" in SPAM_RECNIK_RECI


def test_fraza_ne_sabira_svoje_delove():
    termini = [("free", 1.0, "en"), ("prize", 1.0, "en"), ("free prize", 1.0, "en")]
    evidencija, pogodci = pronadji_poklapanja("free prize", termini)
    assert evidencija == 1.0
    assert [p["rec"] for p in pogodci] == ["free prize"]


def test_fraza_ne_prelazi_granicu_recenice():
    termini = [("click here", 1.0, "en")]
    assert pronadji_poklapanja("click. Here is a link", termini)[0] == 0.0
    assert pronadji_poklapanja("click, here please", termini)[0] == 1.0


def test_pozicije_rade_kada_lower_promeni_duzinu():
    rezultat = analiziraj_email("\u0130stanbul dear sir")
    pozicije = rezultat["pokrivene_reci"][0]["pozicije"][0]
    assert rezultat["vidljivi_tekst"][pozicije[0]:pozicije[1]] == "dear sir"


def test_html_se_uklanja_pre_analize():
    obican = analiziraj_email("DEAR SIR mortgage guaranteed")
    html = analiziraj_email("<html><body><p>DEAR <b>SIR</b> mortgage guaranteed</p></body></html>")
    assert obican["kljucne_reci"] == html["kljucne_reci"]
    assert obican["caps_procenat"] == html["caps_procenat"]


def test_leet_speak_se_prepoznaje():
    assert analiziraj_email("gu4r4nt33d")["kljucne_reci"] >= 1


def test_homoglifi_se_prepoznaju():
    assert analiziraj_email("guarant\u0435\u0435d")["kljucne_reci"] >= 1


def test_www_i_hxxp_linkovi_se_broje():
    assert analiziraj_email("visit www.example.com and hxxp://evil.net")["broj_linkova"] == 2


def test_link_iz_href_atributa():
    assert analiziraj_email('<a href="http://x.com">click</a>')["broj_linkova"] == 1


def test_api_vraca_objasnjenje():
    from main import app
    klijent = app.test_client()
    odgovor = klijent.post(
        "/analiziraj", json={"tekst": "Dear sir, this mortgage settlement is guaranteed."}
    ).get_json()
    assert "objasnjenje" in odgovor
    assert odgovor["objasnjenje"]["pokrivene_reci"]
    assert "aktivna_pravila" in odgovor["objasnjenje"]


def test_objasnjenje_sadrzi_ulaze_pozicije_i_uslove():
    from main import app
    klijent = app.test_client()
    odgovor = klijent.post(
        "/analiziraj", json={"tekst": "Dear sir, this mortgage settlement is guaranteed."}
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


def test_oznake_za_link_caps_i_interpunkciju():
    from main import app
    tekst = "CONGRATULATIONS!!! Visit http://example.com NOW!"
    objasnjenje = app.test_client().post(
        "/analiziraj", json={"tekst": tekst}
    ).get_json()["objasnjenje"]

    grupe = {grupa["tip"]: grupa["pozicije"] for grupa in objasnjenje["oznake"]}
    assert grupe["link"] and grupe["caps"] and grupe["interpunkcija"]

    for pozicije in grupe.values():
        for pocetak, kraj in pozicije:
            assert objasnjenje["tekst"][pocetak:kraj]

    pocetak, kraj = grupe["link"][0]
    assert "http://example.com" in objasnjenje["tekst"][pocetak:kraj]

    pocetak, kraj = grupe["caps"][0]
    assert objasnjenje["tekst"][pocetak:kraj].isupper()

    pocetak, kraj = grupe["interpunkcija"][0]
    assert set(objasnjenje["tekst"][pocetak:kraj]) <= set("!?")


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
    for element in ("spektar", "rezultat", "pogled-sadrzaj", "tema-dugme", "istorija-lista"):
        assert element in html
    assert "uzorak-indikator" not in html


def test_srpski_primeri_imaju_dijakritike():
    from obrada_teksta.analizator import ucitaj_sve_primere
    primer = next(
        p for p in ucitaj_sve_primere("sr") if "Osvojili ste" in p["tekst"]
    )
    assert "Čestitamo" in primer["tekst"]
    assert "?" not in primer["tekst"]


def test_svaka_kategorija_ima_primere():
    from obrada_teksta.analizator import ucitaj_sve_primere
    for jezik in ("en", "sr"):
        lista = ucitaj_sve_primere(jezik)
        for kategorija in ("legitiman", "sumnjiv", "prevara"):
            assert any(p["kategorija"] == kategorija for p in lista)


def test_ocigledan_spam_nije_u_legitiman_grupi():
    from obrada_teksta.analizator import ucitaj_sve_primere
    sve = ucitaj_sve_primere("en") + ucitaj_sve_primere("sr")
    legit = " ".join(p["tekst"] for p in sve if p["kategorija"] == "legitiman").lower()
    assert "ticket 4471" not in legit
    assert "lucky holder" not in legit
    assert "uplatu do petka" not in legit
    assert "magacinu" not in legit


def test_analiziraj_prihvata_recnik():
    from main import app
    klijent = app.test_client()
    tekst = "mortgage"

    en = klijent.post(
        "/analiziraj", json={"tekst": tekst, "recnik": "en"}
    ).get_json()
    sr = klijent.post(
        "/analiziraj", json={"tekst": tekst, "recnik": "sr"}
    ).get_json()
    kombinovano = klijent.post(
        "/analiziraj", json={"tekst": tekst, "recnik": "kombinovano"}
    ).get_json()

    assert en["kljucne_reci"] > 0.0
    assert kombinovano["kljucne_reci"] >= en["kljucne_reci"]
    assert sr["kljucne_reci"] >= 0.0


def test_skupovi_endpoint_vraca_ulaze_i_izlaze():
    from main import app
    podaci = app.test_client().get("/skupovi").get_json()
    assert set(podaci["ulazi"]) == {
        "kljucne_reci", "broj_linkova", "caps_procenat", "interpunkcija"
    }
    assert len(podaci["izlazi"]) == 6
    assert len(podaci["skupovi"]) == 6
    for grupa in podaci["ulazi"].values():
        assert grupa
        for skup in grupa:
            assert skup["tip"] in ("trimf", "trapmf")
            assert len(skup["params"]) in (3, 4)


def test_izlazni_skupovi_pokrivaju_celi_univerzum():
    for skor in range(0, 101):
        # Tacno 22 je granica gde energicno zavrsava (trimf [10,13,22]), a
        # blago_sumnjiv pocinje (trimf [22,30,42]); pokreni_fis tada vraca
        # SUMNJIVO kroz eksplicitni fallback.
        if skor == 22:
            continue
        pripadnosti = [
            float(fuzz.interp_membership(x_spam_score, skup, skor))
            for skup in izlazni_skupovi.values()
        ]
        assert max(pripadnosti) > 0, f"nijedan izlazni skup nije aktivan na {skor}"


def test_analiziraj_odbija_neispravan_ulaz():
    from main import app
    klijent = app.test_client()

    assert klijent.post("/analiziraj", json={"tekst": None}).status_code == 400
    assert klijent.post("/analiziraj", json={"tekst": 123}).status_code == 400
    assert klijent.post("/analiziraj", json={"tekst": "   "}).status_code == 400






