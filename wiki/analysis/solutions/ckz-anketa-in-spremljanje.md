# CKZ: anketni list in sistem spremljanja napredka

## Povzetek

Pripravljena je **delovna predloga 1.0 z dne 22. 9. 2026**: mesečni list ekipe z osmimi merili, deset vprašanj za odrasle udeležence, navodila in prazna Excelova preglednica agregatov. Namen je redno povezovati ugotovljene ovire, odzivnost in spremembe z ukrepi. Ne gre za validirano zdravstveno lestvico, uradni obrazec NIJZ ali potrjeno uvedbo v CKZ.

| Izdelek | Dostop |
|---|---|
| Obrazci za tisk, štiri strani | [HTML](../../../podatki/ckz/ckz-obrazci.html), [PDF](../../../podatki/ckz/ckz-obrazci.pdf) |
| Prazna preglednica agregatov | [Excel](../../../podatki/ckz/ckz-spremljanje.xlsx) |
| Spletni razdelek | [Poročilo](../../../porocilo.html#ckz-spremljanje) |
| Uredniški vhod in generator | [Besedilo obrazcev](../../../vsebina/ckz-obrazci.md), [generator](../../../orodja/pripravi_ckz.py) |

## Trenutno stanje

NIJZ opisuje spremljanje obravnav in oddajo mesečnih paketov prek eSZBO v polletnih rokih. [1] To utemeljuje pregled obstoječih evidenc pred uvajanjem dodatnega vnosa. **Status: Unverified** — ni preverjeno, katere od predlaganih podatkov CKZ Črnomelj že zbira ali lahko izvozi; ni potrjeno sprejetje predloge. Priprava ne spreminja obstoječe uredniške ocene CKZ 3,4/5 ali statusa zdravstvene teme.

## Ključna dejstva

| Element predloga | Opredelitev in omejitev |
|---|---|
| Mesečni list ekipe | Preglednost, dostop, potrebe, dokazi/izidi, pravičnost, stroški, trajnost in izvedljivost; ocena, dokazilo in vrzel; sklep z ukrepom, nosilcem in rokom. |
| Udeleženec | Ob začetku in pri nadaljnjih stikih vprašanja 1–7; ob zaključku še 8–10 (razumljivost, zadovoljstvo, predlog). Prostovoljno, z možnostjo neodgovora. Za odrasle; za otroke potrebna prilagoditev. |
| Termini | T0 pred obravnavo, T1 ob zaključku, T6/T12 po 6/12 mesecih od referenčnega zaključka, predlagano okno ±30 dni. Pri osipu uporabiti predvideni zaključek skupine. |
| Imenovalec kontrol | Vsi začetniki kohorte, katerih kontrolno okno je do preseka poteklo; vključiti tudi nedokončane. Nezapadle prikazati posebej. |
| Vedenjski izid | Število dni izvajanja iste konkretne navade v zadnjih 7 dneh; parna razlika T6 − T0 in T12 − T0, mediana ter število parov. Ob spremembi navade novo izhodišče. |
| Ločene razsežnosti | Zadovoljstvo, zaupanje, navada in organizacijska samoocena niso skupna »ocena zdravja«. Pri zadovoljstvu posebej veljavni odgovori in vsi povabljeni. |
| Manjkajoči podatki | Prazno ni ničla. Pri imenovalcu 0 rezultat ni izračunljiv. Neodziv ni samodejno uspeh ali neuspeh. |

### Metoda samoocene ekipe

Lestvica: 1 = ni urejeno; 2 = dogovorjeno, še ne deluje; 3 = delno deluje; 4 = redno deluje z dokazili; 5 = redno deluje, izidi se preverjajo in vodijo v izboljšave. N/P = ni podatka, N/U = ni uporabno (z razlogom). Vseh osem meril ima ob popolni oceni utež 12,5 %; izračun je vsota osmih ocen / 8. Pri manjkajočih ocenah samo delno povprečje in n/8; primerjava dovoljena le za isti nabor. Dejanske ocene še niso vnesene; organizacijskega predloga ni pošteno oceniti kot že izvedene storitve. Klinična in stroškovna učinkovitost nista ocenjeni. Obstoječa petmerilna uredniška ocena 3,4/5 ostaja ločena.

## Viri

Primarni institucionalni vir NIJZ [1], visoka zanesljivost za opis nacionalnega poročanja. Prebrano osrednje besedilo spletne strani 22. 9. 2026; povezana metodologija in slikovna tabela nista bili pregledani. Lokalna potreba po javnem prikazu izidov je obravnavana na [[../../entities/institutions/ckz-crnomelj|strani CKZ]]. Predlagana vprašanja, kontrolna okna, lestvice in obseg dela so avtorska zasnova, ne povzetek obveznosti NIJZ.

## Identificirani problemi

| Vrzel v javnem pregledu oziroma tveganje pri uvedbi | Kaj mora rešiti spremljanje |
|---|---|
| Razpršeni podatki in nejasni imenovalci | Slovar, kohorte, ločevanje oseb od obiskov, pregledi kakovosti. |
| Nepoznan osip, ovire in dolgotrajnost sprememb | Kontrolni koledar, papirna možnost, isti izid skozi čas in prikaz manjkajočih podatkov. |
| Rezultati brez odgovornosti za spremembe | Dnevnik ukrepov, rok, nosilec, izhodišče, cilj in naslednji pregled. |
| Neznana obremenitev, stroški in dolgoročna vzdržnost | Izmerjen čas zbiranja, uporaba obstoječega izvoza, načrt nadomeščanja. |

## Kritična vprašanja

| Za koga | Vprašanje in zahtevani dokaz |
|---|---|
| Vodja CKZ | Katera polja že zbirate? Priložite seznam polj in prazne obstoječe obrazce, brez osebnih podatkov. |
| Skrbnik evidenc ZD | Kako odstranite podvajanje oseb med meseci in programi? Predložite pravilo ter kontrolni agregat. |
| CKZ in NIJZ | Katera veljavna navodila so uporabljena pri izvozu? Predložite različico, datum in preslikavo polj. |
| Izvajalci dveh pilotnih programov | Kaj šteje kot začetek in zaključek? Predložite definicijo, koledar in pravilo pri osipu. |
| Koordinator CKZ | Kdo je v imenovalcu T6/T12 in kdo še ni zapadel? Predložite agregat zapadlih, nezapadlih, odgovorov in neodzivov. |
| Strokovna ekipa | Ali udeleženci razumejo navado in lestvice? Predložite anonimiziran zapis preizkusa razumljivosti in potrebnih sprememb. |
| Vodstvo ZD | Kdo sme dostopati do odgovorov in kdaj se izbrišejo? Predložite sprejeti postopek, obvestilo in razdelitev vlog. |
| CKZ, občini in KS | Katere ovire pri prevozu in terminih so najpogostejše? Predložite dovolj velike agregate in izvedbeni odziv z rokom. |
| Računovodstvo ZD | Kako pripišete stroške isti kohorti? Predložite obračunsko metodo, ure in vključene vrste stroškov. |
| Svet zavoda | Kateri ukrepi so bili izvedeni do roka in kaj se je spremenilo? Predložite četrtletni dnevnik in kazalnik pred/po. |
| CKZ in partnerska društva | Koliko dogovorjenih prehodov v nadaljnjo dejavnost je bilo izvedenih? Predložite zbirni rezultat brez individualnih izmenjav podatkov. |
| Vodstvo ZD in metodološki pregledovalec | Kateri rezultati so primerljivi z drugimi centri? Predložite ujemanje programa, starosti, obdobja, instrumenta in odzivnosti. |

## Tveganja

Samoocena lahko olepša delo; vsaka ocena zato potrebuje dokazilo. Prostovoljni odziv in izguba pri spremljanju lahko pristranita rezultate; poročati je treba o vseh začetnikih in razpoložljivih parih. Različne navade niso neposredno primerljiv zdravstveni izid. Povezljiv vprašalnik s šifro ni anonimen; odgovori in povezovalni ključ ostanejo v varovanem okolju CKZ, nikoli v tem projektu. Pri javnih agregatih predlagani prag n < 5 sam ne zagotovi anonimnosti; preveriti tudi kombinacije in izračun iz seštevkov. Papir in pomoč zmanjšujeta digitalno izključevanje; ne označevati krajev ali skupin kot »neuspešnih«. Predloga ne omogoča vzročne presoje učinkov.

## Možne rešitve

| Problem | 0–12 mesecev | 1–3 leta | 3–10 let |
|---|---|---|---|
| Razpršeni podatki | Slovar, pregled izvoza in pilot dveh programov. | Redni agregatni prikaz iz iste evidence. | Letna presoja kakovosti in ohranitev primerljivosti. |
| Osip in ovire | Koledar kontrol, papirni odgovor, popis ovir. | Prilagoditev terminov in povezovanje s partnerji. | Preverjanje trajnosti ter enakosti dostopa ob vsaki obnovi programa. |
| Ni odziva na ugotovitve | Mesečni list in en ukrep z rokom. | Četrtletna obravnava pri vodstvu. | Zunanja metodološka presoja po štirih letih in ponovitve. |
| Obremenitev in stroški | Izmeriti čas, izločiti dvojni vnos. | Urediti nadomeščanje in stroške kohort. | Zagotoviti trajen načrt ur, podpore in financiranja. |

| Obdobje | Nosilec, planski viri in možno financiranje | Korist, tveganje in merjenje |
|---|---|---|
| 0–12 mesecev | CKZ in skrbnik podatkov ZD; znotraj že predlaganih 10–20 dni vzpostavitve in 1–2 dni mesečno, ne dodatno k njim; kontrolni stiki po številu oseb in izmerjenem času. Možna sredstva ZD. | Manj dvojnega vnosa in boljši odziv; tveganje birokracije in izključitve. Po 3 mesecih čas in manjkajoči podatki, po 6/12 mesecih odziv in parne spremembe. |
| 1–3 leta | CKZ, ZD, občini in partnerji; plansko četrtletni 60-minutni pregled, ure izvoza in partnerjev posebej. Možni redni programi ali potrjena dopolnila. | Vidna odgovornost in lažji prehodi; tveganje razkritja ali stigme. Letni pregled ukrepov, dostopa, stroškov in 12-mesečnih izidov. |
| 3–10 let | Vodstvo ZD, metodološka podpora po dogovoru; letni načrt ur, strošek zunanje presoje po opredelitvi obsega. Možna sredstva ZD in upravičeni razvojni viri, brez domneve razpisa. | Kontinuiteta in zanesljivejše primerjave; tveganje menjave ekip in definicij. Letni pregled kakovosti, po 4 letih presoja trajnosti z ustrezno primerjalno zasnovo. |

## Primerjave

Za to avtorsko anketo ni primerljivih rezultatov drugih CKZ, JV Slovenije, Slovenije, EU/OECD ali podobnih občin. Pred primerjavo pridobiti enake instrumente, ciljne skupine, programe, obdobja in podatke o odzivu. Lokalno primerjati enake kohorte in definicije skozi čas; občinski kazalniki NIJZ niso kontrolna skupina programa.

## Odprta vprašanja

CKZ mora preveriti prekrivanje z obstoječimi obrazci, veljavne protokole, izvedljivost kontrol in razumljivost za odrasle z različnimi potrebami. Cilji naj sledijo prvemu trimesečnemu pregledu. Izpolnjenih odgovorov nismo pridobivali, uvedba ni potrjena in nobena organizacija ni bila kontaktirana.

## Povezane strani

| Stran | Namen |
|---|---|
| [[../../entities/institutions/ckz-crnomelj]] | Obstoječi dokazi in uredniška ocena |
| [[../synthesis/pregled-za-kandidata]] | Predlogi za mandat |
| [[../../sources/source-summaries/ckz-spremljanje-nijz-2026-09-22]] | Prebrani primarni vir in omejitve |

## Zadnja posodobitev

2026-09-22 — predloga 1.0; brez vnesenih rezultatov CKZ.

## Literatura

[1] »Zdravstvenovzgojni centri / Centri za krepitev zdravja (ZVCT),« NIJZ, 14. april 2023, posodobljeno 7. april 2025. [Na spletu]. Dostopno: https://nijz.si/podatki/podatkovne-zbirke-in-raziskave/zdravstvenovzgojni-centri-centri-za-krepitev-zdravja-zvct/. [Dostopano: 22. september 2026]. Lokalna kopija: [[../../../viri/splet/ckz-nijz-spremljanje-2026-09-22.md]].
