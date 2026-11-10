"""Izlaz neuronske mreže kao peti fazi ulaz.

Mreža (MLP ``(16, 8)``) se trenira na iste četiri interpretabilne
karakteristike koje dobija i fazi sistem. U runtime-u se **ne** koristi za
odluku: njen izlaz je samo peti ulaz ``nn_pouzdanje`` (0-100), koji pravila
``n01``-``n03`` tretiraju kao potvrdu. Konačna ocena ostaje Mamdani + centroid.

Modeli se čuvaju po rečniku (``en``, ``sr``, ``kombinovano``) jer se ulaz
``kljucne_reci`` menja sa rečnikom. Ako model ne postoji, ako je oštećen ili
ako je rečnik ponovo treniran posle modela, vraća se neutralna vrednost 50.
Tada ``nn`` pravila ne mogu da se aktiviraju i sistem se ponaša kao čist fazi
sistem. Greška u mreži nikad ne obara zahtev.
"""

import hashlib
import logging
from pathlib import Path

import joblib
import sklearn

KOREN = Path(__file__).parent.parent
PUTANJA_RECNICI = KOREN / "podaci"

KARAKTERISTIKE = ("kljucne_reci", "broj_linkova", "caps_procenat", "interpunkcija")

PUTANJE_MODELA = {
    nacin: PUTANJA_RECNICI / f"model_nn_{nacin}.joblib"
    for nacin in ("en", "sr", "kombinovano")
}

PUTANJE_RECNIKA = {
    "en": PUTANJA_RECNICI / "recnik_naucen_en.json",
    "sr": PUTANJA_RECNICI / "recnik_naucen_sr.json",
}

NEUTRALNO = 50.0
_SEED = 42

_log = logging.getLogger(__name__)
_MODELI_KEŠ = {}
_HASH_KEŠ = {}
_Upozoreno = set()


def recnik_hash(nacin: str):
    """Hash rečnika koje model koristi; ``None`` ako fajl ne postoji.

    ``kombinovano`` koristi oba rečnika, pa ulazi u isti hash. Time se model
    odbija ako se bilo koji rečnik promeni.
    """
    if nacin not in PUTANJE_MODELA:
        return None

    jezici = ("en", "sr") if nacin == "kombinovano" else (nacin,)
    heš = hashlib.sha256()
    for jezik in jezici:
        putanja = PUTANJE_RECNIKA[jezik]
        try:
            vreme = putanja.stat().st_mtime
        except OSError:
            return None

        keširan = _HASH_KEŠ.get(putanja)
        if keširan and keširan[0] == vreme:
            heš.update(keširan[1])
            continue

        try:
            sadrzaj = putanja.read_bytes()
        except OSError:
            return None
        _HASH_KEŠ[putanja] = (vreme, sadrzaj)
        heš.update(sadrzaj)

    return heš.hexdigest()


def _upozori_jednom(kljuc: str, poruka: str) -> None:
    if kljuc in _Upozoreno:
        return
    _Upozoreno.add(kljuc)
    _log.warning(poruka)


def ucitaj_model(nacin: str):
    """Vraća model za rečnik ili ``None``. Keš se osvežava po mtime-u."""
    putanja = PUTANJE_MODELA.get(nacin)
    if putanja is None:
        return None

    try:
        vreme = putanja.stat().st_mtime
    except OSError:
        _MODELI_KEŠ.pop(nacin, None)
        return None

    keširan = _MODELI_KEŠ.get(nacin)
    if keširan and keširan[0] == vreme:
        return keširan[1]

    try:
        podaci = joblib.load(putanja)
        mreza = podaci["mreza"]
        skaliraj = podaci["skaliraj"]
        meta = podaci.get("meta", {})
    except Exception:
        _upozori_jednom(
            f"ostecen:{nacin}",
            f"Model {putanja.name} ne može da se učita; koristi se neutralno 50.",
        )
        _MODELI_KEŠ[nacin] = (vreme, None)
        return None

    ocekivani = meta.get("recnik_hash")
    trenutni = recnik_hash(nacin)
    if ocekivani is None or trenutni is None or ocekivani != trenutni:
        _upozori_jednom(
            f"hash:{nacin}",
            f"Model {putanja.name} ne odgovara trenutnom rečniku; "
            "koristi se neutralno 50. Ponovo pokrenite treniranje.",
        )
        _MODELI_KEŠ[nacin] = (vreme, None)
        return None

    model = {"mreza": mreza, "skaliraj": skaliraj, "meta": meta}
    _MODELI_KEŠ[nacin] = (vreme, model)
    return model


def pouzdanje_nn(ulazi: dict, nacin: str) -> float:
    """Verovatnoća spama koju daje mreža, izražena 0-100.

    ``50.0`` je neutralna vrednost: mreža tada ne može da aktivira ``n``
    pravila. Funkcija nikad ne podiže izuzetak.
    """
    model = ucitaj_model(nacin)
    if model is None:
        return NEUTRALNO

    try:
        red = [[float(ulazi[ime]) for ime in KARAKTERISTIKE]]
        skalirano = model["skaliraj"].transform(red)
        verovatnoca = float(model["mreza"].predict_proba(skalirano)[0, 1])
    except Exception:
        _upozori_jednom(
            f"predikcija:{nacin}",
            "Predikcija neuronske mreže nije uspela; koristi se neutralno 50.",
        )
        return NEUTRALNO

    return max(0.0, min(100.0, verovatnoca * 100.0))


def sacuvaj_model(nacin: str, skaliraj, mreza) -> Path:
    """Čuva model sa metapodacima koji vezuju model za rečnik."""
    if nacin not in PUTANJE_MODELA:
        raise ValueError(f"Nepoznat rečnik za model: {nacin}")

    putanja = PUTANJE_MODELA[nacin]
    putanja.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {
            "skaliraj": skaliraj,
            "mreza": mreza,
            "meta": {
                "sklearn": sklearn.__version__,
                "recnik": nacin,
                "recnik_hash": recnik_hash(nacin),
                "seed": _SEED,
                "arhitektura": list(mreza.hidden_layer_sizes),
            },
        },
        putanja,
    )
    _MODELI_KEŠ.pop(nacin, None)
    return putanja
