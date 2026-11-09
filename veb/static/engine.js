/* ---------- copy -------------------------------------------------- */

const prevodi = {
    en: {
        jezik: 'SR', jezikNaziv: 'Switch to Serbian',
        temaSvetla: 'Switch to light appearance', temaTamna: 'Switch to dark appearance',
        navProvera: 'Check', navMetod: 'Method',
        naslov: 'Not a guess.\nA traceable score.',
        uvodOpis: 'Four signals, nineteen rules, one defuzzified number — and every step visible.',
        poruka: 'Message', ocisti: 'Clear',
        od: 'From', tema: 'Subject',
        placeholder: 'Paste the email text here…',
        znakova: 'characters',
        uzorakLegitiman: 'Legitimate', uzorakSumnjiv: 'Suspicious', uzorakPrevara: 'Spam', uzorakRandom: 'Random',
        recnik: 'Keyword lexicon', en: 'English', sr: 'Serbian', kombinovano: 'Both',
        pokreni: 'Run analysis', analiziram: 'Analyzing…',
        sitno: 'Only the body is scored · nothing leaves this page.',
        greskaPrazno: 'Add some text first.',
        greskaMreza: 'Could not reach the server.',
        procena: 'Assessment', kopiraj: 'Copy result', kopirano: 'Result copied',
        doprinosiNaslov: 'What contributed',
        prazno: 'Run an analysis to see the score, the active fuzzy sets and the rules that produced it.',
        skorNatpis: 'Spam suspicion · 0–100',
        osaLegitiman: 'Legitimate', osaSumnjivo: 'Suspicious', osaSpam: 'Spam',
        skupLegitiman: 'legitimate', skupEnergicno: 'strongly legitimate',
        skupBlagoSumnjiv: 'mildly suspicious', skupSumnjiv: 'suspicious', skupVisokoSumnjiv: 'highly suspicious', skupSpam: 'spam',
        spektarAria: 'Fuzzy output spectrum: six output sets in three categories. Legitimate: legitimate and strongly legitimate. Suspicious: mildly suspicious, suspicious and highly suspicious. Spam: spam.',
        teziste: 'Centroid',
        tabZasto: 'Why', tabUlazi: 'Inputs', tabPravila: 'Rules',
        pronasli: 'Matched in the text', prepoznate: 'Matched keywords',
        nemaPogodaka: 'No dictionary hits. Here the score comes from links, capitals and punctuation alone.',
        legenda: { keyword: 'keyword', link: 'link', caps: 'capitals', interpunkcija: 'punctuation' },
        izvorRucni: 'hand dictionary', izvorEn: 'English lexicon', izvorSr: 'Serbian lexicon',
        ulaziNaslov: 'Memberships above 0.05',
        pravilaNaslov: 'Rules that fired',
        prethodne: 'Recent checks', ocistiSve: 'Clear all', nemaIstorije: 'Nothing checked yet.',
        podnozjeMetod: 'Mamdani inference · min/max · centroid defuzzification',
        kakoRadi: 'How it works', prototip: 'Design prototype', zatvori: 'Close',
        metodNatpis: 'Method', metodNaslov: 'A score you can verify.',
        metodUvod: 'The fuzzy rules calculate the score. The neural network does not. The system cleans the message, finds keywords, measures four signals, fuzzifies them, applies 19 rules, and calculates one number. The result view shows each step.',
        korak1Naslov: 'Clean the text', korak1Opis: 'The system decodes HTML entities and removes scripts and tags. It analyses only the visible body.',
        korak2Naslov: 'Find keywords', korak2Opis: 'The system compares the body with the learned English and Serbian word lists. It calculates a keyword score from 0 to 10.',
        korak3Naslov: 'Measure signals', korak3Opis: 'The system measures the keyword score, the number of links, the percentage of capital letters, and the punctuation rate.',
        korak4Naslov: 'Fuzzify the signals', korak4Opis: 'Each signal receives a degree of membership in triangular or trapezoidal sets.',
        korak5Naslov: 'Apply the rules', korak5Opis: 'Nineteen Mamdani rules combine the memberships with min and max. Each active rule limits its output set to its activation strength.',
        korak6Naslov: 'Defuzzify and explain', korak6Opis: 'The system aggregates the limited sets with max. The centroid from 0 to 100 is the score. The category comes from the same value.',
        metodSignaliNaslov: 'Measured signals',
        metodSignaliUvod: 'The system scores only the message body. The From and Subject fields give context. They do not go to the classifier.',
        metodTabelaSignal: 'Signal', metodTabelaNacin: 'Definition', metodTabelaSkala: 'Scale',
        signaliKljucneReci: 'Keywords', signaliLinkovi: 'Links', signaliCaps: 'Capitals', signaliInterpunkcija: 'Punctuation',
        metodKljucneOpis: 'The system looks for words in the selected learned word list. Each word has a weight. The system adds the weights of matched words and limits the sum to 10.',
        metodLinkoviOpis: 'Unique URLs in the text or in href attributes. The count is limited to 10.',
        metodCapsOpis: 'Uppercase letters divided by all letters. The system removes links first.',
        metodInterpunkcijaOpis: 'Exclamation marks and question marks divided by non-space characters. The result is multiplied by 100.',
        metodMrezaNaslov: 'Function of the neural network',
        metodMrezaTekst1: 'A neural network (NN) is a model with an input layer, hidden layers and an output layer. Each layer contains neurons. Each connection between neurons has a weight. A perceptron is a simple artificial neuron: it multiplies each input by a weight, adds the results, and passes the sum through an activation function.',
        metodMrezaTekst2: 'The network learns these weights from labelled examples. It is trained offline on SpamAssassin data. It produces only the keyword lexicon: the weights in the two learned word lists.',
        metodMrezaTekst3: 'The network does not see the four signals. It does not calculate the spam score. The fuzzy rules make the decision.',
        metodTabelaModel: 'Model', metodTabelaTacnost: 'Accuracy',
        metodModelFaziEn: 'Fuzzy + EN lexicon', metodModelFaziOba: 'Fuzzy + both lexicons',
        metodModelMrezaEn: 'NN standalone, EN', metodModelMrezaOba: 'NN standalone, both',
        metodTacnostFaziEn: '90.3%', metodTacnostFaziOba: '90.0%',
        metodTacnostMrezaEn: '93.5%', metodTacnostMrezaOba: '92.9%',
        metodF1FaziEn: '0.697', metodF1FaziOba: '0.704',
        metodF1MrezaEn: '0.770', metodF1MrezaOba: '0.736',
        metodMrezaFusnota: 'Held-out SpamAssassin test set: 750 email messages, 125 spam messages. The Serbian corpus is partly synthetic. The Serbian values do not represent production accuracy.',
        metodPravilaNaslov: 'Rules and limitations',
        metodPravilaTekst: 'The system has 19 rules: 4 legitimate, 11 suspicious, and 4 spam. Each rule limits its output set to its activation strength. The system keeps the largest value at each point.',
        metodOgranicenje1: 'The four signals are designed for email. Scores for SMS and chat messages are not reliable.',
        metodOgranicenje2: 'Different emails can receive the same score when the fuzzy sets cannot separate them.',
        metodOgranicenje3: 'The boundaries of the fuzzy sets were calibrated on hand-labelled examples. All reported metrics come from held-out data.',
        metodOgranicenje4: 'The Serbian test set is partly machine-translated and partly synthetic.',
        metodSpektarOpis: 'Six output sets in three bands: 2 legitimate (0–22), 3 suspicious (22–72), 1 spam (72–100).',
        cipPravila: '19 rules', cipSkupovi: 'trimf / trapmf', cipTeziste: 'centroid', cipMreza: 'Neural network supplies the lexicon only',
        metodNapomena: 'The category comes from the same defuzzified value that the screen shows. The score and the category cannot disagree.',
        sada: 'just now', preMin: 'min ago', preH: 'h ago',
        kopirano: 'Copied to clipboard',
        kategorije: { LEGITIMAN: 'LEGITIMATE', SUMNJIVO: 'SUSPICIOUS', SPAM: 'SPAM' },
        opisiKategorija: {
            LEGITIMAN: 'The signals stay inside the legitimate band. No rule pushes the output toward spam.',
            SUMNJIVO: 'The aggregated output sits in the suspicious band; no rule reaches a spam-level output.',
            SPAM: 'The centroid lands in the spam band. The rules below show what pushed it there.'
        },
        signali: { kljucne_reci: 'Keywords', broj_linkova: 'Links', caps_procenat: 'Capitals', interpunkcija: 'Punctuation' },
        jedinice: { kljucne_reci: '/10', broj_linkova: '/10', caps_procenat: '%', interpunkcija: '%' },
        skupovi: {
            kljucne_zanemarljive: 'negligible', kljucne_zastupljene: 'present', kljucne_dominantne: 'dominant',
            linkovi_minimalni: 'minimal', linkovi_umereni: 'moderate', linkovi_brojni: 'numerous',
            caps_uobicajen: 'normal', caps_poviseni: 'elevated', caps_blago_povisen: 'mildly elevated', caps_agresivan: 'aggressive',
            interpunkcija_retka: 'sparse', interpunkcija_blago: 'mild', interpunkcija_umerena: 'moderate', interpunkcija_agresivna: 'aggressive'
        },
        metaRec: n => n === 1 ? 'keyword' : 'keywords',
        metaLink: n => n === 1 ? 'link' : 'links',
        metaCaps: 'caps'
    },
    sr: {
        jezik: 'EN', jezikNaziv: 'Prebaci na engleski',
        temaSvetla: 'Prebaci na svetlu temu', temaTamna: 'Prebaci na tamnu temu',
        navProvera: 'Provera', navMetod: 'Metod',
        naslov: 'Nije nagađanje.\nOcena koja se dokazuje.',
        uvodOpis: 'Četiri signala, devetnaest pravila i jedan defazifikovan broj — sa svakim korakom na vidiku.',
        poruka: 'Poruka', ocisti: 'Očisti',
        od: 'Pošiljalac', tema: 'Tema',
        placeholder: 'Nalepite tekst emaila ovde…',
        znakova: 'znakova',
        uzorakLegitiman: 'Legitiman', uzorakSumnjiv: 'Sumnjiv', uzorakPrevara: 'Prevara', uzorakRandom: 'Nasumično',
        recnik: 'Rečnik ključnih reči', en: 'Engleski', sr: 'Srpski', kombinovano: 'Oba',
        pokreni: 'Pokreni analizu', analiziram: 'Analiziram…',
        sitno: 'Ocenjuje se samo telo poruke · sve ostaje u pregledaču.',
        greskaPrazno: 'Dodajte tekst poruke.',
        greskaMreza: 'Greška u komunikaciji sa serverom.',
        procena: 'Procena', kopiraj: 'Kopiraj rezultat', kopirano: 'Rezultat kopiran',
        doprinosiNaslov: 'Šta je uticalo',
        prazno: 'Pokrenite analizu da vidite ocenu, aktivne fazi skupove i pravila koja su je proizvela.',
        skorNatpis: 'Sumnjivost na spam · 0–100',
        osaLegitiman: 'Legitimno', osaSumnjivo: 'Sumnjivo', osaSpam: 'Spam',
        skupLegitiman: 'legitiman', skupEnergicno: 'izrazito legitiman',
        skupBlagoSumnjiv: 'blago sumnjiv', skupSumnjiv: 'sumnjiv', skupVisokoSumnjiv: 'visoko sumnjiv', skupSpam: 'spam',
        spektarAria: 'Spektar fazi izlaza: šest izlaznih skupova u tri kategorije. Legitimno: legitiman i izrazito legitiman. Sumnjivo: blago sumnjiv, sumnjiv i visoko sumnjiv. Spam: spam.',
        teziste: 'Težište',
        tabZasto: 'Zašto', tabUlazi: 'Ulazi', tabPravila: 'Pravila',
        pronasli: 'Pronađeno u tekstu', prepoznate: 'Pronađene ključne reči',
        nemaPogodaka: 'Nema pogodaka u rečniku. Ocena ovde dolazi samo iz linkova, velikih slova i interpunkcije.',
        legenda: { keyword: 'ključna reč', link: 'link', caps: 'velika slova', interpunkcija: 'interpunkcija' },
        izvorRucni: 'ručni rečnik', izvorEn: 'engleski rečnik', izvorSr: 'srpski rečnik',
        ulaziNaslov: 'Pripadnosti iznad 0,05',
        pravilaNaslov: 'Pravila koja su se aktivirala',
        prethodne: 'Prethodne provere', ocistiSve: 'Očisti sve', nemaIstorije: 'Još nema provera.',
        podnozjeMetod: 'Mamdani · min/max · centroid defazifikacija',
        kakoRadi: 'Kako radi', prototip: 'Dizajn prototip', zatvori: 'Zatvori',
        metodNatpis: 'Metod', metodNaslov: 'Ocena koju možete da proverite.',
        metodUvod: 'Fazi pravila izračunavaju ocenu. Neuronska mreža je ne izračunava. Sistem čisti poruku, pronalazi ključne reči, meri četiri signala, fuzifikuje ih, primenjuje 19 pravila i izračunava jedan broj. Prikaz rezultata pokazuje svaki korak.',
        korak1Naslov: 'Čišćenje teksta', korak1Opis: 'Sistem dekodira HTML entitete i uklanja skripte i oznake. Analizira samo vidljivo telo poruke.',
        korak2Naslov: 'Pronalaženje ključnih reči', korak2Opis: 'Sistem poredi telo poruke sa naučenim engleskim i srpskim listama reči. Izračunava ocenu ključnih reči od 0 do 10.',
        korak3Naslov: 'Merenje signala', korak3Opis: 'Sistem meri ocenu ključnih reči, broj linkova, procenat velikih slova i gustinu interpunkcije.',
        korak4Naslov: 'Fuzifikacija signala', korak4Opis: 'Svaki signal dobija stepen pripadnosti u trouglastim ili trapezoidnim skupovima.',
        korak5Naslov: 'Primena pravila', korak5Opis: 'Devetnaest Mamdani pravila kombinuje pripadnosti kroz min i max. Svako aktivno pravilo ograničava svoj izlazni skup na jačinu aktivacije.',
        korak6Naslov: 'Defazifikacija i objašnjenje', korak6Opis: 'Sistem agregira ograničene skupove kroz max. Težište od 0 do 100 je ocena. Kategorija dolazi iz iste vrednosti.',
        metodSignaliNaslov: 'Signali koji se mere',
        metodSignaliUvod: 'Sistem ocenjuje samo telo poruke. Polja pošiljalac i tema daju kontekst. Ona ne ulaze u klasifikator.',
        metodTabelaSignal: 'Signal', metodTabelaNacin: 'Definicija', metodTabelaSkala: 'Skala',
        signaliKljucneReci: 'Ključne reči', signaliLinkovi: 'Linkovi', signaliCaps: 'Velika slova', signaliInterpunkcija: 'Interpunkcija',
        metodKljucneOpis: 'Sistem traži reči u izabranoj naučenoj listi reči. Svaka reč ima težinu. Sistem sabira težine pronađenih reči i ograničava zbir na 10.',
        metodLinkoviOpis: 'Jedinstveni linkovi u tekstu ili href atributima. Broj je ograničen na 10.',
        metodCapsOpis: 'Velika slova podeljena sa svim slovima. Sistem prvo uklanja linkove.',
        metodInterpunkcijaOpis: 'Znaci uzvika i pitanja podeljeni sa karakterima bez razmaka. Rezultat se množi sa 100.',
        metodMrezaNaslov: 'Uloga neuronske mreže',
        metodMrezaTekst1: 'Neuronska mreža (NM) je model sa ulaznim slojem, skrivenim slojevima i izlaznim slojem. Svaki sloj sadrži neurone. Svaka veza između neurona ima težinu. Perceptron je jednostavan veštački neuron: množi svaki ulaz težinom, sabira rezultate i propušta zbir kroz aktivacionu funkciju.',
        metodMrezaTekst2: 'Mreža uči težine iz označenih primera. Trenira se unapred na SpamAssassin podacima. Daje samo rečnik ključnih reči: težine u dve naučene liste reči.',
        metodMrezaTekst3: 'Mreža ne vidi četiri signala. Ne izračunava ocenu spama. Fazi pravila donose odluku.',
        metodTabelaModel: 'Model', metodTabelaTacnost: 'Tačnost',
        metodModelFaziEn: 'Fazi + EN rečnik', metodModelFaziOba: 'Fazi + oba rečnika',
        metodModelMrezaEn: 'NM samostalno, EN', metodModelMrezaOba: 'NM samostalno, oba',
        metodTacnostFaziEn: '90,3%', metodTacnostFaziOba: '90,0%',
        metodTacnostMrezaEn: '93,5%', metodTacnostMrezaOba: '92,9%',
        metodF1FaziEn: '0,697', metodF1FaziOba: '0,704',
        metodF1MrezaEn: '0,770', metodF1MrezaOba: '0,736',
        metodMrezaFusnota: 'Izdvojeni test skup SpamAssassin: 750 email poruka, 125 spam poruka. Srpski korpus je delimično sintetički. Srpske vrednosti ne predstavljaju tačnost u produkciji.',
        metodPravilaNaslov: 'Pravila i ograničenja',
        metodPravilaTekst: 'Sistem ima 19 pravila: 4 legitimna, 11 sumnjivih i 4 spam. Svako pravilo ograničava svoj izlazni skup na jačinu aktivacije. Sistem zadržava najveću vrednost u svakoj tački.',
        metodOgranicenje1: 'Četiri signala su namenjena email porukama. Za SMS i čet poruke ocena nije pouzdana.',
        metodOgranicenje2: 'Različiti emailovi mogu dobiti istu ocenu kada fazi skupovi ne mogu da ih razlikuju.',
        metodOgranicenje3: 'Granice fazi skupova kalibrisane su na ručno označenim primerima. Sve prikazane metrike dobijene su na izdvojenim podacima.',
        metodOgranicenje4: 'Srpski test skup je delimično mašinski preveden, a delimično sintetički.',
        metodSpektarOpis: 'Šest izlaznih skupova u tri opsega: 2 legitimna (0–22), 3 sumnjiva (22–72), 1 spam (72–100).',
        cipPravila: '19 pravila', cipSkupovi: 'trimf / trapmf', cipTeziste: 'težište', cipMreza: 'neuronska mreža daje samo rečnik',
        metodNapomena: 'Kategorija dolazi iz iste defazifikovane vrednosti koju prikazuje ekran. Ocena i kategorija ne mogu da se raziđu.',
        sada: 'upravo sad', preMin: 'min', preH: 'h',
        kopirano: 'Kopirano',
        kategorije: { LEGITIMAN: 'LEGITIMAN', SUMNJIVO: 'SUMNJIVO', SPAM: 'SPAM' },
        opisiKategorija: {
            LEGITIMAN: 'Signali ostaju u legitimnom opsegu. Nijedno pravilo ne vuče izlaz ka spamu.',
            SUMNJIVO: 'Agregirani izlaz je u sumnjivom opsegu; nijedno pravilo ne dostiže spam opseg.',
            SPAM: 'Težište pada u spam opseg. Pravila ispod pokazuju šta ga je tamo gurnulo.'
        },
        signali: { kljucne_reci: 'Ključne reči', broj_linkova: 'Linkovi', caps_procenat: 'Velika slova', interpunkcija: 'Interpunkcija' },
        jedinice: { kljucne_reci: '/10', broj_linkova: '/10', caps_procenat: '%', interpunkcija: '%' },
        skupovi: {
            kljucne_zanemarljive: 'zanemarljive', kljucne_zastupljene: 'zastupljene', kljucne_dominantne: 'dominantne',
            linkovi_minimalni: 'minimalni', linkovi_umereni: 'umereni', linkovi_brojni: 'brojni',
            caps_uobicajen: 'uobičajen', caps_poviseni: 'povišen', caps_blago_povisen: 'blago povišen', caps_agresivan: 'agresivan',
            interpunkcija_retka: 'retka', interpunkcija_blago: 'blaga', interpunkcija_umerena: 'umerena', interpunkcija_agresivna: 'agresivna'
        },
        metaRec: n => n === 1 ? 'reč' : 'reči',
        metaLink: n => n === 1 ? 'link' : 'linka',
        metaCaps: 'velikih slova'
    }
};

/* ---------- state ------------------------------------------------ */

function ucitajLokalno(kljuc, podrazumevano) {
    try { return localStorage.getItem(kljuc) || podrazumevano; } catch (greska) { return podrazumevano; }
}

function sacuvajLokalno(kljuc, vrednost) {
    try { localStorage.setItem(kljuc, vrednost); } catch (greska) { /* ignorisi */ }
}

const smanjenoKretanje = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const jeMac = /Mac|iPhone|iPad/.test(navigator.platform || navigator.userAgent);

let jezik = ucitajLokalno('fg-prototip-jezik', 'en');
let tema = ucitajLokalno('fg-prototip-tema-v2', 'dark');
let nacinRecnika = ucitajLokalno('fg-prototip-recnik', 'kombinovano');
let trenutniRezultat = null;
let trenutniPogled = 'zasto';
let istorija = [];
let analizaUToku = false;

function t() { return prevodi[jezik] || prevodi.en; }

function pobjegni(tekst) {
    return String(tekst == null ? '' : tekst)
        .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
}

function bojaKategorije(kategorija) {
    if (kategorija === 'SPAM') return 'var(--spam)';
    if (kategorija === 'SUMNJIVO') return 'var(--sumnjivo)';
    return 'var(--legit)';
}

function formatirajBroj(vrednost) {
    const zaokruzeno = Math.round(vrednost * 10) / 10;
    return Number.isInteger(zaokruzeno) ? String(zaokruzeno) : zaokruzeno.toFixed(1).replace('.', jezik === 'sr' ? ',' : '.');
}

function formatirajProcenat(vrednost) {
    const broj = Number(vrednost);
    const zaokruzeno = Number.isFinite(broj) ? Math.round(broj * 10) / 10 : 0;
    return zaokruzeno.toFixed(1).replace('.', jezik === 'sr' ? ',' : '.');
}

function formatirajDva(vrednost) {
    const broj = Number(vrednost);
    const zaokruzeno = Number.isFinite(broj) ? broj : 0;
    return zaokruzeno.toFixed(2).replace('.', jezik === 'sr' ? ',' : '.');
}
/* ---------- fuzzy sets (loaded from /skupovi) -------------------- */

let SKUPOVI_ULAZA = {};
let SKUPOVI_IZLAZA = [];
let skupoviUcitani = null;

async function ucitajSkupove() {
    if (skupoviUcitani) return skupoviUcitani;
    skupoviUcitani = fetch('/skupovi')
        .then(odgovor => {
            if (!odgovor.ok) throw new Error('skupovi');
            return odgovor.json();
        })
        .then(podaci => {
            SKUPOVI_ULAZA = podaci.ulazi || {};
            SKUPOVI_IZLAZA = podaci.izlazi || podaci.skupovi || [];
            return podaci;
        })
        .catch(greska => {
            skupoviUcitani = null;
            throw greska;
        });
    return skupoviUcitani;
}

/* ---------- sample messages -------------------------------------- */

const UZORCI = {
    legitiman: [
        {
            posaljilac: 'Mina Petrović',
            tema: 'Re: sync tomorrow',
            tekst: 'Hi, just wanted to confirm our meeting tomorrow at 3pm. Let me know if that works for you.'
        },
        {
            posaljilac: 'Marko Jovanović',
            tema: 'Sastanak sutra',
            tekst: 'Zdravo, potvrđujem sastanak sutra u 15 časova. Vidimo se u kancelariji.'
        }
    ],
    sumnjiv: [
        {
            posaljilac: 'Dostava',
            tema: 'Vaš paket čeka',
            tekst: 'Poštovani, vaš paket čeka na preuzimanju. Proverite adresu dostave na http://posta-dostava.net ili http://status-paketa.com kako bi isporuka bila završena.'
        },
        {
            posaljilac: 'Dear sir',
            tema: 'Mortgage settlement',
            tekst: 'Dear sir, regarding your mortgage, kindly review the attached settlement.'
        }
    ],
    prevara: [
        {
            posaljilac: 'Account Security',
            tema: 'Action required: your account will be closed',
            tekst: 'URGENT: Your account will be CLOSED unless you ACT NOW! Click http://scam-alert.net to prevent your account from being CLOSED. Verify your details today.'
        },
        {
            posaljilac: 'Nagradna igra',
            tema: 'Čestitamo, osvojili ste!',
            tekst: 'Čestitamo! Osvojili ste besplatnu nagradu. Kliknite ovde da preuzmete nagradu.'
        }
    ]
};

/* ---------- fuzzy math ------------------------------------------- */

function trimf(x, a, b, c) {
    if (x <= a || x >= c) return 0;
    if (x === b) return 1;
    return x < b ? (x - a) / (b - a) : (c - x) / (c - b);
}

function trapmf(x, a, b, c, d) {
    if (x < a || x > d) return 0;
    if (x >= b && x <= c) return 1;
    if (x < b) return a === b ? 1 : (x - a) / (b - a);
    return d === c ? 1 : (d - x) / (d - c);
}

function pripadnost(tip, params, x) {
    return tip === 'trimf' ? trimf(x, ...params) : trapmf(x, ...params);
}

/* ---------- text analysis ---------------------------------------- */

const UZORAK_LINKA = /\b(?:https?:\/\/|hxxps?:\/\/|www\.)[^\s<>"']+/gi;
const UZORAK_CAPS = /\b[A-ZČĆŠŽĐ]{3,}\b/g;
const UZORAK_INTERPUNKCIJA = /[!?]+/g;
async function izracunajRezultat(tekst, nacin) {
    await ucitajSkupove();

    const odgovor = await fetch('/analiziraj', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tekst, recnik: nacin })
    });

    const podaci = await odgovor.json();
    if (!odgovor.ok) {
        throw new Error(podaci.greska || t().greskaMreza);
    }

    const objasnjenje = podaci.objasnjenje || {};
    const ulazi = objasnjenje.ulazi || {};

    const MAPA_SKUPOVA = {
        kljucne_reci: {
            zanemarljive: 'kljucne_zanemarljive',
            zastupljene: 'kljucne_zastupljene',
            dominantne: 'kljucne_dominantne'
        },
        broj_linkova: {
            minimalni: 'linkovi_minimalni',
            umereni: 'linkovi_umereni',
            brojni: 'linkovi_brojni'
        },
        caps_procenat: {
            uobicajen: 'caps_uobicajen',
            poviseni: 'caps_poviseni',
            blago: 'caps_blago_povisen',
            agresivan: 'caps_agresivan'
        },
        interpunkcija: {
            retka: 'interpunkcija_retka',
            blago: 'interpunkcija_blago',
            umerena: 'interpunkcija_umerena',
            agresivna: 'interpunkcija_agresivna'
        }
    };

    const mu = {};
    Object.keys(ulazi).forEach(kljuc => {
        const mapa = MAPA_SKUPOVA[kljuc] || {};
        mu[kljuc] = {};
        Object.keys(ulazi[kljuc].pripadnosti || {}).forEach(ime => {
            mu[kljuc][mapa[ime] || ime] = ulazi[kljuc].pripadnosti[ime];
        });
    });

    const linkovi = [];
    for (let i = 0; i < Number(podaci.broj_linkova); i++) linkovi.push('');

    const vrednosti = {
        kljucne_reci: podaci.kljucne_reci,
        broj_linkova: podaci.broj_linkova,
        caps_procenat: podaci.caps_procenat,
        interpunkcija: podaci.interpunkcija
    };

    const aktivnaPravila = (objasnjenje.aktivna_pravila || []).map(pravilo => ({
        naziv: pravilo.pravilo,
        jacina: pravilo.jacina,
        kategorija: pravilo.kategorija,
        uslov_sr: pravilo.uslov_sr,
        uslov_en: pravilo.uslov_en
    }));

    return {
        tekst,
        vidljivi: objasnjenje.tekst || tekst,
        vrednosti,
        pogodjene: objasnjenje.pokrivene_reci || [],
        oznake: objasnjenje.oznake || [],
        linkovi,
        mu,
        pravila: aktivnaPravila,
        skor: podaci.spam_score,
        kategorija: podaci.kategorija,
        aktivnaPravila
    };
}

/* ---------- spectrum drawing ------------------------------------- */

function skupSaNajvecomPripadnoscu(skor) {
    let najjaci = SKUPOVI_IZLAZA[0];
    let najveca = -1;
    SKUPOVI_IZLAZA.forEach(skup => {
        const mu = pripadnost(skup.tip, skup.params, skor);
        if (mu > najveca) { najveca = mu; najjaci = skup; }
    });
    return najjaci;
}

function nacrtajSpektar(svg, skor, opcije) {
    if (!svg) return;
    const podesavanja = opcije || {};
    const priguseno = !!podesavanja.priguseno;
    const saIglom = typeof skor === 'number' && !priguseno;
    const aktivni = saIglom ? skupSaNajvecomPripadnoscu(skor) : null;

    const sirina = 420;
    const leva = 2;
    const desna = 418;
    const osnova = 78;
    const vrh = 7;
    const xZa = vrednost => leva + (vrednost / 100) * (desna - leva);
    const yZa = mu => osnova - mu * (osnova - vrh);

    const putanja = skup => {
        let tacke = '';
        for (let vrednost = 0; vrednost <= 100; vrednost += 1) {
            tacke += `${vrednost === 0 ? 'M' : 'L'} ${xZa(vrednost).toFixed(2)} ${yZa(pripadnost(skup.tip, skup.params, vrednost)).toFixed(2)} `;
        }
        return tacke + `L ${desna} ${osnova} L ${leva} ${osnova} Z`;
    };

    const delovi = [`<line class="spektar-osnova" x1="${leva}" y1="${osnova}" x2="${desna}" y2="${osnova}"/>`];

    if (!priguseno) {
        // Granice kategorija iz izlaznih skupova: 0–22 legitimno, 22–72
        // sumnjivo, 72–100 spam. Isti brojevi se koriste u opisu spektra.
        [22, 72].forEach(granica => {
            const x = xZa(granica).toFixed(2);
            delovi.push(`<line class="spektar-granica" x1="${x}" y1="${vrh}" x2="${x}" y2="${osnova}"/>`);
            delovi.push(`<line class="spektar-tick" x1="${x}" y1="${osnova}" x2="${x}" y2="${osnova + 4}"/>`);
        });
    }

    const redosled = SKUPOVI_IZLAZA.filter(skup => !aktivni || skup.ime !== aktivni.ime);
    if (aktivni) redosled.push(aktivni);

    redosled.forEach(skup => {
        const aktivan = !!aktivni && skup.ime === aktivni.ime;
        const boja = priguseno ? 'var(--tekst-3)' : bojaKategorije(skup.kategorija);
        delovi.push(
            `<path d="${putanja(skup)}" fill="${boja}" fill-opacity="${aktivan ? 0.14 : 0.045}" ` +
            `stroke="${boja}" stroke-opacity="${aktivan ? 0.9 : 0.3}" stroke-width="${aktivan ? 1.4 : 1}" stroke-linejoin="round"/>`
        );
    });

    if (saIglom) {
        const x = xZa(Math.max(0, Math.min(100, skor))).toFixed(2);
        delovi.push(`<circle cx="${x}" cy="${osnova}" r="7" fill="var(--tekst)" opacity="0.07"/>`);
        delovi.push(`<line class="spektar-igla" x1="${x}" y1="${vrh - 5}" x2="${x}" y2="${osnova}"/>`);
        delovi.push(`<circle class="spektar-tacka" cx="${x}" cy="${osnova}" r="2.6"/>`);
    }

    svg.innerHTML = delovi.join('');
}

/* ---------- result rendering ------------------------------------- */

function animirajSkor(konacan) {
    const element = document.getElementById('skor-broj');
    const cilj = Number(konacan) || 0;

    if (smanjenoKretanje) { element.textContent = formatirajProcenat(cilj); return; }

    const pocetak = performance.now();
    const trajanje = 540;

    function korak(sada) {
        const napredak = Math.min(1, (sada - pocetak) / trajanje);
        const ublazeno = 1 - Math.pow(1 - napredak, 3);
        element.textContent = formatirajProcenat(napredak < 1 ? cilj * ublazeno : cilj);
        if (napredak < 1) requestAnimationFrame(korak);
    }

    requestAnimationFrame(korak);
}

function prikaziRezultat(rezultat, opcije) {
    const podesavanja = opcije || {};
    trenutniRezultat = rezultat;

    document.getElementById('prazno').hidden = true;
    const rezultatElement = document.getElementById('rezultat');
    rezultatElement.hidden = false;
    rezultatElement.classList.remove('ulazi');
    if (!smanjenoKretanje) {
        void rezultatElement.offsetWidth;
        rezultatElement.classList.add('ulazi');
    }

    const boja = bojaKategorije(rezultat.kategorija);
    const status = document.getElementById('status');
    status.hidden = false;
    status.style.setProperty('--boja', boja);
    document.getElementById('status-tekst').textContent = t().kategorije[rezultat.kategorija];

    const kopiraj = document.getElementById('kopiraj-dugme');
    kopiraj.hidden = false;
    kopiraj.disabled = false;

    document.getElementById('skor-opis').textContent = t().opisiKategorija[rezultat.kategorija];
    if (podesavanja.animiraj === false) {
        document.getElementById('skor-broj').textContent = formatirajProcenat(rezultat.skor);
    } else {
        animirajSkor(rezultat.skor);
    }

    nacrtajSpektar(document.getElementById('spektar'), rezultat.skor);

    renderSignali(rezultat);
    renderPogled();
    renderIstorija();
}

function renderSignali(rezultat) {
    const redosled = ['kljucne_reci', 'broj_linkova', 'caps_procenat', 'interpunkcija'];

    document.getElementById('signali').innerHTML = redosled.map(kljuc => {
        const vrednost = rezultat.vrednosti[kljuc];
        const pripadnosti = Object.entries(rezultat.mu[kljuc] || {})
            .sort((prva, druga) => druga[1] - prva[1]);
        const [imeSkupa, dominantaMu] = pripadnosti[0] || [null, 0];
        const definicije = SKUPOVI_ULAZA[kljuc] || [];
        const dominantan = definicije.find(skup => skup.ime === imeSkupa) || { ime: imeSkupa || '—', kategorija: 'SUMNJIVO' };
        const maksimum = (kljuc === 'kljucne_reci' || kljuc === 'broj_linkova') ? 10 : 100;
        const sirina = Math.max(vrednost > 0 ? 2 : 0, Math.min(100, (vrednost / maksimum) * 100));

        return `<div class="signal">
            <div class="signal-vrh">
                <span class="signal-naziv">${pobjegni(t().signali[kljuc])}</span>
                <span class="signal-skup">${pobjegni(t().skupovi[dominantan.ime] || dominantan.ime)} <b>${Number(dominantaMu).toFixed(2)}</b></span>
            </div>
            <div class="signal-vrednost"><b>${pobjegni(formatirajBroj(vrednost))}</b><span>${pobjegni(t().jedinice[kljuc])}</span></div>
            <div class="signal-traka" style="--boja: ${bojaKategorije(dominantan.kategorija)}"><i style="width:${sirina}%"></i></div>
        </div>`;
    }).join('');
}

/* ---------- explanation panels ----------------------------------- */

function renderPogled() {
    const kontejner = document.getElementById('pogled-sadrzaj');
    if (!trenutniRezultat) { kontejner.innerHTML = ''; return; }

    if (trenutniPogled === 'ulazi') {
        kontejner.innerHTML = napraviUlaze(trenutniRezultat);
    } else if (trenutniPogled === 'pravila') {
        kontejner.innerHTML = napraviPravila(trenutniRezultat);
    } else {
        kontejner.innerHTML = napraviZasto(trenutniRezultat);
    }

    document.querySelectorAll('[data-pogled]').forEach(dugme => {
        dugme.setAttribute('aria-selected', dugme.dataset.pogled === trenutniPogled ? 'true' : 'false');
    });
}

function napraviZasto(rezultat) {
    const elementi = [];
    const pregled = napraviPregled(rezultat);

    elementi.push(`<p class="pogled-naslov">${pobjegni(t().doprinosiNaslov)}</p>`);
    elementi.push(napraviDoprinose(rezultat));

    elementi.push(`<p class="pogled-naslov" style="margin-top:13px">${pobjegni(t().pronasli)}</p>`);
    elementi.push(`<div class="pregled">${pregled.html}</div>`);

    if (pregled.kombinacije.size) {
        const redosled = { keyword: 0, link: 1, caps: 2, interpunkcija: 3 };
        const kombinacije = Array.from(pregled.kombinacije).sort((prva, druga) => {
            const prvi = prva.split('+');
            const drugi = druga.split('+');
            return (prvi.length - drugi.length) || (redosled[prvi[0]] - redosled[drugi[0]]);
        });
        elementi.push('<div class="legenda">' + kombinacije.map(kljuc => {
            const tipovi = kljuc.split('+');
            const boje = tipovi.map(bojaTipa);
            const pozadina = boje.length === 1
                ? boje[0]
                : `linear-gradient(90deg, ${boje.map((boja, indeks) =>
                    `${boja} ${(indeks / boje.length) * 100}% ${((indeks + 1) / boje.length) * 100}%`
                ).join(', ')})`;
            return `<span><i style="background:${pozadina}"></i>${pobjegni(tipovi.map(tip => t().legenda[tip]).join(' + '))}</span>`;
        }).join('') + '</div>');
    }

    elementi.push(`<p class="pogled-naslov" style="margin-top:13px">${pobjegni(t().prepoznate)}</p>`);

    if (rezultat.pogodjene.length) {
        elementi.push('<div class="cipovi">' + rezultat.pogodjene.map(stavka => {
            const izvor = stavka.izvor === 'en' ? t().izvorEn
                : stavka.izvor === 'sr' ? t().izvorSr : t().izvorRucni;
            return `<span class="cip" title="${pobjegni(izvor)} · ${formatirajBroj(stavka.tezina)}">` +
                   `${pobjegni(stavka.rec)}${stavka.broj > 1 ? ` <b>×${stavka.broj}</b>` : ''}</span>`;
        }).join('') + '</div>');
    } else {
        elementi.push(`<p class="tiho">${pobjegni(t().nemaPogodaka)}</p>`);
    }

    return elementi.join('');
}

function bojaTipa(tip) {
    if (tip === 'keyword') return 'var(--sumnjivo)';
    if (tip === 'link') return 'var(--link)';
    if (tip === 'caps') return 'var(--spam)';
    return 'var(--ljubicasta)';
}

function napraviDoprinose(rezultat) {
    const redosled = ['kljucne_reci', 'broj_linkova', 'caps_procenat', 'interpunkcija'];
    const tipPoKljucu = {
        kljucne_reci: 'keyword', broj_linkova: 'link',
        caps_procenat: 'caps', interpunkcija: 'interpunkcija'
    };

    return '<div class="doprinosi">' + redosled.map(kljuc => {
        const vrednost = rezultat.vrednosti[kljuc];
        const pripadnosti = rezultat.mu[kljuc] || {};
        const najjaci = Object.keys(pripadnosti).reduce((najbolji, ime) => {
            const mu = Number(pripadnosti[ime]) || 0;
            return mu > najbolji.mu ? { ime, mu } : najbolji;
        }, { ime: '', mu: -1 });
        const skup = najjaci.ime ? (t().skupovi[najjaci.ime] || najjaci.ime) : '—';
        const mu = najjaci.mu >= 0 ? formatirajDva(najjaci.mu) : '—';

        return `<div class="doprinos" style="--boja:${bojaTipa(tipPoKljucu[kljuc])}">
            <span class="doprinos-signal"><i></i>${pobjegni(t().signali[kljuc])}</span>
            <span class="doprinos-vrednost">${pobjegni(formatirajBroj(vrednost))}<small>${pobjegni(t().jedinice[kljuc])}</small></span>
            <span class="doprinos-skup">${pobjegni(skup)} <b>${pobjegni(mu)}</b></span>
        </div>`;
    }).join('') + '</div>';
}

function kljucOznake(skup) {
    return ['keyword', 'link', 'caps', 'interpunkcija'].filter(tip => skup.has(tip)).join('+');
}

function izracunajOznake(rezultat) {
    const tekst = rezultat.vidljivi || '';
    const oznake = Array.from({ length: tekst.length }, () => null);
    const dodaj = (od, do_, tip) => {
        const pocetak = Math.max(0, od);
        const kraj = Math.min(tekst.length, do_);
        for (let indeks = pocetak; indeks < kraj; indeks += 1) {
            if (/\s/.test(tekst[indeks])) continue;
            if (!oznake[indeks]) oznake[indeks] = new Set();
            oznake[indeks].add(tip);
        }
    };

    (rezultat.pogodjene || []).forEach(stavka => {
        (stavka.pozicije || []).forEach(pozicija => dodaj(pozicija[0], pozicija[1], 'keyword'));
    });

    [['link', UZORAK_LINKA], ['caps', UZORAK_CAPS], ['interpunkcija', UZORAK_INTERPUNKCIJA]].forEach(([tip, uzorak]) => {
        Array.from(tekst.matchAll(uzorak)).slice(0, 50).forEach(poklapanje => {
            dodaj(poklapanje.index, poklapanje.index + poklapanje[0].length, tip);
        });
    });

    const kombinacije = new Set();
    oznake.forEach(skup => {
        if (!skup || !skup.size) return;
        kombinacije.add(kljucOznake(skup));
    });

    return { tekst, oznake, kombinacije };
}

function napraviPregled(rezultat) {
    const { tekst, oznake, kombinacije } = izracunajOznake(rezultat);
    let html = '';
    let indeks = 0;

    while (indeks < tekst.length) {
        const skup = oznake[indeks];
        if (!skup || !skup.size) {
            let kraj = indeks + 1;
            while (kraj < tekst.length && (!oznake[kraj] || !oznake[kraj].size)) kraj += 1;
            html += pobjegni(tekst.slice(indeks, kraj));
            indeks = kraj;
            continue;
        }

        const kljuc = kljucOznake(skup);
        let kraj = indeks + 1;
        while (kraj < tekst.length && oznake[kraj] && kljucOznake(oznake[kraj]) === kljuc) kraj += 1;

        const tipovi = kljuc.split('+');
        const klase = tipovi.map(tip => `obj-mark--${tip}`).join(' ');
        const opis = tipovi.map(tip => t().legenda[tip]).join(' + ');
        html += `<mark class="obj-mark ${klase}" title="${pobjegni(opis)}">${pobjegni(tekst.slice(indeks, kraj))}</mark>`;
        indeks = kraj;
    }

    return { html: html || pobjegni(tekst), kombinacije };
}

function napraviUlaze(rezultat) {
    const redosled = ['kljucne_reci', 'broj_linkova', 'caps_procenat', 'interpunkcija'];

    const redovi = redosled.map(kljuc => {
        const vrednost = rezultat.vrednosti[kljuc];
        const pripadnosti = Object.keys(rezultat.mu[kljuc])
            .map(imeSkupa => ({ ime: imeSkupa, mu: rezultat.mu[kljuc][imeSkupa] }))
            .filter(stavka => stavka.mu > 0.05)
            .sort((prva, druga) => druga.mu - prva.mu)
            .map(stavka => `${t().skupovi[stavka.ime]} ${stavka.mu.toFixed(2)}`)
            .join(' · ');

        return `<div class="ulaz">
            <span class="ulaz-naziv">${pobjegni(t().signali[kljuc])}</span>
            <span class="ulaz-vrednost">${pobjegni(formatirajBroj(vrednost))}${pobjegni(t().jedinice[kljuc])}</span>
            <span class="ulaz-skupovi">${pripadnosti ? pobjegni(pripadnosti) : '—'}</span>
        </div>`;
    });

    return `<p class="pogled-naslov">${pobjegni(t().ulaziNaslov)}</p>${redovi.join('')}`;
}

function napraviPravila(rezultat) {
    const aktivna = rezultat.aktivnaPravila.slice().sort((prvo, drugo) => prvo.naziv.localeCompare(drugo.naziv));
    const naslov = `<p class="pogled-naslov">${pobjegni(t().pravilaNaslov)}<span>${aktivna.length}</span></p>`;

    if (!aktivna.length) {
        return naslov + `<p class="tiho">${pobjegni(t().nemaPogodaka)}</p>`;
    }

    const stavke = aktivna.map(pravilo => {
        const opis = (jezik === 'sr' ? pravilo.uslov_sr : pravilo.uslov_en) || '';
        const boja = bojaKategorije(pravilo.kategorija);
        return `<li class="pravilo" style="--boja: ${boja}">
            <div class="pravilo-vrh">
                <span class="pravilo-id">${pravilo.naziv}</span>
                <span class="pravilo-uslov">${pobjegni(opis)}</span>
            </div>
            <div class="pravilo-dno">
                <div class="pravilo-traka"><i style="width:${Math.max(2, pravilo.jacina * 100)}%"></i></div>
                <span class="pravilo-kat">${pobjegni(t().kategorije[pravilo.kategorija])}</span>
                <span class="pravilo-jacina">${pravilo.jacina.toFixed(2)}</span>
            </div>
        </li>`;
    }).join('');

    return naslov + `<ul class="pravila" style="list-style:none;margin:0;padding:0">${stavke}</ul>`;
}

/* ---------- recent checks ---------------------------------------- */

function relativnoVreme(vreme) {
    const minuti = Math.floor((Date.now() - vreme) / 60000);
    if (minuti < 1) return t().sada;
    if (minuti < 60) return `${minuti} ${t().preMin}`;
    return `${Math.floor(minuti / 60)} ${t().preH}`;
}

function renderIstorija() {
    const lista = document.getElementById('istorija-lista');

    if (!istorija.length) {
        lista.innerHTML = `<p class="istorija-prazno">${pobjegni(t().nemaIstorije)}</p>`;
        return;
    }

    lista.innerHTML = istorija.map((stavka, indeks) => {
        const rezultat = stavka.rezultat;
        const kategorija = rezultat.kategorija;
        const boja = bojaKategorije(kategorija);
        const aktivan = !!trenutniRezultat && stavka.tekst === trenutniRezultat.tekst;
        const brojReci = Math.round(rezultat.vrednosti.kljucne_reci);
        const brojLinkova = rezultat.vrednosti.broj_linkova;
        const caps = Math.round(rezultat.vrednosti.caps_procenat);
        const meta = `${brojReci} ${t().metaRec(brojReci)} · ${brojLinkova} ${t().metaLink(brojLinkova)} · ${caps}% ${t().metaCaps}`;
        const pregled = stavka.tekst.replace(/\s+/g, ' ').slice(0, 100);

        return `<button class="istorija-red" type="button" data-indeks="${indeks}" aria-current="${aktivan ? 'true' : 'false'}" style="--boja: ${boja}">
            <span class="istorija-tacka"></span>
            <span class="istorija-tekst">
                <span class="istorija-pregled">${pobjegni(pregled)}</span>
                <span class="istorija-meta">${pobjegni(meta)}</span>
            </span>
            <span class="istorija-skore">${formatirajProcenat(rezultat.skor)}%</span>
            <span class="istorija-vreme">${pobjegni(relativnoVreme(stavka.vreme))}</span>
        </button>`;
    }).join('');
}

function dodajUIstoriju(tekst, posaljilac, tema, rezultat) {
    istorija = istorija.filter(stavka => stavka.tekst !== tekst);
    istorija.unshift({ tekst, posaljilac, tema, rezultat, vreme: Date.now() });
    istorija = istorija.slice(0, 6);
    renderIstorija();
}

function azurirajUIstoriji(tekst, rezultat) {
    const stavka = istorija.find(unos => unos.tekst === tekst);
    if (stavka) {
        stavka.rezultat = rezultat;
        renderIstorija();
    }
}

function ucitajIzIstorije(indeks) {
    const stavka = istorija[indeks];
    if (!stavka) return;

    document.getElementById('tekst').value = stavka.tekst;
    document.getElementById('polje-posaljilac').value = stavka.posaljilac || '';
    document.getElementById('polje-tema').value = stavka.tema || '';
    azurirajBrojZnakova();
    skloniGresku();
    prikaziRezultat(stavka.rezultat, { animiraj: true });
}

/* ---------- composer interactions -------------------------------- */

function azurirajBrojZnakova() {
    const tekst = document.getElementById('tekst').value;
    document.getElementById('broj-znakova').textContent = String(tekst.length);
}

function popuniPolja(uzorak) {
    document.getElementById('polje-posaljilac').value = uzorak.posaljilac;
    document.getElementById('polje-tema').value = uzorak.tema;
    document.getElementById('tekst').value = uzorak.tekst;
    azurirajBrojZnakova();
    skloniGresku();
}

function prikaziGresku(poruka) {
    const greska = document.getElementById('greska');
    greska.textContent = poruka;
    greska.hidden = false;
}

function skloniGresku() {
    document.getElementById('greska').hidden = true;
}

function vratiPraznoStanje() {
    trenutniRezultat = null;
    document.getElementById('rezultat').hidden = true;
    document.getElementById('prazno').hidden = false;
    document.getElementById('status').hidden = true;
    document.getElementById('kopiraj-dugme').hidden = true;
    renderIstorija();
}

function pokreniAnalizu() {
    if (analizaUToku) return;

    const tekst = document.getElementById('tekst').value.trim();
    if (!tekst) {
        prikaziGresku(t().greskaPrazno);
        document.getElementById('tekst').focus();
        return;
    }

    skloniGresku();
    analizaUToku = true;

    const dugme = document.getElementById('pokreni-dugme');
    const natpis = document.getElementById('pokreni-tekst');
    dugme.disabled = true;
    natpis.textContent = t().analiziram;

    window.setTimeout(async () => {
        try {
            const rezultat = await izracunajRezultat(tekst, nacinRecnika);
            prikaziRezultat(rezultat, { animiraj: true });
            dodajUIstoriju(
                tekst,
                document.getElementById('polje-posaljilac').value.trim(),
                document.getElementById('polje-tema').value.trim(),
                rezultat
            );
        } catch (greska) {
            prikaziGresku(greska.message || t().greskaMreza);
        } finally {
            natpis.textContent = t().pokreni;
            dugme.disabled = false;
            analizaUToku = false;
        }
    }, smanjenoKretanje ? 140 : 360);
}

let primeriKes = { en: null, sr: null };

async function ucitajPrimere(jezikPrimera) {
    if (!primeriKes[jezikPrimera]) {
        const odgovor = await fetch('/primeri-svi?jezik=' + jezikPrimera);
        const podaci = await odgovor.json();
        primeriKes[jezikPrimera] = podaci.primeri || [];
    }
    return primeriKes[jezikPrimera];
}

async function izaberiUzorak(kljuc) {
    try {
        const lista = await ucitajPrimere(jezik);
        const grupa = lista.filter(primer => primer.kategorija === kljuc);
        if (!grupa.length) return;

        const uzorak = grupa[Math.floor(Math.random() * grupa.length)];
        popuniPolja(uzorak);

        const rezultat = await izracunajRezultat(uzorak.tekst, nacinRecnika);
        prikaziRezultat(rezultat, { animiraj: true });
        dodajUIstoriju(uzorak.tekst, uzorak.posaljilac, uzorak.tema, rezultat);
    } catch (greska) {
        prikaziGresku(greska.message || t().greskaMreza);
    }
}

async function izaberiRandom() {
    try {
        const lista = await ucitajPrimere(jezik);
        if (!lista.length) return;

        const uzorak = lista[Math.floor(Math.random() * lista.length)];
        popuniPolja(uzorak);

        const rezultat = await izracunajRezultat(uzorak.tekst, nacinRecnika);
        prikaziRezultat(rezultat, { animiraj: true });
        dodajUIstoriju(uzorak.tekst, uzorak.posaljilac, uzorak.tema, rezultat);
    } catch (greska) {
        prikaziGresku(greska.message || t().greskaMreza);
    }
}

function postaviRecnik(nacin) {
    nacinRecnika = nacin;
    sacuvajLokalno('fg-prototip-recnik', nacin);

    document.querySelectorAll('[data-recnik]').forEach(dugme => {
        dugme.setAttribute('aria-pressed', dugme.dataset.recnik === nacin ? 'true' : 'false');
        dugme.classList.toggle('aktivan', dugme.dataset.recnik === nacin);
    });

    const tekst = document.getElementById('tekst').value.trim();
    if (tekst && trenutniRezultat) {
        izracunajRezultat(tekst, nacin).then(rezultat => {
            prikaziRezultat(rezultat, { animiraj: false });
            azurirajUIstoriji(tekst, rezultat);
        }).catch(greska => {
            prikaziGresku(greska.message || t().greskaMreza);
        });
    }
}

function postaviPogled(pogled) {
    trenutniPogled = pogled;
    renderPogled();
}

function ocistiProveru() {
    document.getElementById('tekst').value = '';
    document.getElementById('polje-posaljilac').value = '';
    document.getElementById('polje-tema').value = '';
    azurirajBrojZnakova();
    skloniGresku();
    vratiPraznoStanje();
    document.getElementById('tekst').focus();
}

/* ---------- copy -------------------------------------------------- */

function prikaziObavestenje(poruka) {
    const obavestenje = document.getElementById('obavestenje');
    document.getElementById('obavestenje-tekst').textContent = poruka;
    obavestenje.classList.add('vidljivo');
    window.clearTimeout(prikaziObavestenje.rok);
    prikaziObavestenje.rok = window.setTimeout(() => obavestenje.classList.remove('vidljivo'), 1800);
}

async function kopirajRezultat() {
    if (!trenutniRezultat) return;
    const rezultat = trenutniRezultat;
    const recnik = t();
    const linije = [
        'Fuzzy Guard',
        `${recnik.procena}: ${formatirajProcenat(rezultat.skor)}% (${recnik.kategorije[rezultat.kategorija]})`,
        `${recnik.signali.kljucne_reci}: ${formatirajBroj(rezultat.vrednosti.kljucne_reci)}/10 | ` +
        `${recnik.signali.broj_linkova}: ${rezultat.vrednosti.broj_linkova}/10 | ` +
        `${recnik.signali.caps_procenat}: ${formatirajBroj(rezultat.vrednosti.caps_procenat)}% | ` +
        `${recnik.signali.interpunkcija}: ${formatirajBroj(rezultat.vrednosti.interpunkcija)}%`
    ];

    if (rezultat.pogodjene.length) {
        linije.push(`${recnik.prepoznate}: ${rezultat.pogodjene.map(stavka => stavka.rec).join(', ')}`);
    }
    if (rezultat.aktivnaPravila.length) {
        linije.push(`${recnik.pravilaNaslov}: ${rezultat.aktivnaPravila.map(pravilo => `${pravilo.naziv} (${pravilo.jacina.toFixed(2)})`).join(', ')}`);
    }

    const sadrzaj = linije.join('\n');
    let uspelo = false;

    try {
        await navigator.clipboard.writeText(sadrzaj);
        uspelo = true;
    } catch (greska) {
        const polje = document.createElement('textarea');
        polje.value = sadrzaj;
        polje.style.position = 'fixed';
        polje.style.opacity = '0';
        document.body.appendChild(polje);
        polje.select();
        try { uspelo = document.execCommand('copy'); } catch (drugaGreska) { uspelo = false; }
        document.body.removeChild(polje);
    }

    if (uspelo) prikaziObavestenje(t().kopirano);
}

/* ---------- language and theme ------------------------------------ */

function primeniTemu() {
    document.documentElement.dataset.theme = tema;
    const dugme = document.getElementById('tema-dugme');
    dugme.setAttribute('aria-label', tema === 'dark' ? t().temaSvetla : t().temaTamna);
    sacuvajLokalno('fg-prototip-tema-v2', tema);
}

function promeniTemu() {
    tema = tema === 'dark' ? 'light' : 'dark';
    primeniTemu();
}

function primeniJezik() {
    const recnik = t();
    document.documentElement.lang = jezik;

    document.querySelectorAll('[data-i18n]').forEach(element => {
        const kljuc = element.getAttribute('data-i18n');
        if (recnik[kljuc] !== undefined) element.textContent = recnik[kljuc];
    });


    document.querySelectorAll('[data-i18n-placeholder]').forEach(element => {
        const kljuc = element.getAttribute('data-i18n-placeholder');
        if (recnik[kljuc] !== undefined) element.placeholder = recnik[kljuc];
    });

    document.querySelectorAll('[data-i18n-aria]').forEach(element => {
        const kljuc = element.getAttribute('data-i18n-aria');
        if (recnik[kljuc] !== undefined) element.setAttribute('aria-label', recnik[kljuc]);
    });

    const jezikDugme = document.getElementById('jezik-dugme');
    jezikDugme.textContent = recnik.jezik;
    jezikDugme.setAttribute('aria-label', recnik.jezikNaziv);

    const kopiraj = document.getElementById('kopiraj-dugme');
    kopiraj.setAttribute('aria-label', recnik.kopiraj);
    kopiraj.title = recnik.kopiraj;

    document.getElementById('precica').textContent = jeMac ? '⌘↵' : 'Ctrl ↵';

    primeniTemu();

    if (trenutniRezultat) {
        prikaziRezultat(trenutniRezultat, { animiraj: false });
    } else {
        renderIstorija();
    }
}

function promeniJezik() {
    jezik = jezik === 'sr' ? 'en' : 'sr';
    sacuvajLokalno('fg-prototip-jezik', jezik);
    primeniJezik();
}

/* ---------- method sheet ------------------------------------------ */

async function otvoriMetod() {
    const dijalog = document.getElementById('metod');
    try { await ucitajSkupove(); } catch (greska) { /* spektar ostaje prazan */ }
    nacrtajSpektar(document.getElementById('spektar-metod'), null);
    if (!dijalog.open) dijalog.showModal();
}

function zatvoriMetod() {
    const dijalog = document.getElementById('metod');
    if (dijalog.open) dijalog.close();
}

/* ---------- wiring ------------------------------------------------ */

function poveziDogadjaje() {
    document.getElementById('tema-dugme').addEventListener('click', promeniTemu);
    document.getElementById('jezik-dugme').addEventListener('click', promeniJezik);
    document.getElementById('pokreni-dugme').addEventListener('click', pokreniAnalizu);
    document.getElementById('ocisti-dugme').addEventListener('click', ocistiProveru);
    document.getElementById('kopiraj-dugme').addEventListener('click', kopirajRezultat);
    document.getElementById('ocisti-istoriju').addEventListener('click', () => { istorija = []; renderIstorija(); });
    document.getElementById('tekst').addEventListener('input', () => {
        azurirajBrojZnakova();
        skloniGresku();
        if (!document.getElementById('tekst').value.trim()) vratiPraznoStanje();
    });

    document.querySelectorAll('[data-uzorak]').forEach(dugme => {
        dugme.addEventListener('click', () => izaberiUzorak(dugme.dataset.uzorak));
    });

    document.getElementById('dugme-random').addEventListener('click', izaberiRandom);

    document.querySelectorAll('[data-recnik]').forEach(dugme => {
        dugme.addEventListener('click', () => postaviRecnik(dugme.dataset.recnik));
    });

    document.querySelectorAll('[data-pogled]').forEach(dugme => {
        dugme.addEventListener('click', () => postaviPogled(dugme.dataset.pogled));
    });

    document.querySelectorAll('[data-otvori-metod]').forEach(dugme => {
        dugme.addEventListener('click', otvoriMetod);
    });
    document.querySelectorAll('[data-zatvori-metod]').forEach(dugme => {
        dugme.addEventListener('click', zatvoriMetod);
    });
    document.getElementById('metod').addEventListener('click', dogadjaj => {
        if (dogadjaj.target === dogadjaj.currentTarget) zatvoriMetod();
    });

    document.getElementById('istorija-lista').addEventListener('click', dogadjaj => {
        const dugme = dogadjaj.target.closest('[data-indeks]');
        if (dugme) ucitajIzIstorije(Number(dugme.dataset.indeks));
    });

    document.addEventListener('keydown', dogadjaj => {
        if ((dogadjaj.metaKey || dogadjaj.ctrlKey) && dogadjaj.key === 'Enter') {
            dogadjaj.preventDefault();
            pokreniAnalizu();
        }
    });
}

async function inicijalizuj() {
    if (!['en', 'sr', 'kombinovano'].includes(nacinRecnika)) nacinRecnika = 'kombinovano';
    if (!['en', 'sr'].includes(jezik)) jezik = 'en';
    if (!['dark', 'light'].includes(tema)) tema = 'dark';

    try { await ucitajSkupove(); } catch (greska) { /* spektar ostaje prazan */ }
    nacrtajSpektar(document.getElementById('spektar-prazno'), null, { priguseno: true });

    document.querySelectorAll('[data-recnik]').forEach(dugme => {
        dugme.setAttribute('aria-pressed', dugme.dataset.recnik === nacinRecnika ? 'true' : 'false');
        dugme.classList.toggle('aktivan', dugme.dataset.recnik === nacinRecnika);
    });

    poveziDogadjaje();
    primeniJezik();

    const uzorakLegitiman = UZORCI.legitiman[0];
    const uzorakSumnjiv = UZORCI.sumnjiv[0];
    const uzorakPrevara = UZORCI.prevara[0];

    try {
        const [rezultatLegitiman, rezultatSumnjiv, rezultatPrevara] = await Promise.all([
            izracunajRezultat(uzorakLegitiman.tekst, nacinRecnika),
            izracunajRezultat(uzorakSumnjiv.tekst, nacinRecnika),
            izracunajRezultat(uzorakPrevara.tekst, nacinRecnika)
        ]);

        istorija = [
            { tekst: uzorakPrevara.tekst, posaljilac: uzorakPrevara.posaljilac, tema: uzorakPrevara.tema, rezultat: rezultatPrevara, vreme: Date.now() },
            { tekst: uzorakSumnjiv.tekst, posaljilac: uzorakSumnjiv.posaljilac, tema: uzorakSumnjiv.tema, rezultat: rezultatSumnjiv, vreme: Date.now() - 9 * 60000 },
            { tekst: uzorakLegitiman.tekst, posaljilac: uzorakLegitiman.posaljilac, tema: uzorakLegitiman.tema, rezultat: rezultatLegitiman, vreme: Date.now() - 24 * 60000 }
        ];

        popuniPolja(uzorakPrevara);
        prikaziRezultat(rezultatPrevara, { animiraj: false });
    } catch (greska) {
        popuniPolja(uzorakPrevara);
        vratiPraznoStanje();
    }
}

inicijalizuj();