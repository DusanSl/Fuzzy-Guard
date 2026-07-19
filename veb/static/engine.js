const istorijaNiz = [];
let trenutniJezik = 'en';
let trenutniPodaci = null;

const prevodi = {
    sr: {
        novaProvera: 'Nova provera',
        primerProvera: 'Primer provera',
        prethodneProvere: 'PRETHODNE PROVERE',
        od: 'Od:',
        odVrednost: 'testiranje@spam-filter',
        placeholder: 'Napišite ili zalepite tekst emaila ovde...',
        pokreniAnalizu: 'Pokreni Analizu',
        analiziranje: 'Analiziranje...',
        spamScore: 'SPAM SCORE',
        kljucneReci: 'KLJUČNE REČI',
        brojLinkova: 'BROJ LINKOVA',
        caps: 'CAPS',
        interpunkcija: 'INTERPUNKCIJA',
        kategorije: { SPAM: 'SPAM', SUMNJIVO: 'SUMNJIVO', LEGITIMAN: 'LEGITIMAN' },
        dugmeJezik: 'English'
    },
    en: {
        novaProvera: 'New check',
        primerProvera: 'Sample check',
        prethodneProvere: 'PREVIOUS CHECKS',
        od: 'From:',
        odVrednost: 'testing@spam-filter',
        placeholder: 'Write or paste the email text here...',
        pokreniAnalizu: 'Run analysis',
        analiziranje: 'Analyzing...',
        spamScore: 'SPAM SCORE',
        kljucneReci: 'KEYWORDS',
        brojLinkova: 'LINK COUNT',
        caps: 'CAPS',
        interpunkcija: 'PUNCTUATION',
        kategorije: { SPAM: 'SPAM', SUMNJIVO: 'SUSPICIOUS', LEGITIMAN: 'LEGITIMATE' },
        dugmeJezik: 'Srpski'
    }
};

function promeniJezik() {
    trenutniJezik = trenutniJezik === 'sr' ? 'en' : 'sr';
    primeniJezik();
}

function primeniJezik() {
    const t = prevodi[trenutniJezik];

    document.querySelectorAll('[data-i18n]').forEach(el => {
        const kljuc = el.getAttribute('data-i18n');
        if (t[kljuc] !== undefined) el.textContent = t[kljuc];
    });

    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const kljuc = el.getAttribute('data-i18n-placeholder');
        if (t[kljuc] !== undefined) el.placeholder = t[kljuc];
    });

    document.getElementById('jezik-dugme').textContent = t.dugmeJezik;
    document.documentElement.lang = trenutniJezik;

    const dugme = document.querySelector('.dugme-analiziraj');
    if (!dugme.disabled) dugme.textContent = t.pokreniAnalizu;

    if (trenutniPodaci) prikaziIndikator(trenutniPodaci);
    renderIstorija();
}

function toggleMeni() {
    const sadrzaj = document.getElementById('sidebar-sadrzaj');
    const dugme = document.getElementById('meni-dugme');
    const otvoren = sadrzaj.classList.toggle('otvoren');
    dugme.setAttribute('aria-expanded', otvoren ? 'true' : 'false');
    dugme.textContent = otvoren ? '✕' : '☰';
}

let primeriKes = { en: [], sr: [] };
let preostaliIndeksi = { en: [], sr: [] };

function promesaj(niz) {
    const kopija = [...niz];
    for (let i = kopija.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [kopija[i], kopija[j]] = [kopija[j], kopija[i]];
    }
    return kopija;
}

async function ucitajRandom() {
    const jezik = trenutniJezik;

    if (primeriKes[jezik].length === 0) {
        const odgovor = await fetch('/primeri-svi?jezik=' + jezik);
        const podaci = await odgovor.json();
        primeriKes[jezik] = podaci.primeri;
    }

    if (preostaliIndeksi[jezik].length === 0) {
        preostaliIndeksi[jezik] = promesaj(
            [...Array(primeriKes[jezik].length).keys()]
        );
    }

    const indeks = preostaliIndeksi[jezik].pop();
    document.getElementById('tekst').value = primeriKes[jezik][indeks];
    resetujRezultate();
}

function resetujRezultate() {
    ['score', 'kljucne', 'linkovi', 'caps', 'interpunkcija'].forEach(id => {
        document.getElementById('vrednost-' + id).textContent = '—';
    });
    const scoreKartica = document.getElementById('kartica-score');
    scoreKartica.classList.remove('score-spam', 'score-sumnjivo', 'score-legitiman');
    document.getElementById('indikator-score').textContent = '';
    trenutniPodaci = null;
}

function novaProvera() {
    document.getElementById('tekst').value = '';
    resetujRezultate();
}

function prikaziIndikator(podaci) {
    const t = prevodi[trenutniJezik];
    const scoreKartica = document.getElementById('kartica-score');
    scoreKartica.classList.remove('score-spam', 'score-sumnjivo', 'score-legitiman');

    const indikator = document.getElementById('indikator-score');
    const klasa = podaci.kategorija === 'SPAM' ? 'score-spam'
                : podaci.kategorija === 'SUMNJIVO' ? 'score-sumnjivo'
                : 'score-legitiman';
    scoreKartica.classList.add(klasa);
    indikator.textContent = t.kategorije[podaci.kategorija] || podaci.kategorija;
}

function prikaziRezultate(podaci) {
    trenutniPodaci = podaci;

    document.getElementById('vrednost-score').textContent        = podaci.spam_score + '%';
    document.getElementById('vrednost-kljucne').textContent      = podaci.kljucne_reci;
    document.getElementById('vrednost-linkovi').textContent      = podaci.broj_linkova;
    document.getElementById('vrednost-caps').textContent         = podaci.caps_procenat + '%';
    document.getElementById('vrednost-interpunkcija').textContent = podaci.interpunkcija + '%';

    prikaziIndikator(podaci);
}

async function pokreniAnalizu() {
    const tekst = document.getElementById('tekst').value.trim();
    if (!tekst) return;

    const t = prevodi[trenutniJezik];
    const dugme = document.querySelector('.dugme-analiziraj');
    dugme.textContent = t.analiziranje;
    dugme.disabled = true;

    try {
        const odgovor = await fetch('/analiziraj', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ tekst })
        });

        const podaci = await odgovor.json();

        prikaziRezultate(podaci);

        dodajUIstoriju(tekst, podaci);

    } catch (e) {
        console.error('Greška:', e);
    } finally {
        dugme.textContent = t.pokreniAnalizu;
        dugme.disabled = false;
    }
}

function dodajUIstoriju(tekst, podaci) {
    istorijaNiz.unshift({ tekst, podaci });
    renderIstorija();
}

function renderIstorija() {
    const t = prevodi[trenutniJezik];
    const kontejner = document.getElementById('istorija');
    kontejner.innerHTML = '';

    istorijaNiz.forEach((stavka) => {
        const el = document.createElement('div');
        el.className = 'istorija-stavka';

        el.onclick = () => {
            document.getElementById('tekst').value = stavka.tekst;
            prikaziRezultate(stavka.podaci);
        };

        const klasaBoje = stavka.podaci.kategorija === 'SPAM' ? 'je-spam'
                        : stavka.podaci.kategorija === 'SUMNJIVO' ? 'je-sumnjivo'
                        : 'je-legitiman';

        el.innerHTML = `
            <div class="ist-score ${klasaBoje}">${stavka.podaci.spam_score}%</div>
            <div class="ist-tekst">${stavka.tekst.substring(0, 40)}...</div>
        `;
        kontejner.appendChild(el);
    });
}

primeniJezik();