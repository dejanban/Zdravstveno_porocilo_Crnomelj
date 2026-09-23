"""Ponovljiva gradnja dokaznega popisa v wiki in razdelkov poročila; brez omrežja."""
from pathlib import Path
import json,re,os,markdown
from bs4 import BeautifulSoup
from zgradi_porocilo import sources
P=Path(__file__).resolve().parent.parent; ROOT=P
refs=sources(); source=(P/'kader-sport-vsebina.md').read_text(encoding='utf-8')
existing={'zd2025','oecd'}
source=re.sub(r'\{\{cite:([^}]+)\}\}',lambda m:'{{cite:'+ (m[1] if m[1] in existing else 'kader-'+m[1])+'}}',source)
order=[]
def wiki_cite(m):
    key=m[1]
    assert key in refs,key
    assert (ROOT/refs[key]['local']).exists(),refs[key]['local']
    if key not in order:order.append(key)
    return '['+str(order.index(key)+1)+']'
target=ROOT/'wiki/analysis/synthesis/zdravstveni-kader-in-sport-crnomelj-2026.md'
text=re.sub(r'\{\{cite:([^}]+)\}\}',wiki_cite,source)
def entry(key,i,parent):
    r=refs[key];local=Path(os.path.relpath(ROOT/r['local'],parent)).as_posix()
    return f'[{i}] »{r["title"]},« {r["publisher"]}, {r.get("date","b.d.")}. [Na spletu]. Dostopno: {r["url"]}. [Dostopano: {r.get("access","19. september 2026")}]. Lokalna kopija: [[{local}]].'
text+='\n## Literatura\n\n'+'\n\n'.join(entry(k,i,target.parent) for i,k in enumerate(order,1))+'\n'
target.write_text(text,encoding='utf-8')

intro=source.split('## Povzetek\n',1)[1].split('## Trenutno stanje',1)[0]
facts=source.split('## Ključna dejstva\n',1)[1].split('\n## Viri',1)[0]
chunks=re.split(r'(?=^### )',facts,flags=re.M)
sections=[('kader-pregled','Zdravstveni kader: obseg in metoda popisa',intro+source.split('## Trenutno stanje\n',1)[1].split('\n## Ključna dejstva',1)[0])]
names=['dusevna-pomoc','fizioterapija-prehrana-vadba','zdravniki','primanjkljaj-zdravnikov','sportna-ponudba']
for slug,chunk in zip(names,[c for c in chunks if c.strip()]):
    heading,body=chunk.strip().split('\n',1)
    sections.append((slug,heading.removeprefix('### '),body))
assert len(sections)==6,len(sections)
sections.append(('kader-ukrepi','Ukrepi za boljšo dostopnost zdravstvenih storitev in vadbe',source.split('## Možne rešitve\n',1)[1].split('\n## Primerjave',1)[0]))
html=''
for slug,title,body in sections:
    rendered=markdown.markdown(body,extensions=['tables'])
    soup=BeautifulSoup(rendered,'html.parser')
    for t in soup.select('table'):t.wrap(soup.new_tag('div',attrs={'class':'table-scroll'}))
    for h in soup.select('h3'):h.name='h3'
    html+=f'<section class="section" id="{slug}" data-title="{title}"><h2>{title}</h2>{soup}</section>\n'
(P/'kader-sport.html').write_text(html,encoding='utf-8')
body=(P/'vsebina.html').read_text(encoding='utf-8')
if '{{kader-sport}}' not in body:
    marker='<section class="section" id="kontekst"'
    assert marker in body
    body=body.replace(marker,'{{kader-sport}}\n\n'+marker,1)
    (P/'vsebina.html').write_text(body,encoding='utf-8')

summary=ROOT/'wiki/sources/source-summaries/kader-sport-crnomelj-2026.md'
locators={
 'zd2025':'Tabela 13, natisnjena str. 43; kategorije zaposlenih na 31. 12. 2025.',
 'kader-plan2026':'Poglavje 6, družinska medicina: 7,53 in 5,53 tima; kadrovski načrt 2026 ločeno od realizacije.',
 'kader-zzzsizvlecek':'Preglednica 1. 9. 2026, izvirne vrstice 1330–1338; izločena Gabrijela Plut (Semič).',
 'kader-dsokader':'Tabela 11.2, str. 43–44; vizualno preverjeni stolpci, OCR shranjen.',
 'kader-euratios':'Natisnjena str. 32, okvir 1.4: omejitve modela JRC SANDEM.',
 'kader-euworkpdf':'Executive summary / key messages: nacionalno različni pristopi, lokalno prilagajanje primarne oskrbe.',
 'kader-lokasport2025':'Objava 14. 9. 2025: deset izvajalcev popoldanske športne vadbe za otroke.',
 'oecd':'Gostota zdravnikov za 2023: Slovenija 3,5, EU 4,3 na 1.000.'}
body='# Zdravstveni kader in šport v Črnomlju: viri, september 2026\n\n## Povzetek\n\nPreverjeni so zaposleni 2025, program ZD 2026, seznam ZZZS 1. 9. 2026 ter javno objavljena lokalna ponudba. Ključni rezultat je dokumentirana vrzel dveh timov, ne izračun domnevne evropske občinske norme. Podrobna sinteza: [[../../analysis/synthesis/zdravstveni-kader-in-sport-crnomelj-2026]].\n\n## Evidenca uporabljenih virov\n\n| Vir | Vrsta in zanesljivost | Uporabljeni del / omejitev |\n| --- | --- | --- |\n'
for i,k in enumerate(order,1):
    r=refs[k]
    primary=any(x in r['publisher'] for x in ['ZD ','ZZZS','DSO ','OECD','Evropska komisija','Občina','OŠ Loka'])
    typ='Uradni primarni vir; visoka za navedeni datum in obseg.' if primary else 'Predstavitev ponudnika; srednja za ponudbo, ne potrjuje celotnega kadra ali licence.'
    if k=='kader-kosarka':typ='Izjava kluba, objavljena v mediju; srednja, urnik 2025.'
    body+=f'| {r["title"]} [{i}] | {typ} | {locators.get(k,"Imenik, profil ali opis storitve; prebrani razdelki o kadru, lokaciji in ponudbi. Spletni zajem ni telefonska potrditev.")} |\n'
body+='\n## Omejitve in odprte naloge\n\nNe seštevati oseb in timov. Sedež ZD vključuje tudi ambulanto v Semiču. Enaka oseba v CKZ in dispanzerju se šteje enkrat. Neznano število zasebnikov ni nič. DSO nevropsihiatrija je namenjena stanovalcem. Športni imeniki in objave 2025 niso potrjeni urniki 2026/27. Pridobiti uradne agregate po občini prebivališča in potrditve ponudnikov; nihče ni bil kontaktiran.\n\n## Zadnja posodobitev\n\n2026-09-21.\n\n## Literatura\n\n'
body+='\n\n'.join(entry(k,i,summary.parent) for i,k in enumerate(order,1))+'\n'
summary.write_text(body,encoding='utf-8')
print(f'Sinteza in povzetek virov: {len(order)} virov; poročilo: {len(sections)} novih razdelkov.')
