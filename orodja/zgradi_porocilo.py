"""Gradnja samostojnega poročila, registra in podatkov; brez spletnih zahtev."""
from pathlib import Path
import json,re,csv,html,shutil,math
from bs4 import BeautifulSoup
import openpyxl
from obdelaj_register import process
P=Path(__file__).resolve().parent.parent; ROOT=P
E=lambda s:html.escape(str(s),quote=True)
def fmt(v):return f'{v:,.2f}'.replace(',','@').replace('.',',').replace('@','.').rstrip('0').rstrip(',') if isinstance(v,(int,float)) else '—'

def sources():
    refs={r['key']:r for r in json.loads((P/'podatki/literatura/literatura-zajem.json').read_text(encoding='utf-8'))['records']}
    extra=P/'podatki/starost/starost-viri.json'
    if extra.exists():refs.update(json.loads(extra.read_text(encoding='utf-8')))
    extra=P/'podatki/drustva/drustva-viri.json'
    if extra.exists():refs.update(json.loads(extra.read_text(encoding='utf-8')))
    extra=P/'podatki/kader/kader-sport-viri.json'
    if extra.exists():refs.update({'kader-'+k:v for k,v in json.loads(extra.read_text(encoding='utf-8')).items()})
    extra=P/'podatki/poti/poti-viri.json'
    if extra.exists():refs.update(json.loads(extra.read_text(encoding='utf-8')))
    refs['zd2025']['title']='Letno poročilo Zdravstvenega doma Črnomelj za leto 2025'
    refs['plan2025']['title']='Finančni načrt in program dela za leto 2025'
    refs['oecd']['title']='Slovenia: Country Health Profile 2025'
    refs['urnik']['title']='Urnik delavnic: april in maj 2025'
    refs['kontakti']['title']='Kontakti Centra za krepitev zdravja Črnomelj'
    refs['ckz']['title']='Center za krepitev zdravja Črnomelj'
    refs['ckzdogodki']['title']='Dogodki in aktivnosti CKZ Črnomelj'
    refs['ckz-spremljanje']={'title':'Zdravstvenovzgojni centri / Centri za krepitev zdravja (ZVCT)','publisher':'NIJZ','date':'14. april 2023, posodobljeno 7. april 2025','url':'https://nijz.si/podatki/podatkovne-zbirke-in-raziskave/zdravstvenovzgojni-centri-centri-za-krepitev-zdravja-zvct/','local':'viri/splet/ckz-nijz-spremljanje-2026-09-20.md','access':'20. september 2026','note':'Prebrana spletna stran o spremljanju obravnav in eSZBO; ne potrjuje popolnosti lokalnih evidenc ali spremljanja izidov po 6/12 mesecih.'}
    refs['ckz-spremljanje'].update(json.loads((P/'podatki/ckz/ckz-viri.json').read_text(encoding='utf-8'))['ckz-spremljanje-20260922'])
    refs['predavanje-prosojnice']['title']='Accelerating childhood overweight reduction: lessons learned and the path towards 2030 — prosojnice'
    refs['nijzprofil']['title']='Zdravje v občini 2026: Črnomelj'
    refs['nizi']={'title':'Časovni nizi kazalnikov za Črnomelj, izdaje 2016–2026: 54 Excelovih datotek','publisher':'NIJZ','date':'2026','url':'https://obcine.nijz.si/obcine/crnomelj/17/2026/','local':'viri/nijz','note':'Lokalni izvirniki XLSX; izvoz v podatki/nijz/kazalniki.csv. Leto v nizu pomeni leto objave.'}
    refs['opisi']={'title':'Zdravje v občini 2026 — Opisi kazalnikov','publisher':'NIJZ','date':'marec 2026','url':'https://obcine.nijz.si/vsebine/metodoloska-pojasnila/opisi-kazalnikov-2026-223/','local':'viri/nijz/Opisi_kazalnikov.pdf','note':'Prebran lokalni izvirnik: str. 8–9, 19–20, 66–67, 96–97 in 108–109 (natisnjene strani).'}
    papers=[('slo-gibanje','36811242','P. Jurić, G. Jurak, S. A. Morrison, G. Starc in M. Sorić','Effectiveness of a population-scaled, school-based physical activity intervention for the prevention of childhood obesity','Obesity',2023,'31','3','811–822','10.1002/oby.23695'),('hall','31105044','K. D. Hall in sod.','Ultra-Processed Diets Cause Excess Calorie Intake and Weight Gain: An Inpatient Randomized Controlled Trial of Ad Libitum Food Intake','Cell Metabolism',2019,'30','1','67–77.e3','10.1016/j.cmet.2019.05.008'),('dpp','11832527','W. C. Knowler in sod.','Reduction in the incidence of type 2 diabetes with lifestyle intervention or metformin','New England Journal of Medicine',2002,'346','6','393–403','10.1056/NEJMoa012512'),('sprint','26551272','SPRINT Research Group','A Randomized Trial of Intensive versus Standard Blood-Pressure Control','New England Journal of Medicine',2015,'373','22','2103–2116','10.1056/NEJMoa1511939')]
    for key,pmid,authors,title,journal,year,vol,no,pages,doi in papers:
        refs[key]={'key':key,'title':title,'authors':authors,'publisher':journal,'date':str(year),'volume':vol,'number':no,'pages':pages,'doi':doi,'url':f'https://pubmed.ncbi.nlm.nih.gov/{pmid}/','local':f'viri/splet/zdravstvo-20260919-pubmed-{pmid}.md','note':'Prebran strukturirani povzetek izvirne raziskave; ne celotno besedilo.'}
    refs['hall']['local']='viri/splet/zdravstvo-20260919-hall-2019-povzetek.md'
    mapping={'odeon-vdc':'izobrazevanje-o-najpomembnejsi-vrednoti','odeon-radenci':'festival-zdravja-v-radencih-ob-kolpi','odeon-adlesici':'naravoslovni-dan-zdravje-na-ps-adlesici','odeon-otvoritev':'otvoritev-centra-za-krepitev-zdravja-bela-krajina','odeon-festival':'letosnji-festival-zdravja-je-zakljucen','odeon-doblice':'roznati-koraki-v-doblicah','odeon-zobje':'zobkovadba-na-os-milke-sobar-natase','odeon-vitamini':'vitaminski-dan','odeon-brki':'brkati-pohod-ozavescal-o-zdravju-moskih','odeon-nasmeh':'dan-za-zdrav-nasmeh-in-dobre-navade'}
    odeon=json.loads((P/'podatki/register/zajem-odeon.json').read_text(encoding='utf-8'))['records']
    for k,slug in mapping.items():
        r=next(r for r in odeon if r['url'].rstrip('/').endswith('/'+slug))
        refs[k]={'title':r['title'],'publisher':'Radio Odeon','date':r['dates'][0][:10] if r['dates'] else 'b.d.','url':r['url'],'local':r['local'],'note':'Sekundarni vir; dokaz o objavi oziroma opisu dejavnosti.'}
    return refs

def src_href(p):
    p=str(p).replace("\\","/")
    return p[:-3]+".html" if p.endswith(".md") else (p.rstrip("/")+"/index.html" if (P/p).is_dir() else p)

def citation(ref,n):
    if ref.get('authors'):
        label=f'{ref["authors"]}, »{ref["title"]},« {ref["publisher"]}, zv. {ref["volume"]}, št. {ref["number"]}, str. {ref["pages"]}, {ref["date"]}. doi: {ref["doi"]}.'
    else:label=f'»{ref["title"]},« {ref["publisher"]}, {ref["date"]}.'
    online=f' [Na spletu]. Dostopno: <a href="{E(ref["url"])}">{E(ref["url"])}</a>. [Dostopano: {E(ref.get("access","19. september 2026"))}].' if ref.get('url') else ''
    local=f' Lokalni vir: <a href="{E(src_href(ref["local"]))}">odpri shranjeno gradivo</a>.'
    return f'<p id="vir-{n}"><span class="refno">[{n}]</span> {E(label)}{online}{local} {E(ref.get("note",""))}</p>'

CHART_META={
'K1.1':('Razvitost občine','koeficient; SLO = 1','0,87–0,91; ponovitev iste vrednosti ni nova letna meritev.'),
'K1.5':('Delovna aktivnost','%','Zadnja izdaja 69,3 %; nad slovensko vrednostjo že v izdaji 2019.'),
'K2.2':('Prekomerna prehranjenost otrok','%','Izdaja 2026: meritve 2024. Preddebelost in debelost skupaj.'),
'K2.6':('Nesreče z alkoholiziranimi povzročitelji','% nesreč','Izdaja 2026: povprečje 2020–2024; ne število nesreč v 2026.'),
'K3.4':('Presejanost v programu DORA','%','Izdaja 2026: januar 2024–oktober 2025; manjkajoče vrednosti niso ničle.'),
'K4.6':('Prejemniki zdravil za povišan tlak','standardizirana stopnja / 100','Izdaja 2026: leto 2024. Uporaba zdravil ni enaka razširjenosti bolezni.'),
'K4.8':('Bolnišnične obravnave zaradi srčne kapi','standardizirana stopnja / 1.000','Starost 35–74 let; zadnja izdaja je povprečje 2020–2024.'),
'K4.9':('Bolnišnične obravnave zaradi možganske kapi','standardizirana stopnja / 1.000','Starost 35–84 let; 2026: 2,26 proti 2,21. Razlika ni statistično značilna.'),
'K4.4':('Bolezni, neposredno pripisljive alkoholu','standardizirana stopnja / 1.000','Bolnišnične obravnave, starost 15+; zadnja izdaja je povprečje 2020–2024.'),
'K5.1':('Splošna umrljivost','standardizirana stopnja / 100.000','Prelom 2018/2019: običajno → stalno bivališče. Zadnja izdaja: povprečje 2020–2024.'),
'K5.7':('Umrljivost zaradi samomora','standardizirana stopnja / 100.000','Večletna povprečja; prelom bivališča 2018/2019. Zadnje obdobje 2020–2024.')}

def load_data():
    all_data={};csvrows=[]
    for p in sorted((ROOT/'viri/nijz').glob('NIJZ*.xlsx')):
        w=openpyxl.load_workbook(p,data_only=True,read_only=True);rows=list(w.active.values);w.close()
        if not rows or not str(rows[0][0]).startswith('K'):continue
        key=str(rows[0][0]).split()[0];years=[y for y in rows[0][1:] if isinstance(y,int)];series=[]
        for r in rows[1:]:
            if not r[0]:continue
            if str(r[0]).startswith('Občina'): label='Črnomelj';color='#146859'
            elif str(r[0]).startswith('Regija'):label='JV Slovenija';color='#9d6925'
            elif r[0]=='Slovenija':label='Slovenija';color='#4468a5'
            else: label=str(r[0]);color='#999'
            vals=[v if isinstance(v,(int,float)) else None for v in r[1:len(years)+1]]
            for year,raw in zip(years,r[1:len(years)+1]):csvrows.append([key,str(rows[0][0]),r[0],year,raw])
            if label in ['Črnomelj','JV Slovenija','Slovenija']:series.append({'label':label,'color':color,'values':vals})
        all_data[key]={'title':rows[0][0],'years':years,'series':series,'source':p.relative_to(ROOT).as_posix()}
    with (P/'podatki/nijz/kazalniki.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f,delimiter=';');w.writerow(['sifra','kazalnik','obmocje','leto_objave','vrednost_izvirnika']);w.writerows(csvrows)
    (P/'podatki/nijz/kazalniki.json').write_text(json.dumps(all_data,ensure_ascii=False,indent=2),encoding='utf-8')
    return all_data

def chart(key,d):
    title,unit,note=CHART_META[key];series=d['series'];years=d['years'];vals=[v for s in series for v in s['values'] if isinstance(v,(int,float))];lo,hi=min(vals),max(vals);pad=(hi-lo)*.16 or .1;lo-=pad;hi+=pad
    X=lambda i:58+i/(len(years)-1)*590
    Y=lambda v:215-(v-lo)/(hi-lo)*174
    svg=f'<svg viewBox="0 0 710 252" role="img" aria-label="{E(title)}: časovne vrste po letu objave"><title>{E(title)}</title><desc>{E(note)} Natančne vrednosti so v tabeli pod grafom.</desc>'
    for i in range(5):
        v=lo+i/4*(hi-lo);y=Y(v);svg+=f'<line x1="58" x2="648" y1="{y}" y2="{y}" stroke="#e0e6db"/><text x="49" y="{y+4}" text-anchor="end">{fmt(round(v,2))}</text>'
    svg+=f'<text x="58" y="19">{E(unit)}</text>'
    if key.startswith('K5.'):
        x=(X(2)+X(3))/2;svg+=f'<line x1="{x}" x2="{x}" y1="35" y2="215" stroke="#8c5b3a" stroke-dasharray="4 4"/><text x="{x+5}" y="34">prelom</text>'
    for s in series:
        path='';drawing=False
        for i,v in enumerate(s['values']):
            if v is None:drawing=False;continue
            if key.startswith('K5.') and i==3:drawing=False
            path+=f'{"L" if drawing else "M"}{X(i):.2f},{Y(v):.2f} ';drawing=True
        dash=' stroke-dasharray="6 4"' if s['label']=='JV Slovenija' else ''
        svg+=f'<path d="{path}" fill="none" stroke="{s["color"]}" stroke-width="2.8"{dash}/>'
        for i,v in enumerate(s['values']):
            if v is not None:svg+=f'<circle cx="{X(i)}" cy="{Y(v)}" r="3.3" fill="{s["color"]}"><title>{years[i]} · {E(s["label"])}: {fmt(v)}</title></circle>'
    for i,year in enumerate(years):svg+=f'<text x="{X(i)}" y="234" text-anchor="middle">{year}</text>'
    svg+='<line class="cursor" x1="648" x2="648" y1="38" y2="215" stroke="#42604a" stroke-dasharray="2 4" opacity=".4"/></svg>'
    legend=''.join(f'<span><i style="background:{s["color"]}"></i>{E(s["label"])}</span>' for s in series)
    table='<div class="table-scroll"><table><thead><tr><th scope="col">Izdaja</th>'+''.join(f'<th scope="col">{E(s["label"])}</th>' for s in series)+'</tr></thead><tbody>'+''.join('<tr><th scope="row">'+str(year)+'</th>'+''.join('<td>'+fmt(s['values'][i])+'</td>' for s in series)+'</tr>' for i,year in enumerate(years))+'</tbody></table></div>'
    return f'<article class="chart" data-key="{key}"><h3>{E(title)}</h3><div class="subtle">{key} · leto objave podatkov</div>{svg}<div class="legend">{legend}</div><label class="range-label" for="range-{key}">Izberi izdajo · premik s puščicama na tipkovnici</label><input id="range-{key}" type="range" min="0" max="{len(years)-1}" value="{len(years)-1}" aria-label="Izdaja za {E(title)}"><div class="readout" aria-live="polite"></div><p class="chart-note">{E(note)} {{{{cite:nizi}}}}</p><details><summary>Odpri podatkovno tabelo</summary>{table}</details></article>'

def shell(body,nav='',title='Zdravje v občini Črnomelj',data=None,registry=False):
    css=(P/'vsebina/slog.css').read_text(encoding='utf-8');js=(P/'vsebina/aplikacija.js').read_text(encoding='utf-8')
    aside=f'<aside class="sidebar"><a class="brand" href="#uvod">Črnomelj.<small>Javno zdravje / 2026</small></a><button class="mobile-menu" aria-controls="kazalo" aria-expanded="true">Kazalo</button><div class="nav-label">V tem poročilu</div><nav id="kazalo" aria-label="Kazalo poročila">{nav}</nav><div class="side-bottom">Neodvisni raziskovalni pregled<br>Osnova: 19. 9. 2026<br>Kader in šport: 21. 9. 2026<br>Obrazci CKZ: 22. 9. 2026<br><a href="register-dogodkov.html">Register objav CKZ ↗</a><div class="meter" aria-hidden="true"><span></span></div></div></aside>' if not registry else ''
    bar='<div class="topbar"><span>ČRNOMELJ / DOKAZI IN UKREPI</span><div class="actions"><a class="btn" href="porocilo.pdf">Prenesi PDF ↓</a><button class="btn" data-print>Natisni</button></div></div>'
    datahtml='<script type="application/json" id="chart-data">'+json.dumps(data,ensure_ascii=False).replace('</','<\/')+'</script>' if data else ''
    return f'<!doctype html><html lang="sl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Dokazno podprt pregled zdravja v Črnomlju, dejavnosti CKZ in načrta izboljšav."><title>{E(title)}</title><style>{css}</style></head><body class="{"registry" if registry else "report"}"><a class="skip" href="#vsebina">Preskoči na vsebino</a><div class="{"registry-layout" if registry else "layout"}">{aside}<main id="vsebina">{bar}{body}<footer class="footer">Neodvisni raziskovalni pregled · osnova 19. 9. 2026, kader in šport 21. 9. 2026, obrazci CKZ 22. 9. 2026 · Pripravljeno s pomočjo jezikovnega modela in preverjanjem navedenih virov. Predlogi ukrepov niso že sprejete odločitve.</footer></main></div><button id="backtop" aria-label="Na vrh strani">↑</button>{datahtml}<script>{js}</script></body></html>'

def statshtml(stats):
    c=stats['pripadnost'].get('Črnomelj',0);v=stats['vrste_crnomelj']
    return '<div class="table-scroll"><table><thead><tr><th>Obseg pregleda</th><th>Rezultat</th></tr></thead><tbody>'+''.join(f'<tr><td>{E(k)}</td><td>{E(v)}</td></tr>' for k,v in [('Pregledane lokalne Markdown datoteke',stats['lokalne_datoteke']),('Pregledane spletne objave',stats['pregledane_objave']),('Objave z izrecno povezavo s CKZ Črnomelj',c),('Od tega: vabila',v.get('Vabilo',0)),('Od tega: poročila / novice',v.get('Poročilo / novica',0)),('Od tega: obvestila in preklici',c-v.get('Vabilo',0)-v.get('Poročilo / novica',0)),('Neuspešni zajemi ob zaključku',len(stats['napake']))])+'</tbody></table></div>'

def registry(rows,stats):
    refs=[];table=''
    for i,r in enumerate(rows,1):
        date=r['datum_objave'] or r['datum_dogodka'] or 'Datum ni potrjen';year=date[:4] if re.match(r'\d{4}',date) else 'Neznano'
        table+=f'<tr data-aff="{E(r["pripadnost"])}" data-kind="{E(r["vrsta"])}" data-theme="{E(r["tema"])}" data-year="{year}"><td>{E(date)}<br><span class="subtle">{"datum objave" if r["datum_objave"] else "datum dogodka" if r["datum_dogodka"] else "leto ni razvidno"}</span></td><td><span class="event-title">{E(r["naslov"])}</span> <a class="citation" href="#vir-{i}">[{i}]</a><div class="event-evidence">{E(r["izsek"])}</div><details><summary>Zakaj je objava vključena ali izločena?</summary><p>{E(r["razlog"])}</p><a href="{E(src_href(r["lokalna_kopija"]))}">Celotno zajeto besedilo</a></details></td><td><span class="pill">{E(r["pripadnost"])}</span><br>{E(r["vrsta"])}</td><td>{E(r["tema"])}</td></tr>'
        refs.append(citation({'title':r['naslov'],'publisher':'Radio Odeon','date':r['datum_objave'] or 'b.d.','url':r['url'],'local':r['lokalna_kopija']},i))
    opts=lambda values: '<option value="">Vse</option>'+''.join(f'<option value="{E(v)}">{E(v)}</option>' for v in sorted(set(values)))
    filters=f'<div class="filters"><label>Iskanje po naslovu in besedilu<input type="search" id="event-search" placeholder="Npr. Dobliče, prehrana, stres"></label><label>Center<select id="aff-filter">{opts(r["pripadnost"] for r in rows)}</select></label><label>Vrsta dokaza<select id="kind-filter">{opts(r["vrsta"] for r in rows)}</select></label><label>Tema<select id="theme-filter">{opts(r["tema"] for r in rows)}</select></label><label>Leto objave / znanega dogodka<select id="year-filter">{opts((r["datum_objave"] or r["datum_dogodka"] or "Neznano")[:4] if (r["datum_objave"] or r["datum_dogodka"]) else "Neznano" for r in rows)}</select></label><button class="btn" id="reset-filters">Ponastavi</button></div>'
    filters=filters.replace('<option value="Črnomelj">','<option selected value="Črnomelj">')
    body=f'<header class="hero"><div class="eyebrow">Priloga poročilu · Radio Odeon</div><h1>Register objav<br><em>o dejavnostih CKZ.</em></h1><p>Pregled najdenih objav do 19. 9. 2026. En zapis pomeni eno spletno objavo, ne nujno enega dogodka ali potrjene izvedbe. Vabila brez leta niso samodejno uvrščena v leto 2026.</p><a href="porocilo.html#dogodki">← Nazaj v poročilo</a> · <a href="podatki/register/register-dogodkov.csv" download>Prenesi CSV</a></header>{statshtml(stats)}<div class="callout">Privzeto so prikazane objave z izrecno povezavo s CKZ Črnomelj. Za pregled izločitev izberite »Vse«. Pri novicah je praviloma prikazan datum objave; dejanski datum dogodka je lahko drugačen. Vrsta »Poročilo / novica« sama po sebi ne potrjuje neodvisno vseh trditev avtorja.</div>{filters}<p id="event-count" class="count" aria-live="polite"></p><div class="table-scroll"><table id="events-table"><thead><tr><th scope="col">Datum</th><th scope="col">Objava in dokaz</th><th scope="col">Razvrstitev</th><th scope="col">Področje</th></tr></thead><tbody>{table}</tbody></table></div><p class="empty" id="no-events" hidden>Ni zadetkov za izbrane filtre.</p><details><summary>Metoda in omejitve pregleda</summary><p>Združitev lokalne zbirke in vseh dosegljivih strani notranjega iskalnika za uporabljene izraze. Podvojeni URL-ji so odstranjeni. Izločene so objave drugih centrov in besedila brez dovolj izrecne povezave. Razvrstitev je konservativna; izseki so le orientacijski, celotna vsebina je shranjena ob viru.</p><p>To ni zagotovilo popolnega popisa vseh dogodkov: neindeksirane, izbrisane, slikovne in družbenomedijske objave lahko manjkajo. Isti dogodek se lahko pojavi v več objavah, zato se število izvedenih dogodkov ne izračunava iz števila vrstic. Pri aktualnih poznejših vabilih ni potrditve izvedbe.</p><p>Neuspešni zajemi: {E(json.dumps(stats["napake"],ensure_ascii=False))}.</p></details><section id="literatura" class="section literature"><h2>Literatura (IEEE)</h2>{"".join(refs)}</section>'
    (P/'register-dogodkov.html').write_text(shell(body,title='Register objav CKZ Črnomelj · Radio Odeon',registry=True),encoding='utf-8')

def main():
    archive=P/'arhiv/pred-prenovo-2026-09-19';archive.mkdir(parents=True,exist_ok=True)
    for name in ['porocilo.html','porocilo-print.html','porocilo.pdf']:
        if (P/name).exists() and not (archive/name).exists():shutil.copy2(P/name,archive/name)
    rows=process();stats=json.loads((P/'podatki/register/statistika-registra.json').read_text(encoding='utf-8'));refs=sources();data=load_data()
    assert len(data)==54,len(data)
    body=(P/'vsebina/vsebina.html').read_text(encoding='utf-8')
    if '{{demografija}}' in body:body=body.replace('{{demografija}}',(P/'vsebina/demografija.html').read_text(encoding='utf-8'))
    if '{{drustva}}' in body:body=body.replace('{{drustva}}',(P/'vsebina/drustva.html').read_text(encoding='utf-8'))
    if '{{aed}}' in body:body=body.replace('{{aed}}',(P/'vsebina/aed.html').read_text(encoding='utf-8'))
    if '{{kader-sport}}' in body:body=body.replace('{{kader-sport}}',(P/'vsebina/kader-sport.html').read_text(encoding='utf-8'))
    body=body.replace('{{ckz-spremljanje}}',(P/'vsebina/ckz-spremljanje.html').read_text(encoding='utf-8'))
    if '{{poti}}' in body:body=body.replace('{{poti}}',(P/'vsebina/poti.html').read_text(encoding='utf-8'))
    body=re.sub(r'\{\{chart:([^}]+)\}\}',lambda m:chart(m[1],data[m[1]]),body)
    alltable='<div class="table-scroll"><table><thead><tr><th>Kazalnik</th><th>Zadnja izdaja z vrednostjo</th><th>Črnomelj</th><th>Slovenija iste izdaje</th></tr></thead><tbody>'
    for key,d in sorted(data.items(),key=lambda x:[int(v) for v in x[0][1:].split('.')]):
        loc=next(s for s in d['series'] if s['label']=='Črnomelj');slo=next((s for s in d['series'] if s['label']=='Slovenija'),None);idx=next((i for i in reversed(range(len(d['years']))) if loc['values'][i] is not None),None)
        alltable+=f'<tr><td>{E(d["title"])}</td><td>{d["years"][idx] if idx is not None else "—"}</td><td>{fmt(loc["values"][idx]) if idx is not None else "—"}</td><td>{fmt(slo["values"][idx]) if idx is not None and slo else "—"}</td></tr>'
    alltable+='</tbody></table></div>'
    body=body.replace('{{all-data}}',alltable).replace('{{stats}}',statshtml(stats))
    order=[]
    def cite(m):
        key=m[1];assert key in refs,key
        if key not in order:order.append(key)
        n=order.index(key)+1
        return f'<a class="citation" href="#vir-{n}" title="{E(refs[key]["title"])}">[{n}]</a>'
    body=re.sub(r'\{\{cite:([^}]+)\}\}',cite,body)
    soup=BeautifulSoup(body,'html.parser');nav=''
    for i,s in enumerate(soup.select('section[data-title]'),1):
        h=s.find('h2');head=soup.new_tag('div',attrs={'class':'section-head'});no=soup.new_tag('span',attrs={'class':'section-no'});no.string=f'{i:02}';h.wrap(head);head.insert(0,no)
        nav+=f'<a href="#{s["id"]}"><span>{i:02}</span>{E(s["data-title"])}</a>'
    nav+='<a href="#literatura"><span>↗</span>Literatura</a>'
    body=str(soup)+'<section class="section literature" id="literatura"><h2>Literatura (IEEE)</h2><p>Viri so oštevilčeni po prvem pojavu. Vsak uporabljeni spletni vir ima lokalno kopijo oziroma shranjen uporabljeni izvleček; bibliografski naslovi ostajajo v jeziku izvirnika.</p>'+''.join(citation(refs[key],i) for i,key in enumerate(order,1))+'</section>'
    result=shell(body,nav,data={k:data[k] for k in CHART_META})
    assert '{{' not in result
    (P/'porocilo.html').write_text(result,encoding='utf-8');(P/'porocilo-print.html').write_text(result,encoding='utf-8')
    registry(rows,stats)
    (P/'podatki/literatura/literatura.json').write_text(json.dumps([{**refs[k],'key':k,'number':i} for i,k in enumerate(order,1)],ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'Zgrajeno: {len(data)} nizov, {len(CHART_META)} grafov, {len(order)} virov, {len(rows)} zapisov registra.')

if __name__=='__main__':main()
