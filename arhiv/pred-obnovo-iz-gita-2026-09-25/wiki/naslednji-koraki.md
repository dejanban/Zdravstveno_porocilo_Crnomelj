# Naslednji koraki in stanje projekta

## Navodila in stanje

Uporabnik je naročil modro/jesensko prenovo, povezane zavihke ter raziskavo spanja, zaslonov in družbenih omrežij. Poročilo ima enajst zavihkov s samostojnimi AED-ji, peš/kolesarskimi potmi in športom. Okoljska dopolnitev o življenjskih razmerah, vodi in zraku je ohranjena. Manjkajoča obdobja niso nadomeščena z ničlami. Ohranjeni morajo ostati samostojno delovanje brez omrežja, stara sidra, dostop s tipkovnico, iskanje skrite vsebine in celotna vsebina v PDF.

Ob začetku obnove so bili stari wiki, vhodni fragmenti, generatorji in številni viri prazni; git arhiv je poškodovan. Arhiva sta `arhiv/pred-okoljem-2026-09-24/` in `arhiv/pred-jesensko-modro-prenovo-2026-09-25/`. Osnova ostaja `vsebina/obnovljena-osnova-20260924.html`, okoljsko besedilo pa `vsebina/okolje-20260924.md`. Osnove ne prepisuj z novim izhodom. Stare vsebine niso v celoti ponovno preverjene.

Novo raziskovalno besedilo: `vsebina/spanje-digitalne-navade.md`; slogi in vedenje: `vsebina/prenova.css`, `vsebina/prenova.js`. `orodja/prenovi_porocilo.py` se kliče iz okoljske gradnje pred številčenjem literature. Spremembe vnašaj v te vhode, ne v zgrajeno poročilo.

## Nova raziskava in podatki

Vključenih je osem raziskav in dve objavi NIJZ. Carter 2016, Itani 2017 ter Ahmed 2024/2025 so prebrani samo kot povzetki. Lokalni zajemi so v `viri/spanje-2026-09-25/` in `viri/splet/spanje-20260925-*.md`, register v `podatki/spanje/spanje-viri.json`. Pregled ni izčrpna sistematična raziskava; ni lokalne meritve spanja in ni ločene ocene učinkov posameznih platform. Ocena 3,00/5 pomeni uredniško presojo dokumentiranosti in pripravljenosti spremljanja, ne zdravstvenega stanja ali dela CKZ.

JSON/CSV za AED, poti in ohranjene grafe so obnovljeni samo iz podatkov starega HTML. To ni pridobitev izgubljenih izvirnih GPX/Excelov. 77 manjkajočih ali praznih starih ciljev je označenih v poročilu in `preverjanje/manjkajoci-prenosi.json`.

Kontrolne vsote: 313 razlik je pojasnjenih s pretvorbo LF v CRLF. Šest podedovanih HTML-kopij ima nepojasnjeno neskladje; pričakovane in opažene vsote so v `podatki/spanje/podedovana-neskladja.json`. Preverjanje jih izpiše kot opozorilo, ne kot potrjene izvirnike. Nova sprememba sproži napako. Izvirnih pričakovanih vsot ne prepisuj samo zato, da bi test uspel. Novi viri o spanju imajo strogo preverjene vsote v `viri/manifest.json`.

## Obnovljena gradnja

| Ukaz | Obseg |
|---|---|
| `python -X utf8 zazeni.py zgradi` | Ohranjena osnova, okolje, raziskava spanja, zavihki, povezani podatki, literatura in knjižnica. |
| `python -X utf8 zazeni.py preveri` | Kontrolne vsote z opozorili; pet širin, 11 zavihkov, tipkovnica, zgodovina, iskanje, filtri, zemljevidi, register, delovanje brez JavaScripta in PDF. |
| `python -X utf8 zazeni.py vse` | Gradnja in zgornje preverjanje. |
| `python -X utf8 zazeni.py postrezi` | Lokalni spletni strežnik. |
| `python -X utf8 orodja/pripravi_wiki_prenove.py` | Obnovi deset posamičnih povzetkov novih virov in njihovo kazalo. |

Preverjanje uporablja Playwright v `tmp/okolje-runtime` in nameščeni Microsoft Edge. Zaganjalnik sam nastavi `PYTHONPATH`. Stari generatorji poti in drugih tem niso obnovljeni; `--preracunaj-poti` se izrecno ustavi. Omrežni `orodja/zajemi_spanje.py` ni del običajne gradnje; ob osvežitvi virov je treba pregledno posodobiti dokaze in manifest. Rezultati: `preverjanje/prenova-porocilo.json`, `preverjanje/kontrolne-vsote.json` in posnetki `prenova-*.png`. Izvedba: `dokumentacija/prenova-20260925.md`.

## Odprte naloge

| Naloga | Potrebni dokaz |
|---|---|
| Obnoviti stare prazne datoteke iz varnostne kopije | Neokrnjeni izvirniki in zgodovina; ne prepisuj novih dopolnitev. |
| Razrešiti šest starih neskladij | Neokrnjena kopija ali transparenten nov zajem, z ohranjeno zgodovino. |
| Štirje celotni članki | Carter 2016, Itani 2017 in Ahmed 2024/2025; ponovno preveriti metode in rezultate. |
| Platformno specifični in ciljni ukrepi | Primerljive novejše raziskave ter ločeni preizkusi izklopa obvestil/večerne uporabe. |
| Lokalno spanje in programi CKZ | Aktualni program, pot do podpore in agregirane meritve pooblaščenih izvajalcev; brez zbiranja osebnih zdravstvenih podatkov v projektu. |
| Poti, šport in AED | Aktualni termini, cene, prevoz, podlaga/prehodnost ter dokumentirana namestitev in urniki AED. |
| Voda pred 2011 | Izvorne letne tabele, ne približki iz grafa. |
| Reka Dobličica | Ločena ARSO serija ekološkega in kemijskega stanja, merilna mesta in obdobja. |
| Adlešiči | Dokumentiran vzrok, ukrepi in sled ponovnih kontrol; brez sklepanja o današnji prepovedi. |
| Zrak | Potrjen agregat BaP 2025, zaključek 2026 in ločevanje lokacij. |
| Stres in samooskrba | Lokalni primerljivi podatki, dostop do zemlje in porazdelitev koristi. |

25. september 2026.
