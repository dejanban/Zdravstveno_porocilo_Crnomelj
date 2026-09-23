# Naslednji koraki in trenutno stanje projekta

**Namen te strani**: če nadaljuješ delo v novi seji ali oknu (Claude Code ali Codex), **preberi to stran najprej**, takoj po `AGENTS.md`. Zajema stoječa navodila uporabnika, trajen seznam opravil in tehnično stanje orodij, ki jih `log.md` (kronološki dnevnik) in `index.md` (zemljevid vsebine) ne povzemata na enem mestu. Stran se **prepiše** ob vsaki večji spremembi stanja; ni append-only kot `log.md`.

Zadnja posodobitev: 2026-09-23 — tehnični pregled podatkov in .gitignore; odprta neskladja AED, manjkajoči kopiji virov in manjkajoči Playwright v Windows.

## Pred naslednjo gradnjo

Današnja preverba ni uspešna: `viri/AEDs.xlsx` ne ustreza manifestu, imena in naslovi v njem manjkajo glede na obstoječi JSON; `podatki/aed/aed.csv` ima spremenjeno glavo in neveljavne koordinate. Najprej razjasniti izvor sprememb, ne prepisati manifesta in ne obnoviti poročila iz nepreverjenega vhoda. Podrobnosti, dve manjkajoči bibliografski kopiji, prazen zajem in pokvarjena wikipovezava so v [tehničnem pregledu](../dokumentacija/pregled-podatkov-2026-09-23.md). Ponovitev: `python -X utf8 orodja/preveri_podatke.py`.

Trenutna seja uporablja Windows in Python 3.11.5. `python -X utf8 zazeni.py preveri` se ustavi zaradi manjkajočega modula Playwright. Spodnji uspešni rezultati z 22. 9. so zgodovinski; navodila za Linux opisujejo prejšnje okolje. Lokalna mapa `.python-deps` je izločena z `.gitignore`; viri, podatki, arhiv in izdelki ostajajo vključeni v Git.

## Stanje

| Področje | Stanje |
|---|---|
| Poročilo | `porocilo.html` (26 vsebinskih razdelkov in literatura, 11 grafov NIJZ, zemljevida defibrilatorjev in poti, starost, kader, društva, register, literatura), `porocilo.pdf` (45 strani), `register-dogodkov.html`, `index.html`. |
| Viri | 93 citiranih virov z lokalno kopijo, 1.068 objav registra Radia Odeon, 54 nizov NIJZ, PDF-ji, GPX, AED; 1.291 datotek s SHA-256 v `viri/manifest.json`; bralnik `viri/index.html`. |
| Preverjanje | 22. 9. 2026 uspešna gradnja in preverba: 1.181 strani in 6.636 lokalnih povezav v osnovni preverbi, dodatno obrazci CKZ; 5 širin, brez napak JavaScript ali spletnih zahtev. PDF obrazcev ima 4 strani, poročilo 45. Formule XLSX preračunane v LibreOffice na prazni predlogi in 9 robnih primerih. |
| Gradivo CKZ | `podatki/ckz/ckz-obrazci.html`, `ckz-obrazci.pdf`, `ckz-spremljanje.xlsx`; predloga 1.0, brez odgovorov ali podatkov oseb. Vhodi: `vsebina/ckz-obrazci.md`, `vsebina/ckz-spremljanje.html`; generator `orodja/pripravi_ckz.py`, preverba in izvoz PDF `orodja/preveri_ckz.py`, oba vključena v `zazeni.py`. |
| Wiki | 27 prenesenih strani in infografik iz nadrejenega vaulta; povezave na strani, ki niso del projekta, so pretvorjene v besedilo. Starejši povzetki virov lahko vsebujejo zastarele formulacije, ki jih poročilo popravlja (razdelek »Sled sprememb«). |
| Ocena CKZ | 3,4/5 za javno dokumentirano delo (uredniška ocena, ne klinična ali finančna). Status zdravstvene teme v `pregled-za-kandidata.md`: ❌ zaradi kadrovskega tveganja in odprtega vprašanja upravljanja ZD. |

## Stoječa navodila uporabnika

| Navodilo | Pomen |
|---|---|
| Vsa vsebina wikija in poročila v slovenščini | Shema in navodila so v angleščini. |
| Naštevanja v poročilu so tabele | Ne alineje za primerljive postavke. |
| Literatura po standardu IEEE | Številčenje po prvem pojavu; vsak vir ima lokalno kopijo in pravi datum dostopa. |
| Popravki ostanejo vidni | Napačno trditev se ne prepiše tiho; vpis v »Sled sprememb« in v `log.md`. |
| Nobenega stika z organizacijami | Društvom, ZD ali CKZ ni bilo poslano nobeno sporočilo; razpoložljivost je »navedena na spletu«, ne telefonsko potrjena. Stikov ne vzpostavljaj brez izrecnega naročila. |
| Izdelkov ne urejaj ročno | Spreminjaj vhode (`vsebina/vsebina.html`, `orodja/pripravi_*.py`, podatkovne datoteke v `podatki/`), nato zgradi znova. |

## Ukazi

Iz korena projekta. Prvotno okolje Windows: Python 3.11; preverjeno 22. 9. 2026 tudi na Linuxu s Python 3.14 in Playwright Chromium. V trenutnem Linux okolju uporabite `PYTHONPATH=.python-deps python3 -X utf8 zazeni.py zgradi` oziroma `preveri` / `vse`; potrebni paketi so nameščeni lokalno v `.python-deps`. Stare knjižnice numpy/pyproj/shapely za Windows so zamenjane z različicami za Linux; pri selitvi med sistemi knjižnice namestite znova. Brskalniška preverba v omejenem izvajalnem okolju potrebuje dovoljen zagon Chromiuma.

| Ukaz | Namen |
|---|---|
| `python -X utf8 zazeni.py zgradi` | Obnovi tudi HTML obrazcev in prazno Excelovo predlogo CKZ ter fragmente, poročilo, register in knjižnico virov. Ne shranjujte izpolnjenih preglednic na poti generirane predloge. |
| `python -X utf8 zazeni.py preveri` | Preveri tudi CKZ in izdela štiristranski PDF obrazcev; nato samostojnost, SHA-256, poti, širine in JavaScript ter `porocilo.pdf`. |
| `python -X utf8 zazeni.py vse` | Oboje. |
| `python -X utf8 zazeni.py postrezi` | Lokalni strežnik `http://127.0.0.1:8000/porocilo.html`. |
| `python -X utf8 zazeni.py zgradi --preracunaj-poti` | Ponoven izračun GPX (potrebuje `shapely`, `pyproj`, `numpy`). |
| `python -X utf8 orodja/pripravi_aed.py` | Samo zemljevid defibrilatorjev iz `viri/AEDs.xlsx` in `viri/osm-crnomelj.json`. |

Zajemni skripti `orodja/zajemi_*.py` in `razisci_vire.py` potrebujejo omrežje; `razisci_vire.py` za ponoven popis registra potrebuje zunanji korpus Radia Odeon v `viri/radio-odeon/` (ni priložen; register je zamrznjen v `podatki/register/register-dogodkov.json`). Enkratnih skript v `arhiv/enkratne-skripte/` ne zaganjaj.

## Odprte raziskovalne naloge

| Naloga | Kaj manjka in kaj bi zapolnilo vrzel |
|---|---|
| CKZ: preizkus predloge | Pripravljeno gradivo [[analysis/solutions/ckz-anketa-in-spremljanje]]. Najprej preveriti prekrivanje z obstoječimi evidencami, razumljivost za 5–10 odraslih (planska ocena), odgovorno vlogo in vire; preizkus v dveh programih. Uvedba ni potrjena; podatkov oseb ne pridobivamo. |
| CKZ: doseg in izidi | Število **različnih** uporabnikov 2025 in 2026, napotitve, dokončanje programov, spremljanje po 6 in 12 mesecih, ekvivalenti polnega delovnega časa po poklicih, stroški in prihodki po virih. Dvanajst vprašanj je v poročilu (razdelek »Vprašanja«). |
| Register objav Radia Odeon | Razvrstitev je začetna in avtomatizirana; pregledati mejne primere. Enota je objava, ne izvedeni dogodek. |
| Primerljive občine | Izbrati demografsko in geografsko podobne podeželske občine in primerjati enake kazalnike z enakimi definicijami in obdobji. |
| Defibrilatorji | Datoteka ni preverjena proti nacionalnemu registru; ni podatka o delovanju, servisu, urah dostopa in ključu. V občini jih je 21 od 67 v datoteki (ostalo Metlika, Semič, Predgrad). Preveriti dostopnost gasilskih domov in zasebnih lokacij ter čas dosega z omrežjem cest. |
| Starost po naseljih | Starost in potrebe po oskrbi po naseljih ali KS (SURS na ravni naselij); nizek delež pomoči na domu: manjše potrebe, cena, kader ali čakanje? |
| Vodstvo ZD | Zadnji pregledi niso na novo preverili postopka pri direktorju; preveriti aktualno stanje iz uradnih virov (svet zavoda, ministrstvo). |
| Otroška prehranjenost in gibanje | Pilot na dveh šolah (izhodiščni SLOfit, redno gibanje, prehransko okolje); razlogi za nizko precepljenost proti pnevmokokom (44,4 % v prikazani kohorti). |
| Društva in podpora | Preveriti stroške, članstvo, termine, prevoze in zmogljivosti; ažuriranje imenika CKZ »Povezani za zdravje« (september 2025). |
| Poti | Terenska potrditev tras GPX; izvirni avtorji niso potrjeni. |
| Lint wikija | Primerjati starejše strani (`nijz-zdravje-v-obcini*`, `zd-crnomelj-pregled`) s poročilom in popraviti zastarele formulacije. |

## Kje je zgodovina

Podroben kronološki zapis dela do 21. 9. 2026 je v dnevniku nadrejenega vaulta (`Obcina_Crnomelj_Vault/wiki/log.md`), ki ni del tega projekta; ta projekt se začne z vnosom o ustanovitvi v `log.md`.

## Zadnja tehnična preverba CKZ

Rezultati so v `preverjanje/ckz.json` in `preverjanje/ckz-formule.json`; posnetki `ckz-obrazci-stran-1.png` do `ckz-obrazci-stran-4.png`, `ckz-spremljanje-390.png`, `ckz-spremljanje-1440.png` ter strani poročila 25, 26 in 37. Vizualno pregledano. Arhiv pred spremembo: `arhiv/pred-anketo-ckz-2026-09-22/`. Nov zajem NIJZ je registriran v `podatki/ckz/ckz-viri.json` in manifestu; prejšnji zajem z 20. 9. ostaja ohranjen.
