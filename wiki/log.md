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

## [2026-09-24] update | Dopolnitev glavnega poročila: življenjske razmere, voda in zrak

- Action: Obnovljena gradnja iz ohranjenega HTML; dodana štiri poglavja, letne in mesečne preglednice, 30 vprašanj, ukrepi, ocene, sled popravkov in PDF.
- Sources used: 33 citiranih virov Komunale, ARSO, WHO, SURS in raziskave CAPS; lokalni izvidi in novi arhiv okolje-2026-09-24.
- Pages created: Okoljska tema, povzetek virov, obnovljena sinteza in kazalo; prenosljive CSV tabele.
- Pages updated: Glavno poročilo, knjižnica, literatura, naslednji koraki, obnovljeni zagonski postopek.
- Open questions: Stari prazni izvirniki; voda pred 2011; stanje reke Dobličice; razlaga dogodka Adlešiči; BaP 2025; nepopolno 2026.
- Follow-up tasks: Obnova varnostnih kopij in pridobitev manjkajočih primarnih časovnih vrst. Preverjanje novega obsega je zabeleženo v preverjanje/okolje-porocilo.json; ne potrjuje vseh starih trditev.

## [2026-09-25] ingest | Jesensko-modra prenova in raziskovalni pregled spanja ter digitalnih navad

- Action: Arhivirani prejšnji izhodi; prenovljeni vhodni slogi, skripte in generatorji. Vsa stara poglavja razporejena v 11 povezanih zavihkov. Dodani globalno iskanje, tipkovnična navigacija, filtri športnih dejavnosti, peš/kolesarski pogled in sloj AED na zemljevidu poti. Dodan raziskovalni pregled z grafom, preglednicami, 12 vprašanji, časovno razdeljenimi ukrepi in obrazloženo uredniško oceno. Izdelan PDF s 93 stranmi. Gradnja in funkcionalno preverjanje uspešna pri petih širinah, brez napak JavaScript ali zunanjih zahtev; izveden vizualni pregled spletne in tiskane različice.
- Sources used: Osem raziskav (Chang 2015, Carter 2016, Lund 2021, Gao 2022, Ahmed 2024 in 2025, Itani 2017, Lemahieu 2025) ter dve objavi NIJZ. Carter, Itani in obe raziskavi Ahmed so prebrani samo kot povzetki, kar je označeno. Lokalni zajemi in manifest dopolnjeni; obstoječi podatki AED, poti in grafov obnovljeni samo iz ohranjenega HTML, brez izmišljanja izgubljenih GPX ali Excelov.
- Pages created: Wiki tema spanje-digitalne-navade, deset posamičnih povzetkov virov in skupni pregled, dokumentacija prenove, raziskovalni vhod, lokalni zajemi in obnovljeni podatkovni izvozi. Prej prazni strani CKZ in ZD dopolnjeni s previdno omejenim opisom ter povezavami.
- Pages updated: Poročilo HTML in PDF, knjižnica virov, literatura, manifest, kazalo wiki, sinteza za odločevalce, naslednji koraki, README, zaganjalnik ter gradnja in preverjanje. Popravki trditev o dostopnosti AED in omejitve arhiva vključeni v sled sprememb.
- Open questions: 77 starih ciljev prenosov manjka ali je praznih; prenosi so označeni kot nedostopni. Pri 313 datotekah je razlika kontrolnih vsot pojasnjena s konci vrstic, šest podedovanih neskladij ostaja nerešenih in izrecno označenih. Ni lokalnih meritev spanja, ločenih primerljivih ocen posameznih platform ali potrjenih aktualnih urnikov AED. Pregled literature je usmerjen, ne izčrpen sistematični pregled.
- Follow-up tasks: Pridobiti štiri celotna besedila in manjkajoče izvirnike, razrešiti šest starih neskladij, dokumentirati aktualno ponudbo in dostopnost ter dopolniti platformno specifične dokaze. Rezultati preverjanja so v preverjanje/prenova-porocilo.json in preverjanje/kontrolne-vsote.json; vizualni pregled je opisan v preverjanje/prenova-vizualni-pregled.md.

## [2026-09-25] lint | Pregled prenove, obnova izpraznjenih datotek iz gita in posnetek vodenja ZD

- Action: Pregled celotnega projekta po prenovi. Ugotovljeno, da je commit d96d620 izpraznil 1.087 datotek, ki so nepoškodovane v commitu 0dc0bd4 (prejšnja ocena, da je arhiv neobnovljiv, je bila napačna). Datoteke z 0 bajti obnovljene z novim orodjem `orodja/obnovi_iz_gita.py` (surovi blobi, neprazne datoteke niso prepisane); 1.289 od 1.290 zapisov izvirnega manifesta se ujema (izjema `viri/AEDs.xlsx`, znana od 23. 9.). Izvirni manifest vključen v `viri/manifest.json`, preverjanje razširjeno. Manjkajoči prenosi v poročilu: 77 → 1. Popravljena napaka, ki je telefonsko povezavo `tel:` onemogočila kot »manjkajočo kopijo«. Okrnjene wiki strani (dnevnik, kazalo, sinteza, CKZ, ZD) združene z izvirniki; izvirniki shranjeni v `arhiv/izvirnik-0dc0bd4/`, stanje pred združitvijo v `arhiv/pred-obnovo-iz-gita-2026-09-25/`. Posodobljena zastarela besedila o »izgubljenem arhivu« v poročilu, README in dokumentaciji (z vrstico v Sledi sprememb). Dopolnjena vrstica Gao 2022 (edina »zelo nakazana« povezava: dolg spanec in umrljivost). Preverjene številke Chang, Carter, Itani, Ahmed, Lemahieu, Lund in ARSO (BaP 2,6; PM10 39/34) proti lokalnim zajemom. Dodan datiran razdelek poročila o vodenju ZD in objavljenem razporedu ambulant.
- Sources used: git commit 0dc0bd4; ZD Črnomelj »Upravljanje in vodenje« in »Odsotnost zdravnikov« (25. 9. 2026, visoka); Svet24 23. 4. 2026 (nizka–srednja); Moja Dolenjska 23. 9. 2026 (nizka, »neuradno«). Lokalne kopije v `viri/posodobitve-2026-09-25/` in `viri/splet/posodobitve-20260925-*.md`, SHA-256 v manifestu.
- Pages created: `wiki/sources/source-summaries/zd-vodenje-ambulante-2026-09-25.md`, `orodja/obnovi_iz_gita.py`, `podatki/posodobitve/posodobitve-viri.json`, `preverjanje/obnova-iz-gita.json`.
- Pages updated: 1.087 obnovljenih datotek; `wiki/entities/institutions/zd-crnomelj.md` (aktualno vodstvo; popravek domneve o odhodu dr. Plut), `ckz-crnomelj.md`, `pregled-za-kandidata.md`, `index.md`, `log.md` (obnovljeni vnosi 21.–23. 9.), `naslednji-koraki.md`; `vsebina/spanje-digitalne-navade.md`; `orodja/prenovi_porocilo.py`, `zgradi_okolje_porocilo.py`, `preveri_okoljske_vire.py`, `preveri_prenovo.py`; `zazeni.py`, README, dokumentacija. Poročilo HTML/PDF (94 strani, 141 virov) zgrajeno in preverjeno pri petih širinah; novi razdelek vizualno pregledan pri 1440 in 390 px.
- Open questions: Izbira novega direktorja ni uradno potrjena; datum imenovanja v. d. ni objavljen. Zapis naročnika o dostopnosti AED (23. 9. 2026) ostaja prazen in ga v gitu ni. Šest okoljskih neskladij in `AEDs.xlsx` ostajata. Obnovljene kopije potrjujejo izvirnost virov, ne aktualnosti starejših ugotovitev.
- Follow-up tasks: Ob uradni objavi potrditi ali popraviti navedbo o novem direktorju; ponavljati posnetek razporeda ambulant (mesečno); pridobiti podatke ZZZS o neopredeljenih; od naročnika ponovno pridobiti zapis o AED.

## [2026-09-25] ingest | Šest novih tem: nujna pomoč, neopredeljeni in čakalne dobe, dolgotrajna oskrba, vročina, duševno zdravje mladih, promet in alkohol

- Action: Na zahtevo uporabnika raziskanih in v poročilo vključenih šest tem. Nov zavihek »Dostop do oskrbe« (nujna pomoč, neopredeljeni, dolgotrajna oskrba); vročina v zavihku okolje, duševno zdravje mladih v podpori, promet in alkohol v številkah. Vsaka tema ima povzetek, dejstva s preglednicami, najmanj 10 kritičnih vprašanj, ukrepe za 0–12 mesecev, 1–3 in 3–10 let ter obrazloženo uredniško oceno. Izdelana modelska analiza dostopnosti 111 naselij (OSRM + SURS 2026, `orodja/analiziraj_dostopnost_nmp.py`). Oznake značilnosti NIJZ prebrane iz vektorskih oznak publikacije 2026. Osnutek o prvih posredovalcih popravljen pred objavo po branju letnega poročila ZD 2025 in programa 2026. Gradnja in preverjanje uspešna: 12 zavihkov pri petih širinah, 161 virov, 120 strani PDF; vizualno pregledani novi razdelki pri 1440 in 390 px ter PDF str. 67.
- Sources used: 20 novih virov (pravilnik NMP 2026, strani ZD, NIJZ čakalne dobe 16. 9. 2026, NIJZ vročina in HBSC, Program MIRA, IRSSV 2024, gov.si vstopne točke, CSD DBK, RTV, policija, SURS, OSRM, Scquizzato 2022, Bergen 2014, Ballester 2023, Janoš 2025) ter obstoječi viri poročila (NIJZ 2026, opisi kazalnikov, letno poročilo ZD 2025, program 2026, ZZZS, ARSO 2025).
- Pages created: `wiki/topics/social-affairs/{nujna-pomoc,neopredeljeni,dolgotrajna-oskrba,dusevno-mladi,promet-alkohol}.md`, `wiki/topics/environment/vrocina.md`, `wiki/sources/source-summaries/teme-dostop-oskrba-2026-09-25.md`, `vsebina/teme/*.md`, `podatki/teme/*`, `orodja/zajemi_teme.py`, `orodja/analiziraj_dostopnost_nmp.py`.
- Pages updated: `orodja/prenovi_porocilo.py` (funkcija `teme_content`, zavihek dostop), sinteza za odločevalce, kazalo, manifest, poročilo HTML/PDF.
- Open questions: Dejanski dostopni časi NMP in obseg mreže prvih posredovalcev; število neopredeljenih prebivalcev po ZZZS; čakanje po občini prebivališča; čakalni seznam pomoči na domu; lokalni načrt ob vročini; čakalne dobe psihološke ambulante; lokalni podatki policije o nesrečah.
- Follow-up tasks: Pridobiti celotna besedila štirih raziskav; mesečno ponavljati posnetke čakalnih dob in ambulant; preveriti model OSRM z agregiranimi dejanskimi časi.

## [2026-09-26] update | Celotni članki, scenariji dostopnosti NMP in osnutki zahtev IJZ

- Action: (1) Preverjena prosta dostopnost štirih raziskav (Europe PMC, Unpaywall). Ballester 2023 pridobljen v celoti; dodana ocena za Slovenijo (154 smrti poleti 2022, IZ −24 do 307, 80+: 798 na milijon), ki ni statistično zanesljiva. Bergen 2014 dopolnjen z uradnim povzetkom Community Guide (nočne hude nesreče −22,1 % pri naključnem preverjanju; opozorilo glede kratkotrajnih akcij). Janoš 2025 in Scquizzato 2022 ostajata pri povzetku (zaprt dostop). (2) Model dostopnosti razširjen: izhodišče ZD Metlika, dostopni čas = obdelava klica (predpostavka) + izvoz + vožnja × faktor. Nad 15 min: 25,2 % prebivalcev (razpon 20,1–34,3 %), ob zasedeni ekipi Črnomelj 99,3 % (povprečno 26,5 min). (3) Pet osnutkov zahtev po ZDIJZ v `dokumentacija/zahteve-ijz/` (ZD Črnomelj, ZZZS OE NM, DSO Črnomelj, PU NM, CSD DBK); členi preverjeni v UPB ZDIJZ (5., 12., 13., 16., 17., 22., 23., 24., 27., 34.). Osnutki niso poslani.
- Sources used: Ballester 2023 (celotno besedilo), Community Guide, ZD Metlika NMP, OSRM (3 izhodišča), ZDIJZ UPB (Uradni list RS 51/06), javni imeniki naslovov organov.
- Pages created: `dokumentacija/zahteve-ijz/00-navodila.md` do `05-*.md`.
- Pages updated: `vsebina/teme/{nujna-pomoc,vrocina,promet-alkohol}.md`, `orodja/analiziraj_dostopnost_nmp.py`, `podatki/teme/*`, register virov, sinteza za odločevalce; poročilo (163 virov, 122 strani PDF, 12 zavihkov, preverjanje uspešno).
- Open questions: E-naslov PU Novo mesto ni preverjen. Predpostavke modela (obdelava klica, faktor nujne vožnje) čakajo na dejanske podatke ZD.
- Follow-up tasks: Ko prispejo odgovori IJZ, jih shraniti v `viri/odgovori-ijz/`, vnesti v poročilo in model umeriti na dejanske dostopne čase.

## [2026-09-26] ingest | Trim steza Vražji kamen in Srčna pot Svibnik

- Action: Uporabnik je posredoval štiri vire. Prebrani in shranjeni lokalno (`viri/poti-2026-09-26/`, izvlečki `viri/splet/teme-20260925-*.md`, SHA-256 v manifestu). Ugotovljeno: GPX Ribje poti na strani Srčne poti je enak `viri/gpx/pohodnistvo/ribja-pot.gpx` (SHA-256 82117d8d…); Učna pot (12,3 km) se ujema s trasama 30 in 34 v analizi tras. Trim steza: 7 vadbenih postaj, 57 vaj (brošura CKZ), postaje obnovljene poleti 2020, ureditev parkirišča 2021; trase ni v OSM, GPX v pripravi. Dodano poglavje »Trim steza Vražji kamen in Srčna pot Svibnik« v zavihku poti (10 vprašanj, ukrepi), oznaka Vražji kamen na zemljevidu poti in vrstica v sledi sprememb. Popravljen datum dostopa v orodju za zajem (prej fiksno 25. 9.) in izvleček strani, ki se izrisujejo z JavaScriptom.
- Sources used: CKZ ZD Črnomelj (stran in brošura), Radio Odeon 21. 4. 2021 (WebFetch), spletna stran Srčne poti (HTML, routes.js, GPX, brošura), OSM vozlišče 9272920042.
- Pages created: `vsebina/teme/poti-dopolnitve.md`, `wiki/topics/social-affairs/poti-dopolnitve.md`.
- Pages updated: `orodja/prenovi_porocilo.py`, `orodja/zajemi_teme.py`, register virov, manifest, poročilo (169 virov, 129 strani PDF; preverjanje uspešno).
- Open questions: Dolžina in trasa trim steze; stanje postaj po 2021; uporaba obeh poti.
- Follow-up tasks: Ko uporabnik posreduje GPX trim steze: shraniti v `viri/gpx/pohodnistvo/trim_steza_vrazji_kamen.gpx`, dodati SHA-256, izračunati dolžino, višine in delež v občini, dodati traso na zemljevid poti (podatki poti se berejo iz ohranjene izdaje, zato je potreben dodatek v `route_layer` ali obnova generatorja poti) in posodobiti preglednico v poglavju.

## [2026-09-26] lint | Neujemanje časov vožnje z Google Maps

- Action: Naročnik je ugotovil, da se časi na zemljevidu ne ujemajo z Google Maps. Diagnostika: ZD pravilno umeščen (33 m); povprečna modelska hitrost OSRM 40 km/h; drug model (Valhalla) na istih točkah daje večinoma daljše čase, pri Gribljah drugo pot (OSRM 10,2 km/10,4 min po enopasovni lokalni cesti z OSM `maxspeed=90`, Valhalla 14,2 km/22,2 min). Pridobljeni časi Valhalla za 111 naselij v obe smeri. Zemljevid zdaj kaže razpon OSRM–Valhalla in opozorilo pri različnih poteh. Pripravljeno umerjanje `orodja/kalibracija_casov.py` s predlogo `podatki/teme/kalibracija-google.csv` (14 naselij); po vpisu vsaj 6 Googlovih časov se izbere model z manjšo napako v navzkrižnem preverjanju (google = a + b × model), vpisani Googlovi časi pa se uporabijo neposredno. Dodani opomba v poglavju in vrstica v sledi sprememb.
- Sources used: OSRM, Valhalla (valhalla1.openstreetmap.de), OSM pot 282647601.
- Pages updated: `orodja/zemljevid_nmp.py`, `vsebina/teme/nujna-pomoc.md`, `orodja/prenovi_porocilo.py`, register virov; poročilo (170 virov, 131 strani PDF, preverjanje uspešno).
- Open questions: Googlovi časi za umerjanje (naročnik). Deleži nad 15 min v besedilu so še iz neumerjenega OSRM.
- Follow-up tasks: Ko je predloga izpolnjena: `python -X utf8 orodja/kalibracija_casov.py`, nato `zazeni.py vse`; posodobiti številke v `vsebina/teme/nujna-pomoc.md` in scenarije v `orodja/analiziraj_dostopnost_nmp.py` na umerjene čase. Možen popravek v OSM (maxspeed na poti 282647601) je odločitev naročnika.

## [2026-09-26] ingest | Demenca in demenci prijazna občina; digitalno zdravje

- Action: Na zahtevo uporabnika dodani poglavji v zavihku Dostop do oskrbe (vprašanja, ukrepi, ocena). Demenca: strategija 2030 in akcijski načrt, NIJZ 2026 (14 dejavnikov, 45 %, stroški 546 mio EUR), okvirni lokalni preračun 290–380 (250–440) iz ocene GBD 2019 in SURS 2026, DPT Metlika, program DSO Črnomelj 2018; lokalna DPT ni najdena. Digitalno zdravje: NIJZ (97 % e-receptov, >700.000 uporabnikov zVEM, 180 izvajalcev z e-komunikacijo, digitočke brez Črnomlja), ZD Črnomelj (zVEM testno od 17. 9. 2026, e-komunikacija, naročanje), SURS 2025 (65–74: 71 % uporabnikov, 35 % brez veščin; 75–89: 56 % nikoli). Ocene: demenca 2,43 ❌, digitalno zdravje 2,86 ⚠️. Preverjanje uspešno: 184 virov, 140 strani PDF; vizualni pregled pri 1440 in 390 px.
- Sources used: 14 novih virov v `viri/teme-2026-09-26/` (register `podatki/teme/teme-viri.json`); obstoječi vir-2, vir-3, vir-48. Lancet 2024 ni bil prebran neposredno (povzet po NIJZ); PDF NIJZ o digitalizaciji je strežnik zavrnil (403).
- Pages created: `vsebina/teme/{demenca,digitalno-zdravje}.md`, wiki strani tem.
- Pages updated: `orodja/prenovi_porocilo.py`, sinteza, kazalo, naslednji koraki.
- Open questions: Lokalna uporaba zVEM; lokalni programi za demenco; lokalno število oseb z demenco.
- Follow-up tasks: Zahtevati agregirane podatke NIJZ o zVEM po starosti za občino; preveriti z občino in DSO obstoj programov za demenco.

## [2026-09-26] solution | Vprašalnik o izkušnjah pacientov za letno poročilo

- Action: Na zahtevo uporabnika pripravljen anonimen vprašalnik (15 vprašanj + 4 demografska, ~4 min) za paciente ZD, s pravili za letno obdobje zbiranja (enkrat na pacienta v obdobju, ponovno naslednje leto, brez povezovanja), preprečevanjem podvajanja (SMS enkrat na številko, vprašanje 0 na papirju), kazalniki za letno poročilo, pravili objave (n < 10 se ne objavi, n po vprašanju, IZ 95 %) in izračunom vzorca (~385 za ±5 o. t.; 143 → ±8 o. t.). Pet vprašanj in splošna ocena 1–5 ohranjajo primerljivost z anketo, ki jo ZD uporablja od 2014. Poglavje v zavihku Ukrepi; natisljiv HTML/PDF (2 strani A4) z `orodja/pripravi_vprasalnik.py`. Preverjanje uspešno: 185 virov, 143 strani PDF.
- Sources used: Letno poročilo ZD 2025 (str. 35–36: 143 anket, 4,57/5, upad odziva, načrt SMS; 2 ankete eZdravje); obstoječi spletni vprašalnik ZD (`viri/teme-2026-09-26/zd-anketa.*`); obstoječi obrazci CKZ.
- Pages created: `vsebina/teme/vprasalnik-pacienti.md`, `wiki/analysis/solutions/vprasalnik-pacienti.md`, `podatki/vprasalnik/vprasalnik-izkusnje-pacientov.{html,pdf}`, `orodja/pripravi_vprasalnik.py`.
- Open questions: Vprašalnik ni validiran in ga ZD ni potrdil; SMS vabila zahtevajo preverbo varstva podatkov.
- Follow-up tasks: Pilot na 10–15 pacientih za razumljivost; dogovor z ZD o obdobju zbiranja.

## [2026-09-26] ingest | Debelost otrok, referenčne ambulante, povzetek za prebivalce in imenik »Kam po pomoč«

- Action: Na zahtevo uporabnika dodana štiri poglavja. Debelost in gibanje otrok (zavihek Številke): NIJZ K2.2 2016–2026 (28,3 % proti 24,2 %, značilno slabše; starost 6–14 let po legendi 2026), K2.1 (45,1 proti 49,4, ni značilno), SLOfit ŠVK 2025 (presnovna debelost), Cochrane Brown 2019; ocena 3,14 → ❌. Referenčne ambulante (zavihek Preventiva in podpora): letno poročilo ZD 2025 (1.645 povabljenih, 1.366 pregledanih, 923 z dejavniki tveganja, novo odkritih 236/165/144/67/20), NIJZ pravila (30+, vsakih 5 let), načrtovalna ocena ~2.050 pregledov/leto za Črnomelj (10.265 oseb 30+), Cochrane Krogsbøll 2019; ocena 3,29 ⚠️. Povzetek v preprostem jeziku in imenik »Kam po pomoč« na začetku zavihka Pregled; vse telefonske številke iz shranjenih uradnih strani, telefonsko nepreverjene. Popravki pred objavo: trditev o dispečerjevih navodilih pri AED zamenjana s podprto trditvijo iz pravilnika; ublažena trditev o času reševalcev in o demenci prijazni točki. Preverjanje uspešno: 196 virov, 155 strani PDF; vizualni pregled pri 1440 in 390 px.
- Sources used: 11 novih virov v `viri/teme-2026-09-26/` (SLOfit 2025, Cochrane ×2, NIJZ preventivni pregled in PZVO, ZD referenčne ambulante, patronaža, kontakti, CSD Črnomelj, DSO Črnomelj, Program MIRA »Kam po pomoč«); obstoječi vir-2, vir-3, vir-5, vir-6, vir-48.
- Pages created: `vsebina/teme/{debelost-otroci,referencne-ambulante,za-prebivalce,kam-po-pomoc}.md`, wiki strani prvih dveh.
- Pages updated: `orodja/prenovi_porocilo.py`, `vsebina/prenova.css`, sinteza, kazalo, naslednji koraki.
- Open questions: Izidi po preventivnih pregledih; podatki SLOfit po šolah; telefonska preverba kontaktov.
- Follow-up tasks: Dodati izide po pregledu v zahtevo IJZ za ZD; pridobiti nacionalne podatke PZVO za primerjavo.
