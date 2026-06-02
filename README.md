# Inbox Guard

Projekat iz predmeta **Meko računarstvo**. Sistem za detekciju spam emailova zasnovan na **fazi logici (fuzzy logic)** — umesto da email klasifikuje kao strogo spam ili ne-spam, sistem računa *stepen* sumnjivoosti na skali od 0 do 100%.

---

## Kako radi

Klasični spam filteri rade sa pravilima tipa "ako email sadrži reč FREE → spam". Fazi pristup je drugačiji: svaka karakteristika emaila se mapira na **stepen pripadnosti** fazi skupu, pravila se kombinuju kroz **Mamdani inferenciju**, a konačni score se dobija **centroid defazifikacijom**.

Sistem analizira četiri ulazne karakteristike i proizvodi jedan izlaz:

| Ulaz | Opis |
|---|---|
| `kljucne_reci` | Broj prepoznatih spam reči/fraza (0–10) |
| `broj_linkova` | Broj URL linkova u emailu (0–10) |
| `caps_procenat` | Procenat velikih slova u tekstu (0–100%) |
| `interpunkcija` | Gustina uzvičnika i upitnika (0–100%) |

Izlaz `spam_score` (0–100%) se klasifikuje u jednu od tri kategorije: **LEGITIMAN**, **SUMNJIVO**, ili **SPAM**.

---

## Tehnologije

- **Python** — fazi logika (`scikit-fuzzy`, `numpy`, `scipy`)
- **Flask** — web server i REST rute
- **HTML + CSS** — korisnički interfejs

---

## Struktura projekta

```
spam_filter/
├── fazi/
│   ├── skupovi.py          # Definicije fazi skupova (trapezoid, trougao)
│   ├── pravila.py          # Fazi pravila i fuzzifikacija ulaza
│   ├── zakljucivanje.py    # Pokretanje FIS-a (fuzzy inference system)
│   └── defazifikacija.py   # Centroid defazifikacija i određivanje kategorije
├── veb/
│   ├── static/
│   │   ├── fonts/
│   │   │   └── MonaSansVF[wght,opsz].woff2
│   │   └── style.css       # Stilovi — tamna tema, responzivan layout
│   └── sabloni/
│       ├── index.html      # Glavna stranica sa formom i rezultatima
│       └── rezultat.html   # HTML prikaz rezultata (fallback bez JS-a)
├── obrada_teksta/
│   └── analizator.py       # Ekstrakcija karakteristika iz teksta emaila
├── main.py                 # Flask aplikacija i rute
├── potrebne_biblioteke.txt # Spisak zavisnosti
├── ulazi_i_izlazi.txt      # Dokumentacija fazi varijabli
├── primeri.txt             # Testni emailovi (separator: ---)
└── .gitignore
```

---

## Instalacija i pokretanje

```bash
# Kloniranje repozitorijuma
git clone https://github.com/DusanSl/Fuzzy-spam-filter.git
cd spam_filter

# Instalacija zavisnosti
pip install -r potrebne_biblioteke.txt

# Pokretanje
python main.py
```

Aplikacija se pokreće na `http://localhost:5000`.

---

## Fazi skupovi

Svaka ulazna varijabla je podeljena na tri lingvistička termina. Krajnji skupovi su trapezoidni (drže kraj ose), srednji su trouglasti.

**Ključne reči** `[0–10]`
- `zanemarljive` — trapmf `[0, 0, 1, 3]`
- `zastupljene` — trimf `[1, 4, 7]`
- `dominantne` — trapmf `[5, 7, 10, 10]`

**Broj linkova** `[0–10]`
- `minimalni` — trapmf `[0, 0, 0, 1]`
- `umereni` — trimf `[0, 1, 3]`
- `brojni` — trapmf `[2, 4, 10, 10]`

**CAPS procenat** `[0–100%]`
- `uobicajen` — trapmf `[0, 0, 1, 10]`
- `poviseni` — trimf `[7, 18, 35]`
- `agresivan` — trapmf `[25, 45, 100, 100]`

**Interpunkcija** `[0–100%]`
- `retka` — trapmf `[0, 0, 2, 5]`
- `umerena` — trimf `[3, 10, 20]`
- `agresivna` — trapmf `[15, 25, 100, 100]`

**Spam score** `[0–100]`
- `score_legitiman` — trapmf `[0, 0, 10, 25]`
- `score_sumnjiv` — trimf `[15, 35, 55]`
- `score_spam` — trapmf `[45, 65, 100, 100]`

---

## Fazi pravila

| Pravilo | Uslov | Zaključak |
|---|---|---|
| p01 | zanemarljive AND minimalni AND uobicajen AND retka | legitiman |
| p02 | zastupljene AND umereni AND poviseni AND umerena | sumnjiv |
| p03 | zastupljene AND minimalni linkovi | sumnjiv |
| p04 | (zanemarljive OR zastupljene) AND umereni linkovi | sumnjiv |
| p05 | dominantne AND uobicajen caps | sumnjiv |
| p06 | dominantne OR brojni | spam |
| p07 | zastupljene AND (agresivan caps OR agresivna interpunkcija) | spam |
| p08 | umereni linkovi AND (agresivan caps OR agresivna interpunkcija) | spam |
| p09 | dominantne ključne reči | spam |

---

## API

### `POST /analiziraj`

Prima JSON sa tekstom emaila, vraća rezultat analize.

**Zahtev:**
```json
{
  "tekst": "CONGRATULATIONS! You WON a FREE prize! Click http://fakesite.com NOW!"
}
```

**Odgovor:**
```json
{
  "tekst": "...",
  "kljucne_reci": 7,
  "broj_linkova": 1,
  "caps_procenat": 28.57,
  "interpunkcija": 4.35,
  "spam_score": 74.21,
  "kategorija": "SPAM"
}
```

### `GET /primer`

Vraća nasumičan testni email iz `primeri.txt`.
