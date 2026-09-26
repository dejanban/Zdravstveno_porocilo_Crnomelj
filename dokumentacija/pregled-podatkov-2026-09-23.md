# Tehnični pregled podatkov, 23. september 2026

Pregled lokalnih datotek je odkril šest napak in dve opozorili. To ni nova vsebinska verifikacija zdravstvenih trditev, aktualnosti storitev ali primerljivosti kazalnikov. Izvirniki, manifest, preglednice in zgrajeno poročilo niso bili spremenjeni. Obstoječa sprememba README.md je ohranjena.

## Obseg in rezultati

| Preverba | Rezultat |
|---|---|
| Popis | 2.555 datotek v `podatki/`, `viri/`, `wiki/` in `vsebina/`; začasne datoteke Excel `~$*` izločene. Zgodovinski arhiv in lokalne odvisnosti niso predmet preverjanja podatkov. |
| Formati | Razčlenjenih 28 JSON/GeoJSON, 10 CSV, 57 XLSX, 20 PDF, 43 GPX in 6 SVG; brez napak odpiranja. Preverjena širina vrstic CSV, koordinate GPX in shranjene Excelove napake. Formule niso ponovno izračunane, videz ni pregledan. |
| Manifest | Ujema se 1.290 od 1.291 kontrolnih vsot. Izjema je `viri/AEDs.xlsx`. Pričakovane vsote niso prepisane. |
| Bibliografija | Preverjenih 166 lokalnih sklicev v glavni in tematskih evidencah; dve manjkajoči kopiji. |
| Register | 1.068 enoličnih URL-jev, lokalne datoteke obstajajo; CSV se ujema z JSON po vseh poljih, statistika pripadnosti ustreza zapisom. Obstoj datoteke ne pomeni, da vsebuje besedilo. |
| NIJZ | Pri 54 kazalnikih so leta urejena in enolična, dolžine nizov ustrezajo letom, vrednosti so številke ali manjkajoče. Posamezne številke niso ponovno primerjane z vsemi izvornimi celicami. |
| Poti | 43 GPX ustreza številu tras, njihove vsote ustrezajo zapisom, dolžine v občini so znotraj celotnih dolžin. Prostorski izračun ni ponovljen. |
| HTML | 1.182 dokumentov in 6.640 lokalnih povezav brez manjkajočih ciljev ali izhodov iz projekta. Sidra preverjena znotraj istega dokumenta; sidra med dokumenti niso vključena. |
| Wiki | Preverjenih 326 povezav oblike `[[...]]`; ena nerazrešena. Navadne povezave Markdown niso vključene v ta števec. |

## Ugotovitve in potrebni popravki

| Datoteka oziroma področje | Ugotovitev | Nadaljnji korak |
|---|---|---|
| `viri/AEDs.xlsx` | Kontrolna vsota se ne ujema. Delovni list ima 67 podatkovnih vrstic, glavo WKT/LON/LAT, stolpca imen in naslovov pa sta prazna. Obstoječi `aed.json` ima 67 imen in 66 naslovov. | Ugotoviti namen spremembe in primerjati s prejšnjo kopijo. Ne potrditi novega hasha brez pojasnila izvora; ne zagnati generatorja, ki bi izgubil imena. |
| `podatki/aed/aed.csv` | Manjkajo stolpca `ime` in `naslov`; koordinate vsebujejo več decimalnih pik (npr. `1.514.389`), zato niso veljavna decimalna števila. | Po razjasnitvi izvirnika obnoviti CSV iz preverjenega vhoda. Ne ugibati položaja decimalnega ločila. Seznam vrstic je v strojni preverbi. |
| `podatki/kader/kader-sport-viri.json` | Manjkata `viri/splet/kader-sport-20260921-manualna.md` in `viri/splet/kader-sport-20260921-ninjatrenerji.md`. | Obnoviti arhivski kopiji ali vira ponovno zajeti s pravim datumom dostopa ter posodobiti evidence. |
| `viri/splet/zdravstvo-20260919-novice-ne-pozabite-prepoved-gibanja-med-deveto-uro-zvecer-in-sesto-uro-zjutraj-6edc1f616.md` | Datoteka je prazna, četudi njena kontrolna vsota ustreza manifestu. | Preveriti zgodovino zajema, obnoviti vsebino ali izrecno označiti neuspešen zajem. |
| `wiki/entities/associations/zdravstvena-podporna-mreza.md` | Povezava `[[pregled-drustev]]` nima lokalnega cilja. | Določiti ustrezno lokalno stran ali ohraniti omembo kot navadno besedilo, če gre za stran nadrejenega vaulta. |
| `podatki/starost/starost-preverjanje.json` | Že dokumentirana razlika dveh oseb za Slovenijo leta 2008: skupaj 2.025.866, vsota starosti 2.025.864. Glavni prikaz 2011–2026 tega leta ne vključuje. | Ohraniti opombo; razlog v izvornem odgovoru ostaja odprt. V tem pregledu seštevek ni ponovno izračunan. |

Spremembi AED izvirnika (23. 9. ob 09:27:53) in CSV (09:31:25, lokalni čas) sta bili zaznani pred pregledom. Namen sprememb ni ugotovljen. Tehnični pregled ne spreminja ocen zdravstvenih tem ali kandidatove sinteze.

## Ponovitev in omejitve okolja

| Ukaz oziroma datoteka | Namen oziroma stanje |
|---|---|
| `python -X utf8 orodja/preveri_podatke.py` | Neodvisni pregled, ki zbere napake in izpiše `preverjanje/podatki-pregled.json`; ob napakah vrne izhodno kodo 1. |
| `python -X utf8 orodja/preveri_samostojnost.py` | Zagnano; ustavi se pri neustreznem SHA-256 AED. Stare datoteke `preverjanje/samostojnost.json` zato ne razumeti kot današnje uspešne preverbe. |
| `python -X utf8 zazeni.py preveri` | Zagnano; ustavi se pri manjkajočem modulu Playwright. Trenutno okolje je Windows, Python 3.11.5, ne Linux iz prejšnje seje. |
| `.gitignore` | Izloča lokalne odvisnosti, virtualna okolja, predpomnilnike, lokalne `.env` in začasne datoteke. Viri, podatki, zgodovina, preverjanje in izdelki ostajajo sledljivi. Preverjeno z `git check-ignore`. |

Celotna brskalniška preverba, preračun formul in vizualna preverba PDF v tej seji niso opravljeni. Nova vsebinska spletna raziskava ni bila izvedena. Pred ponovno gradnjo je treba razjasniti izvirnik AED in pripraviti Windows odvisnosti po `requirements.txt` ter Chromium za Playwright.

## Povezave

| Gradivo | Povezava |
|---|---|
| Strojni rezultati z natančnimi hashi in vrsticami | [podatki-pregled.json](../preverjanje/podatki-pregled.json) |
| Trajne naloge | [naslednji-koraki.md](../wiki/naslednji-koraki.md) |
| Kazalo | [index.md](../wiki/index.md) |
