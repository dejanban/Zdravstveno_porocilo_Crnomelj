# Vir: 43 tras GPX in prostorska pokritost občine

## Povzetek

**Pregled 21. 9. 2026:** obdelanih je **43 datotek GPX: 26 pohodnih in 17 kolesarskih**. Znotraj meje Črnomlja ima merljiv odsek **22 tras (14 pohodnih in 8 kolesarskih)**; **21 tras je v celoti zunaj te meje**. To je regionalna zbirka, ne 43 poti v celoti znotraj občine. Pri Poti Gozdna železnica gre le za približno **40 m obmejnega odseka**, zato je treba pripadnost te poti preveriti tudi na uradni meji. [1][2]

Najmočnejša ugotovitev je razlika med vrstama aktivnosti: do pohodniške trase je znotraj **1 km zračne razdalje 62 od 111 točk krajev (55,9 %)**, do kolesarske pa **89 (80,2 %)**. Točke krajev niso gospodinjstva ali urejeni vstopi na pot; deleža **nista deleža prebivalcev**. [1][2]

## Izvor in zanesljivost

GPX je zagotovil uporabnik. Zanesljivost je visoka za vsebino datotek in ponovljive izračune, neznana za aktualno stanje v naravi in popolnost. OSM je sekundarna kartografska osnova; uradne meje in naselja niso bili pridobljeni. Izvirne datoteke niso spremenjene. [1][2]

### Metoda izračuna in omejitve

| Korak | Postopek in omejitev |
| --- | --- |
| Vhod | Vseh 43 predloženih GPX, 67.518 trasnih točk; razvrstitev po mapah. Izračun ni dopolnjeval manjkajočih poti. |
| Razmejitev | OpenStreetMap, relacija 1685747, zajem 20. 9. 2026; izračunana površina približno 339,4 km². OSM ni uradna geodetska meja. |
| Dolžine | Vsak segment ločeno, brez povezovanja konca enega z začetkom naslednjega. Za lokalno dolžino je posebej obrezan vsak zaporedni par točk: ponovni prehodi so ohranjeni. WGS84 geodetska dolžina; preseki s poligonom občine v UTM 33N. |
| Kraji | 111 točk tipa town/village iz obstoječega OSM zajema. Brez zaselkov tipa hamlet, brez uteži prebivalstva in brez trditve, da gre za vsa uradna naselja. |
| Razdalja | Najkrajša zračna razdalja do črte **znotraj občine** v metrih, ne samo do najbližje shranjene točke. Zunajobčinski odseki niso uporabljeni za ta kazalnik. |
| Pasovi | Polmer 500 / 1.000 / 2.000 m, unija in presek z občino. Za površino so trase poenostavljene največ 5 m; loki imajo 16 odsekov na kvadrant. Zemljevid dodatno poenostavi pasove za 20 m, kar ne spremeni že izračunanih tabel. |
| Kakovost | 0 neveljavnih koordinat, 0 povsem enakih geometrij datotek. Največji razmik zaporednih točk je 537 m: GPX med točkami predpostavlja ravno povezavo. Brez terenske potrditve. |
| Česa ne merimo | Prebivalcev v dosegu, časa hoje/vožnje, prometa, podlage, naklona, zapor, lastništva, oznak, stroškov, vzdrževanja in zdravstvenega učinka. Datumi v GPS posnetku niso datum terenske preverbe. |

## Glavne ugotovitve

| Vrsta | Datoteke | Z odsekom v občini | Celotne trase (km) | Odseki v občini (km) |
| --- | --- | --- | --- | --- |
| Pohodništvo | 26 | 14 | 265,7 | 143,9 |
| Kolesarstvo | 17 | 8 | 751,7 | 292,5 |
| Skupaj | 43 | 22 | 1.017,3 | 436,4 |

**To so vsote dolžin posameznih tras. Ponovni prehodi po odseku in skupni odseki več tras so šteti večkrat; 436,4 km ni dolžina edinstvenega omrežja ali zgrajenih ločenih poti.** Kolesarski GPX lahko poteka po navadni cesti, pohodni po kolovozu. Oblike infrastrukture iz same sledi ne ugotovimo. Dolžine so dvodimenzionalne in ne vključujejo višinske komponente. [1][2]

## Povezane strani

[[../../analysis/synthesis/pokritost-poti-crnomelj-2026]] · pregled peš poti, kolesarskih poti in športnih objektov (stran nadrejenega vaulta, ni del tega projekta)

## Zadnja posodobitev

2026-09-21.

## Literatura

[1] »Predložena zbirka 43 poti GPX,« naročnik poročila, obdelava 21. septembra 2026. Lokalni izvirniki: `viri/gpx/`; [[../../../viri/splet/poti-gpx-20260921-manifest|manifest s kontrolnimi vsotami]]. Izračuni: [[../../../podatki/poti/poti-podatki.json]], [[../../../podatki/poti/poti-pokritost-naselij.csv]].

[2] »Meja Črnomlja in točke krajev,« sodelavci OpenStreetMap, 20. september 2026. [Na spletu]. Dostopno: https://www.openstreetmap.org/relation/1685747. [Dostopano: 20. september 2026]. Lokalna kopija: [[../../../viri/splet/osm-crnomelj-poti-20260921]]. © sodelavci OpenStreetMap, ODbL.
