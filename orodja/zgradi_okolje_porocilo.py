"""Obnovljiva dopolnitev poročila iz ohranjenega posnetka in novih virov."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tmp/okolje-runtime'))
from bs4 import BeautifulSoup
import markdown, re, json, hashlib, html, csv

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'viri/okolje-2026-09-24'
def write(path,text):
    p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')
def slug_source(slug):
    manifest=json.loads((SOURCE/'manifest.json').read_text(encoding='utf-8'))
    row=next(x for x in manifest if Path(x['path']).stem==slug)
    return row

TITLES={
'who-determinante':('Social determinants of health','WHO','6. maj 2025'),
'who-stres':('Stress','WHO','30. marec 2026'),
'who-prehrana':('Healthy diet','WHO','b.d.'),
'who-pitna-voda':('Drinking-water','WHO','b.d.'),
'who-zrak':('Ambient (outdoor) air pollution','WHO','b.d.'),
'who-smernice-zrak':('WHO global air quality guidelines','WHO','2021'),
'surs-crnomelj-2024':('Črnomelj: Slovenske regije in občine v številkah, podatki za 2024','SURS','b.d.'),
'vrtovi-rct':('Effects of a community gardening intervention on diet, physical activity, and anthropometry outcomes in the USA (CAPS): an observer-blind, randomised controlled trial','J. S. Litt in sod., The Lancet Planetary Health','2023'),
'zrak-2024':('Kakovost zraka v Sloveniji v letu 2024','ARSO','2025'),
'zrak-december-2025':('Naše okolje, december 2025: letni pregled kakovosti zraka, str. 142','ARSO','2026'),
'zrak-februar-2025':('Naše okolje, februar 2025: selitev postaje Črnomelj','ARSO','2025'),
'zrak-podatki-27':('Povprečna mesečna raven delcev PM10 v letu 2025','ARSO','3. februar 2026'),
'zrak-podatki-28':('Povprečna mesečna raven delcev PM10 v letu 2026, januar–julij','ARSO','31. avgust 2026'),
'zrak-podatki-29':('Preseganje delcev PM10 v letu 2026, januar–julij','ARSO','b.d.'),
'zrak-podatki-34':('Dnevne ravni policikličnih aromatskih ogljikovodikov v delcih PM10 na merilnem mestu Črnomelj v letu 2025','ARSO','15. maj 2026'),
'komunala-vzorci-crnomelj':('Rezultati vzorčenj VS Črnomelj','Komunala Črnomelj','b.d.'),
'vzorec-2026-1':('Poročilo o izvedeni nalogi: vzorec 26/89747, Griblje OŠ, odvzem 2. 9. 2026','NLZOH / Komunala Črnomelj','8. september 2026'),
'vzorec-2026-8':('Poročilo o izvedeni nalogi: vzorec 26/88801, Adlešiči KZ, odvzem 31. 8. 2026','NLZOH / Komunala Črnomelj','7. september 2026')}
for year in range(2011,2026):
    TITLES[f'voda-{year}-{year-2010}']=(f'Kakovost pitne vode v občinah Črnomelj in Semič v letu {year}', 'Komunala Črnomelj' if year<2021 else 'NLZOH / Komunala Črnomelj',str(year+1))

def main():
    text=(ROOT/'vsebina/okolje-20260924.md').read_text(encoding='utf-8')
    used=list(dict.fromkeys(re.findall(r'\[@([^\]]+)\]',text)))
    records={}
    for slug in used:
        r=slug_source(slug);title,publisher,date=TITLES[slug]
        records[slug]={**r,'id':'env-'+slug,'title':title,'publisher':publisher,'date':date,'accessed':'2026-09-24','reliability':'srednja' if (slug.startswith('voda-201') or slug=='voda-2020-10' or slug=='vrtovi-rct') else 'visoka za obseg vira'}
        # Zahtevana spletna kopija; izvirni dokument ostaja v tematskem arhivu.
        capture=(SOURCE/(slug+'.md')).read_text(encoding='utf-8')
        capture=capture.replace('naslov: '+slug,'naslov: '+title).replace('izdajatelj: '+r['url'].split('/')[2],'izdajatelj: '+publisher)
        if slug=='voda-2021-11': capture+='\n\nOCR (Tesseract slv+eng; tabela 2 dodatno vizualno preverjena):\n'+(SOURCE/(slug+'.ocr.txt')).read_text(encoding='utf-8')
        write('viri/splet/okolje-20260924-'+slug+'.md',capture)

    wiki=text
    for i,slug in enumerate(used,1):wiki=wiki.replace('[@'+slug+']',f'[{i}]')
    wiki+='\n\n## Literatura\n\n'
    for i,slug in enumerate(used,1):
        r=records[slug]
        wiki+=f'[{i}] »{r["title"]},« {r["publisher"]}, {r["date"]}. [Na spletu]. Dostopno: {r["url"]}. [Dostopano: 24. september 2026]. Lokalna kopija: [[../../../viri/splet/okolje-20260924-{slug}.md]]. Izvirnik: [[../../../{r["path"]}]].\n\n'
    write('wiki/topics/environment/zivljenjske-razmere-voda-zrak.md',wiki)

    soup=BeautifulSoup((ROOT/'vsebina/obnovljena-osnova-20260924.html').read_text(encoding='utf-8'),'html.parser')
    old_refs={p['id']:p for p in soup.select('#literatura p[id]')}
    def cite(slug):return f'<a class="citation" href="#env-{slug}" title="{html.escape(records[slug]["title"],quote=True)}">[vir]</a>'
    rendered=re.sub(r'\[@([^\]]+)\]',lambda m:cite(m[1]),text)
    parts=[
        ('okolje-zdravje','Razvitost, dohodki, stres in domača hrana',rendered.split('## Povzetek\n',1)[1].split('## Ključna dejstva')[0].replace('## Trenutno stanje\n','')),
        ('pitna-voda','Pitna voda: pregled letnih meritev',rendered.split('### Pitna voda: vir Dobliče ni enako voda iz pipe\n',1)[1].split('### Zrak:')[0]),
        ('zrak','Kakovost zraka: meritve in njihove omejitve',rendered.split('### Zrak: lokalne meritve in prelom lokacije\n',1)[1].split('## Viri')[0]),
        ('okolje-ukrepi','Okolje in zdravje: odgovornost, vprašanja in ukrepi', '### Dokazna podlaga\n'+rendered.split('## Viri\n',1)[1].split('## Povezane strani')[0])]
    target=soup.select_one('#starost')
    for sid,title,body in parts:
        body=re.sub(r'^## ', '### ',body,flags=re.M)
        section=BeautifulSoup(f'<section class="section okolje" id="{sid}" data-title="{title}"><div class="section-head"><span class="section-no"></span><h2>{title}</h2></div><p class="subtle">Dopolnitev 24. septembra 2026 · obdobja meritev so navedena pri podatkih</p>'+markdown.markdown(body,extensions=['tables'])+'</section>','html.parser').section
        for table in section.find_all('table'):
            wrapper=soup.new_tag('div',attrs={'class':'table-scroll'});table.wrap(wrapper)
            first=table.find('th')
            if first:first['style']='width:18%;min-width:90px'
        if sid=='pitna-voda':
            section.append(BeautifulSoup('<p>Podatkovne tabele: <a href="podatki/okolje/tabele.json">kazalo preglednic CSV</a>. Na ozkem zaslonu preglednice pomaknite vodoravno.</p>','html.parser'))
        target.insert_before(section)
    # Dodatni namig v obstoječem poglavju, povzetku in sled sprememb.
    soup.select_one('#kontekst').append(BeautifulSoup('<p>Razlago povezav med razvitostjo in zdravjem dopolnjujejo naslednja poglavja z meritvami <a href="#pitna-voda">pitne vode</a>, <a href="#zrak">zraka</a> in predlogi <a href="#okolje-ukrepi">ukrepov</a>.</p>','html.parser'))
    summary=f'<tr><td><b>Voda in zrak potrebujeta ločeno presojo.</b> Poročilo o vodi za 2025 izpostavlja parazite v Adlešičih; zrak 2024 pri ZD je imel benzo(a)piren 2,6 ng/m³. {cite("voda-2025-15")}{cite("zrak-2024")}</td><td>Preveriti trajno odpravo vzrokov v vodi, izboljšati nadzor omrežja in zmanjševati zimske izpuste. Letni pregled zraka 2025 navaja PM10 19 in PM2,5 15 µg/m³; selitev postaje omejuje trend. {cite("zrak-december-2025")}{cite("zrak-februar-2025")} <a href="#pitna-voda">Podrobni podatki</a>.</td></tr>'
    soup.select_one('#povzetek tbody').append(BeautifulSoup(summary,'html.parser'))
    changes=[('Prejšnja izdaja še ni vsebovala letnega pregleda vode in lokalnih meritev zraka.',f'24. 9. 2026: dodani letni viri vode 2011–2025, delni izvidi 2026 in zrak 2024–2026. Manjkajoča leta so označena. {cite("komunala-vzorci-crnomelj")}'),('Možna napačna razlaga: 100 % rutinskih vzorcev pomeni odsotnost vseh nevarnosti.',f'Rutinske analize 2025 ločene od dodatnih pozitivnih preiskav parazitov v Adlešičih. Ne gre za trditev o današnji prepovedi uporabe. {cite("voda-2025-15")}'),('Možna napačna razlaga: 39 dni PM10 samodejno pomeni neskladnost; 2025 dokazuje izboljšanje.',f'Za 2024 je ARSO po odštetju naravnega prispevka navedel 34 dni. Leta 2025 se je merilnik preselil. {cite("zrak-2024")}{cite("zrak-februar-2025")}')]
    for a,b in changes:soup.select_one('#popravki tbody').append(BeautifulSoup('<tr><td>'+a+'</td><td>'+b+'</td></tr>','html.parser'))
    soup.select_one('.hero-meta').append(BeautifulSoup('<span>Voda, zrak in življenjske razmere: 24. september 2026</span>','html.parser'))
    nav=soup.select_one('#kazalo');nav.clear()
    sections=soup.select('main > section')
    num=0
    for sec in sections:
        title=sec.find('h2').get_text(' ',strip=True)
        if sec['id']=='literatura': label='↗'
        else:num+=1;label=f'{num:02}'
        if sec.select_one('.section-no'):sec.select_one('.section-no').string=label
        a=soup.new_tag('a',href='#'+sec['id']);sp=soup.new_tag('span');sp.string=label;a.append(sp);a.append(title);nav.append(a)
    # Literatura se preštevilči po prvem pojavu v celotnem poročilu.
    refs=dict(old_refs)
    for slug,r in records.items():
        refs[r['id']]=BeautifulSoup(f'<p id="{r["id"]}"><span class="refno">[vir]</span> »{html.escape(r["title"])},« {html.escape(r["publisher"])}, {r["date"]}. [Na spletu]. Dostopno: <a href="{html.escape(r["url"],quote=True)}">{html.escape(r["url"])}</a>. [Dostopano: 24. september 2026]. Lokalni vir: <a href="{r["path"]}">celotni izvirnik</a>; <a href="viri/splet/okolje-20260924-{slug}.md">shranjeni izvleček</a>.</p>','html.parser').p
    from prenovi_porocilo import prepare, mark_missing_downloads
    sleep_records=prepare(soup,refs)
    ordered=[]
    for a in soup.select('a.citation'):
        key=a.get('href','')[1:]
        if key in refs and key not in ordered:ordered.append(key)
    ordered += [x for x in refs if x not in ordered]
    mapping={key:i+1 for i,key in enumerate(ordered)}
    for a in soup.select('a.citation'):
        key=a['href'][1:]
        if key in mapping:a['href']=f'#vir-{mapping[key]}';a.string=f'[{mapping[key]}]'
    lit=soup.select_one('#literatura');lit.clear()
    lit.append(BeautifulSoup('<h2>Literatura (IEEE)</h2><p>Številčenje sledi prvemu pojavu v poročilu. Novi viri o spanju imajo lokalne kopije in kontrolne vsote; obseg branja je naveden pri vsakem. Starejše lokalne kopije so bile 25. 9. 2026 obnovljene iz prve različice projekta in preverjene z izvirnim manifestom SHA-256 (1.289 od 1.290 ujemanj). Pri okoljskem arhivu ostaja šest neskladij HTML-kopij. Kontrolne vsote potrjujejo izvirnost kopij, ne aktualnosti starejših ugotovitev.</p>','html.parser'))
    all_ledger=[]
    for key in ordered:
        p=refs[key];p['id']=f'vir-{mapping[key]}';p.select_one('.refno').string=f'[{mapping[key]}]'
        empty=[]
        for a in p.select('a[href]'):
            href=a['href']
            if not re.match(r'^(https?:|#|mailto:)',href):
                fp=ROOT/href.split('#')[0]
                if not fp.is_file() or fp.stat().st_size==0:empty.append(href)
        if empty:p.append(' Opomba: lokalna kopija manjka ali je prazna in je ni bilo mogoče obnoviti iz zgodovine projekta; potrebna je ponovna pridobitev izvirnika.')
        lit.append(p)
        all_ledger.append({'number':mapping[key],'id':p['id'],'text':p.get_text(' ',strip=True),'links':[a['href'] for a in p.select('a[href]')],'missing_or_empty':empty})
    css='''\n/* Okoljska dopolnitev */\n.okolje td,.okolje th{overflow-wrap:anywhere}.okolje table{min-width:620px}.okolje p{max-width:84ch}.okolje h3{margin-top:30px}.literature a{overflow-wrap:anywhere}@media print{.okolje{break-before:page}.okolje table{min-width:0;table-layout:fixed;width:100%}.okolje table th,.okolje table td{overflow-wrap:anywhere;font-size:8pt}.okolje .table-scroll{overflow:visible}.okolje h3{margin-top:18px}.okolje p{max-width:none}.literature p{break-inside:avoid}}'''
    style=soup.new_tag('style');style.string=css;soup.head.append(style)
    mark_missing_downloads(soup)
    built=str(soup)
    write('porocilo.html',built);write('porocilo-print.html',built)
    write('podatki/literatura/literatura.json',json.dumps(all_ledger,ensure_ascii=False,indent=2))
    write('podatki/okolje/okolje-viri.json',json.dumps(list(records.values()),ensure_ascii=False,indent=2))
    write('vsebina/okolje.html','\n'.join(str(soup.select_one('#'+x[0])) for x in parts))
    # Obnovljena knjižnica kaže tako ohranjene kot manjkajoče stare kopije.
    lib='<html lang="sl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Knjižnica virov</title><style>body{font:16px system-ui;max-width:1000px;margin:auto;padding:24px}p{overflow-wrap:anywhere;border-bottom:1px solid #ddd;padding:12px}</style><h1>Lokalna knjižnica virov</h1><a href="../porocilo.html">Poročilo</a>'
    for p in lit.find_all('p',recursive=False):
        cp=BeautifulSoup(str(p),'html.parser').p
        for a in cp.select('a[href]'):
            if not re.match(r'^(https?:|#|mailto:)',a['href']):a['href']='../'+a['href']
        lib+=str(cp)
    write('viri/index.html',lib+'</html>')
    write('podatki/okolje/stanje-obnove.json',json.dumps({'base':'vsebina/obnovljena-osnova-20260924.html','new_sources':len(records),'prior_empty_citations':sum(bool(x['missing_or_empty']) for x in all_ledger),'note':'Ohranjene stare vsebine; izpraznjene datoteke obnovljene iz commita 0dc0bd4 (preverjanje/obnova-iz-gita.json).'},ensure_ascii=False,indent=2))
    print('Poročilo zgrajeno;',len(records),'okoljskih virov;',len(all_ledger),'vseh referenc.')

if __name__=='__main__':main()
