import numpy as np
import skfuzzy as fuzz
from fazi.skupovi import x_spam_score


def defazifikuj(agregirani_skup: np.ndarray) -> float:
    if agregirani_skup.max() == 0:
        return 0.0

    return float(fuzz.defuzz(x_spam_score, agregirani_skup, "centroid"))