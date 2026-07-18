import numpy as np
from fazi.pravila import (
    fuzzifikuj,
    kontroler_spam_score,
)
from fazi.defazifikacija import defazifikuj


def pokreni_fis(
    val_kljucne:       float,
    val_linkovi:       float,
    val_caps:          float,
    val_interpunkcija: float,
) -> dict:

    mu = fuzzifikuj(val_kljucne, val_linkovi, val_caps, val_interpunkcija)

    agregirani_skup, alfe = kontroler_spam_score(mu)

    spam_score = defazifikuj(agregirani_skup)

    if max(alfe.values()) == 0:
        kategorija = "LEGITIMAN"
    else:
        prioritet = {"SPAM": 2, "SUMNJIVO": 1, "LEGITIMAN": 0}
        kategorija = max(alfe, key=lambda k: (alfe[k], prioritet[k]))

    return {
        "spam_score": spam_score,
        "kategorija": kategorija,
    }