# Pohodne in kolesarske trase v poročilu

Interaktivni prikaz: `porocilo.html`, poglavje »Pohodne in kolesarske poti«. Deluje brez omrežja; GPX, CSV, GeoJSON in SVG so lokalni prenosi. Izvirnikov v `viri/gpx/` ne spreminjamo.

## Ponovna gradnja

Ukaze izvajaj iz te mape. Dodatne prostorske knjižnice so nameščene lokalno v `.python-deps`; namestitev v novem okolju:

```powershell
python -m pip install --target .python-deps -r requirements-poti.txt
```

Preostale odvisnosti obstoječega poročila: Python-Markdown, BeautifulSoup, openpyxl, Playwright s Chromiumom in PyMuPDF.

```powershell
python -X utf8 analiziraj_poti.py
python -X utf8 pripravi_poti.py
python -X utf8 zgradi_porocilo.py
python -X utf8 preveri_poti.py
python -X utf8 preveri_porocilo.py
```

Prvi korak izračuna geometrijo, dolžine in pasove; traja približno minuto ali dve. Pri spremembi samo besedila ali sloga ni potreben. Drugi korak izdela poglavje, SVG in dve wiki strani; besedilo urejaj v `pripravi_poti.py`, slog v `poti.css`, interakcije v `poti.js`. Zadnji korak preveri celotno poročilo in izdela PDF.

## Izvozi in omejitve

| Datoteka | Vsebina |
| --- | --- |
| `poti-manifest.json` | Izvirne datoteke, kontrolne vsote, lastnosti in izračunane dolžine. |
| `poti-podatki.json` | Polne koordinate, odseki znotraj/zunaj občine, pasovi in statistika. |
| `poti.csv` | Seznam 43 tras. |
| `poti-pokritost-naselij.csv` | Oddaljenost 111 točk OSM od obeh vrst tras. |
| `poti.geojson` | Vseh 43 polnih tras v WGS84 za uporabo v GIS. |
| `poti-zemljevid.svg` | Samostojni vektorski zemljevid občine. |
| `poti-analiza.md` | Bralna različica analize z metodo in ukrepi. |

Pokritost pomeni zračno bližino lokalnih odsekov iz predložene zbirke. Ne pomeni pokritosti prebivalstva, potrjene varnosti ali vseh dejanskih poti. Meja in točke krajev so iz obstoječega zajema OSM 20. 9. 2026. Za dolžine obrežemo vsak zaporedni par točk ločeno, da ne izgubimo ponovnih prehodov; segmentov ne povezujemo med seboj. Dolžine seštejejo ponovne prehode in prekrivajoče trase, površine pasov pa uporabljajo unijo.

Ob novem naboru dopolni preslikavo imen v `analiziraj_poti.py` in datirane trditve v generatorju, ponovno preveri vse rezultate ter ohrani stare manifeste. Besedilo je pripravljeno za konkretni nabor 43 GPX z dne 21. 9. 2026; ni samodejno poročilo za poljuben nov nabor.
