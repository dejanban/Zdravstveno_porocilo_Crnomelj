# Naslednji koraki in stanje projekta

## Navodila in stanje

Uporabnik je naročil dopolnitev glavnega poročila s podatki o življenjskih razmerah, vodi in zraku. Okoljska dopolnitev je vključena v HTML in PDF. Manjkajoča obdobja so označena, niso nadomeščena z ničlami.

Ob začetku obnove so bili stari wiki, vhodni fragmenti, generatorji in številni viri prazni; git arhiv je poškodovan. Ohranjena izdaja poročila je arhivirana v `arhiv/pred-okoljem-2026-09-24/`. Osnova nove gradnje je `vsebina/obnovljena-osnova-20260924.html`, okoljsko besedilo pa `vsebina/okolje-20260924.md`. Osnove ne prepisuj z novim izhodom. Stare vsebine so ohranjene, niso v celoti ponovno preverjene.

## Obnovljena gradnja

| Ukaz | Obseg |
|---|---|
| `python -X utf8 zazeni.py zgradi` | Novi generator iz ohranjene osnove, okoljske vsebine in virov. |
| `python -X utf8 zazeni.py preveri` | Kontrolne vsote obnovljenega obsega, pet širin, sidra, JavaScript, zunanje zahteve, drsnik; izdelava PDF. |
| `python -X utf8 zazeni.py vse` | Gradnja in zgornje preverjanje. |
| `python -X utf8 zazeni.py postrezi` | Lokalni spletni strežnik. |

Preverjanje uporablja Playwright v `tmp/okolje-runtime` in nameščeni Chrome. V omejenem izvajalnem okolju zagon brskalnika zahteva tehnično dovoljenje. Stari generatorji poti, demografije in drugih tem niso obnovljeni; `--preracunaj-poti` se izrecno ustavi. Manifest beleži stanje obnovljenih virov, ne izgubljenih izvirnih kontrolnih vsot.

## Odprte naloge

| Naloga | Potrebni dokaz |
|---|---|
| Obnoviti stare prazne datoteke iz varnostne kopije | Neokrnjeni izvirniki in zgodovina; ne prepisuj novih dopolnitev. |
| Voda pred 2011 | Izvorne letne tabele, ne približki iz grafa. |
| Reka Dobličica | Ločena ARSO serija ekološkega in kemijskega stanja, merilna mesta in obdobja. |
| Adlešiči | Dokumentiran vzrok, ukrepi in sled ponovnih kontrol; brez sklepanja o današnji prepovedi. |
| Zrak | Potrjen agregat BaP 2025, zaključek 2026 in ločevanje lokacij. |
| Stres in samooskrba | Lokalni primerljivi podatki, dostop do zemlje in porazdelitev koristi. |

24. september 2026.
