const prevodi = {
    sr: {
        novaProvera: 'Nova provera',
        primerProvera: 'Nasumičan primer',
        teskiPrimer: 'Težak primer',
        prethodneProvere: 'Prethodne provere',
        placeholder: 'Nalepite tekst emaila ovde...',
        pokreniAnalizu: 'Pokreni analizu',
        analiziranje: 'Analiziram...',
        rezultat: 'Rezultat',
        praznoStanje: 'Nalepite email da vidite rezultat.',
        emailTekst: 'Tekst emaila',
        znakova: 'znakova',
        kopiraj: 'Kopiraj rezultat',
        kopirano: 'Kopirano',
        ocisti: 'očisti',
        tabZasto: 'Zašto',
        tabUlazi: 'Ulazi',
        tabPravila: 'Pravila',
        gdeJePokrenuto: 'Gde je pokrenuto',
        pokriveneReci: 'Prepoznate reči',
        ulaziNaslov: 'Ulazi i pripadnosti',
        ulaz: 'ulaz',
        vrednost: 'vrednost',
        pripadnosti: 'pripadnosti',
        aktivnaPravila: 'Aktivna pravila',
        nemaObjasnjenja: 'Nema dovoljno signala za objašnjenje.',
        izvorRucni: 'ručni rečnik',
        izvorNauceni: 'naučeni rečnik',
        jacina: 'jačina',
        kljucneReci: 'KLJUČNE REČI',
        brojLinkova: 'BROJ LINKOVA',
        caps: 'CAPS',
        interpunkcija: 'INTERPUNKCIJA',
        istorijaPrazna: 'Još nema provera.',
        greskaPrazno: 'Unesite tekst emaila.',
        greskaMreza: 'Greška u komunikaciji sa serverom.',
        temaSvetla: 'Prebaci na svetlu temu',
        temaTamna: 'Prebaci na tamnu temu',
        sada: 'sada',
        kategorije: { SPAM: 'SPAM', SUMNJIVO: 'SUMNJIVO', LEGITIMAN: 'LEGITIMAN' },
        ulaziNazivi: {
            kljucne_reci: 'ključne reči',
            broj_linkova: 'linkovi',
            caps_procenat: 'velika slova',
            interpunkcija: 'interpunkcija'
        },
        dugmeJezik: 'English'
    },
    en: {
        novaProvera: 'New check',
        primerProvera: 'Random sample',
        teskiPrimer: 'Hard sample',
        prethodneProvere: 'Previous checks',
        placeholder: 'Write or paste the email text here...',
        pokreniAnalizu: 'Run analysis',
        analiziranje: 'Analyzing...',
        rezultat: 'Verdict',
        praznoStanje: 'Paste an email to see the verdict.',
        emailTekst: 'Email text',
        znakova: 'chars',
        kopiraj: 'Copy result',
        kopirano: 'Copied',
        ocisti: 'clear',
        tabZasto: 'Why',
        tabUlazi: 'Inputs',
        tabPravila: 'Rules',
        gdeJePokrenuto: 'Where it was triggered',
        pokriveneReci: 'Matched words',
        ulaziNaslov: 'Inputs and memberships',
        ulaz: 'input',
        vrednost: 'value',
        pripadnosti: 'memberships',
        aktivnaPravila: 'Active rules',
        nemaObjasnjenja: 'Not enough signal to explain.',
        izvorRucni: 'hand dictionary',
        izvorNauceni: 'learned lexicon',
        jacina: 'strength',
        kljucneReci: 'KEYWORDS',
        brojLinkova: 'LINK COUNT',
        caps: 'CAPS',
        interpunkcija: 'PUNCTUATION',
        istorijaPrazna: 'No checks yet.',
        greskaPrazno: 'Please enter email text.',
        greskaMreza: 'Could not reach the server.',
        temaSvetla: 'Switch to light theme',
        temaTamna: 'Switch to dark theme',
        sada: 'now',
        kategorije: { SPAM: 'SPAM', SUMNJIVO: 'SUSPICIOUS', LEGITIMAN: 'LEGITIMATE' },
        ulaziNazivi: {
            kljucne_reci: 'keywords',
            broj_linkova: 'links',
            caps_procenat: 'caps',
            interpunkcija: 'punctuation'
        },
        dugmeJezik: 'Srpski'
    }
};

function ucitajLokalno(kljuc) {
    try { return localStorage.getItem(kljuc); } catch (e) { return null; }
}

function sacuvajLokalno(kljuc, vrednost) {
    try { localStorage.setItem(kljuc, vrednost); } catch (e) { /* ignore */ }
}

let trenutniJezik = ucitajLokalno('fg-jezik') || 'en';
let trenutnaTema = ucitajLokalno('fg-tema') || 'dark';
let trenutniPodaci = null;
let trenutniTab = 'zasto';
let istorijaNiz = [];
let spektarDefinicije = null;

function escapeHtml(tekst) {
    return String(tekst)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
}

function klasaKategorije(kategorija) {
    return kategorija === 'SPAM' ? 'je-spam'
         : kategorija === 'SUMNJIVO' ? 'je-sumnjivo'
         : 'je-legitiman';
}

/* --- tema i jezik ------------------------------------------------------ */

function primeniTemu() {
    document.documentElement.dataset.theme = trenutnaTema;
    const dugme = document.getElementById('tema-dugme');
    const t = prevodi[trenutniJezik];
    dugme.textContent = trenutnaTema === 'dark' ? '☀' : '☾';
    dugme.title = trenutnaTema === 'dark' ? t.temaSvetla : t.temaTamna;
    sacuvajLokalno('fg-tema', trenutnaTema);
}

function promeniTemu() {
    trenutnaTema = trenutnaTema === 'dark' ? 'light' : 'dark';
    primeniTemu();
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

    document.querySelectorAll('[data-i18n-title]').forEach(el => {
        const kljuc = el.getAttribute('data-i18n-title');
        if (t[kljuc] !== undefined) el.title = t[kljuc];
    });

    document.querySelectorAll('[data-i18n-aria]').forEach(el => {
        const kljuc = el.getAttribute('data-i18n-aria');
        if (t[kljuc] !== undefined) el.setAttribute('aria-label', t[kljuc]);
    });

    document.getElementById('jezik-dugme').textContent = t.dugmeJezik;
    document.documentElement.lang = trenutniJezik;

    const dugme = document.querySelector('.dugme-analiziraj');
    if (dugme && !dugme.disabled) dugme.textContent = t.pokreniAnalizu;

    if (trenutniPodaci) renderTab();
    renderIstorija();
    primeniTemu();
    sacuvajLokalno('fg-jezik', trenutniJezik);
}

function promeniJezik() {
    trenutniJezik = trenutniJezik === 'sr' ? 'en' : 'sr';
    primeniJezik();
}

function toggleMeni() {
    const sadrzaj = document.getElementById('sidebar-sadrzaj');
    const dugme = document.getElementById('meni-dugme');
    const otvoren = sadrzaj.classList.toggle('otvoren');
    dugme.setAttribute('aria-expanded', otvoren ? 'true' : 'false');
    dugme.textContent = otvoren ? '✕' : '☰';
}

/* --- primeri ----------------------------------------------------------- */

let primeriKes = { en: [], sr: [] };
let preostaliIndeksi = { en: [], sr: [] };
let teskiKes = { en: [], sr: [] };
let preostaliTeski = { en: [], sr: [] };

function promesaj(niz) {
    const kopija = [...niz];
    for (let i = kopija.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [kopija[i], kopija[j]] = [kopija[j], kopija[i]];
    }
    return kopija;
}

async function ucitajPrimer(teski) {
    const jezik = trenutniJezik;
    const kes = teski ? teskiKes : primeriKes;
    const preostali = teski ? preostaliTeski : preostaliIndeksi;
    const putanja = teski ? '/primeri-teski' : '/primeri-svi';

    if (kes[jezik].length === 0) {
        const odgovor = await fetch(putanja + '?jezik=' + jezik);
        const podaci = await odgovor.json();
        kes[jezik] = podaci.primeri || [];
    }

    if (kes[jezik].length === 0) return;

    if (preostali[jezik].length === 0) {
        preostali[jezik] = promesaj([...Array(kes[jezik].length).keys()]);
    }

    const indeks = preostali[jezik].pop();
    const tekst = kes[jezik][indeks];
    document.getElementById('tekst').value = tekst;
    document.getElementById('broj-znakova').textContent = tekst.length;
    resetujRezultate();
    skloniPoruku();
}

function ucitajRandom() {
    return ucitajPrimer(false);
}

function ucitajTeski() {
    return ucitajPrimer(true);
}

/* --- unos i stanje ----------------------------------------------------- */

function naUnos() {
    const tekst = document.getElementById('tekst').value;
    document.getElementById('broj-znakova').textContent = tekst.length;
    if (trenutniPodaci) resetujRezultate();
    skloniPoruku();
}

function novaProvera() {
    document.getElementById('tekst').value = '';
    document.getElementById('broj-znakova').textContent = '0';
    resetujRezultate();
    skloniPoruku();
    document.getElementById('tekst').focus();
}

function prikaziPoruku(poruka) {
    const el = document.getElementById('poruka');
    el.textContent = poruka;
    el.hidden = false;
}

function skloniPoruku() {
    document.getElementById('poruka').hidden = true;
}

function resetujRezultate() {
    trenutniPodaci = null;
    document.getElementById('verdict-sadrzaj').hidden = true;
    document.getElementById('verdict-prazno').hidden = false;
    document.getElementById('tab-sadrzaj').innerHTML = '';
    document.getElementById('spektar').innerHTML = '';
    document.getElementById('spektar-oznake').innerHTML = '';
    document.getElementById('dugme-kopiraj').disabled = true;
}

/* --- analiza ----------------------------------------------------------- */

async function pokreniAnalizu() {
    const tekst = document.getElementById('tekst').value.trim();
    const t = prevodi[trenutniJezik];

    if (!tekst) {
        prikaziPoruku(t.greskaPrazno);
        document.getElementById('tekst').focus();
        return;
    }

    skloniPoruku();
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

        if (!odgovor.ok) {
            prikaziPoruku(podaci.greska || t.greskaMreza);
            return;
        }

        prikaziRezultate(podaci);
        dodajUIstoriju(tekst, podaci);
    } catch (e) {
        prikaziPoruku(t.greskaMreza);
    } finally {
        dugme.textContent = t.pokreniAnalizu;
        dugme.disabled = false;
    }
}

function prikaziRezultate(podaci) {
    trenutniPodaci = podaci;

    document.getElementById('verdict-prazno').hidden = true;
    document.getElementById('verdict-sadrzaj').hidden = false;

    const skor = document.getElementById('vrednost-score');
    skor.textContent = podaci.spam_score + '%';
    skor.className = 'skor ' + klasaKategorije(podaci.kategorija);

    const indikator = document.getElementById('indikator-score');
    indikator.textContent = prevodi[trenutniJezik].kategorije[podaci.kategorija] || podaci.kategorija;
    indikator.className = 'kategorija ' + klasaKategorije(podaci.kategorija);

    document.getElementById('dugme-kopiraj').disabled = false;

    nacrtajSpektar(podaci.spam_score);

    trenutniTab = 'zasto';
    document.querySelectorAll('.tab').forEach(btn => {
        const aktivan = btn.dataset.tab === 'zasto';
        btn.classList.toggle('aktivan', aktivan);
        btn.setAttribute('aria-selected', aktivan ? 'true' : 'false');
    });
    renderTab();
}

/* --- fuzzy spektar ----------------------------------------------------- */

async function ucitajSpektar() {
    try {
        const odgovor = await fetch('/skupovi');
        const podaci = await odgovor.json();
        spektarDefinicije = podaci.skupovi || null;
        if (trenutniPodaci) nacrtajSpektar(trenutniPodaci.spam_score);
    } catch (e) {
        spektarDefinicije = null;
    }
}

function pripadnost(tip, params, x) {
    if (tip === 'trimf') {
        const [a, b, c] = params;
        if (x <= a || x >= c) return 0;
        if (x === b) return 1;
        return x < b ? (x - a) / (b - a) : (c - x) / (c - b);
    }
    const [a, b, c, d] = params;
    if (x <= a || x >= d) return 0;
    if (x >= b && x <= c) return 1;
    return x < b ? (x - a) / (b - a) : (d - x) / (d - c);
}

function bojaZa(kategorija) {
    return kategorija === 'SPAM' ? 'var(--spam)'
         : kategorija === 'SUMNJIVO' ? 'var(--suspicious)'
         : 'var(--legit)';
}

function nacrtajSpektar(score) {
    const svg = document.getElementById('spektar');
    if (!spektarDefinicije) {
        svg.innerHTML = '';
        document.getElementById('spektar-oznake').innerHTML = '';
        return;
    }

    const w = 400;
    const h = 92;
    const padX = 4;
    const padY = 8;
    const osnova = h - padY;
    const xZa = v => padX + (v / 100) * (w - 2 * padX);
    const yZa = m => osnova - m * (h - 2 * padY);

    let aktivni = null;
    let najveca = -1;
    spektarDefinicije.forEach(skup => {
        const m = pripadnost(skup.tip, skup.params, score);
        if (m > najveca) {
            najveca = m;
            aktivni = skup.ime;
        }
    });

    let html = `<line class="spektar-osnova" x1="${padX}" y1="${osnova}" x2="${w - padX}" y2="${osnova}"/>`;

    spektarDefinicije.forEach(skup => {
        const boja = bojaZa(skup.kategorija);
        const aktivan = skup.ime === aktivni;
        let d = `M ${xZa(0).toFixed(2)} ${osnova}`;
        for (let v = 0; v <= 100; v += 1) {
            d += ` L ${xZa(v).toFixed(2)} ${yZa(pripadnost(skup.tip, skup.params, v)).toFixed(2)}`;
        }
        d += ` L ${xZa(100).toFixed(2)} ${osnova} Z`;
        html += `<path d="${d}" fill="${boja}" ` +
                `fill-opacity="${aktivan ? 0.32 : 0.08}" ` +
                `stroke="${boja}" stroke-opacity="${aktivan ? 0.95 : 0.35}" ` +
                `stroke-width="${aktivan ? 1.6 : 0.8}"/>`;
    });

    const x = xZa(score);
    html += `<line class="spektar-igla" x1="${x.toFixed(2)}" y1="${padY - 2}" x2="${x.toFixed(2)}" y2="${osnova}"/>`;
    html += `<circle class="spektar-tocka" cx="${x.toFixed(2)}" cy="${osnova}" r="3"/>`;
    svg.innerHTML = html;

    document.getElementById('spektar-oznake').innerHTML = spektarDefinicije.map(skup => {
        const klasa = skup.ime === aktivni ? 'aktivna' : '';
        return `<span class="spektar-oznaka ${klasa}" style="--boja:${bojaZa(skup.kategorija)}">` +
               `${escapeHtml(skup.naziv)}</span>`;
    }).join('');
}

/* --- tabovi i objasnjenje --------------------------------------------- */

function promeniTab(tab) {
    trenutniTab = tab;
    document.querySelectorAll('.tab').forEach(btn => {
        const aktivan = btn.dataset.tab === tab;
        btn.classList.toggle('aktivan', aktivan);
        btn.setAttribute('aria-selected', aktivan ? 'true' : 'false');
    });
    renderTab();
}

function renderTab() {
    const kontejner = document.getElementById('tab-sadrzaj');
    if (!trenutniPodaci) {
        kontejner.innerHTML = '';
        return;
    }
    if (trenutniTab === 'ulazi') {
        kontejner.innerHTML = napraviUlaze(trenutniPodaci);
    } else if (trenutniTab === 'pravila') {
        kontejner.innerHTML = napraviPravila(trenutniPodaci);
    } else {
        kontejner.innerHTML = napraviZasto(trenutniPodaci);
    }
}

function napraviPregled(tekst, reci) {
    const ogranicen = tekst.length > 1200 ? tekst.slice(0, 1200) : tekst;
    const pozicije = [];
    (reci || []).forEach(stavka => {
        (stavka.pozicije || []).forEach(pozicija => pozicije.push(pozicija));
    });
    pozicije.sort((a, b) => a[0] - b[0]);

    let html = '';
    let poz = 0;
    for (const [pocetak, kraj] of pozicije) {
        if (pocetak < poz || pocetak > ogranicen.length) continue;
        html += escapeHtml(ogranicen.slice(poz, pocetak));
        html += '<mark class="obj-mark">' + escapeHtml(ogranicen.slice(pocetak, kraj)) + '</mark>';
        poz = kraj;
    }
    html += escapeHtml(ogranicen.slice(poz));
    if (tekst.length > ogranicen.length) html += '…';
    return html;
}

function napraviZasto(podaci) {
    const t = prevodi[trenutniJezik];
    const objasnjenje = podaci.objasnjenje || {};
    const reci = objasnjenje.pokrivene_reci || [];

    if (!objasnjenje.tekst && !reci.length) {
        return `<div class="obj-prazno">${t.nemaObjasnjenja}</div>`;
    }

    let html = '';

    if (objasnjenje.tekst) {
        html += `<div class="obj-podnaslov">${t.gdeJePokrenuto}</div>`;
        html += `<div class="obj-pregled">${napraviPregled(objasnjenje.tekst, reci)}</div>`;
    }

    if (reci.length) {
        html += `<div class="obj-podnaslov">${t.pokriveneReci}</div><div class="obj-cipovi">`;
        reci.forEach(stavka => {
            const izvor = stavka.izvor === 'nauceni' ? t.izvorNauceni : t.izvorRucni;
            const tezina = Number(stavka.tezina).toFixed(2);
            const puta = stavka.broj > 1 ? ` ×${stavka.broj}` : '';
            html += `<span class="obj-cip" title="${izvor} · ${tezina}">` +
                    `${escapeHtml(stavka.rec)}${puta}</span>`;
        });
        html += '</div>';
    }

    return html;
}

function napraviUlaze(podaci) {
    const t = prevodi[trenutniJezik];
    const ulazi = (podaci.objasnjenje || {}).ulazi || {};
    const imena = Object.keys(ulazi);

    if (!imena.length) return `<div class="obj-prazno">${t.nemaObjasnjenja}</div>`;

    let html = '<table class="obj-tabela"><thead><tr>' +
        `<th>${t.ulaz}</th><th>${t.vrednost}</th><th>${t.pripadnosti}</th>` +
        '</tr></thead><tbody>';

    imena.forEach(ime => {
        const podatak = ulazi[ime] || {};
        const naziv = (t.ulaziNazivi && t.ulaziNazivi[ime]) || ime;
        const pripadnosti = Object.entries(podatak.pripadnosti || {})
            .filter(([, w]) => Number(w) > 0.05)
            .map(([kljuc, w]) => `${kljuc} ${Number(w).toFixed(2)}`)
            .join(', ');
        html += `<tr><td>${naziv}</td><td>${podatak.vrednost}</td>` +
                `<td>${pripadnosti || '—'}</td></tr>`;
    });

    return html + '</tbody></table>';
}

function napraviPravila(podaci) {
    const t = prevodi[trenutniJezik];
    const pravila = (podaci.objasnjenje || {}).aktivna_pravila || [];

    if (!pravila.length) return `<div class="obj-prazno">${t.nemaObjasnjenja}</div>`;

    let html = '<ul class="obj-pravila">';
    pravila.forEach(stavka => {
        const uslov = trenutniJezik === 'sr' ? stavka.uslov_sr : stavka.uslov_en;
        const klasa = klasaKategorije(stavka.kategorija);
        const naziv = t.kategorije[stavka.kategorija] || stavka.kategorija;
        html += `<li><span class="obj-pravilo">${stavka.pravilo}</span>` +
                `<span class="obj-uslov">${escapeHtml(uslov || '')}</span>` +
                `<span class="obj-jacina">${t.jacina} ${Number(stavka.jacina).toFixed(2)}</span>` +
                `<span class="obj-kat ${klasa}">${naziv}</span></li>`;
    });
    return html + '</ul>';
}

/* --- kopiranje --------------------------------------------------------- */

async function kopirajRezultat() {
    if (!trenutniPodaci) return;

    const t = prevodi[trenutniJezik];
    const p = trenutniPodaci;
    const objasnjenje = p.objasnjenje || {};

    const linije = [
        'Fuzzy Guard',
        `${t.rezultat}: ${p.spam_score}% (${t.kategorije[p.kategorija] || p.kategorija})`,
        `${t.kljucneReci}: ${p.kljucne_reci} | ${t.brojLinkova}: ${p.broj_linkova} | ` +
        `${t.caps}: ${p.caps_procenat}% | ${t.interpunkcija}: ${p.interpunkcija}%`
    ];

    const reci = (objasnjenje.pokrivene_reci || []).map(stavka => stavka.rec);
    if (reci.length) linije.push(`${t.pokriveneReci}: ${reci.join(', ')}`);

    const pravila = (objasnjenje.aktivna_pravila || [])
        .map(stavka => `${stavka.pravilo} (${Number(stavka.jacina).toFixed(2)})`);
    if (pravila.length) linije.push(`${t.aktivnaPravila}: ${pravila.join(', ')}`);

    const tekst = linije.join('\n');
    let uspelo = false;

    try {
        if (navigator.clipboard && window.isSecureContext) {
            await navigator.clipboard.writeText(tekst);
            uspelo = true;
        }
    } catch (e) {
        uspelo = false;
    }

    if (!uspelo) {
        const polje = document.createElement('textarea');
        polje.value = tekst;
        polje.style.position = 'fixed';
        polje.style.opacity = '0';
        document.body.appendChild(polje);
        polje.select();
        try { uspelo = document.execCommand('copy'); } catch (e) { uspelo = false; }
        document.body.removeChild(polje);
    }

    const dugme = document.getElementById('dugme-kopiraj');
    if (uspelo) {
        dugme.textContent = '✓';
        setTimeout(() => { dugme.textContent = '⧉'; }, 1400);
    }
}

/* --- istorija ---------------------------------------------------------- */

function relativnoVreme(vreme) {
    const t = prevodi[trenutniJezik];
    const sekunde = Math.floor((Date.now() - vreme) / 1000);
    if (sekunde < 45) return t.sada;
    const minuti = Math.floor(sekunde / 60);
    if (minuti < 60) return `${minuti} min`;
    const sati = Math.floor(minuti / 60);
    if (sati < 24) return `${sati} h`;
    return `${Math.floor(sati / 24)} d`;
}

function dodajUIstoriju(tekst, podaci) {
    istorijaNiz.unshift({ tekst, podaci, vreme: Date.now() });
    istorijaNiz = istorijaNiz.slice(0, 12);
    renderIstorija();
}

function renderIstorija() {
    const t = prevodi[trenutniJezik];
    const kontejner = document.getElementById('istorija');
    kontejner.innerHTML = '';

    if (!istorijaNiz.length) {
        kontejner.innerHTML = `<div class="istorija-prazna">${t.istorijaPrazna}</div>`;
        return;
    }

    istorijaNiz.forEach(stavka => {
        const el = document.createElement('button');
        el.type = 'button';
        el.className = 'istorija-stavka';
        el.onclick = () => {
            document.getElementById('tekst').value = stavka.tekst;
            document.getElementById('broj-znakova').textContent = stavka.tekst.length;
            prikaziRezultate(stavka.podaci);
            skloniPoruku();
        };

        const klasa = klasaKategorije(stavka.podaci.kategorija);
        el.innerHTML = `<span class="istorija-skore ${klasa}">${stavka.podaci.spam_score}%</span>` +
            `<span class="istorija-tekst">${escapeHtml(stavka.tekst.slice(0, 42))}</span>` +
            `<span class="istorija-vreme">${relativnoVreme(stavka.vreme)}</span>`;
        kontejner.appendChild(el);
    });
}

function ocistiIstoriju() {
    istorijaNiz = [];
    renderIstorija();
}

/* --- init -------------------------------------------------------------- */

document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        pokreniAnalizu();
    } else if (e.key === 'Escape') {
        novaProvera();
    }
});

primeniTemu();
primeniJezik();
renderIstorija();
ucitajSpektar();
