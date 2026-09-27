# Dnevnik (log)

Kronološki, samo-dodajajoč zapisnik. Format vsakega vnosa: `## [LETO-MESEC-DAN] tip | Naslov`.

Starejša zgodovina dela (poročilo o zdravstvu, CKZ, starost, društva, kader in šport, poti, defibrilatorji, 19.–21. 9. 2026) je v dnevniku nadrejenega vaulta `Obcina_Crnomelj_Vault/wiki/log.md`; ta dnevnik se začne z ustanovitvijo samostojnega projekta.

## [2026-09-21] update | Ustanovitev samostojnega raziskovalnega projekta o zdravju

- Action: Mapa `porocila/zdravstvo-obcina-crnomelj` je pripravljena kot samostojen projekt. Skripte so v `orodja/` (koren = mapa projekta), poti do virov so projektno relativne (`raw/web/` → `viri/splet/`, `raw/Zdravje_kraja` → `viri/nijz`), v `viri/` je lokalna kopija vseh virov, ki jih poročilo navaja (93 citiranih virov, 1.068 objav registra Radia Odeon, 54 nizov NIJZ, PDF-ji, GPX, AED), dodan je `viri/manifest.json` s SHA-256. V `wiki/` je prenesen izbor zdravstvenih strani (27 datotek), s povezavami preusmerjenimi v projekt; povezave na strani, ki niso del projekta, so pretvorjene v navadno besedilo. Dodani so `AGENTS.md` (navodila agenta kot raziskovalca zdravja), `CLAUDE.md`, `README.md`, `requirements.txt`, `wiki/index.md`, `log.md`, `naslednji-koraki.md` in zdravstveni `pregled-za-kandidata.md`. Enkratne skripte (`dokoncaj_zajem`, `dopolni_*`, `posodobi_wiki`, `vlozi_*`) so premaknjene v `arhiv/enkratne-skripte/`; izvirna besedila pred preusmeritvijo poti so v `arhiv/pred-samostojnim-projektom-2026-09-21/`.
- Sources used: obstoječi viri in izdelki mape; kopije iz `raw/web/` in `raw/Zdravje_kraja` nadrejenega vaulta.
- Pages created: `AGENTS.md`, `CLAUDE.md`, `README.md`, `wiki/index.md`, `wiki/log.md`, `wiki/naslednji-koraki.md`, `wiki/analysis/synthesis/pregled-za-kandidata.md`, `viri/manifest.json`, 26 prenesenih wiki strani in infografik.
- Pages updated: vse podatkovne datoteke in skripte s potmi do virov.
- Open questions: nekatere strani prenesenega wikija (npr. starejši povzetki virov NIJZ) vsebujejo starejše formulacije, ki jih poročilo popravlja; pred uporabo preveriti proti `porocilo.html`, razdelek »Sled sprememb«.
- Follow-up tasks: pri prvi seji v novem projektu zagnati `python -X utf8 zazeni.py vse` in preveriti rezultat; nadaljevati odprte raziskave iz `naslednji-koraki.md`.

## [2026-09-21] update | Pospravljanje map projekta

- Action: Datoteke iz korena razvrščene v mape: `vsebina/` (razdelki, slogi, skripte poročila), `podatki/{aed,starost,drustva,kader,poti,register,nijz,literatura}/` (podatkovne in bibliografske datoteke), `dokumentacija/` (opombe o poteh). V korenu ostanejo izdelki, `zazeni.py`, `AGENTS.md`, `CLAUDE.md`, `README.md`. Poti posodobljene v vseh generatorjih `orodja/*.py`, povezavah za prenos v poročilu in wikiju; `AGENTS.md`, `README.md` in `naslednji-koraki.md` usklajeni.
- Sources used: /
- Pages created: /
- Pages updated: `naslednji-koraki.md`, wiki strani s sklici na `kazalniki.csv` in podatke o poteh/starosti.
- Open questions: /
- Follow-up tasks: Varnostna kopija stanja pred premikom je v `arhiv/pred-pospravljanjem-2026-09-21/`. `python -X utf8 zazeni.py vse` je po premiku uspešen (1.180 strani, 6.620 lokalnih povezav, 43 strani PDF, 93 viri).


## [2026-09-22] solution | Anketni list CKZ in spremljanje napredka

- Action: Pripravljena predloga 1.0: mesečni anketni list ekipe (8 meril), vprašalnik za odrasle (10 vprašanj, začetek/zaključek/6/12 mesecev), pravila imenovalcev, osipa in parnih sprememb ter predlogi ukrepov za 0–12 mesecev, 1–3 in 3–10 let. Dodana štiristranski HTML/PDF in prazna Excelova predloga s petimi listi. Spletni razdelek je v kazalu poročila; popravljen splošni časovni presek z vidno vrstico v »Sledi sprememb«. Ocena CKZ 3,4/5 in zdravstveni status nista spremenjena.
- Sources used: Primarna stran NIJZ ZVCT, ponovno prebrana 22. 9. 2026; lokalni izvleček, bibliografski zapis in SHA-256. Obstoječa stran CKZ in prejšnji predlog spremljanja; vprašalnik in lestvica sta avtorska, ne validirana.
- Pages created: `wiki/analysis/solutions/ckz-anketa-in-spremljanje.md`, `wiki/sources/source-summaries/ckz-spremljanje-nijz-2026-09-22.md`, `vsebina/ckz-obrazci.md`, `vsebina/ckz-spremljanje.html`, `orodja/pripravi_ckz.py`, `orodja/preveri_ckz.py`, obrazci in preglednica v `podatki/ckz/`.
- Pages updated: stran CKZ, kandidatova sinteza, index, handoff, README, vhodi in generator poročila, `zazeni.py`, manifest in bibliografija, zgrajeni izdelki. Celotna gradnja in preverba uspeli: poročilo 45 strani, obrazci 4; 93 virov, 1.291 SHA-256, 1.181 strani, 6.636 lokalnih povezav; 5 širin, filtri, zemljevidi in JavaScript brez napak, brez omrežnih zahtev. Vizualno pregledani namizni/telefonski prikaz, obrazci ter spremenjene strani poročila. Excel preračunan v LibreOffice na prazni kopiji in 9 robnih primerih; brez osebnih podatkov.
- Open questions: Katere podatke CKZ že zbira, razumljivost vprašalnika, izvedljivost kontrol in odgovorne vloge. Uvedba obrazca in rezultati niso potrjeni; organizacij nismo kontaktirali.
- Follow-up tasks: Preizkus v dveh programih po preverbi obstoječih evidenc; cilji po trimesečnem izhodišču. Gradnja prepiše prazno predlogo XLSX, izpolnjenih kopij ne hraniti na tej poti. Linux uporablja `PYTHONPATH=.python-deps python3`; odvisnosti nameščene za ta sistem. Arhiv prejšnjih izdelkov: `arhiv/pred-anketo-ckz-2026-09-22/`.

## [2026-09-23] lint | Gitignore in tehnični pregled podatkov

- Action: Dodan .gitignore in ponovljivi lokalni pregled podatkov. Popisanih 2.555 datotek; preverjeni strukturirani formati, 1.291 SHA-256, 166 bibliografskih poti, register, struktura nizov NIJZ, GPX, AED in lokalne povezave. Šest napak in dve opozorili. Izvirniki, manifest in izdelki niso spremenjeni.
- Sources used: Lokalni viri, podatki, manifest, generator AED in obstoječe preverbe; brez novih spletnih virov.
- Pages created: `dokumentacija/pregled-podatkov-2026-09-23.md`, `preverjanje/podatki-pregled.json`, `orodja/preveri_podatke.py`, `.gitignore`.
- Pages updated: `wiki/index.md`, `wiki/naslednji-koraki.md`, `wiki/log.md`.
- Open questions: Izvor spremembe AED XLSX in CSV, dve manjkajoči kopiji iz evidence kader/sport, prazen spletni zajem, nerazrešena povezava pregled-drustev. Celotna preverba se ustavi zaradi manjkajočega Playwrighta; preverba samostojnosti zaradi hasha AED. Formule in aktualnost zdravstvenih trditev niso ponovno verificirane.
- Follow-up tasks: Razjasniti AED pred obnovo poročila; obnoviti manjkajoče vire in povezavo; pripraviti odvisnosti Windows in nato ponoviti celotno preverbo. Stare uspešne rezultate obravnavati kot zgodovinske.
