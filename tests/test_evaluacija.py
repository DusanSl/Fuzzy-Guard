"""Testovi za evaluacione pomoćne funkcije u ``neuronska_mreza.treniraj``.

Ove funkcije ne utiču na runtime, ali proizvode brojeve koji idu u README i u
odbranu. Greška u njima ne obara aplikaciju, nego tiho pokvari izveštaj, pa
zato imaju svoje testove.
"""

import numpy as np

from neuronska_mreza.treniraj import (
    INTERNA_VALIDACIJA,
    SEME_INTERNE_VALIDACIJE,
    SEME_TESTA,
    TEST_SIZE,
    broj_aktiviranja,
    fazi_rezultati,
    indeksi_interne_validacije,
    indeksi_podela,
    skorovi_i_oznake,
)

# Mnogo ključnih reči, mnogo linkova, velika slova i uzvici.
SPAM_RED = [9.0, 6.0, 40.0, 20.0]
# Nijedan signal.
LEGITIMAN_RED = [0.0, 0.0, 0.0, 0.0]


def test_fazi_rezultati_prihvata_jedan_broj_za_sve_redove():
    """Neutralno 50 mora da važi za svaki red, ne samo za prvi.

    Zamka je ``zip(X, 50.0)``: skalarni peti ulaz bi pukao ili bi tiho uzeo
    samo prvi red. Ovaj test čuva broadcast.
    """
    X = np.array([SPAM_RED, LEGITIMAN_RED])

    jedan_broj = fazi_rezultati(X, 50.0, ())
    po_redovima = fazi_rezultati(X, [50.0, 50.0], ())

    assert [r["spam_score"] for r in jedan_broj] == [
        r["spam_score"] for r in po_redovima
    ]
    assert [r["kategorija"] for r in jedan_broj] == [
        r["kategorija"] for r in po_redovima
    ]


def test_skorovi_i_oznake_prate_kategoriju():
    rezultati = fazi_rezultati(
        np.array([SPAM_RED, LEGITIMAN_RED]), [50.0, 50.0], ()
    )
    skorovi, oznake = skorovi_i_oznake(rezultati)

    assert len(skorovi) == len(oznake) == len(rezultati)
    assert set(int(oznaka) for oznaka in oznake) <= {0, 1}
    assert np.allclose(
        skorovi, [rezultat["spam_score"] for rezultat in rezultati]
    )

    # Oznaka je 1 tačno kada je kategorija SPAM, ništa drugo.
    assert list(oznake) == [
        1 if rezultat["kategorija"] == "SPAM" else 0 for rezultat in rezultati
    ]
    assert oznake[0] == 1
    assert oznake[1] == 0


def test_broj_aktiviranja_radi_na_izabranim_pravilima():
    # Brojni linkovi, a mreža je sigurna da nije spam: aktivira se n02.
    X = np.array([[0.0, 8.0, 5.0, 1.0]])

    brojaci = broj_aktiviranja(X, [10.0], ("n01", "n02"))
    assert brojaci.get("n02") == 1
    assert "n01" not in brojaci

    # Bez n pravila u bazi, brojanje ne sme da vrati nijedno n pravilo.
    bez_n = broj_aktiviranja(X, [10.0], ())
    assert [naziv for naziv in bez_n if naziv.startswith("n")] == []

    # n02 jačina je 0.025, ispod praga 0.05, pa se ne broji.
    ispod_praga = broj_aktiviranja(X, [49.5], ("n01", "n02"))
    assert "n02" not in ispod_praga


def test_podela_je_fiksna_i_interna_validacija_ne_dira_test():
    oznake = np.array([0] * 160 + [1] * 40)
    indeksi_treninga, indeksi_testa = indeksi_podela(oznake)

    assert len(indeksi_testa) == int(round(TEST_SIZE * len(oznake)))

    # Determinizam: test se ne pomera između poziva. Bez ovoga bi ablacija i
    # završna ocena mogle da gledaju različite redove.
    ponovo_trening, ponovo_test = indeksi_podela(oznake)
    assert np.array_equal(indeksi_treninga, ponovo_trening)
    assert np.array_equal(indeksi_testa, ponovo_test)

    # Dve podele su disjunktne i zajedno pokrivaju sve redove.
    assert not set(indeksi_treninga) & set(indeksi_testa)
    assert set(indeksi_treninga) | set(indeksi_testa) == set(range(len(oznake)))

    # Stratifikacija: udeo spama u testu prati udeo u celom skupu.
    assert abs(oznake[indeksi_testa].mean() - oznake.mean()) < 0.02

    y_train = oznake[indeksi_treninga]
    indeksi_unutra, indeksi_validacije = indeksi_interne_validacije(y_train)
    assert len(indeksi_validacije) == int(round(INTERNA_VALIDACIJA * len(y_train)))
    assert not set(indeksi_unutra) & set(indeksi_validacije)
    assert set(indeksi_unutra) | set(indeksi_validacije) == set(
        range(len(y_train))
    )

    # Validacija je unutar treninga, nikad u testu.
    globalna_validacija = {int(indeksi_treninga[p]) for p in indeksi_validacije}
    assert not globalna_validacija & set(indeksi_testa)

    # Konstante na kojima README zasniva tvrdnju o dve razdvojene podele.
    assert TEST_SIZE == 0.25
    assert INTERNA_VALIDACIJA == 0.20
    assert SEME_TESTA == 42
    assert SEME_INTERNE_VALIDACIJE == 7
