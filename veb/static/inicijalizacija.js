/* Primenjuje sačuvanu temu i jezik pre prvog iscrtavanja, da stranica ne bi
   treperila. Fajl je odvojen od dashboard.html zato što Content-Security-Policy
   dozvoljava samo skripte sa istog porekla (script-src 'self'). */

try {
    var sacuvanaTema = localStorage.getItem('fg-prototip-tema-v2');
    if (sacuvanaTema === 'light' || sacuvanaTema === 'dark') {
        document.documentElement.dataset.theme = sacuvanaTema;
    }
    var sacuvanJezik = localStorage.getItem('fg-prototip-jezik');
    if (sacuvanJezik === 'en' || sacuvanJezik === 'sr') {
        document.documentElement.lang = sacuvanJezik;
    }
} catch (greska) { /* zadrži podrazumevano */ }
