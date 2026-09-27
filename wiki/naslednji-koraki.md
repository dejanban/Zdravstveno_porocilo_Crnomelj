# Naslednji koraki in stanje projekta

## Navodila in stanje

Veljajo navodila uporabnika: modra/jesenska prenova z enajstimi povezanimi zavihki, raziskava spanja in digitalnih navad, okoljska dopolnitev (življenjske razmere, voda, zrak). Manjkajoča obdobja niso nadomeščena z ničlami. Ohranjeni morajo ostati samostojno delovanje brez omrežja, stara sidra, dostop s tipkovnico, iskanje skrite vsebine in celotna vsebina v PDF. 25. 9. 2026 je uporabnik naročil celovit pregled, ureditev in dopolnitev z relevantnimi viri, nato še šest novih tem: nujna pomoč in prvi posredovalci, neopredeljeni in čakalne dobe, vročinski valovi, duševno zdravje mladih, dolgotrajna oskrba in pomoč na domu, prometna varnost in alkohol. Poročilo ima zdaj 12 zavihkov (nov: »Dostop do oskrbe«).

**Obnova arhiva (25. 9. 2026):** commit d96d620 je po nesreči izpraznil 1.087 datotek; obnovljene so iz commita 0dc0bd4 z `orodja/obnovi_iz_gita.py` (samo datoteke z 0 bajti). Izvirni manifest je v `viri/manifest.json` pod `izvorni_manifest` in se preverja ob vsakem `preveri`. Izvirniki takrat okrnjenih živih datotek so v `arhiv/izvirnik-0dc0bd4/`. Še vedno prazno brez različice v gitu (1.183 datotek): predvsem zajem spletišča Komunale v `viri/Komunala_Crnomelj/`, `arhiv/pred-popravkom-aed-2026-09-23/`, `viri/aed/javna-dostopnost-2026-09-23.*` in `podatki/aed/aed-viri.json`. Git na Windows ne vidi dolgih poti Komunale: uporabljaj `git -c core.longpaths=true`.

Gradnja izhaja iz `vsebina/obnovljena-osnova-20260924.html`; osnove ne prepisuj z novim izhodom. Spremembe vnašaj v vhode: `vsebina/okolje-20260924.md`, `vsebina/spanje-digitalne-navade.md`, `vsebina/prenova.css`, `vsebina/prenova.js`, `orodja/prenovi_porocilo.py` (tudi `update_content` za datirane posodobitve iz `podatki/posodobitve/posodobitve-viri.json`) in `orodja/zgradi_okolje_porocilo.py`. Nove teme: besedila v `vsebina/teme/*.md` (citati `[@oznaka]` za vire iz `podatki/teme/teme-viri.json`, `[@ref:vir-N]` ali `[@ref:env-…]` za obstoječe vire poročila), funkcija `teme_content` v `orodja/prenovi_porocilo.py` ustvari poglavja in wiki strani. Obnovljeni stari generatorji (`pripravi_*.py`, `zgradi_porocilo.py`) niso del trenutne gradnje; ne zaganjaj jih, ker bi prepisali novo poročilo.

## Gradnja

| Ukaz | Obseg |
|---|---|
| `python -X utf8 zazeni.py zgradi` | Ohranjena osnova, okolje, spanje, posodobitve ZD, zavihki, literatura in knjižnica. |
| `python -X utf8 zazeni.py preveri` | Kontrolne vsote (novi viri, okolje, izvirni manifest), pet širin, 11 zavihkov, tipkovnica, iskanje, filtri, zemljevidi, register, brez JavaScripta, PDF. |
| `python -X utf8 zazeni.py vse` | Gradnja in preverjanje (zadnji uspešen zagon 26. 9. 2026: 12 zavihkov, 155 strani PDF, 196 virov, zemljevid dostopnosti, 1 manjkajoč prenos). |
| `python -X utf8 orodja/obnovi_iz_gita.py` | Ponovno obnovi datoteke z 0 bajti iz 0dc0bd4 (varno; neprazne preskoči). |
| `python -X utf8 orodja/zajemi_teme.py [--osvezi]` | Izvlečki in manifest za vire novih tem; z `--osvezi` ponovno prenese izvirnike (omrežje). |
| `python -X utf8 orodja/zajemi_poti_nmp.py [--osvezi]` | Cestne poti OSRM za zemljevid (omrežje, ~4 min); zemljevid gradi `orodja/zemljevid_nmp.py` v okviru `zgradi`. |
| `python -X utf8 orodja/analiziraj_dostopnost_nmp.py [--osvezi]` | Modelska dostopnost naselij; z `--osvezi` ponovno pokliče OSRM. |

Preverjanje uporablja Playwright v `tmp/okolje-runtime` in Microsoft Edge (`channel='msedge'`). `--preracunaj-poti` se ustavi.

## Odprte naloge

| Naloga | Potrebni dokaz |
|---|---|
| Vodstvo ZD | Uradna potrditev izbire direktorja (zapisnik sveta 21. 9. 2026, soglasje občinskega sveta); datum in trajanje imenovanja v. d. |
| Razpored ambulant | Mesečno ponoviti posnetek strani »Odsotnost zdravnikov«; pridobiti podatke ZZZS o neopredeljenih osebah in čakalnih dobah. |
| Zapis naročnika o AED (23. 9. 2026) | Uporabnik naj ponovno posreduje besedilo; v gitu ga ni. |
| Zajem spletišča Komunale | Prazne `.md`/strani v `viri/Komunala_Crnomelj/` ponovno zajeti ali izbrisati iz evidence, če se ne uporabljajo. |
| Šest okoljskih neskladij in `AEDs.xlsx` | Neokrnjena kopija ali transparenten nov zajem. |
| Štirje celotni članki o spanju | Carter 2016, Itani 2017, Ahmed 2024/2025. |
| Aktualnost starejših ugotovitev | Kader, šport, društva, AED in NIJZ so presek 19.–22. 9. 2026; ob naslednji seji ponovno preveriti ključne. |
| Voda pred 2011, Dobličica, Adlešiči, BaP 2025 | Kot v okoljski temi. |
| Nove teme: manjkajoči lokalni podatki | Dostopni časi NMP in obseg mreže prvih posredovalcev (ZD), neopredeljeni po ZZZS, čakanje po prebivališču (NIJZ/SB NM), čakalni seznam pomoči na domu (DSO), načrt ob vročini (občina), čakalne dobe psihološke ambulante, podatki PP Črnomelj o nesrečah. |
| Zahteve IJZ (osnutki 26. 9. 2026) | Uporabnik jih pošlje sam iz `dokumentacija/zahteve-ijz/`; rok 20 delovnih dni. Odgovore shraniti v `viri/odgovori-ijz/`. Pri PU Novo mesto preveriti e-naslov. |
| Model dostopnosti | Scenariji A (predpostavke 1–2 min obdelave klica, faktor vožnje 0,8–1,2) in B (druga ekipa). Umeriti na dejanske dostopne čase ZD; dve naselji (Podbrežje, Gorenja Paka) nista povezani s SURS. |
| GPX trim steze Vražji kamen | Uporabnik ga bo posredoval. Postopek je v zadnjem vnosu dnevnika (26. 9. 2026): shraniti v viri/gpx/pohodnistvo/, izračunati kazalnike, dodati traso v `route_layer` in popraviti preglednico v `vsebina/teme/poti-dopolnitve.md`. |
| Umerjanje časov vožnje | Naročnik vpiše Googlove čase v `podatki/teme/kalibracija-google.csv` (vsaj 6 od 14); nato `orodja/kalibracija_casov.py` in `zazeni.py vse`; posodobiti številke v poglavju o nujni pomoči. |
| Demenca in digitalno zdravje: lokalni podatki | Uporaba zVEM po starosti v občini (NIJZ), obstoj lokalnih programov za demenco (občina, DSO, CSD), agregirani podatki ZZZS o zdravljenju demence. |
| Imenik »Kam po pomoč« | Kontakti so s spletnih strani (26. 9. 2026), ne telefonsko preverjeni; ob vsaki večji posodobitvi jih preveriti. |
| Zaprti članki | Janoš 2025 in Scquizzato 2022 samo povzetek; Bergen 2014 povzetek + Community Guide. |
| Še neobdelane predlagane teme | Radon, romska naselja (dostop do vode in zdravstva, brez stigmatizacije), cepljenje (pnevmokok je značilno slabši), klopni meningoencefalitis. |

25. september 2026.
