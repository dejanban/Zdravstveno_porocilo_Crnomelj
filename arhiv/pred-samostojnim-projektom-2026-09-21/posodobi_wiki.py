"""Vloži preverjeno sintezo in ohrani predhodne različice za sledljivost."""
from pathlib import Path
import re,json,shutil,os
from bs4 import BeautifulSoup,NavigableString
from zgradi_porocilo import sources
P=Path(__file__).resolve().parent; R=P.parents[1]
raw=BeautifulSoup((P/'vsebina.html').read_text(encoding='utf-8'),'html.parser'); refs=sources()
stats=json.loads((P/'statistika-registra.json').read_text(encoding='utf-8'))

def convert(n):
    if isinstance(n,NavigableString):return str(n)
    if n.name in ['script','style','input','button','svg']:return ''
    if n.name=='table':
        rows=[]
        for row in n.find_all('tr'):
            rows.append('| '+' | '.join(' '.join(convert(c).split()).replace('|','/') for c in row.find_all(['td','th'],recursive=False))+' |')
        if rows:rows.insert(1,'| '+' | '.join('---' for _ in n.find('tr').find_all(['td','th']))+' |')
        return '\n\n'+'\n'.join(rows)+'\n\n'
    inner=''.join(convert(c) for c in n.children)
    if n.name in ['b','strong']:return '**'+inner+'**'
    if n.name=='br':return ' '
    if n.name in ['h1','h2','h3']:return '\n\n### '+inner+'\n\n'
    if n.name in ['p','div','section','article','header']:return '\n\n'+inner+'\n\n'
    if n.name=='a':return inner # evidence uses cite placeholders; navigation supplied below
    return inner

def section(id):
    n=raw.find(id=id);s=convert(n)
    s=re.sub(r'\{\{chart:[^}]+\}\}','\nGraf in izvorna tabela sta v spremljajočem poročilu.\n',s)
    s=s.replace('{{all-data}}','Izvoz vseh 54 kazalnikov: `porocila/zdravstvo-obcina-crnomelj/kazalniki.csv`.')
    s=s.replace('{{stats}}',f"Zajetih {stats['pregledane_objave']} različnih spletnih objav; začetna besedilna razvrstitev povezuje {stats['pripadnost']['Črnomelj']} objav s CKZ Črnomelj. Preostalih ne prištevamo njegovi oceni. Brez neuspešnih zajemov na pregledanih iskalnih straneh. Register ni popis enkratnih izvedenih dogodkov.")
    return re.sub(r'\n{3,}','\n\n',s).strip()

def archive(p):
    dst=P/'arhiv/pred-prenovo-2026-09-19'/p.relative_to(R)
    if p.exists() and not dst.exists():dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dst)

def write_page(rel,title,summary,ids,problems,solutions=True):
    p=R/rel;archive(p)
    body=f'# {title}\n\n## Povzetek\n\n{summary}\n\n## Trenutno stanje\n\nPresek virov: 19. september 2026. Letnice izdaj NIJZ niso letnice meritev.\n\n## Ključna dejstva\n\n'+'\n\n'.join(section(i) for i in ids)
    body+='\n\n## Viri\n\nPrimarni viri NIJZ, ZD Črnomelj, WHO in izvirne raziskave; Radio Odeon je sekundarni dokaz o objavi dejavnosti. Natančni naslovi, datumi, lokalne kopije in meje branja so v literaturi. Zanesljivost uradnih poročil je visoka za njihove evidence, ne za neodvisen dokaz učinka. Raziskave niso lokalna vzročna študija.\n\n## Identificirani problemi\n\n'+problems
    body+='\n\n## Kritična vprašanja\n\n'+section('vprasanja')
    body+='\n\n## Tveganja\n\nZamenjava leta objave in meritve, sklepanje o vzročnosti iz občinskih trendov, štetje vabil kot izvedb in zamenjava financiranih timov za zaposlene vodijo v napačno oceno. Rezultati skupine 17 oseb brez primerjave ne omogočajo sklepa o celotnem prebivalstvu. {{cite:opisi}}{{cite:zd2025}}'
    body+='\n\n## Možne rešitve\n\n'+(section('resitve') if solutions else 'Podrobni ukrepi po obdobjih, nosilcih, virih in merilih uspeha: [[../../analysis/synthesis/zdravstvo-preventiva-ckz-2026]].')
    body+='\n\n## Primerjave\n\nPrimerjave z drugimi CKZ niso mogoče brez enotnih podatkov o dosegu, stroških in izidih. Občinske kazalnike primerjamo s Slovenijo ob isti definiciji in obdobju; dnevni kadilci niso vsi kadilci, debelost ni prekomerna prehranjenost. {{cite:opisi}}{{cite:oecd}}'
    body+='\n\n## Odprta vprašanja\n\nPridobiti agregat različnih uporabnikov CKZ, dokončanje programov, spremljanje po 6 in 12 mesecih, stroške in kadrovske ekvivalente, doseg po krajih ter primerljive občine. Lokalni delež vpliva prehrane, gibanja, socialnih razmer in dostopa do oskrbe ostaja nepreverjen.'
    links=['wiki/entities/institutions/ckz-crnomelj.md','wiki/topics/social-affairs/zdravje-obcina-nijz-trendi.md','wiki/topics/social-affairs/zdravje-obcina-eu-primerjava.md','wiki/analysis/synthesis/zdravstvo-preventiva-ckz-2026.md','wiki/sources/source-summaries/zdravstvo-ckz-splet-literatura-2026-09.md']
    body+='\n\n## Povezane strani\n\n'+'\n'.join('- [['+Path(os.path.relpath(R/l,p.parent)).as_posix()[:-3]+']]' for l in links if l!=rel)
    body+='\n\n### Sledljivost popravkov\n\nPrejšnje besedilo je ohranjeno v `porocila/zdravstvo-obcina-crnomelj/arhiv/pred-prenovo-2026-09-19/wiki/`. Ta različica nadomešča napačne trditve o neznanem vodstvu, 2–3 zaposlenih CKZ, odsotnosti izboljšanja prehranjenosti otrok, trojnem preobratu bolezni, neposredno primerljivi umrljivosti 2016–2026 in primerjavi vseh kadilcev z dnevnimi. Podrobni popravki so v poročilu.'
    order=[]
    def cite(m):
        k=m[1]
        if k not in order:order.append(k)
        return '['+str(order.index(k)+1)+']'
    body=re.sub(r'\{\{cite:([^}]+)\}\}',cite,body)
    body+='\n\n## Literatura\n\n'
    for i,k in enumerate(order,1):
        r=refs[k];loc=Path(os.path.relpath(R/r['local'],p.parent)).as_posix()
        label=f'{r.get("authors","")} »{r["title"]},« {r["publisher"]}, {r["date"]}.'
        if r.get('doi'):label+=f' zv. {r["volume"]}, št. {r["number"]}, str. {r["pages"]}. doi: {r["doi"]}.'
        body+=f'[{i}] {label.strip()} [Na spletu]. Dostopno: {r["url"]}. [Dostopano: 19. september 2026]. Lokalna kopija: [[{loc}]]. {r.get("note","")}\n\n'
    body+='## Zadnja posodobitev\n\n2026-09-19 — ponovna preverba virov, popravek metodologije in povezava s prenovljenim poročilom.\n'
    assert '{{' not in body;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(body,encoding='utf-8')

write_page('wiki/entities/institutions/ckz-crnomelj.md','Center za krepitev zdravja Črnomelj','**Ocena javno dokumentiranega dela: 3,4/5.** Raznolika in ponavljajoča se dejavnost je dokumentirana, klinična in stroškovna učinkovitost pa nista ocenljivi iz pregledanih javnih virov. Uradna vodja je Tatjana Gregorič. {{cite:kontakti}}',['ckz','dogodki'],'Manjkajo celovit agregat dosega, izidi celotnega programa in stroškovna analiza. Neobjavljenih podatkov ne enačimo z nedelovanjem centra.')
write_page('wiki/topics/social-affairs/zdravje-obcina-nijz-trendi.md','Zdravje v občini Črnomelj — pravilna razlaga trendov NIJZ','Prehranjenost otrok se je med izdajama 2016 in 2026 izboljšala, vendar ostaja nad slovenskim povprečjem. DORA in Svit sta ugodna. Pri razlagi umrljivosti je nujno upoštevati metodološki prelom. {{cite:nizi}}{{cite:opisi}}',['metoda','kontekst','dejavniki','presejanje','kronicne'],'Vztrajajo vrzel pri otroški prehranjenosti, alkoholnih nesrečah, cepljenju proti pnevmokokom in pomoči na domu. Večina drugih razlik v zadnjem profilu ni statistično značilna. {{cite:nijzprofil}}')
write_page('wiki/topics/social-affairs/zdravje-obcina-eu-primerjava.md','Zdravje — primerjava s Slovenijo in EU','Evropski podatki dajejo kontekst, ne neposredne občinske lestvice. Primerjati je treba enake opredelitve in obdobja. {{cite:oecd}}',['eu','metoda'],'Prejšnja različica je primerjala vse kadilce v občini z dnevnimi kadilci v EU ter prekomerno prehranjenost z debelostjo. Takšne lestvice se umaknejo.',False)
write_page('wiki/analysis/synthesis/zdravstvo-preventiva-ckz-2026.md','Zdravstvo in preventiva — dokazi ter ukrepi skozi čas','Povezava lokalnih ugotovitev, javno dokumentiranega dela CKZ in raziskav. Učinki raziskav niso napoved lokalnega rezultata; ukrepi zahtevajo izhodiščno meritev in spremljanje.',['povzetek','vzroki','ckz'],'Preventiva potrebuje povezavo med rednim delom, dostopnostjo, prehranskim in gibalnim okoljem ter izmerjenimi dolgoročnimi rezultati.')

p=R/'wiki/sources/source-summaries/zdravstvo-ckz-splet-literatura-2026-09.md'
p.write_text('# Viri: zdravstvo, CKZ in raziskave — september 2026\n\nPregled zajema 33 virov osrednjega poročila, 54 izvirnih nizov NIJZ in '+str(stats['pregledane_objave'])+' različnih objav Radia Odeon na '+str(stats['iskalne_strani'])+' iskalnih straneh. Vse zajete objave imajo lokalno kopijo v `raw/web/`. Razvrstitev celotnega registra je avtomatizirana; izbrani primeri v poročilu so vsebinsko preverjeni. Število objav ni število izvedenih dogodkov.\n\n## Ugotovitve\n\nVodstvo CKZ je uradno javno imenovano; financirani timi niso število zaposlenih; 13/17 pomeni 76,5 %, ne 79 %. NIJZ objave združujejo različna referenčna obdobja. Podrobna evidenca in IEEE literatura: [[../../analysis/synthesis/zdravstvo-preventiva-ckz-2026]], [[../../entities/institutions/ckz-crnomelj]], [[../../topics/social-affairs/zdravje-obcina-nijz-trendi]].\n\n## Omejitve\n\nPrebrani so izvlečki štirih izvirnih raziskav, uradna priporočila ter gradiva spletnih seminarjev WHO; celotni video posnetki niso bili pregledani. Javno dostopna stran ni dokaz popolnega arhiva dogodkov. Izvajanje programov ni dokaz njihove vzročne učinkovitosti.\n\n## Zadnja posodobitev\n\n2026-09-19.\n',encoding='utf-8')

p=R/'wiki/sources/source-summaries/zd-crnomelj-letno-porocilo-2025.md';archive(p);s=p.read_text(encoding='utf-8').replace('+15,8 %','+17,94 %').replace('uradno, revidirano letno poročilo','uradno letno poročilo').replace('SO javno pripravljeni in revidirani','SO javno objavljeni').replace('uradnega revidiranega poročila','uradnega poročila')
s+='\n\n## Dopolnitev in popravek 2026-09-19\n\nSveži uradni PDF je javno dostopen. Prihodki so narasli za 17,94 % (prej napačno 15,8 %). Presežek 296.363 EUR je pred obdavčitvijo, 294.256 EUR po njej. Tabela programov uporablja enoto TIMI, ne FTE zaposlenih. V skupini 17 udeležencev je 13 zmanjšanj maščobne mase 76,5 %; poročilo samo napačno navaja 79 %. Objava dokumenta sama ne dokazuje neodvisne revizije vseh njegovih trditev. Natančni vir, strani in omejitve: [[../../entities/institutions/ckz-crnomelj]]. Prejšnja različica je arhivirana ob prenovi poročila.\n';p.write_text(s,encoding='utf-8')

p=R/'wiki/analysis/synthesis/pregled-za-kandidata.md';archive(p);s=p.read_text(encoding='utf-8');m=re.search(r'^### .*Zdravstvo.*',s,re.M);end=s.find('\n### ',m.end())
new='''### 🏥 Zdravstvo — Zdravstveni dom Črnomelj

**Ocena: ❌** — Obstoječa ocena zavoda ostaja zaradi dokumentiranega kadrovskega tveganja in odprtega vprašanja upravljanja. Prejšnje povprečje petih ocen 2,6 bi pomenilo ⚠️; potrjeno nerešeno tveganje dostopnosti oskrbe sproži strožjo oznako. Današnji pregled ne predstavlja nove preverbe postopka pri direktorju in te ocene ne prenaša na CKZ.

#### ✅ Kar deluje

- ZD je za 2025 objavil pozitivno poslovanje; prihodki 9,75 mio EUR, presežek pred davkom 296.363 EUR. Rast prihodkov je 17,94 %, ne prej navedenih 15,8 %.
- DORA in Svit sta nad slovenskim povprečjem. Prehranjenost otrok se je izboljšala z 31,1 na 28,3 %, čeprav ostaja nadpovprečna.
- CKZ ima javno imenovano vodjo, strokovne kontakte in dokumentirano terensko delo. Ocena javno dokumentiranega dela **3,4/5**, brez trditve o dokazani klinični učinkovitosti.

#### ❌ Kar ne deluje

- Zavod v letnem poročilu navaja pomanjkanje zdravnikov. Manjka primerljiv celovit pregled dosega, stroškov in izidov CKZ.
- Profil NIJZ opozarja na otroško prehranjenost, alkoholne nesreče, cepljenje proti pnevmokokom in pomoč na domu. Kazalnikov zdravil ni mogoče enačiti s prevalenco bolezni; trendov ni mogoče pripisati CKZ.

#### 💡 Priporočila za naslednji mandat (4 leta)

**Takoj / prvo leto:** občina in ZD naj objavita kadrovski načrt, CKZ pa agregat uporabnikov, izvedb, stroškov in izhodiščnih rezultatov; s šolami vzpostaviti redno gibanje in izboljševanje prehranskega okolja.

**Do konca mandata:** spremljati rezultate po 6 in 12 mesecih, širiti preverjeno učinkovite obravnave, zmanjševati ovire na podeželju in pripraviti primerjavo z demografsko podobnimi občinami. Raziskave podpirajo večletno dosledno delo; enkratni dogodki niso zadostna strategija.

Vir: [[../../topics/social-affairs/zd-crnomelj-pregled]], [[../../topics/social-affairs/zdravje-obcina-nijz-trendi]], [[../../topics/social-affairs/zdravje-obcina-eu-primerjava]], [[../../entities/institutions/ckz-crnomelj]], [[zdravstvo-preventiva-ckz-2026]]. Zgodovina starejših ugotovitev je ohranjena v analitičnih straneh in arhivu pred prenovo.

---
'''
s=s[:m.start()]+new+s[end:];s=s.replace('# Pregled', '# Pregled',1);s+='\n\nPregled zdravstvenega razdelka in zadnja posodobitev: 2026-09-19 — metodološki popravki NIJZ, popravljena ocena CKZ in raziskovalna sinteza.\n';p.write_text(s,encoding='utf-8')

p=R/'wiki/index.md';s=p.read_text(encoding='utf-8');s=re.sub(r'Zadnja posodobitev: 2026-09-19[^\n]*','Zadnja posodobitev: 2026-09-19 — prenovljeno poročilo o zdravstvu, 33 virov IEEE, 54 nizov NIJZ in register '+str(stats['pregledane_objave'])+' objav. CKZ: 3,4/5 za dokumentirano delo; izidi in gospodarnost niso ocenjeni. Metodološki popravki nadomeščajo prejšnje navedbe o neznanem vodstvu, FTE in trendih.',s,count=1)
s+='\n\n### Zdravstvo — dopolnitev 2026-09-19\n\n- [[analysis/synthesis/zdravstvo-preventiva-ckz-2026]] — sinteza; raziskave o vzrokih, časovno opredeljeni ukrepi, odgovornosti, sredstva in merila uspeha.\n- [[sources/source-summaries/zdravstvo-ckz-splet-literatura-2026-09]] — povzetek virov; obseg spletnega pregleda in omejitve zajema.\n- [[entities/institutions/ckz-crnomelj]] — ustanova; posodobljena ocena 3,4/5 in preverjene dejavnosti.\n- [[topics/social-affairs/zdravje-obcina-nijz-trendi]] — tema; metodologija in popravljeni trendi.\n- [[topics/social-affairs/zdravje-obcina-eu-primerjava]] — tema; primerjave z enotnimi definicijami.\n';p.write_text(s,encoding='utf-8')
p=R/'wiki/naslednji-koraki.md';s=p.read_text(encoding='utf-8');i=s.find('\n');s=s[:i]+'''\n\n## Aktualna predaja — 2026-09-19, prenova zdravstva

Poročilo `porocila/zdravstvo-obcina-crnomelj/porocilo.html` je vsebinsko in oblikovno prenovljeno, z lokalnim PDF, 33 viri IEEE, 11 grafi in ločenim iskalnim registrom Radia Odeon. Ocena CKZ je 3,4/5 za javno dokumentirano delo; ne gre za klinično ali finančno oceno. Spodnje starejše navedbe o 2–3 FTE, neznani vodji, otrocih brez izboljšanja in trojnem preobratu bolezni so **zgodovinsko stanje, nadomeščeno s popravki** na aktualnih straneh.

Ponovna gradnja brez omrežja: v mapi poročila `python zgradi_porocilo.py`; preverjanje in PDF: `python preveri_porocilo.py` (Python 3.11, Playwright Chromium, PyMuPDF, BeautifulSoup, openpyxl). V PowerShell nastavite `$env:PYTHONIOENCODING='utf-8'`. Viri in skripte so ob poročilu; izvorne spletne kopije v `raw/web/zdravstvo-20260919-*`. Prejšnje različice so v `arhiv/pred-prenovo-2026-09-19/`. Register uporablja začetno avtomatizirano razvrstitev; izbrani primeri v poročilu so preverjeni. Ne šteti objav kot enkratnih izvedenih dogodkov.

Nadaljnje raziskave: od CKZ pridobiti različne uporabnike, napotitve, dokončanje, spremljanje po 6/12 mesecih, FTE in stroške; pregledati mejne razvrstitve registra; izbrati primerljive občine. Star širši `javno-porocilo` in stare SVG ilustracije niso ponovno zgrajeni; pred objavo jih uskladiti s popravki v novi sintezi. Preostale trajne naloge in navodila spodaj ostajajo v veljavi.
\n'''+s[i:];p.write_text(s,encoding='utf-8')
p=R/'wiki/log.md'
with p.open('a',encoding='utf-8') as f:f.write(f'''\n\n## [2026-09-19] update | Prenova poročila o zdravstvu, register CKZ in raziskave

- Action: Ponovna preverba in prenova celotnega samostojnega poročila; 54 nizov, 11 grafov, 33 virov IEEE, HTML/PDF in register {stats['pregledane_objave']} objav Radia Odeon. Ocena CKZ 3,4/5 se nanaša na dokumentirano delo. Popravljeni timi/FTE, vodstvo, odstotki, obdobja NIJZ in neprimerljive evropske primerjave. Predhodne različice arhivirane.
- Sources used: NIJZ profil 2026 in metodologija; ZD letno poročilo 2025 in kontakti; Radio Odeon; WHO, OECD, štiri izvirne raziskave. Lokalni izvlečki v raw/web in bibliografija v poročilu.
- Pages created: analysis/synthesis/zdravstvo-preventiva-ckz-2026; sources/source-summaries/zdravstvo-ckz-splet-literatura-2026-09.
- Pages updated: entities/institutions/ckz-crnomelj; topics/social-affairs/zdravje-obcina-nijz-trendi; topics/social-affairs/zdravje-obcina-eu-primerjava; povzetek letnega poročila ZD; pregled-za-kandidata; index; naslednji-koraki.
- Open questions: Doseg, stroški in dolgoročni izidi CKZ; primerljivi centri; mejni primeri avtomatizirane razvrstitve. Celotnega zgodovinskega popisa dogodkov ni mogoče zagotoviti.
- Follow-up tasks: Pridobiti agregate CKZ, izvesti nadaljnjo vsebinsko revizijo registra ter pred novo objavo uskladiti stare skupne javne dokumente in SVG prikaze.
''')
print('Wiki posodobljen; predhodne različice ohranjene.')
