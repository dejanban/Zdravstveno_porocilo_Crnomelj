"""Evidenca obnove in prenosljive tabele okoljske dopolnitve."""
from pathlib import Path
import csv, json, hashlib, re
P=Path(__file__).resolve().parents[1]
def write(name,text):
    p=P/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')
topic='topics/environment/zivljenjske-razmere-voda-zrak.md'
text=(P/'vsebina/okolje-20260924.md').read_text(encoding='utf-8')
tables=[]
for block in re.findall(r'(?:^\|.*\n)+',text,re.M):
    rows=[[x.strip() for x in line.strip().strip('|').split('|')] for line in block.splitlines()]
    if len(rows)>2:
        rows.pop(1);tables.append(rows)
out=[]
for i,rows in enumerate(tables,1):
    name=f'podatki/okolje/tabela-{i:02}.csv'
    with (P/name).open('w',encoding='utf-8-sig',newline='') as f:csv.writer(f,delimiter=';').writerows(rows)
    out.append({'datoteka':name,'stolpci':rows[0],'vrstice':len(rows)-1})
write('podatki/okolje/tabele.json',json.dumps(out,ensure_ascii=False,indent=2))
write('podatki/okolje/README.md','# Podatki okoljske dopolnitve\n\nTabele CSV so prepis preglednic iz avtorskega vhodnega besedila `vsebina/okolje-20260924.md`; niso dodatne meritve. Ločilo je podpičje, kodiranje UTF-8 z BOM. Praznine in besedilne omejitve se ohranijo. Oznake `[@…]` ustrezajo ključem virov v `okolje-viri.json`. Kazalo preglednic: `tabele.json`.\n')
write('wiki/sources/source-summaries/okolje-voda-zrak-20260924.md','''# Viri: življenjske razmere, pitna voda in zrak

## Povzetek

Dopolnitev povezuje 33 citiranih uradnih in raziskovalnih virov. Popolna bibliografija, navedbe po trditvah in lokalne kopije so na [[../../topics/environment/zivljenjske-razmere-voda-zrak.md]]. Register: [[../../../podatki/okolje/okolje-viri.json]].

## Kaj je bilo prebrano

| Gradivo | Prebrani obseg in zanesljivost | Omejitev |
|---|---|---|
| Komunala, letna poročila 2011–2025 | Celotna izvlečena besedila; 2021 OCR in vizualna kontrola preglednice. Visoka za objavljene izvide, srednja za zbirne interpretacije. | Različni obsegi vzorčenja; napake odstotkov in letnic so navedene v temi. |
| Posamični lokalni izvidi in javni izvidi 2026 | Izvlečki 176 lokalnih PDF in 88 objavljenih dokumentov 2026; datumi odvzema ločeni od objave. Visoka za konkretni vzorec. | Vzorec ne predstavlja neprekinjenega nadzora celotnega omrežja. |
| ARSO 2022–2024, bilteni 2025 in začasne tabele 2026 | Letna poročila in relevantne preglednice; lokacija, povprečja, preseganja, BaP in kovine. Visoka za potrjene letne podatke. | Selitev postaje 2025; 2026 delno in nepotrjeno. |
| WHO, SURS in raziskava CAPS | Shranjeno besedilo strani in raziskave; WHO preglednica priporočil tudi vizualno. Visoka za uradne definicije, srednja za prenos raziskave vrtov v Črnomelj. | Mehanizmi niso dokaz lokalnega vzročnega učinka. |

## Odprta vprašanja

Izvorne tabele vode pred 2011, ekološko in kemijsko stanje reke Dobličice, dokumentirana odprava vzrokov dogodka Adlešiči in potrjena letna vrednost BaP 2025 ostajajo odprti. Stare prazne kopije drugih tem niso obnovljene.

## Zadnja posodobitev

24. september 2026.
''')
empty=[p.relative_to(P/'wiki').as_posix() for p in (P/'wiki').rglob('*.md') if p.stat().st_size==0]
write('wiki/index.md',f'''# Kazalo zdravstvene raziskave Črnomlja

Zadnja posodobitev: 24. september 2026. Kazalo je obnovljeno v omejenem obsegu; prazne stare strani niso vsebinsko rekonstruirane.

| Stran | Vsebina |
|---|---|
| [[{topic}]] | Dohodki, stres, hrana, letni pregled vode in zraka, omejitve, vprašanja in ukrepi. |
| [[sources/source-summaries/okolje-voda-zrak-20260924.md]] | Obseg prebranih virov in zanesljivost. |
| [[analysis/synthesis/pregled-za-kandidata.md]] | Kratka sinteza ugotovitev za odločanje. |
| [[naslednji-koraki.md]] | Stanje obnove in nadaljnje naloge. |
| [[log.md]] | Sled opravljenega dela. |
| [[../porocilo.html]] | Glavno poročilo. |
| [[../viri/index.html]] | Lokalna knjižnica in opozorila o manjkajočih starih virih. |

## Ob obnovi zaznane prazne strani

Inventar je shranjen v [[../podatki/okolje/prazne-wiki-strani.json]]. Izvirna vsebina teh strani ni dostopna; nova dopolnitev je ne nadomešča.
''')
write('podatki/okolje/prazne-wiki-strani.json',json.dumps(empty,ensure_ascii=False,indent=2))
write('wiki/analysis/synthesis/pregled-za-kandidata.md','''# Pregled za kandidata

Zadnja posodobitev: 24. september 2026. Obnovljen je okoljski del; stare prazne sinteze drugih tem niso rekonstruirane. Dokazi, definicije, ocene in literatura: [[../../topics/environment/zivljenjske-razmere-voda-zrak.md]].

| Tema in status | Kaj deluje | Kaj manjka | Prednost v štiriletnem mandatu |
|---|---|---|---|
| ⚠️ Pitna voda, 3,57/5 | Letna poročila in javni posamični izvidi omogočajo nadzor. | Pozitivne dodatne preiskave parazitov v Adlešičih 2025 zahtevajo dokumentirano pojasnilo; rutinska skladnost ne zajame vseh nevarnosti. | Javen register dogodkov, ukrepov in ponovnih kontrol; ciljni nadzor omrežja. |
| ⚠️ Zrak, 3,14/5 | Lokalne meritve od 2024 omogočajo spremljanje delcev. | BaP 2024 nad ciljno vrednostjo; selitev 2025 omeji trend. | Zmanjševanje zimskih izpustov in transparentno spremljanje po merilni lokaciji. |
| ⚠️ Življenjske razmere, 2,71/5 | Možne koristi dostopa do hrane, gibanja in podpornih vezi imajo raziskovalno podlago. | Ni lokalnega dokaza o manj stresa ali učinku samooskrbe; plače na delovnem mestu niso dohodek gospodinjstva. | Izmeriti dostop in ovire, izvesti dostopen pilot vrtnarjenja z evalvacijo. |

Ocene so uredniška presoja sedmih enako uteženih meril, ne klinične učinkovitosti. Stroški niso ocenjeni zaradi manjkajočih podatkov. Zgodovinski dogodki sami ne dokazujejo trenutnega nerešenega tveganja; izredni prehod na ❌ zato ni uporabljen.
''')
write('wiki/naslednji-koraki.md','''# Naslednji koraki in stanje projekta

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
''')
log=P/'wiki/log.md'
entry='''\n## [2026-09-24] update | Dopolnitev glavnega poročila: življenjske razmere, voda in zrak

- Action: Obnovljena gradnja iz ohranjenega HTML; dodana štiri poglavja, letne in mesečne preglednice, 30 vprašanj, ukrepi, ocene, sled popravkov in PDF.
- Sources used: 33 citiranih virov Komunale, ARSO, WHO, SURS in raziskave CAPS; lokalni izvidi in novi arhiv okolje-2026-09-24.
- Pages created: Okoljska tema, povzetek virov, obnovljena sinteza in kazalo; prenosljive CSV tabele.
- Pages updated: Glavno poročilo, knjižnica, literatura, naslednji koraki, obnovljeni zagonski postopek.
- Open questions: Stari prazni izvirniki; voda pred 2011; stanje reke Dobličice; razlaga dogodka Adlešiči; BaP 2025; nepopolno 2026.
- Follow-up tasks: Obnova varnostnih kopij in pridobitev manjkajočih primarnih časovnih vrst. Preverjanje novega obsega je zabeleženo v preverjanje/okolje-porocilo.json; ne potrjuje vseh starih trditev.
'''
if 'Dopolnitev glavnega poročila: življenjske' not in log.read_text(encoding='utf-8'):
    with log.open('a',encoding='utf-8') as f:f.write(entry)
files=[]
for folder in ['viri/okolje-2026-09-24','viri/splet']:
    for p in (P/folder).rglob('*'):
        if p.is_file() and p.stat().st_size:
            files.append({'path':p.relative_to(P).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
write('viri/manifest.json',json.dumps({'scope':'Obnovljeni okoljski arhiv in neprazne spletne kopije; stare prazne datoteke niso potrjene.','datum':'2026-09-24','files':files},ensure_ascii=False,indent=2))
print('Evidenca in',len(tables),'preglednic shranjenih.')
