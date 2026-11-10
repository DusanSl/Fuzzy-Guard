

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

function pomoc(kljuc, naslov, tekst) {
    return `<span class="pomoc">
        <button class="pomoc-dugme" type="button" aria-expanded="false" aria-controls="pomoc-${pobjegni(kljuc)}" aria-label="${pobjegni(naslov)}">?</button>
        <span class="pomoc-panel" id="pomoc-${pobjegni(kljuc)}" role="tooltip" hidden><b>${pobjegni(naslov)}</b>${pobjegni(tekst)}</span>
    </span>`;
}

function zatvoriPomoc(osim) {
    document.querySelectorAll('.pomoc-dugme[aria-expanded="true"]').forEach(dugme => {
        if (dugme === osim) return;
        dugme.setAttribute('aria-expanded', 'false');
        const panel = document.getElementById(dugme.getAttribute('aria-controls'));
        if (!panel) return;
        panel.hidden = true;
        panel.style.position = '';
        panel.style.top = '';
        panel.style.left = '';
    });
}

function pozicionirajPomoc(dugme, panel) {
    const dugmeRect = dugme.getBoundingClientRect();
    const panelRect = panel.getBoundingClientRect();
    const margina = 8;
    let top = dugmeRect.bottom + 7;
    if (top + panelRect.height > window.innerHeight - margina) {
        top = Math.max(margina, dugmeRect.top - panelRect.height - 7);
    }
    const left = Math.max(margina, Math.min(dugmeRect.left, window.innerWidth - panelRect.width - margina));
    panel.style.position = 'fixed';
    panel.style.top = `${top}px`;
    panel.style.left = `${left}px`;
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
const UZORAK_RAZMAKA = /\s/;
async function izracunajRezultat(tekst) {
    await ucitajSkupove();

    const odgovor = await fetch('/analiziraj', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tekst, recnik: 'auto' })
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
        },
        nn_pouzdanje: {
            nisko: 'nn_nisko',
            srednje: 'nn_srednje',
            visoko: 'nn_visoko'
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
        interpunkcija: podaci.interpunkcija,
        nn_pouzdanje: podaci.nn_pouzdanje ?? 50
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
        recnik: podaci.recnik || null,
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
    const redosled = ['kljucne_reci', 'broj_linkova', 'caps_procenat', 'interpunkcija', 'nn_pouzdanje'];

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
        const aktivan = dugme.dataset.pogled === trenutniPogled;
        dugme.setAttribute('aria-selected', aktivan ? 'true' : 'false');
        dugme.tabIndex = aktivan ? 0 : -1;
        if (aktivan && dugme.id) kontejner.setAttribute('aria-labelledby', dugme.id);
    });
}

function napraviZasto(rezultat) {
    const elementi = [];
    const pregled = napraviPregled(rezultat);

    elementi.push(`<div class="pogled-naslov-red"><p class="pogled-naslov">${pobjegni(t().doprinosiNaslov)}</p>${pomoc('doprinosi', t().pomocDoprinosiNaslov, t().pomocDoprinosi)}</div>`);
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
            const uzorak = tipovi.map(tip => `legenda-uzorak--${tip}`).join(' ');
            return `<span><i class="legenda-uzorak ${uzorak}"></i>${pobjegni(tipovi.map(tip => t().legenda[tip]).join(' + '))}</span>`;
        }).join('') + '</div>');
    }

    elementi.push(`<div class="pogled-naslov-red" style="margin-top:13px"><p class="pogled-naslov">${pobjegni(t().prepoznate)}</p>${pomoc('tezine', t().pomocTezineNaslov, t().pomocTezine)}</div>`);

    if (rezultat.recnik) {
        const nazivRecnika = t()[rezultat.recnik] || rezultat.recnik;
        elementi.push(`<p class="leksikon-status"><span>${pobjegni(t().recnik)}: ${pobjegni(nazivRecnika)} (${pobjegni(t().recnikAuto)})</span> ${pomoc('recnik', t().pomocRecnikNaslov, t().pomocRecnik)}</p>`);
    }

    if (rezultat.pogodjene.length) {
        elementi.push('<div class="cipovi">' + rezultat.pogodjene.map(stavka => {
            const izvor = stavka.izvor === 'en' ? t().izvorEn
                : stavka.izvor === 'sr' ? t().izvorSr : t().izvorRucni;
            const ukupno = stavka.tezina * stavka.broj;
            return `<span class="cip" title="${pobjegni(izvor)} · ${pobjegni(t().tezinaPoPogotku)} ${formatirajBroj(stavka.tezina)}">` +
                   `${pobjegni(stavka.rec)}${stavka.broj > 1 ? ` <b>×${stavka.broj}</b>` : ''}` +
                   ` <b class="cip-tezina">+${formatirajBroj(ukupno)}</b></span>`;
        }).join('') + '</div>');

        const siroviZbir = rezultat.pogodjene.reduce((zbir, stavka) => zbir + stavka.tezina * stavka.broj, 0);
        const prikazZbira = Number(rezultat.vrednosti.kljucne_reci) || 0;
        const dodatak = siroviZbir > prikazZbira + 0.05
            ? ` <span>(${pobjegni(t().siroviZbir)} ${pobjegni(formatirajBroj(siroviZbir))})</span>`
            : '';
        elementi.push(`<p class="zbir-tezina">${pobjegni(t().zbirTezina)}: <b>${pobjegni(formatirajBroj(prikazZbira))} / 10</b>${dodatak}</p>`);
    } else {
        elementi.push(`<p class="tiho">${pobjegni(t().nemaPogodaka)}</p>`);
    }

    return elementi.join('');
}

function napraviDoprinose(rezultat) {
    const redosled = ['kljucne_reci', 'broj_linkova', 'caps_procenat', 'interpunkcija', 'nn_pouzdanje'];

    return '<div class="doprinosi">' + redosled.map(kljuc => {
        const vrednost = rezultat.vrednosti[kljuc];
        const pripadnosti = rezultat.mu[kljuc] || {};
        const najjaci = Object.keys(pripadnosti).reduce((najbolji, ime) => {
            const mu = Number(pripadnosti[ime]) || 0;
            return mu > najbolji.mu ? { ime, mu } : najbolji;
        }, { ime: '', mu: -1 });
        const skup = najjaci.ime ? (t().skupovi[najjaci.ime] || najjaci.ime) : '—';
        const mu = najjaci.mu >= 0 ? formatirajDva(najjaci.mu) : '—';

        return `<div class="doprinos">
            <span class="doprinos-signal">${pobjegni(t().signali[kljuc])}</span>
            <span class="doprinos-vrednost">${pobjegni(formatirajBroj(vrednost))}<small>${pobjegni(t().jedinice[kljuc])}</small></span>
            <span class="doprinos-skup">${pobjegni(skup)} <b>${pobjegni(mu)}</b></span>
        </div>`;
    }).join('') + '</div>';
}

const OZNAKA_BIT = { keyword: 1, link: 2, caps: 4, interpunkcija: 8 };
const OZNAKA_REDOSLED = ['keyword', 'link', 'caps', 'interpunkcija'];
const KES_KLJUCA_OZNAKA = new Map();

function kljucOznake(maska) {
    const zapamcen = KES_KLJUCA_OZNAKA.get(maska);
    if (zapamcen !== undefined) return zapamcen;
    const kljuc = OZNAKA_REDOSLED.filter(tip => maska & OZNAKA_BIT[tip]).join('+');
    KES_KLJUCA_OZNAKA.set(maska, kljuc);
    return kljuc;
}

function izracunajOznake(rezultat) {
    const tekst = rezultat.vidljivi || '';
    // Uint8Array umesto niza Set-ova: dug email ne pravi po jednu alokaciju
    // za svaki obeleženi znak. Redosled bitova je isti kao u legendi.
    const oznake = new Uint8Array(tekst.length);
    const dodaj = (od, do_, tip) => {
        const bit = OZNAKA_BIT[tip];
        const pocetak = Math.max(0, od);
        const kraj = Math.min(tekst.length, do_);
        for (let indeks = pocetak; indeks < kraj; indeks += 1) {
            if (UZORAK_RAZMAKA.test(tekst[indeks])) continue;
            oznake[indeks] |= bit;
        }
    };

    (rezultat.pogodjene || []).forEach(stavka => {
        (stavka.pozicije || []).forEach(pozicija => dodaj(pozicija[0], pozicija[1], 'keyword'));
    });

    [['link', UZORAK_LINKA], ['caps', UZORAK_CAPS], ['interpunkcija', UZORAK_INTERPUNKCIJA]].forEach(([tip, uzorak]) => {
        let broj = 0;
        for (const poklapanje of tekst.matchAll(uzorak)) {
            dodaj(poklapanje.index, poklapanje.index + poklapanje[0].length, tip);
            broj += 1;
            if (broj >= 50) break;
        }
    });

    const kombinacije = new Set();
    for (let indeks = 0; indeks < oznake.length; indeks += 1) {
        if (oznake[indeks]) kombinacije.add(kljucOznake(oznake[indeks]));
    }

    return { tekst, oznake, kombinacije };
}

function napraviPregled(rezultat) {
    const { tekst, oznake, kombinacije } = izracunajOznake(rezultat);
    let html = '';
    let indeks = 0;

    while (indeks < tekst.length) {
        const maska = oznake[indeks];
        if (!maska) {
            let kraj = indeks + 1;
            while (kraj < tekst.length && !oznake[kraj]) kraj += 1;
            html += pobjegni(tekst.slice(indeks, kraj));
            indeks = kraj;
            continue;
        }

        const kljuc = kljucOznake(maska);
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
    const redosled = ['kljucne_reci', 'broj_linkova', 'caps_procenat', 'interpunkcija', 'nn_pouzdanje'];

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
                <span class="pravilo-id">${pobjegni(pravilo.naziv)}</span>
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
            const rezultat = await izracunajRezultat(tekst);
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

        const rezultat = await izracunajRezultat(uzorak.tekst);
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

        const rezultat = await izracunajRezultat(uzorak.tekst);
        prikaziRezultat(rezultat, { animiraj: true });
        dodajUIstoriju(uzorak.tekst, uzorak.posaljilac, uzorak.tema, rezultat);
    } catch (greska) {
        prikaziGresku(greska.message || t().greskaMreza);
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
        `${recnik.signali.interpunkcija}: ${formatirajBroj(rezultat.vrednosti.interpunkcija)}% | ` +
        `${recnik.signali.nn_pouzdanje}: ${formatirajBroj(rezultat.vrednosti.nn_pouzdanje ?? 50)}%`
    ];

    if (rezultat.recnik) {
        linije.push(`${recnik.recnik}: ${recnik[rezultat.recnik] || rezultat.recnik} (${recnik.recnikAuto})`);
    }
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
    document.getElementById('marka').addEventListener('click', dogadjaj => dogadjaj.preventDefault());
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

    const tabovi = [...document.querySelectorAll('.segment-pogled [data-pogled]')];
    tabovi.forEach((dugme, indeks) => {
        dugme.addEventListener('click', () => postaviPogled(dugme.dataset.pogled));
        dugme.addEventListener('keydown', dogadjaj => {
            if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(dogadjaj.key)) return;
            dogadjaj.preventDefault();
            let novi = indeks;
            if (dogadjaj.key === 'ArrowLeft') novi = (indeks - 1 + tabovi.length) % tabovi.length;
            if (dogadjaj.key === 'ArrowRight') novi = (indeks + 1) % tabovi.length;
            if (dogadjaj.key === 'Home') novi = 0;
            if (dogadjaj.key === 'End') novi = tabovi.length - 1;
            tabovi[novi].focus();
            postaviPogled(tabovi[novi].dataset.pogled);
        });
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

    document.addEventListener('click', dogadjaj => {
        const dugme = dogadjaj.target.closest('.pomoc-dugme');
        if (dugme) {
            const otvoreno = dugme.getAttribute('aria-expanded') === 'true';
            zatvoriPomoc();
            if (!otvoreno) {
                dugme.setAttribute('aria-expanded', 'true');
                const panel = document.getElementById(dugme.getAttribute('aria-controls'));
                if (panel) {
                    panel.hidden = false;
                    pozicionirajPomoc(dugme, panel);
                }
            }
            return;
        }
        if (!dogadjaj.target.closest('.pomoc')) zatvoriPomoc();
    });

    window.addEventListener('scroll', () => zatvoriPomoc(), true);
    window.addEventListener('resize', () => zatvoriPomoc());

    document.addEventListener('keydown', dogadjaj => {
        if (dogadjaj.key === 'Escape') zatvoriPomoc();
        if ((dogadjaj.metaKey || dogadjaj.ctrlKey) && dogadjaj.key === 'Enter') {
            dogadjaj.preventDefault();
            pokreniAnalizu();
        }
    });
}

async function inicijalizuj() {
    if (!['en', 'sr'].includes(jezik)) jezik = 'en';
    if (!['dark', 'light'].includes(tema)) tema = 'dark';

    try { await ucitajSkupove(); } catch (greska) { /* spektar ostaje prazan */ }
    nacrtajSpektar(document.getElementById('spektar-prazno'), null, { priguseno: true });

    poveziDogadjaje();
    primeniJezik();

    const uzorakLegitiman = UZORCI.legitiman[0];
    const uzorakSumnjiv = UZORCI.sumnjiv[0];
    const uzorakPrevara = UZORCI.prevara[0];

    try {
        const [rezultatLegitiman, rezultatSumnjiv, rezultatPrevara] = await Promise.all([
            izracunajRezultat(uzorakLegitiman.tekst),
            izracunajRezultat(uzorakSumnjiv.tekst),
            izracunajRezultat(uzorakPrevara.tekst)
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