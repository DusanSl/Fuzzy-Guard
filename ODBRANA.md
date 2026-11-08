# Odbrana — priprema i očekivana pitanja

Kratke, odbrambene teze. Brojeve treba znati napamet; objašnjenja treba
izgovoriti svojim rečima.

## Arhitektura u tri rečenice

Ulaz je tekst emaila iz kojeg se izvlače četiri numeričke karakteristike:
broj ključnih reči (0–10), broj linkova (0–10), procenat velikih slova (0–100%)
i gustina interpunkcije (0–100%). Te vrednosti se fazifikuju kroz trouglaste i
trapezoidne funkcije pripadnosti, a 19 pravila (Mamdani, min/max) daje izlazni
fazi skup. Defazifikacijom težištem (centroid) dobija se `spam_score` 0–100%,
a kategorija se čita kao skup sa najvećom pripadnošću u toj tački.

---

## 1. Zašto fazi, a ne obični pragovi?

Običan filtar ima oštre granice: 3 ključne reči = sumnjivo, 2 = nije. Fazi
sistem dozvoljava delimičnu pripadnost, pa email sa dve reči i puno velikih
slova može biti sumnjiv iako nijedan pojedinačni uslov nije prekoračen. Rezultat
je stepen sumnje, ne binarna odluka.

## 2. Zašto Mamdani, a ne Sugeno?

Mamdani daje lingvistički izlaz („legitiman”, „sumnjiv”, „spam”), što je
razumljivo korisniku i direktno se crta. Sugeno je brži i lakši za optimizaciju,
ali izlaz je linearna funkcija ulaza, pa gubi interpretabilnost. Za ovaj
projekat je interpretabilnost prioritet.

## 3. Zašto min/max?

`min` je standardna t-norma za AND, `max` standardna t-konorma za OR u Mamdani
sistemu. Alternativa je proizvod/algebarska suma; ona daje glatkije prelaze, ali
`min/max` su ono što se radi na kursu i lakše se objasne.

## 4. Zašto težište (centroid) za defazifikaciju?

Centroid koristi celu površinu agregiranog skupa, pa je stabilniji od MOM
(sredina maksimuma) i manje osetljiv na oblik od bisector-a. Nedostatak je
računski skuplji, ali univerzum ima samo 101 tačku.

## 5. Zašto trouglovi i trapezoidi?

To su dva oblika obrađena na kursu. Trougao ima jednu tačku pune pripadnosti,
trapezoid dozvoljava interval pune pripadnosti, što odgovara izrazima kao
„umereno” (interval) i „dominantno” (raste do kraja).

## 6. Zašto baš ove četiri karakteristike?

Pokrivaju četiri nezavisna signala spama: sadržaj (reči), strukturu (linkovi),
stil pisanja (velika slova) i stil interpunkcije. Sve četiri se jeftino računaju
i objašnjive su korisniku.

## 7. Kako su određene granice skupova? (najvažnije pitanje)

Merenjem na skupu primera iz `primeri.txt`: legitimni emailovi imaju do ~6%
velikih slova, spam 26–60%; najveća izmerena interpunkcija je ~14%. Te granice su
zatim proverene na **odvojenom test skupu** (SpamAssassin, 25% podataka), nikad
na istim podacima na kojima su podešavane.

Ako profesor primeti da je kalibracija rađena na malom skupu — priznati to
otvoreno: skup je mali, zato su svi brojevi u README-u sa held-out testa, ne sa
skupa za podešavanje.

## 8. Da li je baza pravila kompletna?

Da. Test `test_pokrivenost_celog_univerzuma` prolazi kroz mrežu ulaza i tvrdi da
bar jedno pravilo ima jačinu > 0 u svakoj tački. Pre popravke je 54 tačke
ostajalo bez ijednog aktivnog pravila (npr. 3 ključne reči, 1 link, 0% velikih
slova, 5% interpunkcije), pa je skor padao na hardkodovanu konstantu.

## 9. Šta znači 73%?

To je težište agregiranog izlaznog fazi skupa. Nije verovatnoća. Znači da je
ukupna „masa” dokaza za spam na 73% skale od 0 do 100. Kategorija se čita iz
istog broja, pa se broj i oznaka ne mogu razići.

## 10. Zašto dva različita emaila imaju isti procenat?

Ako dva ulaza imaju iste stepene pripadnosti u svim skupovima i aktiviraju ista
pravila istom jačinom, Mamdani izlaz je po definiciji isti. To nije greška nego
posledica diskretne lingvističke reprezentacije. Razlikovanje bi zahtevalo
dodatnu informaciju koju model nema (npr. dužinu teksta ili nove karakteristike).

## 11. Zašto ne ANFIS?

ANFIS bi naučio parametre pripadnosti iz podataka, ali: (a) zahteva veći
označeni skup, (b) klasično koristi zvonaste/gausove funkcije, ne trouglove,
(c) gubi se direktna interpretacija pravila. Navesti kao mogući budući rad.

## 12. Neuronska mreža

- Iste četiri karakteristike kao fazi sistem — fer poređenje.
- MLP 16–8, ReLU, stratifikovani 75/25 split, rani prekid.
- SpamAssassin, 750 test emailova (125 spam):

| Model | Tačnost | Preciznost | Odziv | F1 |
|---|---|---|---|---|
| MLP | 0.929 | 0.883 | 0.664 | 0.758 |
| Fazi | 0.771 | 0.382 | 0.608 | 0.469 |

- Mreža je tačnija, ali fazi sistem je interpretabilan i ne zahteva trening.
- Mreža **ne ulazi** u `spam_score`; služi kao drugo mišljenje i poređenje.
- Na SMS korpusu fazi sistem ima odziv samo 3%: karakteristike su pravljene za
  email (SMS nema linkove ni velika slova). To je ograničenje domena.

## 13. Ograničenja koja treba sami navesti

- Kalibracija na malom skupu primera; mali broj označenih emailova na srpskom.
- Srpski pokriva samo rečnik i pravila; mreža je samo engleski.
- Isti skor za različite emailove (vidi pitanje 10).
- Duplikati se ne rešavaju veštačkim linearnim članom — to bi bilo nedefendabilno
  na kursu fazi logike.

## 14. Šta biste uradili sa još vremena?

Veći označeni skup (uključujući srpski), ANFIS kao eksperiment uz zadržane
trouglaste funkcije, i dodatne ulaze (dužina teksta, broj attachments-a) koji bi
povećali rezoluciju skora.

---

## Brojevi koje treba zapamtiti

- 4 ulaza, **19 pravila**, 6 izlaznih skupova, univerzum 0–100 (korak 1).
- 50 demonstracionih emailova → **29 različitih skorova** (pre popravke 26).
- SpamAssassin: **MLP F1 0.758**, **fazi F1 0.469**.
- Baza pravila: **0 nepokrivenih tačaka** (pre: 54).
- Bug koji je popravljen: skok velikih slova 30% → 40% obarao je skor sa ~87 na
  47; sada razlika < 3 poena.
