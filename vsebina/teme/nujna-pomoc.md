# Dostop do nujne pomoči in prvi posredovalci

## Povzetek

Od 3. junija 2026 velja nov pravilnik o službi nujne medicinske pomoči (NMP). Povprečni dostopni čas prve ekipe za intervencije I. prioritete sme na letni ravni znašati največ 15 minut. Prvi posredovalci so po novem izrecna naloga izvajalcev NMP, sredstva za njihovo usposabljanje pa zagotavlja državni proračun. [@pravilnik-nmp-2026] ZD Črnomelj v letnem poročilu 2025 cilj »dokončna vzpostavitev prvih posredovalcev v občini Črnomelj« označuje kot realiziran, v programu 2026 pa napoveduje nadaljevanje izobraževanj. [@ref:vir-5] [@ref:vir-8] Števila usposobljenih prvih posredovalcev, njihove razporeditve po krajih, aktivacij in dejanskih dostopnih časov NMP zavod ne objavlja.

Modelska ocena pokaže okvir problema. Ko je ekipa ZD Črnomelj prosta, ima po srednji predpostavki ocenjen dostopni čas nad 15 minut 25 % prebivalcev (razpon 20–34 % glede na hitrost vožnje). Največ takih ljudi živi v Poljanski dolini, ob Kolpi in v okolici Vinice. Ko je ekipa zasedena in mora priti druga iz Metlike ali Novega mesta, je nad 15 minut skoraj vsa občina (99 %, povprečno 26,5 minute). [@osrm-tabela] [@surs-naselja-2026] [@zd-metlika-nmp] Za takšna območja raziskave podpirajo sistem aktiviranih prvih posredovalcev: v metaanalizi je bilo preživetje srčnega zastoja zunaj bolnišnice ob njihovi aktivaciji višje (9,1 % proti 8,3 %). [@scquizzato-2022]

## Trenutno stanje

ZD Črnomelj navaja, da je NMP organizirana 24 ur na dan. Na spletni strani piše, da zdravnik ob delu v ambulanti opravlja tudi nujne obiske na terenu, medicinska sestra pa je stalno prisotna in sprejema nujne klice. [@zd-nmp] Letno poročilo 2025 in program 2026 navajata dežurno službo, triažo satelitskega urgentnega centra (SUC), nujno reševalno vozilo (NRV) in vozilo urgentnega zdravnika (VUZ). V letu 2025 je zavod dobil dodatnih 0,5 tima NRV. [@ref:vir-5] [@ref:vir-8] Zavod piše tudi, da zdravniki poleg ambulante sodelujejo v SUC, urgentni in dežurni službi. Od 1. 2. 2023 delajo še v ambulantah za neopredeljene. [@ref:vir-8] Koliko intervencij se prekriva in koliko časa je ekipa odsotna iz ambulante, ni objavljeno.

Prvi posredovalci: ZD cilj vzpostavitve mreže v letnem poročilu 2025 označuje kot »realiziran« z opisnim kazalnikom. [@ref:vir-5] To je samoocena zavoda. Število evidentiranih prvih posredovalcev, sodelujoča društva, pokritost odmaknjenih krajev in način aktivacije niso objavljeni. Status: Unverified.

## Ključna dejstva

### Kaj določa pravilnik iz leta 2026

| Določba | Vsebina | Pomen za Črnomelj |
|---|---|---|
| Dostopni čas | Čas od dviga slušalke v dispečerski službi do prihoda ekipe na kraj. Letno povprečje prve prispele ekipe za I. prioriteto ne sme presegati 15 minut; izvozni čas največ 1 minuta. [@pravilnik-nmp-2026] | Povprečje lahko prikrije daljše čase za oddaljena naselja. Potreben je prikaz po naseljih oz. razdaljah. |
| Prvi posredovalec | Polnoletna, usposobljena in evidentirana oseba, ki jo aktivira dispečerska služba in začne temeljne ukrepe pred prihodom NMP. Znanje obnavlja vsaj enkrat na leto. [@pravilnik-nmp-2026] | Najbolj smiseln je v naseljih, kamor ekipa NMP potrebuje največ časa. |
| Naloge izvajalca NMP | Ugotavlja potrebe po prvih posredovalcih, usposablja kandidate, vodi evidenco in poroča ministrstvu; lahko sklene dogovor z organiziranimi skupinami (npr. gasilci). [@pravilnik-nmp-2026] | ZD Črnomelj kot izvajalec NMP je zadolžen za oceno potreb na svojem območju. |
| Financiranje | Sredstva za naloge izvajalcev pri prvih posredovalcih zagotavlja proračun RS. [@pravilnik-nmp-2026] | Uvedba ni odvisna samo od občinskega proračuna. |
| AED | Javno dostopni AED se vključijo v evidenco dispečerske službe; nevzdrževane naprave se iz nje izključijo. [@pravilnik-nmp-2026] | Povezuje se z zavihkom AED: lokacija sama ni dovolj, pomembni sta vzdrževanje in vključenost v evidenco. |
| Poročanje | Letno poročilo vključuje aktivacije prvih posredovalcev, njihov odzivni čas, oživljanja, defibrilacije in povprečni čas do prihoda ekipe. [@pravilnik-nmp-2026] | Podatki bodo obstajali in jih je mogoče javno zahtevati v agregirani obliki. |

### Modelska dostopnost naselij

Metoda: 111 naselij iz OpenStreetMap smo povezali s prebivalstvom SURS 1. 1. 2026 po imenu (109 ujemanj, 13.943 od 14.170 prebivalcev). Za vsako naselje smo s strežnikom OSRM izračunali čas običajne vožnje po cestah od ZD Črnomelj (Delavska pot 4), ZD Metlika in Splošne bolnišnice Novo mesto z urgentnim centrom. [@surs-naselja-2026] [@osrm-tabela] Dostopni čas po pravilniku teče od dviga slušalke v dispečerski službi do prihoda ekipe. [@pravilnik-nmp-2026] Ocenili smo ga kot vsoto treh delov: obdelava klica (predpostavka 1–2 min), izvoz (največ 1 min po pravilniku) in vožnja, pomnožena s faktorjem. Faktor 0,8 predstavlja hitrejšo nujno vožnjo, 1,0 običajno vožnjo in 1,2 slabše razmere; vse tri vrednosti so predpostavke. Model ne pozna dejanske zasedenosti ekip, vremena, iskanja naslova ali poti od vozila do bolnika. To ni izmerjeni dostopni čas.

| Scenarij | Ocenjen dostopni čas nad 15 min: prebivalci | Delež | Od tega 65+ | Uteženo povprečje |
|---|---|---|---|---|
| A: ekipa ZD Črnomelj prosta, srednja predpostavka (1,5 + 1 + vožnja × 1,0) | 3.512 | 25,2 % | 943 | 11,4 min |
| A: hitrejša nujna vožnja (1 + 1 + vožnja × 0,8) | 2.801 | 20,1 % | 758 | 9,2 min |
| A: počasnejša vožnja (2 + 1 + vožnja × 1,2) | 4.784 | 34,3 % | 1.266 | 13,7 min |
| B: ekipa ZD Črnomelj zasedena, pride najbližja druga ekipa (ZD Metlika ali UC Novo mesto), srednja predpostavka | 13.842 | 99,3 % | 3.518 | 26,5 min |

**Opozorilo o natančnosti (26. 9. 2026):** preverjanje naročnika z Google Maps je pokazalo, da se modelski časi ne ujemajo z Googlovimi. Drug odprtokodni model (Valhalla) na istih cestah pogosto vrne daljše čase; pri Gribljah OSRM izbere ozko lokalno cesto z vpisano omejitvijo 90 km/h. Zgornji deleži so zato okvirni, dokler časi niso umerjeni na Googlove vrednosti. Zemljevid spodaj že kaže razpon obeh modelov. [@valhalla-casi]

Scenarij B pokaže, kako pomembni sta druga ekipa v Črnomlju in mreža prvih posredovalcev. Kolikokrat na leto pride do sočasnih intervencij, ni objavljeno. ZD Metlika ima NMP organizirano 24 ur na dan. [@zd-metlika-nmp]

| Samo čas vožnje od ZD Črnomelj (brez klica in izvoza) | Naselja | Prebivalci | Delež zajetih prebivalcev | Od tega 65+ |
|---|---|---|---|---|
| do 10 minut | 34 | 9.159 | 65,7 % | 2.274 |
| 10–15 minut | 20 | 1.790 | 12,8 % | 454 |
| 15–20 minut | 19 | 1.142 | 8,2 % | 288 |
| 20–30 minut | 19 | 1.221 | 8,8 % | 336 |
| nad 30 minut | 17 | 631 | 4,5 % | 188 |

| Primer naselja | Prebivalci 2026 | Modelska vožnja od ZD | Zračna razdalja do najbližjega AED v registru |
|---|---|---|---|
| Vinica | 245 | 27,0 min | 0,18 km |
| Zilje | 139 | 30,2 min | 0,91 km |
| Preloka | 103 | 33,0 min | 0,13 km |
| Učakovci | 105 | 33,9 min | 2,73 km |
| Vukovci | 33 | 36,8 min | 2,82 km |
| Dalnje Njive | 16 | 36,8 min | 1,87 km |

Celotna preglednica 111 naselij je v [podatkih o dostopnosti (CSV)](podatki/teme/dostopnost-naselij.csv). Poti in čase za vsako naselje prikazuje [interaktivni zemljevid](#zemljevid-nmp). Razdalja do AED je zračna in ne pove, ali je naprava dosegljiva ponoči, ali je zaklenjena in kdo jo lahko prinese. Točka naselja v OSM je ena koordinata, ne naslov posameznega doma.

### Kaj kažejo raziskave o prvih posredovalcih

| Raziskava | Zasnova | Ugotovitev | Omejitve |
|---|---|---|---|
| Scquizzato in sod., 2022 [@scquizzato-2022] | Sistematični pregled in metaanaliza, 10 raziskav, 23.351 bolnikov s srčnim zastojem zunaj bolnišnice; aktivacija državljanov prek mobilnih aplikacij proti običajnemu odzivu. | Preživetje do odpusta ali 30 dni 9,1 % proti 8,3 % (OR 1,45; 95-% IZ 1,21–1,74); oživljanje očividcev 65 % proti 53 %; uporaba AED pred prihodom ekipe 7,2 % proti 4,2 %. Nevrološko ugoden izid se ni statistično razlikoval. | Opazovalne raziskave, različni sistemi in države; prebran povzetek. Učinek je povezava, ne zagotovljen lokalni rezultat. |

## Viri

Pravilnik je prebran v primarnem besedilu Uradnega lista (1.–20. člen in prilogi 7 in 8). Organizacija NMP ZD je iz uradne strani zavoda. Časi vožnje so modelski izračun in imajo nižjo zanesljivost kot izmerjeni dostopni časi. Metaanaliza je prebrana kot povzetek.

## Identificirani problemi

| Problem | Dokaz oziroma meja znanja |
|---|---|
| Dejanski dostopni časi NMP za Črnomelj niso javni | Pravilnik zahteva letno poročanje, podatki za občino v pregledanih virih niso objavljeni. |
| Četrtina prebivalcev ima ocenjen dostopni čas nad 15 minut | Model OSRM, SURS 2026 in predpostavke (razpon 20–34 %); zahteva preverjanje z dejanskimi časi. |
| Ranljivost ob sočasnih intervencijah | Če je ekipa Črnomelj zasedena, je po modelu nad 15 minut 99 % prebivalcev. |
| Mreža prvih posredovalcev ni javno opisana | ZD jo označuje kot vzpostavljeno, podatkov o obsegu in pokritosti ni. [@ref:vir-5] |
| Zdravniki hkrati pokrivajo več služb | Ambulanta, SUC, urgentna in dežurna služba ter ambulante za neopredeljene. [@ref:vir-8] |
| Odmaknjena naselja so starejša | V naseljih z ocenjenim dostopnim časom nad 15 minut živi 943 oseb, starih 65 let ali več (srednji scenarij). |

## Kritična vprašanja

| Za koga | Vprašanje in zahtevani dokaz |
|---|---|
| Vodstvo ZD Črnomelj | Kolikšen je bil povprečni in 90. percentilni dostopni čas za I. prioriteto v letih 2024–2026? Agregirani podatki po letih in po krajevnih skupnostih. |
| Vodstvo ZD Črnomelj | Koliko prvih posredovalcev je evidentiranih, v katerih krajih in koliko aktivacij je bilo v letih 2025–2026? Na čem temelji oznaka »realizirano« v letnem poročilu 2025? Agregirana evidenca in ocena potreb po 19. členu pravilnika. |
| Vodstvo ZD Črnomelj | Koliko intervencij na leto se zgodi, ko je ekipa NMP že na terenu? Število sočasnih klicev in čas čakanja na drugo ekipo. |
| Dispečerska služba zdravstva | Koliko AED z območja Črnomlja je v evidenci DSZ in koliko jih je izključenih zaradi vzdrževanja? Izpis evidence. |
| Gasilska zveza Črnomelj | Katera društva bi bila pripravljena sodelovati kot organizirana skupina prvih posredovalcev? Seznam društev, članov in opreme. |
| Občinska uprava | Ali bo občina sofinancirala opremo prvih posredovalcev, ki je državna sredstva ne pokrijejo? Proračunska postavka in merila. |
| Občinski svet | Ali bo občina zahtevala letno javno poročilo o dostopnih časih in aktivacijah? Sklep sveta in oblika poročila. |
| Ministrstvo za zdravje | Kdaj bodo objavljeni podatki iz letnih poročil izvajalcev NMP po Prilogi 7? Terminski načrt in raven razčlenitve. |
| Svet zavoda ZD | Kako bo pomanjkanje zdravnikov vplivalo na razpoložljivost NMP ponoči in ob koncih tedna? Razpored dežurstev 2026. |
| Šole in športna društva | Koliko zaposlenih in trenerjev je v zadnjih dveh letih opravilo tečaj temeljnih postopkov oživljanja? Agregirano število in leto usposabljanja. |
| Policija | Ali lahko policijske patrulje na odmaknjenih območjih nosijo AED? Opis opreme in dogovor z ZD. |

## Tveganja

Prvi posredovalci ne nadomeščajo ekipe NMP. Brez rednega usposabljanja, zavarovanja in psihološke podpore se lahko hitro izčrpajo. Prostovoljci na podeželju so pogosto isti ljudje v gasilstvu, civilni zaščiti in društvih. Objava podatkov po naseljih ne sme omogočiti prepoznave posameznih bolnikov, zato je treba majhne številke združevati. Modelski čas ne sme služiti kot dokaz za ali proti posamezni lokaciji ekipe.

## Možne rešitve

| Rok | Ukrep in odgovorni | Viri in financiranje (načrtovalna ocena) | Korist, tveganje in merilo uspeha |
|---|---|---|---|
| 0–12 mesecev | ZD objavi agregiran pregled obstoječe mreže prvih posredovalcev in jo dopolni tam, kjer je modelski čas nad 15 minut; dogovor z gasilsko zvezo. | 30–60 ur strokovnega dela; usposabljanje iz proračuna RS po 19. členu pravilnika. | Hitrejša prva pomoč; tveganje neenakomerne pokritosti. Po 6 mesecih: zemljevid pokritosti po krajevnih skupnostih; po 12 mesecih: delež odmaknjenih KS z vsaj dvema aktivnima prvima posredovalcema. |
| 0–12 mesecev | Občina in ZD preverita AED v evidenci DSZ, dostopnost ponoči in vzdrževanje. | 20–40 ur; stroški vzdrževanja nosi lastnik naprave. | Manj »mrtvih« naprav; tveganje nejasnega lastništva. Po 12 mesecih: delež AED z dokumentiranim pregledom in 24-urnim dostopom. |
| 1–3 leta | ZD letno javno objavi agregirane dostopne čase in aktivacije prvih posredovalcev. | 10–20 ur letno; obstoječi podatki iz Priloge 7. | Pregled nad dostopnostjo; tveganje napačne razlage povprečij. Letno poročilo z mediano, 90. percentilom in razčlenitvijo po območjih. |
| 1–3 leta | Tečaji temeljnih postopkov oživljanja v šolah, društvih in podjetjih, najprej v odmaknjenih krajih. | Načrtovalna ocena 3.000–8.000 EUR letno; občina, ZZZS preventiva ali donatorji, če so na voljo. | Več usposobljenih očividcev; tveganje enkratnih akcij brez obnove. Število usposobljenih na 1.000 prebivalcev po krajevnih skupnostih. |
| 3–10 let | Občina, ZD in ministrstvo presodijo, ali je za jug občine potrebna dodatna mobilna enota ali drugačna razporeditev. | Investicija in kadri po presoji; državna mreža NMP. | Krajši dostopni časi; tveganje, da ni kadra. Merilo: 90. percentil dostopnega časa za I. prioriteto v odmaknjenih KS. |

### Uredniška ocena dokumentiranosti

Ocenjujemo javno dokumentiranost in pripravljenost sistema, ne kakovosti dela ekip NMP. Lestvica je 1–5 (1 = skoraj nič dokumentirano, 5 = celovito in neodvisno preverjeno), sedem meril ima enako utež.

| Merilo | Ocena in obrazložitev |
|---|---|
| Transparentnost | 2: organizacija in cilj glede prvih posredovalcev sta opisana, dostopni časi, obseg mreže in aktivacije niso objavljeni. |
| Dostop in razpoložljivost | 3: NMP deluje 24 ur; odmaknjena naselja so po modelu daleč, ena ekipa pokriva ambulanto in teren. |
| Usklajenost s potrebami | 3: starejše prebivalstvo in razpršena poselitev zahtevata dodatne rešitve, ki niso dokumentirane. |
| Dokazna podlaga in spremljanje | 2: pravilnik uvaja poročanje, lokalni podatki niso javni. |
| Pravičnost in doseg | 2: prebivalci jugovzhoda so v slabšem položaju, ciljni ukrepi niso dokumentirani. |
| Stroški in učinkovitost | Ni ocene: ni podatkov. |
| Vzdržnost | 3: državno financiranje prvih posredovalcev je predpisano, ZD načrtuje nadaljnja izobraževanja; obseg ni javen. |
| Izvedljivost | 4: gasilska mreža in AED že obstajata, pravni okvir je jasen. |

Izračun: (2 + 3 + 3 + 2 + 2 + 3 + 4) / 7 = **2,71/5, ⚠️**. Izredni prehod na ❌ ni uporabljen, ker za Črnomelj ni dokaza o preseženih dostopnih časih. To bi preverili dejanski podatki.

## Primerjave

Pravilnik določa enoten nacionalni cilj (15 minut povprečno). Primerljivih objavljenih dostopnih časov po občinah v pregledanih virih ni. Ko bodo objavljeni, je treba primerjati enako opredelitev (dostopni čas od dviga slušalke do prihoda, I. prioriteta, prva prispela ekipa) in enako obdobje. Primerjava z drugimi ZD s sistemi prvih posredovalcev je smiselna šele z enakimi kazalniki iz Priloge 7.

## Odprta vprašanja

| Vrzel | Nadaljnji korak |
|---|---|
| Dejanski dostopni časi | Zahteva po informacijah javnega značaja za agregirane podatke 2024–2026. |
| Obseg in pokritost prvih posredovalcev | Uradni odgovor ZD in gasilske zveze (število, kraji, aktivacije). |
| Natančnost modela | Ko ZD posreduje agregirane dostopne čase po krajevnih skupnostih, jih primerjati s scenariji A; če odstopajo, popraviti predpostavke (obdelava klica, faktor vožnje). Zahteva je pripravljena v `dokumentacija/zahteve-ijz/`. |
| Pogostost sočasnih intervencij | Podatek ZD o številu intervencij, ko je bila ekipa že na terenu (potrebno za oceno scenarija B). |

## Povezane strani

AED-ji, poti in starost prebivalcev. Neopredeljeni pacienti in dolgotrajna oskrba sta sosednji temi v istem zavihku.

## Zadnja posodobitev

25. september 2026.
