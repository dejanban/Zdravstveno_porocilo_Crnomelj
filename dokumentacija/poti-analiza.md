# Predložene pohodne in kolesarske trase: prostorska analiza občine

**Pregled 21. 9. 2026:** obdelanih je **43 datotek GPX: 26 pohodnih in 17 kolesarskih**. Znotraj meje Črnomlja ima merljiv odsek **22 tras (14 pohodnih in 8 kolesarskih)**; **21 tras je v celoti zunaj te meje**. To je regionalna zbirka, ne 43 poti v celoti znotraj občine. Pri Poti Gozdna železnica gre le za približno **40 m obmejnega odseka**, zato je treba pripadnost te poti preveriti tudi na uradni meji. [1][2]

Najmočnejša ugotovitev je razlika med vrstama aktivnosti: do pohodniške trase je znotraj **1 km zračne razdalje 62 od 111 točk krajev (55,9 %)**, do kolesarske pa **89 (80,2 %)**. Točke krajev niso gospodinjstva ali urejeni vstopi na pot; deleža **nista deleža prebivalcev**. [1][2]

### Predložene trase in dolžine odsekov v občini

| Vrsta | Datoteke | Z odsekom v občini | Celotne trase (km) | Odseki v občini (km) |
| --- | --- | --- | --- | --- |
| Pohodništvo | 26 | 14 | 265,7 | 143,9 |
| Kolesarstvo | 17 | 8 | 751,7 | 292,5 |
| Skupaj | 43 | 22 | 1.017,3 | 436,4 |

**To so vsote dolžin posameznih tras. Ponovni prehodi po odseku in skupni odseki več tras so šteti večkrat; 436,4 km ni dolžina edinstvenega omrežja ali zgrajenih ločenih poti.** Kolesarski GPX lahko poteka po navadni cesti, pohodni po kolovozu. Oblike infrastrukture iz same sledi ne ugotovimo. Dolžine so dvodimenzionalne in ne vključujejo višinske komponente. [1][2]

### Bližina tras krajem in občinskemu ozemlju

| Bližina trase | Pohodne: kraji | Kolesarske: kraji | Katerakoli: kraji | Delež ozemlja: pohodne / kolesarske / katerakoli |
| --- | --- | --- | --- | --- |
| 0,5 km | 52/111 (46,8 %) | 67/111 (60,4 %) | 80/111 (72,1 %) | 20,9 % / 38,4 % / 46,6 % |
| 1 km | 62/111 (55,9 %) | 89/111 (80,2 %) | 96/111 (86,5 %) | 35,4 % / 62,9 % / 70,9 % |
| 2 km | 84/111 (75,7 %) | 109/111 (98,2 %) | 110/111 (99,1 %) | 61,5 % / 91,4 % / 94,4 % |

Razdalje 0,5 / 1 / 2 km so **analitični pragovi**, ne zdravstveni, evropski ali prometni standard. Delež ozemlja meri geometrijsko bližino, vključno z gozdovi in neposeljenimi območji. Pasovi so unija, prekrivanje se pri površini ne podvaja. Skupna bližina obeh vrst ne pomeni, da je kolesarska trasa primerna za pešce. [1][2]

### Prednostna območja za preverbo dostopa

| Kraj (točka OSM) | Do pohodne trase | Do kolesarske trase |
| --- | --- | --- |
| Vranoviči | 5,6 km | 3,5 km |
| Ručetna vas | 5,4 km | 0,6 km |
| Zastava | 5,0 km | 1,4 km |
| Mihelja vas | 4,9 km | 0,7 km |
| Pavičiči | 4,8 km | 0,8 km |
| Petrova vas | 4,4 km | 1,0 km |
| Gorenja Paka | 4,4 km | 1,7 km |
| Rožanec | 4,0 km | 1,2 km |

**Prednostna preverba za hojo:** Vranoviči, Ručetna vas, Zastava, Mihelja vas in Pavičiči. Razvrstitev je po oddaljenosti od predloženih pohodnih GPX, ne po številu prebivalcev, starosti ali prometni nevarnosti. Obstoječe lokalne poti, ki jih v zbirki ni, lahko sliko bistveno spremenijo. [1][2]

**Pri kolesarjenju** sta najdlje Vranoviči (3,49 km) in Miliči (2,44 km). Vranoviči so edina od 111 zajetih točk več kot 2 km od katerekoli obravnavane trase znotraj občine. Za ukrepanje najprej preveriti, ali manjka GPX, označena povezava ali dejansko varna infrastruktura. [1][2]

### Možnosti za vsakodnevno gibanje in omejitve podatkov

V celoti oziroma vsaj 95-odstotno znotraj občine sta v zbirki **le dve celotni pohodniški trasi dolgi največ 5 km**: Ribja pot – srčna pot Svibnik (4,64 km) in Učna pot Grički kal (4,61 km). Prag 5 km je raziskovalni izbor krajših tras, **ne priporočena razdalja za vsakega uporabnika**. Podatki ne potrjujejo zahtevnosti, prehodnosti z vozičkom, klopi, sence, dostopa brez avtomobila ali dovoljenosti prehoda. [1][2]

Kolesarska krožna pot Črnomelj meri 10,39 km, od tega 10,39 km v občini. Druge lokalno prisotne kolesarske trase so daljše regionalne ture ali njihovi odseki. Za vsakodnevno preventivno vadbo je smiselno **preveriti in opisati krajše uporabne odseke**, ne vsake celotne ture predstavljati kot primerne za začetnike. Pot Dobličica je v mapi pohodnih poti, njeno interno ime GPX pa je »Morning Ride«; vrsta dejavnosti zato zahteva potrditev. [1][2]

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

### Predlagani naslednji koraki

Ukrepi so raziskovalni predlogi. Okvir ur je orientacijska organizacijska ocena, ne ponudba ali potrjen občinski strošek.

| Rok | Ukrep in odgovorni | Viri / možno financiranje | Korist, tveganje in kazalnik |
| --- | --- | --- | --- |
| 0–3 mesece | RIC, občina in lokalna društva preverijo 43 vnosov, prvotni vir, upravljavca, označenost ter manjkajoče trase. Najprej razjasnijo 40 m mejnega stika Poti Gozdna železnica in vrsto poti Dobličica. | 20–40 ur pisarniškega dela; obstoječa sredstva upravljavcev. | Uporaben register; tveganje neodzivnosti. Delež poti s potrjenim upravljavcem in datumom preverbe. |
| 0–12 mesecev | Občina, KS in CKZ preverijo dostopne kratke odseke pri Vranovičih, Ručetni vasi in drugih oddaljenih krajih ter pri Svibniku/Griču opravijo ogled obstoječih krajših tras. | 5–8 terenskih ogledov po 2 osebi, približno 40–80 človek-ur; občinski program športa/turizma in sredstva partnerjev. | Loči vrzel podatkov od vrzeli dostopa; tveganje neurejenih pravic ali cestnih prehodov. Število opisov z varnim dostopom, podlago, ovirami in dolžino. |
| 1–3 leta | Na podlagi ogledov urediti prednostne manjkajoče povezave, označevanje in dogovorjeno vzdrževanje; odgovorni občina, upravljavci cest in lastniki. | Ločen popis del in projektantska ocena; možni občinski proračun, LAS ali namenski razpisi, upravičenost še ni preverjena. | Več uporabnih povezav; tveganje gradnje brez uporabnikov ali vzdrževanja. Število potrjenih dostopnih povezav in števci uporabe. |
| 1–3 leta | CKZ in društva preizkusijo redno vodeno hojo na preverjenih odsekih; spremljajo vključitev, vztrajanje in ovire dostopa. | Najprej dve skupini, okvirno 2–4 ure vodenja/koordinacije tedensko skupaj; sredstva programov izvajalcev. | Povezava poti z dejansko dejavnostjo; tveganje osipa. Udeležba po treh in šestih mesecih, ne samo število dogodkov. |
| 3–10 let | Vzpostaviti letno obnavljan register poti in dostopa iz naselij, povezan z uradnimi prostorskimi podatki, prebivalstvom in proračunom. | Letni načrt vzdrževanja in podatkov; obseg naložb šele po prioritetah. | Trajnejša dostopnost; tveganje zastarelih podatkov. Delež prebivalcev z dejansko varnim dostopom po mreži in pravočasno izvedeno vzdrževanje. |

## Literatura

[1] Predložena zbirka GPX, naročnik poročila, obdelava 21. 9. 2026. Izvirniki: `viri/gpx/`; kontrolne vsote: `podatki/poti/poti-manifest.json`.

[2] Meja Črnomlja in točke krajev, sodelavci OpenStreetMap, zajem 20. 9. 2026. https://www.openstreetmap.org/relation/1685747. Lokalna kopija: `viri/osm-crnomelj.json`; metodologija v wiki sintezi `pokritost-poti-crnomelj-2026.md`.
