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
        recnik: 'Keyword lexicon', rucni: 'Manual', nauceni: 'Learned', kombinovano: 'Combined',
        pokreni: 'Run analysis', analiziram: 'Analyzing…',
        sitno: 'Only the body is scored · nothing leaves this page.',
        greskaPrazno: 'Add some text first.',
        greskaMreza: 'Could not reach the server.',
        procena: 'Assessment', kopiraj: 'Copy result', kopirano: 'Result copied',
        prazno: 'Run an analysis to see the score, the active fuzzy sets and the rules that produced it.',
        skorNatpis: 'Spam suspicion · 0–100',
        osaLegitiman: 'Legitimate', osaSumnjivo: 'Suspicious', osaSpam: 'Spam',
        teziste: 'Centroid',
        tabZasto: 'Why', tabUlazi: 'Inputs', tabPravila: 'Rules',
        pronasli: 'Matched in the text', prepoznate: 'Matched words',
        nemaPogodaka: 'No dictionary hits. Here the score comes from links, capitals and punctuation alone.',
        legenda: { keyword: 'keyword', link: 'link', caps: 'capitals', interpunkcija: 'punctuation' },
        izvorRucni: 'hand dictionary', izvorNauceni: 'learned lexicon',
        ulaziNaslov: 'Memberships above 0.05',
        pravilaNaslov: 'Rules that fired',
        prethodne: 'Recent checks', ocistiSve: 'Clear all', nemaIstorije: 'Nothing checked yet.',
        podnozjeMetod: 'Mamdani inference · min/max · centroid defuzzification',
        kakoRadi: 'How it works', prototip: 'Design prototype',
        metodNatpis: 'Method', metodNaslov: 'A score you can take apart.',
        metodUvod: 'No machine learning decides the verdict. Four extracted signals are fuzzified, evaluated against nineteen rules, aggregated and defuzzified into one number.',
        korak1Naslov: 'Extract', korak1Opis: 'Keywords, links, capitals and punctuation are counted from the body.',
        korak2Naslov: 'Fuzzify', korak2Opis: 'Each value gets a degree of membership in triangular and trapezoidal sets.',
        korak3Naslov: 'Infer', korak3Opis: 'Nineteen Mamdani rules combine memberships with min and max.',
        korak4Naslov: 'Defuzzify', korak4Opis: 'The aggregated output set is reduced to its centroid, 0–100.',
        metodSpektarOpis: 'All six output sets, drawn from the membership functions used in the score.',
        cipPravila: '19 rules', cipSkupovi: 'trimf / trapmf', cipTeziste: 'centroid', cipMreza: 'NN supplies vocabulary only',
        metodNapomena: 'The category is read from the same defuzzified value that is displayed, so the score and the label cannot disagree.',
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
        recnik: 'Rečnik ključnih reči', rucni: 'Ručni', nauceni: 'Naučeni', kombinovano: 'Kombinovano',
        pokreni: 'Pokreni analizu', analiziram: 'Analiziram…',
        sitno: 'Ocenjuje se samo telo poruke · sve ostaje u pregledaču.',
        greskaPrazno: 'Dodajte tekst poruke.',
        greskaMreza: 'Greška u komunikaciji sa serverom.',
        procena: 'Procena', kopiraj: 'Kopiraj rezultat', kopirano: 'Rezultat kopiran',
        prazno: 'Pokrenite analizu da vidite ocenu, aktivne fazi skupove i pravila koja su je proizvela.',
        skorNatpis: 'Sumnjivost na spam · 0–100',
        osaLegitiman: 'Legitimno', osaSumnjivo: 'Sumnjivo', osaSpam: 'Spam',
        teziste: 'Težište',
        tabZasto: 'Zašto', tabUlazi: 'Ulazi', tabPravila: 'Pravila',
        pronasli: 'Pronađeno u tekstu', prepoznate: 'Prepoznate reči',
        nemaPogodaka: 'Nema pogodaka u rečniku. Ocena ovde dolazi samo iz linkova, velikih slova i interpunkcije.',
        legenda: { keyword: 'ključna reč', link: 'link', caps: 'velika slova', interpunkcija: 'interpunkcija' },
        izvorRucni: 'ručni rečnik', izvorNauceni: 'naučeni rečnik',
        ulaziNaslov: 'Pripadnosti iznad 0,05',
        pravilaNaslov: 'Pravila koja su se aktivirala',
        prethodne: 'Prethodne provere', ocistiSve: 'Očisti sve', nemaIstorije: 'Još nema provera.',
        podnozjeMetod: 'Mamdani · min/max · centroid defazifikacija',
        kakoRadi: 'Kako radi', prototip: 'Dizajn prototip',
        metodNatpis: 'Metod', metodNaslov: 'Ocena koju možete da rastavite.',
        metodUvod: 'Odluku ne donosi neuronska mreža. Četiri izdvojena signala se fuzifikuju, proveravaju kroz devetnaest pravila, agregiraju i defazifikuju u jedan broj.',
        korak1Naslov: 'Izdvajanje', korak1Opis: 'Ključne reči, linkovi, velika slova i interpunkcija broje se iz tela poruke.',
        korak2Naslov: 'Fuzifikacija', korak2Opis: 'Svaka vrednost dobija stepen pripadnosti u trouglastim i trapezoidnim skupovima.',
        korak3Naslov: 'Zaključivanje', korak3Opis: 'Devetnaest Mamdani pravila kombinuje pripadnosti kroz min i max.',
        korak4Naslov: 'Defazifikacija', korak4Opis: 'Agregirani izlazni skup svodi se na svoje težište, 0–100.',
        metodSpektarOpis: 'Svih šest izlaznih skupova, iz istih funkcija pripadnosti koje ulaze u ocenu.',
        cipPravila: '19 pravila', cipSkupovi: 'trimf / trapmf', cipTeziste: 'centroid', cipMreza: 'mreža daje samo rečnik',
        metodNapomena: 'Kategorija se čita iz iste defazifikovane vrednosti koja je prikazana, pa ocena i oznaka ne mogu da se raziđu.',
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
let tema = ucitajLokalno('fg-prototip-tema', 'dark');
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
/* ---------- fuzzy sets ------------------------------------------- */

const SKUPOVI_ULAZA = {
    kljucne_reci: [
        { ime: 'kljucne_zanemarljive', tip: 'trapmf', params: [0, 0, 1, 3], kategorija: 'LEGITIMAN' },
        { ime: 'kljucne_zastupljene', tip: 'trimf', params: [1, 3, 7], kategorija: 'SUMNJIVO' },
        { ime: 'kljucne_dominantne', tip: 'trapmf', params: [5, 8, 10, 10], kategorija: 'SPAM' }
    ],
    broj_linkova: [
        { ime: 'linkovi_minimalni', tip: 'trapmf', params: [0, 0, 0, 1], kategorija: 'LEGITIMAN' },
        { ime: 'linkovi_umereni', tip: 'trimf', params: [0, 1, 3], kategorija: 'SUMNJIVO' },
        { ime: 'linkovi_brojni', tip: 'trapmf', params: [2, 8, 10, 10], kategorija: 'SPAM' }
    ],
    caps_procenat: [
        { ime: 'caps_uobicajen', tip: 'trapmf', params: [0, 0, 1, 12], kategorija: 'LEGITIMAN' },
        { ime: 'caps_poviseni', tip: 'trimf', params: [7, 16, 32], kategorija: 'SUMNJIVO' },
        { ime: 'caps_blago_povisen', tip: 'trimf', params: [10, 25, 65], kategorija: 'SUMNJIVO' },
        { ime: 'caps_agresivan', tip: 'trapmf', params: [45, 85, 100, 100], kategorija: 'SPAM' }
    ],
    interpunkcija: [
        { ime: 'interpunkcija_retka', tip: 'trapmf', params: [0, 0, 2, 5], kategorija: 'LEGITIMAN' },
        { ime: 'interpunkcija_blago', tip: 'trimf', params: [2, 5, 10], kategorija: 'SUMNJIVO' },
        { ime: 'interpunkcija_umerena', tip: 'trimf', params: [6, 12, 25], kategorija: 'SUMNJIVO' },
        { ime: 'interpunkcija_agresivna', tip: 'trapmf', params: [14, 40, 100, 100], kategorija: 'SPAM' }
    ]
};

const SKUPOVI_IZLAZA = [
    { ime: 'score_legitiman', tip: 'trapmf', params: [0, 0, 8, 20], kategorija: 'LEGITIMAN' },
    { ime: 'score_legitiman_energicno', tip: 'trimf', params: [10, 13, 22], kategorija: 'LEGITIMAN' },
    { ime: 'score_blago_sumnjiv', tip: 'trimf', params: [24, 30, 42], kategorija: 'SUMNJIVO' },
    { ime: 'score_sumnjiv', tip: 'trimf', params: [38, 44, 58], kategorija: 'SUMNJIVO' },
    { ime: 'score_visoko_sumnjiv', tip: 'trimf', params: [54, 60, 74], kategorija: 'SUMNJIVO' },
    { ime: 'score_spam', tip: 'trapmf', params: [72, 88, 100, 100], kategorija: 'SPAM' }
];

const SKUP_PO_IMENU = {};
SKUPOVI_IZLAZA.forEach(skup => { SKUP_PO_IMENU[skup.ime] = skup; });

/* ---------- lexicons --------------------------------------------- */

// Ručni rečnik je preuzet iz obrada_teksta/analizator.py. Ne skraćivati ga:
// on je jedina srpska pokrivenost i osnova za poređenje bez mreže.
const RECNIK_RUCNI = [
    'win', 'winner', 'won', 'free', 'click', 'offer', 'prize',
    'congratulations', 'claim', 'cash', 'bonus', 'reward', 'rewards',
    'urgent', 'limited', 'exclusive', 'guarantee', 'guaranteed', 'deal',
    'cheap', 'discount', 'income', 'profit', 'rich', 'million', 'dollar',
    'dollars', 'money', 'selected', 'opportunity',
    'account', 'verify', 'unusual', 'eligible', 'refund', 'confirm',
    'update', 'settings', 'subscription', 'expire', 'expires', 'renew',
    'approved', 'loan', 'jackpot', 'unlimited', 'access',
    'pobedi', 'pobednik', 'pobedniku', 'pobednika',
    'osvojio', 'osvojili', 'osvojite', 'osvoji',
    'besplatno', 'besplatnu', 'besplatni', 'besplatna', 'besplatne', 'besplatan',
    'klikni', 'kliknite', 'kliknete',
    'ponuda', 'ponude', 'ponudu',
    'nagrada', 'nagradu', 'nagrade', 'nagradi',
    'čestitamo', 'čestitam',
    'preuzmi', 'preuzmite', 'preuzmete', 'preuzimite',
    'gotovina', 'gotovinu', 'gotovine',
    'hitno', 'hitna', 'hitni', 'hitne',
    'ograničeno', 'ograničena', 'ograničenu', 'ograničene', 'ograničeni',
    'neograničeno', 'neograničena', 'neograničenu', 'neograničene', 'neograničeni',
    'ekskluzivno', 'ekskluzivna', 'ekskluzivnu', 'ekskluzivne', 'ekskluzivni',
    'garantovano', 'garantovana', 'garantujemo', 'garantovanu',
    'jeftino', 'jeftina', 'jeftine', 'jeftini', 'jeftinu',
    'popust', 'popusta', 'popustu', 'popustom',
    'novac', 'novca', 'novcem', 'novcu',
    'prihod', 'prihoda', 'prihode', 'prihodom',
    'zarada', 'zaradu', 'zarade', 'zaradite', 'zaraditi',
    'bogat', 'bogata', 'bogati', 'bogatstvo',
    'milion', 'miliona', 'milione', 'milionima',
    'dolar', 'dolara', 'dolare', 'dolarima',
    'dinar', 'dinara', 'dinare', 'dinarima',
    'izabran', 'izabrana', 'izabrani', 'izabrano', 'izabrane',
    'prilika', 'prilike', 'priliku', 'prilikama',
    'pogodba', 'pogodbe', 'pogodbu',
    'nalog', 'naloga', 'nalogu',
    'verifikuj', 'verifikujte', 'verifikuje',
    'aktivnost', 'aktivnosti',
    'potvrdite', 'potvrdi', 'potvrdite',
    'povraćaj', 'povraćaja',
    'ažuriranje', 'ažurirajte', 'ažurirate',
    'podešavanja', 'podešavanje',
    'pretplata', 'pretplatu', 'pretplate',
    'ističe', 'ističu',
    'obnovite', 'obnovi', 'obnova',
    'pristup', 'pristupa',
    'kredit', 'kredita',
    'odobren', 'odobrena', 'odobreno',
    'keš',
    'naplatite', 'naplati',
    'dobitnik', 'dobitnica', 'dobitnika',
    'džekpot', 'džekpota'
];

const RECNIK_FRAZE = [
    'buy now', 'act now', 'order now', 'click here', 'limited time',
    'limited offer', 'free prize', 'you won', 'you have won',
    'claim now', 'claim your', 'get rich', 'make money',
    'gift card', 'get paid', 'lose access',
    'kupi sad', 'deluj odmah', 'naruči odmah', 'klikni ovde',
    'ograničena ponuda', 'besplatna nagrada', 'osvojio si', 'preuzmi nagradu',
    'reaguj odmah'
];

// Skraćen izvoz neuronske mreže (podaci/recnik_naucen.json, top termini).
// U pravom sistemu stiže svih 271 termina; ovde je dovoljan za prototip.
const RECNIK_NAUCENI = {
    'guaranteed': 2.0, 'dear': 1.9435, 'sir': 1.6935, 'removal': 1.6795,
    'face': 1.672, 'obligation': 1.5865, 'mortgage': 1.545,
    'assistance': 1.541, 'click link': 1.5409, 'dear sir': 1.5267,
    'sincerely': 1.4421, 'subject line': 1.43, 'emails': 1.3867,
    'earn': 1.3753, 'sir madam': 1.3435, 'prices': 1.3295, 'title': 1.3263,
    'subscriber': 1.323, 'nigeria': 1.3188, 'mailings': 1.3165,
    'madam': 1.3131, 'opt': 1.3067, 'lenders': 1.2825, 'bonus': 1.2615,
    'tobacco': 1.2422, 'security company': 1.2413, 'lowest': 1.2074,
    'shipping': 1.2042, 'deposit': 1.1958, 'assist': 1.1921,
    'qualified': 1.1804, 'email address': 1.1656, 'mail address': 1.1407
};

/* ---------- sample messages -------------------------------------- */

const UZORCI = {
    legitiman: [
        {
            posaljilac: 'Mina Petrovi?',
            tema: 'Re: sync tomorrow',
            tekst: 'Hi, just wanted to confirm our meeting tomorrow at 3pm. Let me know if that works for you.'
        },
        {
            posaljilac: 'Marko Jovanovi?',
            tema: 'Sastanak sutra',
            tekst: 'Zdravo, potvr?ujem sastanak sutra u 15 ?asova. Vidimo se u kancelariji.'
        }
    ],
    sumnjiv: [
        {
            posaljilac: 'Dostava',
            tema: 'Va? paket ?eka',
            tekst: 'Po?tovani, va? paket ?eka na preuzimanju. Proverite adresu dostave na http://posta-dostava.net ili http://status-paketa.com kako bi isporuka bila zavr?ena.'
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
            tema: '?estitamo, osvojili ste!',
            tekst: '?estitamo! Osvojili ste besplatnu nagradu. Kliknite ovde da preuzmete nagradu.'
        }
    ]
};

/* ---------- rule descriptions ------------------------------------ */

const OPISI_PRAVILA = {
    p01: { en: 'negligible keywords + minimal links + normal caps + sparse punctuation', sr: 'zanemarljive reči + minimalni linkovi + uobičajena velika slova + retka interpunkcija' },
    p02: { en: 'mildly elevated caps + negligible keywords + minimal links', sr: 'blago povišena velika slova + zanemarljive reči + minimalni linkovi' },
    p03: { en: 'mild punctuation + negligible keywords + minimal links', sr: 'blaga interpunkcija + zanemarljive reči + minimalni linkovi' },
    p03a: { en: 'moderate punctuation + negligible keywords + minimal links', sr: 'umerena interpunkcija + zanemarljive reči + minimalni linkovi' },
    p04: { en: 'negligible keywords + moderate links + normal caps + sparse punctuation', sr: 'zanemarljive reči + umereni linkovi + uobičajena velika slova + retka interpunkcija' },
    p05: { en: 'present keywords + minimal links', sr: 'zastupljene reči + minimalni linkovi' },
    p06: { en: 'present keywords + moderate links + normal caps + sparse punctuation', sr: 'zastupljene reči + umereni linkovi + uobičajena velika slova + retka interpunkcija' },
    p06a: { en: 'present keywords + moderate links', sr: 'zastupljene reči + umereni linkovi' },
    p07: { en: 'moderate/numerous links + elevated/mild/aggressive caps + negligible keywords', sr: 'umereni/brojni linkovi + povišena/blaga/agresivna velika slova + zanemarljive reči' },
    p08: { en: 'moderate/numerous links + moderate/mild/aggressive punctuation + negligible keywords', sr: 'umereni/brojni linkovi + umerena/blaga/agresivna interpunkcija + zanemarljive reči' },
    p09: { en: 'present keywords + moderate links + elevated caps + moderate punctuation', sr: 'zastupljene reči + umereni linkovi + povišena velika slova + umerena interpunkcija' },
    p10: { en: 'dominant keywords + moderate links + normal caps + sparse punctuation', sr: 'dominantne reči + umereni linkovi + uobičajena velika slova + retka interpunkcija' },
    p11: { en: 'dominant keywords + normal caps', sr: 'dominantne reči + uobičajena velika slova' },
    p12: { en: 'aggressive caps + negligible keywords + minimal links', sr: 'agresivna velika slova + zanemarljive reči + minimalni linkovi' },
    p13: { en: 'aggressive punctuation + negligible keywords + minimal links', sr: 'agresivna interpunkcija + zanemarljive reči + minimalni linkovi' },
    p14: { en: 'dominant keywords OR numerous links', sr: 'dominantne reči ILI brojni linkovi' },
    p15: { en: 'present keywords + (aggressive caps OR aggressive punctuation)', sr: 'zastupljene reči + (agresivna velika slova ILI agresivna interpunkcija)' },
    p16: { en: 'moderate links + (aggressive caps OR aggressive punctuation)', sr: 'umereni linkovi + (agresivna velika slova ILI agresivna interpunkcija)' },
    p17: { en: '(present or dominant) keywords + (moderate or numerous) links + (elevated, mild or aggressive) caps', sr: '(zastupljene ili dominantne) reči + (umereni ili brojni) linkovi + (povišena, blaga ili agresivna) velika slova' }
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

function fuzzifikuj(vrednosti) {
    const mu = {};
    Object.keys(SKUPOVI_ULAZA).forEach(imeUlaza => {
        mu[imeUlaza] = {};
        SKUPOVI_ULAZA[imeUlaza].forEach(skup => {
            mu[imeUlaza][skup.ime] = pripadnost(skup.tip, skup.params, vrednosti[imeUlaza]);
        });
    });
    return mu;
}

function sastaviPravila(mu) {
    const kljucne_reci = mu.kljucne_reci;
    const broj_linkova = mu.broj_linkova;
    const caps_procenat = mu.caps_procenat;
    const interpunkcija = mu.interpunkcija;

    return [
        { naziv: 'p01', jacina: Math.min(kljucne_reci.kljucne_zanemarljive, broj_linkova.linkovi_minimalni, caps_procenat.caps_uobicajen, interpunkcija.interpunkcija_retka), skup: 'score_legitiman', kategorija: 'LEGITIMAN' },
        { naziv: 'p02', jacina: Math.min(caps_procenat.caps_blago_povisen, kljucne_reci.kljucne_zanemarljive, broj_linkova.linkovi_minimalni), skup: 'score_legitiman_energicno', kategorija: 'LEGITIMAN' },
        { naziv: 'p03', jacina: Math.min(interpunkcija.interpunkcija_blago, kljucne_reci.kljucne_zanemarljive, broj_linkova.linkovi_minimalni), skup: 'score_legitiman_energicno', kategorija: 'LEGITIMAN' },
        { naziv: 'p03a', jacina: Math.min(interpunkcija.interpunkcija_umerena, kljucne_reci.kljucne_zanemarljive, broj_linkova.linkovi_minimalni), skup: 'score_legitiman_energicno', kategorija: 'LEGITIMAN' },
        { naziv: 'p04', jacina: Math.min(kljucne_reci.kljucne_zanemarljive, broj_linkova.linkovi_umereni, caps_procenat.caps_uobicajen, interpunkcija.interpunkcija_retka), skup: 'score_blago_sumnjiv', kategorija: 'SUMNJIVO' },
        { naziv: 'p05', jacina: Math.min(kljucne_reci.kljucne_zastupljene, broj_linkova.linkovi_minimalni), skup: 'score_sumnjiv', kategorija: 'SUMNJIVO' },
        { naziv: 'p06', jacina: Math.min(kljucne_reci.kljucne_zastupljene, broj_linkova.linkovi_umereni, caps_procenat.caps_uobicajen, interpunkcija.interpunkcija_retka), skup: 'score_sumnjiv', kategorija: 'SUMNJIVO' },
        { naziv: 'p06a', jacina: Math.min(kljucne_reci.kljucne_zastupljene, broj_linkova.linkovi_umereni), skup: 'score_sumnjiv', kategorija: 'SUMNJIVO' },
        { naziv: 'p07', jacina: Math.min(Math.max(broj_linkova.linkovi_umereni, broj_linkova.linkovi_brojni), Math.max(caps_procenat.caps_poviseni, caps_procenat.caps_blago_povisen, caps_procenat.caps_agresivan), kljucne_reci.kljucne_zanemarljive), skup: 'score_sumnjiv', kategorija: 'SUMNJIVO' },
        { naziv: 'p08', jacina: Math.min(Math.max(broj_linkova.linkovi_umereni, broj_linkova.linkovi_brojni), Math.max(interpunkcija.interpunkcija_umerena, interpunkcija.interpunkcija_blago, interpunkcija.interpunkcija_agresivna), kljucne_reci.kljucne_zanemarljive), skup: 'score_sumnjiv', kategorija: 'SUMNJIVO' },
        { naziv: 'p09', jacina: Math.min(kljucne_reci.kljucne_zastupljene, broj_linkova.linkovi_umereni, caps_procenat.caps_poviseni, interpunkcija.interpunkcija_umerena), skup: 'score_visoko_sumnjiv', kategorija: 'SUMNJIVO' },
        { naziv: 'p10', jacina: Math.min(kljucne_reci.kljucne_dominantne, broj_linkova.linkovi_umereni, caps_procenat.caps_uobicajen, interpunkcija.interpunkcija_retka), skup: 'score_visoko_sumnjiv', kategorija: 'SUMNJIVO' },
        { naziv: 'p11', jacina: Math.min(kljucne_reci.kljucne_dominantne, caps_procenat.caps_uobicajen), skup: 'score_visoko_sumnjiv', kategorija: 'SUMNJIVO' },
        { naziv: 'p12', jacina: Math.min(caps_procenat.caps_agresivan, kljucne_reci.kljucne_zanemarljive, broj_linkova.linkovi_minimalni), skup: 'score_visoko_sumnjiv', kategorija: 'SUMNJIVO' },
        { naziv: 'p13', jacina: Math.min(interpunkcija.interpunkcija_agresivna, kljucne_reci.kljucne_zanemarljive, broj_linkova.linkovi_minimalni), skup: 'score_visoko_sumnjiv', kategorija: 'SUMNJIVO' },
        { naziv: 'p14', jacina: Math.max(kljucne_reci.kljucne_dominantne, broj_linkova.linkovi_brojni), skup: 'score_spam', kategorija: 'SPAM' },
        { naziv: 'p15', jacina: Math.min(kljucne_reci.kljucne_zastupljene, Math.max(caps_procenat.caps_agresivan, interpunkcija.interpunkcija_agresivna)), skup: 'score_spam', kategorija: 'SPAM' },
        { naziv: 'p16', jacina: Math.min(broj_linkova.linkovi_umereni, Math.max(caps_procenat.caps_agresivan, interpunkcija.interpunkcija_agresivna)), skup: 'score_spam', kategorija: 'SPAM' },
        { naziv: 'p17', jacina: Math.min(Math.max(kljucne_reci.kljucne_zastupljene, kljucne_reci.kljucne_dominantne), Math.max(broj_linkova.linkovi_umereni, broj_linkova.linkovi_brojni), Math.max(caps_procenat.caps_poviseni, caps_procenat.caps_blago_povisen, caps_procenat.caps_agresivan)), skup: 'score_spam', kategorija: 'SPAM' }
    ];
}

function defazifikuj(pravila) {
    let imenilac = 0;
    let brojilac = 0;

    for (let x = 0; x <= 100; x += 1) {
        let agregat = 0;
        pravila.forEach(pravilo => {
            const skup = SKUP_PO_IMENU[pravilo.skup];
            const pripadnostIzlaza = pripadnost(skup.tip, skup.params, x);
            agregat = Math.max(agregat, Math.min(pravilo.jacina, pripadnostIzlaza));
        });
        brojilac += x * agregat;
        imenilac += agregat;
    }

    return imenilac > 0 ? brojilac / imenilac : 0;
}

function kategorijaZaSkor(skor) {
    let najjaci = SKUPOVI_IZLAZA[0];
    let najveca = -1;

    SKUPOVI_IZLAZA.forEach(skup => {
        const mu = pripadnost(skup.tip, skup.params, skor);
        if (mu > najveca) {
            najveca = mu;
            najjaci = skup;
        }
    });

    return najjaci.kategorija;
}

/* ---------- text analysis ---------------------------------------- */

const UZORAK_LINKA = /\b(?:https?:\/\/|hxxps?:\/\/|www\.)[^\s<>"']+/gi;
const UZORAK_CAPS = /\b[A-ZČĆŠŽĐ]{3,}\b/g;
const UZORAK_INTERPUNKCIJA = /[!?]+/g;
const ESCAPE_UZORAK = /[.*+?^${}()|[\]\\]/g;

function ocistiHtml(tekst) {
    return String(tekst)
        .replace(/<script[\s\S]*?<\/script>/gi, ' ')
        .replace(/<style[\s\S]*?<\/style>/gi, ' ')
        .replace(/<br\s*\/?>|<\/p>|<\/div>|<\/li>|<\/tr>|<\/h[1-6]>/gi, ' ')
        .replace(/<[^>]+>/g, ' ')
        .replace(/\s+/g, ' ')
        .trim();
}

function napraviUzorak(termin) {
    const imaRazmak = /\s/.test(termin);
    const osnova = termin.replace(ESCAPE_UZORAK, '\\$&');
    try {
        return new RegExp(imaRazmak ? osnova : `(?<![\\p{L}\\p{N}])${osnova}(?![\\p{L}\\p{N}])`, 'giu');
    } catch (greska) {
        return new RegExp(imaRazmak ? osnova : `\\b${osnova}\\b`, 'gi');
    }
}

const RUCNI_TERMINI = new Set([...RECNIK_RUCNI, ...RECNIK_FRAZE]);

const UZORCI_RUCNI = RECNIK_RUCNI.concat(RECNIK_FRAZE).map(termin => ({
    termin, tezina: 1.0, izvor: 'rucni', uzorak: napraviUzorak(termin)
}));

const UZORCI_NAUCENI = Object.keys(RECNIK_NAUCENI).map(termin => ({
    termin, tezina: RECNIK_NAUCENI[termin], izvor: 'nauceni', uzorak: napraviUzorak(termin)
}));

function izracunajKljucneReci(tekst, nacin) {
    let evidencija = 0;
    const pogodjene = [];

    function dodajPogotke(uzorak, termin, tezina, izvor) {
        const poklapanja = Array.from(tekst.matchAll(uzorak));
        if (!poklapanja.length) return;

        evidencija += poklapanja.length * tezina;
        pogodjene.push({
            rec: termin,
            broj: poklapanja.length,
            tezina,
            izvor,
            pozicije: poklapanja.slice(0, 10).map(poklapanje => [poklapanje.index, poklapanje.index + poklapanje[0].length])
        });
    }

    if (nacin === 'rucni' || nacin === 'kombinovano') {
        UZORCI_RUCNI.forEach(uzorak => dodajPogotke(uzorak.uzorak, uzorak.termin, uzorak.tezina, uzorak.izvor));
    }

    if (nacin === 'nauceni' || nacin === 'kombinovano') {
        UZORCI_NAUCENI.forEach(uzorak => {
            if (nacin === 'kombinovano' && RUCNI_TERMINI.has(uzorak.termin)) return;
            dodajPogotke(uzorak.uzorak, uzorak.termin, uzorak.tezina, uzorak.izvor);
        });
    }

    pogodjene.sort((prva, druga) => (druga.broj * druga.tezina) - (prva.broj * prva.tezina));

    return { vrednost: Math.min(evidencija, 10), pogodjene: pogodjene.slice(0, 8) };
}

function izvuciLinkove(tekst) {
    const kandidati = Array.from(tekst.matchAll(UZORAK_LINKA)).map(poklapanje => poklapanje[0]);
    const ocisceni = kandidati.map(link =>
        link.replace(/[.,;:!?)\]}>"']+$/, '').toLowerCase()
    ).filter(Boolean);
    return Array.from(new Set(ocisceni));
}

function izracunajCapsProcenat(tekstBezLinkova) {
    const slova = Array.from(tekstBezLinkova).filter(znak => /\p{L}/u.test(znak));
    if (!slova.length) return 0;
    const velika = slova.filter(znak => znak === znak.toUpperCase() && znak !== znak.toLowerCase()).length;
    return Math.round((velika / slova.length) * 10000) / 100;
}

function izracunajInterpunkciju(tekstBezLinkova) {
    const uzvici = (tekstBezLinkova.match(/!/g) || []).length;
    const upitnici = (tekstBezLinkova.match(/\?/g) || []).length;
    const znakovi = tekstBezLinkova.replace(/\s/g, '').length;
    return znakovi ? Math.round(((uzvici + upitnici) / znakovi) * 10000) / 100 : 0;
}

async function izracunajRezultat(tekst, nacin) {
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
    const cilj = Math.round(konacan);

    if (smanjenoKretanje) { element.textContent = String(cilj); return; }

    const pocetak = performance.now();
    const trajanje = 540;

    function korak(sada) {
        const napredak = Math.min(1, (sada - pocetak) / trajanje);
        const ublazeno = 1 - Math.pow(1 - napredak, 3);
        element.textContent = String(Math.round(cilj * ublazeno));
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
        document.getElementById('skor-broj').textContent = String(Math.round(rezultat.skor));
    } else {
        animirajSkor(rezultat.skor);
    }

    nacrtajSpektar(document.getElementById('spektar'), rezultat.skor);

    document.getElementById('centroid').textContent = formatirajBroj(rezultat.skor);
    const tragKategorija = document.getElementById('trag-kategorija');
    tragKategorija.textContent = t().kategorije[rezultat.kategorija];
    tragKategorija.style.setProperty('--boja', boja);

    renderSignali(rezultat);
    renderPogled();
    renderIstorija();
}

function renderSignali(rezultat) {
    const redosled = ['kljucne_reci', 'broj_linkova', 'caps_procenat', 'interpunkcija'];

    document.getElementById('signali').innerHTML = redosled.map(kljuc => {
        const vrednost = rezultat.vrednosti[kljuc];
        const skupovi = SKUPOVI_ULAZA[kljuc].slice().sort((prvi, drugi) =>
            pripadnost(drugi.tip, drugi.params, vrednost) - pripadnost(prvi.tip, prvi.params, vrednost)
        );
        const dominantan = skupovi[0];
        const dominantaMu = pripadnost(dominantan.tip, dominantan.params, vrednost);
        const maksimum = (kljuc === 'kljucne_reci' || kljuc === 'broj_linkova') ? 10 : 100;
        const sirina = Math.max(vrednost > 0 ? 2 : 0, Math.min(100, (vrednost / maksimum) * 100));

        return `<div class="signal">
            <div class="signal-vrh">
                <span class="signal-naziv">${pobjegni(t().signali[kljuc])}</span>
                <span class="signal-skup">${pobjegni(t().skupovi[dominantan.ime])} <b>${dominantaMu.toFixed(2)}</b></span>
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
    const tipovi = new Set();

    (rezultat.pogodjene || []).forEach(stavka => {
        if (stavka.pozicije.length) tipovi.add('keyword');
    });
    if (rezultat.linkovi.length) tipovi.add('link');
    if (/\b[A-ZČĆŠŽĐ]{3,}\b/.test(rezultat.vidljivi)) tipovi.add('caps');
    if (/[!?]/.test(rezultat.vidljivi)) tipovi.add('interpunkcija');

    elementi.push(`<p class="pogled-naslov">${pobjegni(t().pronasli)}</p>`);
    elementi.push(`<div class="pregled">${napraviPregled(rezultat)}</div>`);

    if (tipovi.size) {
        elementi.push('<div class="legenda">' + Array.from(tipovi).map(tip =>
            `<span style="--boja: var(--${tip === 'keyword' ? 'sumnjivo' : tip === 'link' ? 'link' : tip === 'caps' ? 'spam' : 'ljubicasta'})"><i></i>${pobjegni(t().legenda[tip])}</span>`
        ).join('') + '</div>');
    }

    elementi.push(`<p class="pogled-naslov" style="margin-top:13px">${pobjegni(t().prepoznate)}</p>`);

    if (rezultat.pogodjene.length) {
        elementi.push('<div class="cipovi">' + rezultat.pogodjene.map(stavka => {
            const izvor = stavka.izvor === 'nauceni' ? t().izvorNauceni : t().izvorRucni;
            return `<span class="cip" title="${pobjegni(izvor)} · ${formatirajBroj(stavka.tezina)}">` +
                   `${pobjegni(stavka.rec)}${stavka.broj > 1 ? ` <b>×${stavka.broj}</b>` : ''}</span>`;
        }).join('') + '</div>');
    } else {
        elementi.push(`<p class="tiho">${pobjegni(t().nemaPogodaka)}</p>`);
    }

    return elementi.join('');
}

function napraviPregled(rezultat) {
    const tekst = rezultat.vidljivi || '';
    const delovi = [];
    const prioritet = { link: 4, caps: 3, keyword: 2, interpunkcija: 1 };

    (rezultat.pogodjene || []).forEach(stavka => {
        stavka.pozicije.forEach(pozicija => delovi.push({ a: pozicija[0], b: pozicija[1], tip: 'keyword' }));
    });

    [['link', UZORAK_LINKA], ['caps', UZORAK_CAPS], ['interpunkcija', UZORAK_INTERPUNKCIJA]].forEach(([tip, uzorak]) => {
        Array.from(tekst.matchAll(uzorak)).slice(0, 50).forEach(poklapanje => {
            delovi.push({ a: poklapanje.index, b: poklapanje.index + poklapanje[0].length, tip });
        });
    });

    delovi.sort((prvi, drugi) =>
        (prioritet[drugi.tip] - prioritet[prvi.tip]) ||
        ((drugi.b - drugi.a) - (prvi.b - prvi.a)) ||
        (prvi.a - drugi.a)
    );

    const prihvaceni = [];
    delovi.forEach(deo => {
        if (deo.a >= deo.b) return;
        if (prihvaceni.some(uzet => deo.a < uzet.b && deo.b > uzet.a)) return;
        prihvaceni.push(deo);
    });
    prihvaceni.sort((prvi, drugi) => prvi.a - drugi.a);

    let html = '';
    let pozicija = 0;
    prihvaceni.forEach(deo => {
        if (deo.a < pozicija || deo.a > tekst.length) return;
        html += pobjegni(tekst.slice(pozicija, deo.a));
        html += `<mark class="obj-mark obj-mark--${deo.tip}">${pobjegni(tekst.slice(deo.a, deo.b))}</mark>`;
        pozicija = deo.b;
    });
    html += pobjegni(tekst.slice(pozicija));

    return html || pobjegni(tekst);
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
        const opis = (jezik === 'sr' ? pravilo.uslov_sr : pravilo.uslov_en)
            || (OPISI_PRAVILA[pravilo.naziv] ? OPISI_PRAVILA[pravilo.naziv][jezik] : '');
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
            <span class="istorija-skore">${Math.round(rezultat.skor)}%</span>
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
    sakrijIndikatorUzorka();
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

const INDEKS_UZORKA = { legitiman: 0, sumnjiv: 0, prevara: 0 };
const KATEGORIJA_UZORKA = { legitiman: 'LEGITIMAN', sumnjiv: 'SUMNJIVO', prevara: 'SPAM' };
let trenutniUzorakIndikator = null;

function prikaziIndikatorUzorka(kljuc) {
    const indikator = document.getElementById('uzorak-indikator');
    const tekst = document.getElementById('uzorak-indikator-tekst');
    const kategorija = KATEGORIJA_UZORKA[kljuc];
    trenutniUzorakIndikator = kljuc;
    indikator.hidden = false;
    indikator.style.setProperty('--boja', bojaKategorije(kategorija));
    tekst.textContent = t().kategorije[kategorija];
}

function sakrijIndikatorUzorka() {
    trenutniUzorakIndikator = null;
    document.getElementById('uzorak-indikator').hidden = true;
}

async function izaberiUzorak(kljuc, nasumicno) {
    const grupa = UZORCI[kljuc];
    if (!grupa || !grupa.length) return;

    if (!nasumicno) sakrijIndikatorUzorka();

    let indeks;
    if (nasumicno) {
        indeks = Math.floor(Math.random() * grupa.length);
    } else {
        indeks = INDEKS_UZORKA[kljuc] % grupa.length;
        INDEKS_UZORKA[kljuc] = (indeks + 1) % grupa.length;
    }

    const uzorak = grupa[indeks];
    popuniPolja(uzorak);

    try {
        const rezultat = await izracunajRezultat(uzorak.tekst, nacinRecnika);
        prikaziRezultat(rezultat, { animiraj: true });
        dodajUIstoriju(uzorak.tekst, uzorak.posaljilac, uzorak.tema, rezultat);
    } catch (greska) {
        prikaziGresku(greska.message || t().greskaMreza);
    }
}

let primeriKes = { en: null, sr: null };

async function izaberiRandom() {
    const jezikUzorka = jezik;

    try {
        if (!primeriKes[jezikUzorka]) {
            const odgovor = await fetch('/primeri-svi?jezik=' + jezikUzorka);
            const podaci = await odgovor.json();
            primeriKes[jezikUzorka] = podaci.primeri || [];
        }

        const lista = primeriKes[jezikUzorka];
        if (!lista.length) return;

        const uzorak = lista[Math.floor(Math.random() * lista.length)];

        if (uzorak.kategorija && KATEGORIJA_UZORKA[uzorak.kategorija]) {
            prikaziIndikatorUzorka(uzorak.kategorija);
        } else {
            sakrijIndikatorUzorka();
        }

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
    sakrijIndikatorUzorka();
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
        `${recnik.procena}: ${Math.round(rezultat.skor)}% (${recnik.kategorije[rezultat.kategorija]})`,
        `${recnik.teziste}: ${formatirajBroj(rezultat.skor)}`,
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
    sacuvajLokalno('fg-prototip-tema', tema);
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

    if (trenutniUzorakIndikator) prikaziIndikatorUzorka(trenutniUzorakIndikator);

    document.querySelectorAll('[data-i18n-placeholder]').forEach(element => {
        const kljuc = element.getAttribute('data-i18n-placeholder');
        if (recnik[kljuc] !== undefined) element.placeholder = recnik[kljuc];
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

function otvoriMetod() {
    const dijalog = document.getElementById('metod');
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
    if (!['rucni', 'nauceni', 'kombinovano'].includes(nacinRecnika)) nacinRecnika = 'kombinovano';
    if (!['en', 'sr'].includes(jezik)) jezik = 'en';
    if (!['dark', 'light'].includes(tema)) tema = 'dark';

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