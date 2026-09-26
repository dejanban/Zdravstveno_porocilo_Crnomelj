"""Sestavljanje zavihkov iz ohranjenih poglavij in nove raziskovalne vsebine."""
from pathlib import Path
import json,re,html,csv,statistics,hashlib
from bs4 import BeautifulSoup
import markdown
ROOT=Path(__file__).resolve().parents[1]

GROUPS=[
 ('pregled','Pregled',['za-prebivalce','povzetek','kam-po-pomoc'],'Kako zdravi smo, kaj je na voljo in kaj lahko izboljšamo? Začnite s povzetkom ali izberite področje spodaj.'),
 ('stevilke','Zdravje v številkah',['starost','dejavniki','debelost-otroci','promet-alkohol','kronicne','eu'],'Kazalniki in demografski kontekst. Letnica na drsniku NIJZ je leto izdaje; referenčna obdobja so navedena ob grafih in v metodologiji.'),
 ('ckz','Delovanje CKZ',['ckz','ckz-spremljanje','dogodki'],'Programi, dokumentirane dejavnosti in predlogi spremljanja. Objave, udeležba in zdravstveni izidi so različne enote; trend občine ni dokaz učinka CKZ.'),
 ('spanje','Spanje in digitalne navade',['spanje-povzetek','spanje-raziskave','spanje-ukrepi'],'Kaj kažejo raziskave o večernih zaslonih, spanju in družbenih omrežjih? Mednarodne ugotovitve niso lokalna meritev Črnomlja.'),
 ('poti','Peš in kolesarske poti',['poti','poti-dopolnitve'],'Izberite pešpoti ali kolesarske sledi in si oglejte izračune GPX. Zemljevid opisuje trase; prehodnost, prometna varnost in primernost niso samodejno potrjene.'),
 ('sport','Športne dejavnosti',['sportna-ponudba'],'Poiščite vrsto dejavnosti in izvajalca. Ohranjeni pregled objav ni potrjen tekoči urnik; cene, prosta mesta in dostopnost ostajajo neznani, kjer ni dokaza.'),
 ('aed','AED-ji',['aed'],'Lokacije iz ohranjenega registra. Javno navedena lokacija ne pomeni potrjene dostopnosti 24 ur na dan ali znanega odzivnega časa.'),
 ('podpora','Preventiva in podpora',['presejanje','referencne-ambulante','ustanova','kader-pregled','dusevna-pomoc','dusevno-mladi','fizioterapija-prehrana-vadba','zdravniki','primanjkljaj-zdravnikov','drustva'],'Presejanje, zdravstvene storitve in podporne mreže. Kontakti in ponudba so navedeni po objavljenih virih, brez telefonske potrditve.'),
 ('dostop','Dostop do oskrbe',['nujna-pomoc','zemljevid-nmp','neopredeljeni','digitalno-zdravje','dolgotrajna-oskrba','demenca'],'Kako hitro pride nujna pomoč, kdo nima osebnega zdravnika, koliko se čaka, kdo zmore digitalne poti in kako je poskrbljeno za starejše in osebe z demenco doma. Modelski časi vožnje niso izmerjeni dostopni časi NMP.'),
 ('okolje','Okolje in življenjske razmere',['kontekst','okolje-zdravje','pitna-voda','zrak','vrocina'],'Dohodki, stres, domača hrana, pitna voda in kakovost zraka. Razlikujte obdobja meritev, lokacije in manjkajoče podatke.'),
 ('ukrepi','Ukrepi in odprta vprašanja',['resitve','vprasalnik-pacienti','kader-ukrepi','okolje-ukrepi','vprasanja'],'Predlogi za občino, ZD, CKZ, šole in partnerje. Načrtovane aktivnosti in sredstva še niso potrjena izvedba ali odobreno financiranje.'),
 ('viri','Viri in metodologija',['metoda','vzroki','popravki','literatura'],'Kako beremo podatke, kaj je bilo popravljeno in na katerih dokazih temeljijo ugotovitve. Vsaka navedba vodi do bibliografskega zapisa in stanja lokalne kopije.'),
]
RELATED={
 'pregled':[('stevilke','Podatki za razumevanje potreb'),('ukrepi','Od ugotovitev do ukrepov')],
 'stevilke':[('ckz','Programi, ki naslavljajo potrebe'),('podpora','Presejanje in storitve'),('viri','Definicije in obdobja')],
 'ckz':[('stevilke','Zdravstvene potrebe občine'),('spanje','Dokazi za nove vsebine'),('podpora','Društva in podporna mreža')],
 'spanje':[('ckz','Možnosti vključitve v preventivo'),('podpora','Podporne službe'),('sport','Možnosti dejavnega prostega časa'),('poti','Gibanje na prostem')],
 'poti':[('sport','Organizirane dejavnosti'),('aed','Lokacije AED-jev'),('okolje','Okolje za gibanje')],
 'sport':[('poti','Poti za samostojno gibanje'),('ckz','Vadba v okviru preventive'),('aed','Pregled lokacij AED-jev')],
 'aed':[('poti','Lokacije tudi na zemljevidu poti'),('dostop','Dostop do nujne pomoči'),('sport','Šport in rekreacija'),('ukrepi','Vrzel med lokacijo in dostopnostjo')],
 'podpora':[('ckz','Preventivni programi'),('spanje','Spanje in digitalne navade'),('dostop','Dostop do oskrbe'),('stevilke','Kazalniki zdravstvenih potreb')],
 'dostop':[('aed','Lokacije AED-jev'),('podpora','Zdravniki in podporne službe'),('stevilke','Starost prebivalcev'),('ukrepi','Ukrepi in odprta vprašanja')],
 'okolje':[('stevilke','Zdravje in demografija'),('poti','Prostor za gibanje'),('ukrepi','Okoljski ukrepi in odgovornost')],
 'ukrepi':[('ckz','Spremljanje rezultatov'),('spanje','Vprašanja o digitalnih navadah'),('viri','Preverite podlago pred odločitvijo')],
 'viri':[('stevilke','Nazaj k podatkom'),('ukrepi','Kaj še potrebujemo')],
}
def fragment(s):return BeautifulSoup(s,'html.parser')
def write(path,text):
 p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')
def dump(path,data):write(path,json.dumps(data,ensure_ascii=False,indent=2))
def write_csv(path,headers,rows):
 p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.writer(f);w.writerow(headers);w.writerows(rows)

def sleep_content(soup,refs):
 records=json.loads((ROOT/'podatki/spanje/spanje-viri.json').read_text(encoding='utf-8'))
 data={r['slug']:r for r in records}
 text=(ROOT/'vsebina/spanje-digitalne-navade.md').read_text(encoding='utf-8')
 used=list(dict.fromkeys(re.findall(r'\[@([^\]]+)\]',text)))
 assert all(k in data for k in used),'Manjka zajem vira'
 wiki=text
 for i,k in enumerate(used,1):wiki=wiki.replace('[@'+k+']',f'[{i}]')
 wiki+='\n\n## Literatura\n\n'
 for i,k in enumerate(used,1):
  r=data[k]
  wiki+=f'[{i}] »{r["title"]},« {r["publisher"]}, {r["date"]}. [Na spletu]. Dostopno: {r["url"]}. [Dostopano: 25. september 2026]. Lokalna kopija: [[../../../{r["local"]}]]. Obseg: {r["scope"]}.\n\n'
  refs[r['id']]=fragment(f'<p id="{r["id"]}"><span class="refno">[vir]</span> {html.escape(r["authors"])}. »{html.escape(r["title"])},« {html.escape(r["publisher"])}, {r["date"]}. [Na spletu]. Dostopno: <a href="{r["url"]}">{r["url"]}</a>. [Dostopano: 25. september 2026]. Lokalna kopija: <a href="{r["local"]}">zajeto besedilo</a>; <a href="{r["path"]}">izvirni prenos</a>. Obseg: {r["scope"]}.</p>').p
 write('wiki/topics/social-affairs/spanje-digitalne-navade.md',wiki)
 def cite(m):
  r=data[m[1]];title=html.escape(r['title'],quote=True).replace('|','&#124;');return f'<a class="citation" href="#{r["id"]}" title="{title}">[vir]</a>'
 rendered=re.sub(r'\[@([^\]]+)\]',cite,text)
 parts=[('spanje-povzetek','Spanje in digitalne navade: ključna sporočila',rendered.split('## Povzetek\n')[1].split('## Ključna dejstva')[0]),('spanje-raziskave','Kaj kažejo raziskave',rendered.split('## Ključna dejstva\n')[1].split('## Viri')[0]),('spanje-ukrepi','Lokalna vprašanja, ukrepi in omejitve','## Viri\n'+rendered.split('## Viri\n')[1].split('## Povezane strani')[0])]
 for sid,title,body in parts:
  body=re.sub(r'^## ', '### ',body,flags=re.M)
  sec=fragment(f'<section class="section sleep" id="{sid}" data-title="{title}"><div class="section-head"><span class="section-no"></span><h2>{title}</h2></div>'+markdown.markdown(body,extensions=['tables'])+'</section>').section
  for t in sec.find_all('table'):t.wrap(soup.new_tag('div',attrs={'class':'table-scroll'}))
  soup.select_one('#literatura').insert_before(sec)
 # Graf in podatkovna alternativa iz ene metaanalize, brez mešanja mer.
 rows=[('Nezadosten spanec',2.17,1.42,3.32),('Slaba kakovost',1.46,1.14,1.88),('Dnevna zaspanost',2.72,1.32,5.61)]
 x=lambda v:210+v*73
 svg='<svg viewBox="0 0 760 228" role="img" aria-labelledby="spanje-graf-title spanje-graf-desc"><title id="spanje-graf-title">Večerna uporaba naprav in spanje: razmerja obetov</title><desc id="spanje-graf-desc">Carter 2016, otroci in mladostniki. Tri ocene OR s 95-odstotnimi intervali zaupanja. Vrednosti so tudi v tabeli spodaj. Opazovalne povezave, ne dokaz vzročnosti.</desc><line x1="283" x2="283" y1="24" y2="172" stroke="#8e6542" stroke-dasharray="5 4"/>'
 for i,(label,v,lo,hi) in enumerate(rows):
  y=43+i*49;value=f'{v:.2f}'.replace('.',',');svg+=f'<text x="5" y="{y+5}" font-size="15" fill="#19334b">{label}</text><line x1="{x(lo)}" x2="{x(hi)}" y1="{y}" y2="{y}" stroke="#245a80" stroke-width="3"/><circle cx="{x(v)}" cy="{y}" r="5" fill="#a25c37"/><text x="680" y="{y+5}" font-size="14">{value}</text>'
 for v in range(7):svg+=f'<text x="{x(v)}" y="190" text-anchor="middle" font-size="13">{v}</text>'
 svg+='<text x="435" y="218" text-anchor="middle" font-size="14">OR in 95-% interval zaupanja; OR = 1: brez povezave</text></svg>'
 fig=fragment('<figure class="evidence-chart">'+svg+'<figcaption>Večerna uporaba naprav: raziskave do junija 2015, starost 6–19 let. OR ni relativno tveganje in ne pove deleža prizadetih v Črnomlju. <a class="citation" href="#sleep-carter-2016">[vir]</a></figcaption></figure>').figure
 soup.select_one('#spanje-raziskave .section-head').insert_after(fig)
 write_csv('podatki/spanje/carter-2016-or.csv',['izid','OR','IZ95_spodaj','IZ95_zgoraj','vir','obdobje'],[list(r)+['10.1001/jamapediatrics.2016.2341','iskanje do junija 2015'] for r in rows])
 fig.append(fragment('<p><a href="podatki/spanje/carter-2016-or.csv" download>Prenesi podatke grafa (CSV)</a>. Vrednosti in omejitve so tudi v preglednici raziskav spodaj.</p>'))

def update_content(soup,refs):
 """Datirane posodobitve 25. 9. 2026: vodenje ZD in objavljen razpored ambulant."""
 records=json.loads((ROOT/'podatki/posodobitve/posodobitve-viri.json').read_text(encoding='utf-8'))
 data={r['slug']:r for r in records}
 for r in records:
  refs[r['id']]=fragment(f'<p id="{r["id"]}"><span class="refno">[vir]</span> »{html.escape(r["title"])},« {html.escape(r["publisher"])}, {html.escape(r["date"])}. [Na spletu]. Dostopno: <a href="{r["url"]}">{html.escape(r["url"])}</a>. [Dostopano: 25. september 2026]. Lokalna kopija: <a href="{r["local"]}">zajeto besedilo</a>; <a href="{r["path"]}">izvirni HTML</a>. Zanesljivost: {html.escape(r["reliability"])}.</p>').p
 def c(slug):return f'<a class="citation" href="#{data[slug]["id"]}" title="{html.escape(data[slug]["title"],quote=True)}">[vir]</a>'
 body=f'''<h3 id="zd-vodenje-2026-09">Vodenje zavoda in razpoložljivost ambulant: posnetek 25. 9. 2026</h3>
<p>Po medijskem poročanju je svet zavoda aprila 2026 začel postopek predčasne razrešitve dotedanjega direktorja, ker Zakon o zdravstveni dejavnosti za direktorja zdravstvenega doma zahteva najmanj drugostopenjsko izobrazbo; ministrstvo je februarja od ZD in občine zahtevalo tudi pojasnila o tržni dejavnosti in vnosu podatkov v zbirko NIJZ. {c("svet24-matkovic")} Uradna stran ZD 25. 9. 2026 navaja v. d. direktorja, ki je hkrati strokovna vodja zavoda. {c("zd-upravljanje")} Po <em>neuradnem</em> medijskem poročilu z 23. 9. 2026 je svet zavoda po razpisu z dne 13. 8. 2026 (štiri prijave) izbral novega direktorja; imenovanje po navedbi članka postane dokončno s soglasjem ustanoviteljice ali po poteku 60-dnevnega roka. {c("mojadolenjska-direktor")} Uradne objave izbire ob zajemu nismo našli, zato je ne štejemo za potrjeno.</p>
<div class="table-scroll"><table><thead><tr><th>Področje</th><th>Objava ZD 25. 9. 2026</th><th>Kako razumeti</th></tr></thead><tbody>
<tr><td>Družinska medicina</td><td>Tri ambulante za neopredeljene (SA 2 in SA 3 v Črnomlju, SA Semič 2): »nadomeščanje po razporedu«.</td><td>Ambulante so namenjene ljudem brez izbranega zdravnika. To je skladno z vrzeljo 2,00 tima iz programa 2026, ne pove pa števila neopredeljenih oseb ali čakalnih dob.</td></tr>
<tr><td>Otroci in mladi</td><td>Otroška ambulanta z nekdanjo nosilko in zobna ambulanta za mlade 1: nadomeščanje po razporedu.</td><td>Stalni nosilec ni objavljen; obseg nadomeščanja v urah ni znan.</td></tr>
<tr><td>Zobozdravstvo</td><td>Ambulanta za odrasle 4 in ortodontija: nadomeščanje po razporedu; Vinica: odsotnost 22. 9.–30. 10.</td><td>Za Vinico to pomeni daljšo prekinitev lokalne zobozdravstvene ambulante; nadomestna lokacija ni navedena.</td></tr>
<tr><td>Duševno zdravje</td><td>Ena od treh navedenih psihologinj: »odsotna do nadaljnjega«.</td><td>Zmanjšana zmogljivost psihološke obravnave; čakalna doba ni objavljena.</td></tr>
<tr><td>Medicina dela</td><td>»Do nadaljnjega ne dela«.</td><td>Delodajalci in delavci morajo preventivne preglede opraviti drugje; vpliv na dostop ni izmerjen.</td></tr>
</tbody></table></div>
<p>Vir za preglednico: {c("zd-odsotnost")} Omejitve: stran je tekoči razpored in ne kadrovska evidenca. Enkratni posnetek ni trend; za primerjavo ga je treba ponavljati (npr. mesečno) in dopolniti s podatki ZZZS o neopredeljenih osebah ter čakalnih dobah.</p>'''
 sec=soup.select_one('#ustanova')
 for part in fragment(body).contents:sec.append(part)
 target=soup.select_one('#primanjkljaj-zdravnikov .section-head')
 if target:target.insert_after(fragment('<p class="callout">Posnetek objavljenega razporeda ambulant in stanje vodenja zavoda 25. 9. 2026: <a href="#zd-vodenje-2026-09">Zdravstveni dom Črnomelj</a>.</p>'))
 soup.select_one('#popravki tbody').append(fragment(f'<tr><td>Poročilo ni vsebovalo aktualnega stanja vodenja ZD in objavljenega razporeda ambulant.</td><td>25. 9. 2026: dodan datiran posnetek. Izbira novega direktorja je označena kot neuradna, dokler je ne potrdi uradni vir. {c("zd-upravljanje")}{c("mojadolenjska-direktor")}</td></tr>'))

TEME=[('nujna-pomoc','Dostop do nujne pomoči in prvi posredovalci','social-affairs'),
 ('neopredeljeni','Neopredeljeni pacienti in čakalne dobe','social-affairs'),
 ('dolgotrajna-oskrba','Dolgotrajna oskrba in pomoč na domu','social-affairs'),
 ('vrocina','Vročinski valovi in zdravje','environment'),
 ('dusevno-mladi','Duševno zdravje mladih','social-affairs'),
 ('promet-alkohol','Prometna varnost in alkohol','social-affairs'),
 ('poti-dopolnitve','Trim steza Vražji kamen in Srčna pot Svibnik','social-affairs'),
 ('digitalno-zdravje','Digitalno zdravje: eNaročanje, zVEM in e-posvet','social-affairs'),
 ('demenca','Demenca in demenci prijazna občina','social-affairs'),
 ('vprasalnik-pacienti','Vprašalnik o izkušnjah pacientov za letno poročilo','analysis/solutions'),
 ('debelost-otroci','Debelost in gibanje otrok','social-affairs'),
 ('referencne-ambulante','Referenčne ambulante: kaj odkrijejo preventivni pregledi','social-affairs'),
 ('za-prebivalce','Na kratko za prebivalce',None),
 ('kam-po-pomoc','Kam po pomoč',None)]
ZLOZENO=['Kritična vprašanja','Možne rešitve','Odprta vprašanja']

def teme_content(soup,refs):
 """Nove teme 25. 9. 2026 iz vsebina/teme/*.md; viri v podatki/teme/teme-viri.json."""
 records={r['slug']:r for r in json.loads((ROOT/'podatki/teme/teme-viri.json').read_text(encoding='utf-8'))}
 for r in records.values():
  refs['tema-'+r['slug']]=fragment(f'<p id="tema-{r["slug"]}"><span class="refno">[vir]</span> {html.escape(r["authors"])}. »{html.escape(r["title"])},« {html.escape(r["publisher"])}, {html.escape(r["date"])}. [Na spletu]. Dostopno: <a href="{html.escape(r["url"],quote=True)}">{html.escape(r["url"])}</a>. [Dostopano: {r.get("accessed_sl","25. september 2026")}]. Lokalna kopija: <a href="{r["local"]}">izvleček</a>; <a href="{r["path"]}">izvirnik</a>. Obseg: {html.escape(r["scope"])} Zanesljivost: {html.escape(r["reliability"])}.</p>').p
 def key(tok):return tok[4:] if tok.startswith('ref:') else 'tema-'+tok
 for slug,title,folder in TEME:
  text=(ROOT/'vsebina/teme'/(slug+'.md')).read_text(encoding='utf-8')
  toks=list(dict.fromkeys(re.findall(r'\[@([^\]]+)\]',text)))
  missing=[t for t in toks if key(t) not in refs];assert not missing,(slug,missing)
  # Wiki stran: IEEE številčenje po prvem pojavu na strani.
  wiki=text
  for i,t in enumerate(toks,1):wiki=wiki.replace('[@'+t+']',f'[{i}]')
  wiki=wiki.replace('](podatki/','](../../../podatki/')+'\n## Literatura\n\n'
  for i,t in enumerate(toks,1):
   if t.startswith('ref:'):
    ref=re.sub(r'^\[\S+\]\s*','',refs[key(t)].get_text(' ',strip=True));wiki+=f'[{i}] {ref}\n\n'
   else:
    r=records[t];wiki+=f'[{i}] {r["authors"]}, »{r["title"]},« {r["publisher"]}, {r["date"]}. [Na spletu]. Dostopno: {r["url"]}. [Dostopano: {r.get("accessed_sl","25. september 2026")}]. Lokalna kopija: [[../../../{r["local"]}]]. Izvirnik: [[../../../{r["path"]}]]. Obseg: {r["scope"]} Zanesljivost: {r["reliability"]}.\n\n'
  if folder:write(f'wiki/{folder}/{slug}.md' if '/' in folder else f'wiki/topics/{folder}/{slug}.md',wiki)
  # Poglavje poročila.
  def cite(m):
   k=key(m[1]);t=refs[k].get_text(' ',strip=True)[:160]
   return f'<a class="citation" href="#{k}" title="{html.escape(t,quote=True)}">[vir]</a>'
  body=text.split('## Povzetek\n',1)[1].split('## Povezane strani')[0]
  body='## Povzetek\n'+re.sub(r'\[@([^\]]+)\]',cite,body)
  body=re.sub(r'^(#{2,3}) ',lambda m:'#'+m[1]+' ',body,flags=re.M)
  sec=fragment(f'<section class="section tema" id="{slug}" data-title="{title}"><div class="section-head"><span class="section-no"></span><h2>{title}</h2></div><p class="subtle">Dopolnitev {"26" if slug in ("poti-dopolnitve","digitalno-zdravje","demenca","vprasalnik-pacienti","debelost-otroci","referencne-ambulante","za-prebivalce","kam-po-pomoc") else "25"}. septembra 2026 · referenčna obdobja so navedena pri podatkih</p>'+markdown.markdown(body,extensions=['tables'])+'</section>').section
  for t in sec.find_all('table'):t.wrap(soup.new_tag('div',attrs={'class':'table-scroll'}))
  for heading in list(sec.find_all('h3',recursive=False)):
   if heading.get_text(strip=True) not in ZLOZENO:continue
   detail=soup.new_tag('details',attrs={'class':'content-layer'});summary=soup.new_tag('summary');summary.string=heading.get_text(strip=True);detail.append(summary);heading.insert_before(detail)
   nxt=heading.next_sibling;heading.extract()
   while nxt is not None and getattr(nxt,'name',None)!='h3':following=nxt.next_sibling;detail.append(nxt.extract());nxt=following
  soup.select_one('#literatura').insert_before(sec)
 # Interaktivni zemljevid dostopnosti (orodja/zemljevid_nmp.py) takoj za poglavjem o nujni pomoči.
 import zemljevid_nmp
 zem=fragment('<section class="section tema" id="zemljevid-nmp" data-title="Zemljevid dostopnosti"><div class="section-head"><span class="section-no"></span><h2>Zemljevid: pot do zdravstvenega doma in čas nujne pomoči</h2></div>'+zemljevid_nmp.build()+'</section>').section
 soup.select_one('#nujna-pomoc').insert_after(zem)
 st=soup.new_tag('style',id='zemljevid-nmp-css');st.string=zemljevid_nmp.CSS;soup.head.append(st)
 js=soup.new_tag('script',id='zemljevid-nmp-js');js.string=zemljevid_nmp.JS;soup.body.append(js)
 soup.select_one('.hero-meta').append(fragment('<span>Dostop do oskrbe, nove teme in povzetek za prebivalce: 25.–26. september 2026</span>'))
 soup.select_one('#povzetek tbody').append(fragment('<tr><td><b>Dostop do oskrbe je najšibkejši člen.</b> 3.142 ljudi je registriranih v ambulantah za neopredeljene, nove paciente sprejema 1 od 9 ambulant, v SB Novo mesto 47,3 % čakajočih na prvi pregled čaka dlje od dopustne dobe. V pomoč na domu je vključen 1,0 % starejših (Slovenija 1,8 %), delež prometnih nezgod z alkoholom je 12,9 % (Slovenija 8,2 %).</td><td>Objaviti dostopne čase NMP in obseg mreže prvih posredovalcev, pripraviti načrt ob vročini in pomoč pri vlogah za dolgotrajno oskrbo v Črnomlju. <a href="#neopredeljeni">Podrobnosti</a>.</td></tr>'))
 soup.select_one('#popravki tbody').append(fragment('<tr><td>Poročilo ni obravnavalo dostopa do nujne pomoči, neopredeljenih pacientov, vročine, duševnega zdravja mladih, dolgotrajne oskrbe ter prometa in alkohola.</td><td>25. 9. 2026: dodanih šest poglavij z 20 novimi lokalno shranjenimi viri. Modelski časi vožnje (OSRM) so označeni kot ocena, ne kot dostopni čas NMP. Popravek med pripravo: prvotni osnutek je trdil, da mreža prvih posredovalcev ni dokumentirana; letno poročilo ZD 2025 jo navaja kot vzpostavljeno, zato je trditev popravljena pred objavo.</td></tr>'))
 soup.select_one('#popravki tbody').append(fragment('<tr><td>Poročilo ni omenjalo trim steze Vražji kamen, Ribje in Učne poti pa ni povezalo s Srčno potjo koronarnih bolnikov.</td><td>26. 9. 2026: dodano poglavje v zavihku poti in oznaka na zemljevidu. GPX Ribje poti s strani Srčne poti je enak že analiziranemu (SHA-256). Trasa trim steze bo dodana, ko bo GPX na voljo.</td></tr>'))
 soup.select_one('#popravki tbody').append(fragment('<tr><td>Zemljevid dostopnosti je prikazoval en sam modelski čas (OSRM) kot oceno vožnje.</td><td>26. 9. 2026: naročnik je s primerjavo z Google Maps ugotovil neujemanje. Dodan drug model (Valhalla), prikazan razpon obeh ter pripravljeno umerjanje na Googlove čase (<a href="podatki/teme/kalibracija-google.csv">predloga</a>). Najdena napaka v podatkih: enopasovna lokalna cesta proti Gribljam ima v OSM vpisano omejitev 90 km/h.</td></tr>'))

def recover_data(soup):
 """Obnovi samo podatke, dejansko vgrajene v ohranjeno izdajo."""
 aed=json.loads(soup.select_one('#aed-data').text);routes=json.loads(soup.select_one('#poti-data').text);charts=json.loads(soup.select_one('#chart-data').text)
 dump('podatki/aed/aed.json',aed);write_csv('podatki/aed/aed.csv',['lokacija','naslov','lat','lon','v_obcini','oznaka_starega_registra','casovna_dostopnost'],[[r['ime'],r.get('naslov',''),r['lat'],r['lon'],r['in'],r.get('javno_dostopen'),'ni preverjena'] for r in aed])
 for r in routes['poti']:
  p=ROOT/r['datoteka'];r['izvirnik_na_voljo']=p.is_file() and p.stat().st_size>0
 soup.select_one('#poti-data').string=json.dumps(routes,ensure_ascii=False)
 dump('podatki/poti/poti-podatki.json',routes);cols=list(routes['poti'][0]);write_csv('podatki/poti/poti.csv',cols,[[r.get(k) for k in cols] for r in routes['poti']])
 write('podatki/poti/poti-zemljevid.svg',str(soup.select_one('#poti svg')).replace('viewbox=','viewBox='))
 dump('podatki/nijz/obnovljeni-grafi.json',charts)
 write_csv('podatki/nijz/obnovljeni-grafi.csv',['kazalnik','izdaja','obmocje','vrednost'],[[key,year,series['label'],series['values'][i]] for key,d in charts.items() for i,year in enumerate(d['years']) for series in d['series']])
 # Izvirne celotne tabele ne nadomeščamo z delnim naborom grafov.
 soup.select_one('#metoda').append(fragment('<p><a href="podatki/nijz/obnovljeni-grafi.csv" download>Prenesi vrednosti ohranjenih grafov (CSV)</a> (izpis iz prikaza). Celotna izvirna tabela kazalnikov je v <a href="podatki/nijz/kazalniki.csv" download>kazalniki.csv</a>, izvirnih 54 Excelov NIJZ pa v mapi viri/nijz in lokalni <a href="viri/index.html">knjižnici virov</a> (obnovljeni iz commita 0dc0bd4 25. 9. 2026 in preverjeni z izvirnim manifestom SHA-256).</p>'))
 dump('podatki/prenova-obnovljeni-podatki.json',{'datum':'2026-09-25','osnova':'vsebina/obnovljena-osnova-20260924.html','obseg':['AED podatki iz vgrajenega JSON','poti in kraji iz vgrajenega JSON','vrednosti ohranjenih grafov NIJZ'],'omejitev':'Obnova prikaza ni ponovna preverba primarnih virov. Izvirni GPX, Exceli NIJZ ter izvirna podatkovna izvoza AED in poti (s celotno geometrijo) so bili 25. 9. 2026 obnovljeni iz commita 0dc0bd4: viri/gpx, viri/nijz, arhiv/izvirnik-0dc0bd4/podatki.'})
 return aed,routes

def route_layer(soup,aed,data):
 from pyproj import Transformer
 t=Transformer.from_crs(4326,32633,always_xy=True)
 pts=[]
 for node in soup.select('#poti .pot-place'):
  r=data['naselja'][int(node['data-id'])];x,y=t.transform(r['lon'],r['lat']);pts.append([x,y,float(node.circle['cx']),float(node.circle['cy'])])
 fits=[]
 for a,b in [(0,2),(1,3)]:
  xm=statistics.mean(p[a] for p in pts);ym=statistics.mean(p[b] for p in pts)
  scale=sum((p[a]-xm)*(p[b]-ym) for p in pts)/sum((p[a]-xm)**2 for p in pts);offset=ym-scale*xm;error=max(abs(scale*p[a]+offset-p[b]) for p in pts)
  assert error<.02,('Nepotrjena projekcija zemljevida',error)
  fits.append((scale,offset,error))
 group=soup.new_tag('g',attrs={'id':'poti-aed-layer','class':'route-aed','style':'display:none','aria-label':'Lokacije AED; dostopnost ni preverjena'})
 for r in aed:
  x,y=t.transform(r['lon'],r['lat']);x=x*fits[0][0]+fits[0][1];y=y*fits[1][0]+fits[1][1]
  a=soup.new_tag('a',href='#aed-lokacija-'+str(r['i']),attrs={'tabindex':'0','aria-label':r['ime']+' – podatki AED'})
  a.append(soup.new_tag('circle',cx=f'{x:.3f}',cy=f'{y:.3f}',r='4'))
  title=soup.new_tag('title');title.string=r['ime']+'; časovna dostopnost ni preverjena';a.append(title);group.append(a)
 soup.select_one('#poti svg').append(group)
 # Vražji kamen (vrh, OSM 9272920042): trasa trim steze čaka na GPX.
 vx,vy=t.transform(15.2026363,45.6044502);vx=vx*fits[0][0]+fits[0][1];vy=vy*fits[1][0]+fits[1][1]
 soup.select_one('#poti svg').append(fragment(f'<a href="#poti-dopolnitve" class="route-note" aria-label="Vražji kamen: trim steza, GPX v pripravi"><path d="M{vx:.2f} {vy-7:.2f}L{vx+6:.2f} {vy+4:.2f}L{vx-6:.2f} {vy+4:.2f}Z" fill="#5b3f8c" stroke="#fff" stroke-width="1.5"/><text x="{vx+8:.2f}" y="{vy-8:.2f}" font-size="11" fill="#3c2a5e" paint-order="stroke" stroke="#fff" stroke-width="3">Trim steza Vražji kamen</text><title>Vražji kamen: trim steza z vadbenimi postajami; trasa GPX še ni na voljo</title></a>'))
 soup.select_one('.poti-tools').append(fragment('<label><input type="checkbox" id="poti-aed"> AED-ji (rdeče točke)</label>'))
 soup.select_one('#poti .poti-tools').insert_before(fragment('<div class="route-modes" aria-label="Vrsta poti"><button type="button" data-mode="vse" aria-pressed="true">Vse trase</button><button type="button" data-mode="pes" aria-pressed="false">Pešpoti</button><button type="button" data-mode="kolo" aria-pressed="false">Kolesarske poti</button></div><p class="subtle">Sloj AED uporablja iste podatke kot zavihek AED-ji. Točke ne potrjujejo časovne dostopnosti, varnosti poti ali odzivnega časa. Izberite točko za podatke o napravi.</p>'))
 for row in soup.select('#aed-table tbody tr'):
  row['id']='aed-lokacija-'+row['data-i']
  record=next(r for r in aed if r['i']==int(row['data-i']))
  cells=row.find_all('td');cells[4].string=('V starem registru označen kot javno dostopen; urnik ni preverjen' if record.get('javno_dostopen') else 'Ni potrjenega podatka o časovni dostopnosti')
 dump('podatki/aed/poti-projekcija.json',{'metoda':'Ujemanje ohranjenih OSM kontrolnih točk s projekcijo EPSG:32633 in afino pretvorbo SVG; preverjene vse kontrolne točke.','kontrolne_tocke':len(pts),'x':fits[0],'y':fits[1],'opomba':'To je rekonstrukcija prikaza, ne terenska preverba lokacij.'})

def prepare(soup,refs):
 sleep_content(soup,refs)
 update_content(soup,refs)
 teme_content(soup,refs)
 aed,routes=recover_data(soup);route_layer(soup,aed,routes)
 # Zamenjava samo navigacijskega dela stare skripte; interaktivni grafi ostanejo.
 for script in soup.find_all('script'):
  if "?'Javno dostopen'" in script.text:script.string=script.text.replace("?'Javno dostopen'","?'V ohranjenem registru označen kot javno dostopen'")
  if 'const nav=document.querySelector' in script.text:
   txt=script.text;start=txt.index('const nav=document.querySelector');end=txt.index("document.querySelectorAll('[data-print]')")
   txt=txt[:start]+txt[end:];txt=re.sub(r"if\(nav&&'IntersectionObserver'[\s\S]*?(?=const dataNode=)",'',txt);script.string=txt
 # Transparenten popravek preveč gotove uvodne trditve prejšnje izdaje.
 soup.select_one('.lede').string='Podatki o zdravju, pregled preventive in možnosti za dejavno življenje v Beli krajini. Povezane analize, lokalni zemljevidi in vprašanja za boljše odločitve.'
 soup.select_one('.hero-meta').append(fragment('<span>Oblikovna prenova in raziskave spanja: 25. september 2026</span>'))
 soup.select_one('#popravki tbody').append(fragment('<tr><td>Uvod je navajal »preverjeno oceno dela CKZ«; oznaka AED »javno dostopen« je lahko zvenela kot zagotovljen dostop.</td><td>25. 9. 2026: ocena CKZ ostaja uredniška presoja dokumentiranega dela. Dostopnost AED je ločena od nepreverjenega urnika in namestitve; ohranjeni zapis ni nova terenska potrditev. Dokaz: ohranjena izdaja v arhivu in njeni podatkovni zapisi.</td></tr><tr><td>Spanje in digitalne navade niso imeli samostojnega raziskovalnega pregleda.</td><td>25. 9. 2026: dodana ločena presoja populacij, vzročnosti in omejitev dostopa do člankov. <a class="citation" href="#sleep-ahmed-2024">[vir]</a><a class="citation" href="#sleep-odklop-2025">[vir]</a></td></tr>'))
 table=soup.select_one('#sportna-ponudba table');table['id']='sport-table';options=''
 for row in table.select('tbody tr'):
  kind=row.td.get_text(' ',strip=True);row['data-sport']=kind;options+=f'<option>{html.escape(kind)}</option>'
 controls=fragment('<div class="sport-controls"><label>Išči dejavnost ali izvajalca<input id="sport-search" type="search" placeholder="Npr. ples, hoja, Črnomelj"></label><label>Vrsta dejavnosti<select id="sport-type"><option value="">Vse vrste</option>'+options+'</select></label></div><p id="sport-count" class="subtle" role="status"></p><p class="subtle">Cena, prosti termini in gibalna dostopnost niso sistematično dokumentirani. Ponudbe zato ne filtriramo po domnevnih vrednostih.</p>')
 table.parent.insert_before(controls)
 for sid,msg in [('aed','Namestitev znotraj ali zunaj objekta ter urnik dostopnosti nista dokumentirano preverjena za posamezne naprave. Obnova iz ohranjenega poročila: 25. 9. 2026; to ni datum terenskega preverjanja.'),('sportna-ponudba','Pregled je ohranjen iz izdaje 21. 9. 2026 in vključuje tudi objave iz 2025. Tekoči urniki, cene in prosta mesta niso na novo potrjeni.')]:
  soup.select_one('#'+sid+' .section-head').insert_after(fragment('<p class="callout warning">'+msg+'</p>'))
 for node in soup.select_one('#aed').find_all(string=True):
  if 'Vsi AED-ji v občini Črnomelj so javno dostopni.' in node:
   node.replace_with(node.replace('Vsi AED-ji v občini Črnomelj so javno dostopni.','V ohranjenem uporabniškem popisu so AED-ji v občini Črnomelj označeni kot javno dostopni; urnik ni preverjen.'))
 # Vsi prvotni odseki morajo pripadati natanko enemu zavihku.
 sections={x['id']:x for x in soup.select('main > section')};expected=[sid for _,_,ids,_ in GROUPS for sid in ids]
 assert set(sections)==set(expected),(set(sections)-set(expected),set(expected)-set(sections))
 nav=soup.select_one('#kazalo');nav.clear();nav['role']='tablist';nav['aria-orientation']='vertical';nav['aria-label']='Področja zdravstvenega poročila'
 anchor=soup.select_one('main > footer')
 for n,(key,label,ids,description) in enumerate(GROUPS,1):
  pid='zavihek-'+key;tid='tab-'+key
  nav.append(fragment(f'<a role="tab" id="{tid}" href="#{pid}" aria-controls="{pid}" aria-selected="false"><span>{n:02}</span>{label}</a>'))
  panel=soup.new_tag('div',attrs={'class':'report-panel','id':pid,'role':'tabpanel','aria-labelledby':tid,'data-label':label,'tabindex':'0'})
  panel.append(fragment(f'<div class="panel-intro"><div class="eyebrow">Področje {n:02} / Črnomelj</div><h2>{label}</h2><p>{description}</p><nav class="panel-index" aria-label="Poglavja: {label}">'+''.join(f'<a href="#{sid}">{html.escape(sections[sid].find("h2").get_text(" ",strip=True))}</a>' for sid in ids)+'</nav></div>'))
  if key=='pregled':
   panel.append(fragment('<div class="topic-grid">'+''.join(f'<a class="topic-card" href="#zavihek-{k}"><strong>{l}</strong><span>{d.split(". ")[0]}.</span></a>' for k,l,_,d in GROUPS if k!='pregled')+'</div>'))
  for sid in ids:
   sec=sections[sid];panel.append(sec.extract())
   rel='<aside class="related" aria-label="Povezane vsebine"><strong>Povezano</strong>'+''.join(f'<a href="#zavihek-{k}">{l} →</a>' for k,l in RELATED[key])
   if key!='viri':rel+='<a href="#zavihek-viri">Viri in metodologija →</a>'
   sec.append(fragment(rel+'</aside>'))
  anchor.insert_before(panel)
 # Uvod in kazalniki ostanejo v pregledu, ne se ponavljajo pred vsakim zavihkom.
 overview=soup.select_one('#zavihek-pregled');intro=overview.select_one('.panel-intro')
 intro.insert_after(soup.select_one('.kpis').extract());intro.insert_after(soup.select_one('#uvod').extract())
 tools=fragment('<div class="report-tools no-print"><div><label for="report-search">Poiščite temo, kraj ali storitev</label><input id="report-search" type="search" placeholder="Npr. spanje, Adlešiči, CKZ …" aria-controls="report-results" aria-describedby="report-search-status"></div><button id="clear-report-search" type="button">Počisti iskanje</button></div><p class="search-status no-print" id="report-search-status" role="status"></p><div class="search-results no-print" id="report-results" hidden></div>')
 soup.select_one('main .topbar').insert_after(tools)
 soup.select_one('.nav-label').string='Raziskujte področja'
 soup.select_one('.side-bottom').insert(0,fragment('<p>Povezani podatki, preventiva in lokalne možnosti.</p>'))
 soup.select_one('#povzetek .section-head').insert_after(fragment('<p class="callout warning">Pomembno o dokazih: lokalne kopije starejših virov, ki so bile ob prenosu izpraznjene, so bile 25. 9. 2026 obnovljene iz prve različice projekta in preverjene s kontrolnimi vsotami. To potrjuje, da so kopije izvirne, ne pa, da so starejše ugotovitve še aktualne; te v prenovi niso ponovno v celoti preverjene. Pri štirih raziskavah o spanju je prebran samo povzetek. Stanje virov je označeno v literaturi.</p>'))
 soup.select_one('#popravki tbody').append(fragment('<tr><td>Stari manifest je bil opisan kot potrjen za celoten obnovljeni obseg.</td><td>25. 9. 2026: pri 313 besedilnih datotekah je potrjena ekvivalentnost po pretvorbi koncev vrstic. Šest podedovanih HTML-kopij se še ne ujema; pričakovane in opažene vsote so ohranjene v <a href="podatki/spanje/podedovana-neskladja.json">registru neskladij</a>. Izvirnih pričakovanih vsot nismo nadomestili z novimi.</td></tr>'))
 soup.select_one('#popravki tbody').append(fragment('<tr><td>Prenova 25. 9. 2026 je navajala, da je del starega arhiva izgubljen in da 77 prenosov ter izvirni GPX in Exceli NIJZ niso na voljo.</td><td>25. 9. 2026 (popoldne): 1.087 izpraznjenih datotek je obnovljenih iz prve git različice projekta (commit 0dc0bd4). 1.289 od 1.290 datotek izvirnega manifesta se ujema z zapisanimi SHA-256 (razlika le v koncih vrstic); izjema je <code>viri/AEDs.xlsx</code>, katere neskladje je bilo zabeleženo že 23. 9. Manjka le še zapis naročnika o dostopnosti AED z dne 23. 9. Postopek: <a href="preverjanje/obnova-iz-gita.json">seznam obnovljenih datotek</a>.</td></tr>'))
 # Metodološke podrobnosti so dostopne na drugi/treti ravni; omejitve ostanejo vidne.
 for sid in ['spanje-ukrepi']:
  sec=soup.select_one('#'+sid)
  heads=sec.find_all('h3',recursive=False)
  for heading in heads:
   if heading.text not in ['Kritična vprašanja','Možne rešititve','Možne rešitve','Uredniška ocena dokumentiranosti']:continue
   detail=soup.new_tag('details',attrs={'class':'content-layer'});summary=soup.new_tag('summary');summary.string=heading.text;detail.append(summary);heading.insert_before(detail)
   nxt=heading.next_sibling;heading.extract()
   while nxt and not(getattr(nxt,'name',None) in ['h3','aside']):following=nxt.next_sibling;detail.append(nxt.extract());nxt=following
 style=soup.new_tag('style',id='prenova-css');style.string=(ROOT/'vsebina/prenova.css').read_text(encoding='utf-8');soup.head.append(style)
 script=soup.new_tag('script',id='prenova-js');script.string=(ROOT/'vsebina/prenova.js').read_text(encoding='utf-8');soup.body.append(script)
 return json.loads((ROOT/'podatki/spanje/spanje-viri.json').read_text(encoding='utf-8'))

def mark_missing_downloads(soup):
 unavailable=[]
 for a in soup.select('a[href]'):
  href=a['href']
  if re.match(r'^(https?:|#|mailto:|tel:|data:)',href):continue
  from urllib.parse import unquote
  p=(ROOT/unquote(href.split('#')[0])).resolve()
  assert p.is_relative_to(ROOT),href
  if not p.is_file() or p.stat().st_size==0:
   unavailable.append(href);a['data-original-href']=href;del a['href'];a.attrs.pop('download',None);a['aria-disabled']='true';a['class']=a.get('class',[])+['missing-source'];a['title']='Izvirnik manjka ali je prazen v podedovanem arhivu: '+href;a.append(' [kopija manjka]')
 dump('preverjanje/manjkajoci-prenosi.json',sorted(set(unavailable)))
