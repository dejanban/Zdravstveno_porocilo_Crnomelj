# Naslednji koraki in trenutno stanje projekta

**Namen te strani**: če nadaljuješ delo v novi seji ali oknu (Claude Code ali Codex), **preberi to stran najprej**, takoj po `AGENTS.md`. Zajema stoječa navodila uporabnika, trajen seznam opravil in tehnično stanje orodij, ki jih `log.md` (kronološki dnevnik) in `index.md` (zemljevid vsebine) ne povzemata na enem mestu. Stran se **prepiše** ob vsaki večji spremembi stanja; ni append-only kot `log.md`.

Zadnja posodobitev: 2026-09-21 — ustanovitev samostojnega raziskovalnega projekta o zdravju v Občini Črnomelj.

## Stanje

| Področje | Stanje |
|---|---|
| Poročilo | `porocilo.html` (26 razdelkov, 11 grafov NIJZ, zemljevida defibrilatorjev in poti, starost, kader, društva, register, literatura), `porocilo.pdf` (43 strani), `register-dogodkov.html`, `index.html`. |
| Viri | 93 citiranih virov z lokalno kopijo, 1.068 objav registra Radia Odeon, 54 nizov NIJZ, PDF-ji, GPX, AED; 1.289 datotek s SHA-256 v `viri/manifest.json`; bralnik `viri/index.html`. |
| Preverjanje | `python -X utf8 zazeni.py vse` je uspešen tudi v kopiji projekta na drugi lokaciji: 1.180 strani, 6.620 lokalnih povezav, brez povezav izven projekta, 5 širin, brez napak JavaScript. |
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
| Izdelkov ne urejaj ročno | Spreminjaj vhode (`vsebina.html`, `orodja/pripravi_*.py`, podatkovne datoteke), nato zgradi znova. |

## Ukazi

Iz korena projekta (Python 3.11, `PYTHONIOENCODING=utf-8`, Playwright Chromium):

| Ukaz | Namen |
|---|---|
| `python -X utf8 zazeni.py zgradi` | Obnovi fragmente, `porocilo.html`, register in knjižnico virov. |
| `python -X utf8 zazeni.py preveri` | Preveri samostojnost in vire (SHA-256), poti, zemljevid, širine, JavaScript; izdela `porocilo.pdf`. |
| `python -X utf8 zazeni.py vse` | Oboje. |
| `python -X utf8 zazeni.py postrezi` | Lokalni strežnik `http://127.0.0.1:8000/porocilo.html`. |
| `python -X utf8 zazeni.py zgradi --preracunaj-poti` | Ponoven izračun GPX (potrebuje `shapely`, `pyproj`, `numpy`). |
| `python -X utf8 orodja/pripravi_aed.py` | Samo zemljevid defibrilatorjev iz `viri/AEDs.xlsx` in `viri/osm-crnomelj.json`. |

Zajemni skripti `orodja/zajemi_*.py` in `razisci_vire.py` potrebujejo omrežje; `razisci_vire.py` za ponoven popis registra potrebuje zunanji korpus Radia Odeon v `viri/radio-odeon/` (ni priložen; register je zamrznjen v `register-dogodkov.json`). Enkratnih skript v `arhiv/enkratne-skripte/` ne zaganjaj.

## Odprte raziskovalne naloge

| Naloga | Kaj manjka in kaj bi zapolnilo vrzel |
|---|---|
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
