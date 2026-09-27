"""Iz izračunov ustvari interaktivni zemljevid, poglavje poročila in wiki sintezo."""
from pathlib import Path
import json,html,re,math,shutil,os
import markdown
from bs4 import BeautifulSoup
from analiziraj_poti import F,lines
P=Path(__file__).resolve().parent.parent; ROOT=P
E=lambda s:html.escape(str(s),quote=True)
def f(n,d=1):return f'{n:,.{d}f}'.replace(',','~').replace('.',',').replace('~','.')
def table(headers,rows):return '| '+' | '.join(headers)+' |\n| '+' | '.join(['---']*len(headers))+' |\n'+'\n'.join('| '+' | '.join(str(x) for x in r)+' |' for r in rows)+'\n'
def render(md):
    s=BeautifulSoup(markdown.markdown(md,extensions=['tables']),'html.parser')
    for t in s.select('table'):t.wrap(s.new_tag('div',attrs={'class':'table-scroll'}))
    return str(s)
def main():
    d=json.loads((P/'podatki/poti/poti-podatki.json').read_text(encoding='utf-8'));r=d['poti'];ns=d['naselja'];stats=d['statistika']
    aed=json.loads((P/'podatki/aed/aed.json').read_text(encoding='utf-8'))
    pxy=[F(*c) for route in r for seg in route['trasa'] for c in seg]+[F(*c) for c in d['meja']]
    ox=min(x for x,y in pxy)-1000;oy=max(y for x,y in pxy)+1000;scale=50
    def xy(c):x,y=F(*c);return (x-ox)/scale,(oy-y)/scale
    def path(points):return 'M'+'L'.join(f'{x:.2f},{y:.2f}' for x,y in map(xy,points))
    def box(points,pad=600):
        pts=list(map(xy,points));xs=[p[0] for p in pts];ys=[p[1] for p in pts];pad/=scale
        return [min(xs)-pad,min(ys)-pad,max(max(xs)-min(xs)+2*pad,30),max(max(ys)-min(ys)+2*pad,30)]
    whole=box([c for route in r for s in route['trasa'] for c in s]);local=box(d['meja'],1500)
    def poly(geo):
        polygons=geo['coordinates'] if geo['type']=='MultiPolygon' else [geo['coordinates']]
        return ''.join(path(ring)+'Z' for polygon in polygons for ring in polygon)
    svg=f'<svg class="poti-svg" xmlns="http://www.w3.org/2000/svg" viewBox="{" ".join(map(str,local))}" role="group" tabindex="0" aria-label="Pohodne in kolesarske trase iz GPX ter kraji v občini Črnomelj"><title>Trase GPX v občini Črnomelj in okolici</title>'
    svg+=f'<path class="pot-boundary" d="{path(d["meja"])}Z"/>'
    for radius,g in d['pasovi']['skupaj'].items():svg+=f'<path class="pot-buffer" data-radius="{radius}" d="{poly(g)}" fill-rule="evenodd" style="display:none"/>'
    svg+=''.join(f'<path class="pot-road" d="{path(c)}"/>' for c in aed['ceste'])
    svg+=''.join(f'<path class="pot-river" d="{path(c)}"/>' for c in aed['reke'])
    for route in r:
        svg+=f'<g class="pot-route {route["vrsta"]}" data-id="{route["id"]}" tabindex="0" role="button" aria-label="{E(route["ime"])}"><title>{E(route["ime"])}</title>'
        for typ,parts in [('outside',route['zunaj']),('inside',route['znotraj'])]:
            svg+=''.join(f'<path class="pot-{typ}" d="{path(c)}"/>' for c in parts)
        svg+='</g>'
        route['bbox']=box([c for s in route['trasa'] for c in s])
        route['bbox_inside']=box([c for s in route['znotraj'] for c in s]) if route['znotraj'] else route['bbox']
    major={'Črnomelj','Vinica','Dragatuš','Adlešiči','Stari trg ob Kolpi','Dobliče','Griblje','Kanižarica','Vranoviči','Petrova vas','Tanča Gora','Sinji Vrh'}
    for i,n in enumerate(ns):
        x,y=xy((n['lon'],n['lat']));far=n['skupaj_m']>1000
        svg+=f'<g class="pot-place {"far" if far else "near"}" data-id="{i}" tabindex="0" role="button" aria-label="{E(n["ime"])}"><circle cx="{x:.2f}" cy="{y:.2f}" r="4"/><title>{E(n["ime"])}: {f(n["skupaj_m"]/1000)} km od najbližje trase</title>'
        if n['ime'] in major:svg+=f'<text class="pot-label" x="{x+6:.2f}" y="{y-5:.2f}">{E(n["ime"])}</text>'
        svg+='</g>'
    # Statično merilo ima dolžino 5 km v projekciji.
    sx,sy=local[0]+15,local[1]+local[3]-20
    svg+=f'<g class="pot-scale"><path d="M{sx},{sy}h100" stroke="#233c31" stroke-width="2" vector-effect="non-scaling-stroke"/><text class="pot-label" x="{sx}" y="{sy-7}">5 km · sever ↑</text></g></svg>'
    mapdata={'poti':[{k:v for k,v in t.items() if k not in ['trasa','znotraj','zunaj']} for t in r],'naselja':ns,'obcina':local,'vse':whole}
    intro=f'''**Pregled 21. 9. 2026:** obdelanih je **43 datotek GPX: 26 pohodnih in 17 kolesarskih**. Znotraj meje Črnomlja ima merljiv odsek **22 tras (14 pohodnih in 8 kolesarskih)**; **21 tras je v celoti zunaj te meje**. To je regionalna zbirka, ne 43 poti v celoti znotraj občine. Pri Poti Gozdna železnica gre le za približno **40 m obmejnega odseka**, zato je treba pripadnost te poti preveriti tudi na uradni meji. [1][2]

Najmočnejša ugotovitev je razlika med vrstama aktivnosti: do pohodniške trase je znotraj **1 km zračne razdalje {stats['pohodnistvo']['pokritost'][1]['naselja']} od {len(ns)} točk krajev ({f(stats['pohodnistvo']['pokritost'][1]['naselja_delez'])} %)**, do kolesarske pa **{stats['kolesarstvo']['pokritost'][1]['naselja']} ({f(stats['kolesarstvo']['pokritost'][1]['naselja_delez'])} %)**. Točke krajev niso gospodinjstva ali urejeni vstopi na pot; deleža **nista deleža prebivalcev**. [1][2]
'''
    summary=table(['Vrsta','Datoteke','Z odsekom v občini','Celotne trase (km)','Odseki v občini (km)'],[[label,stats[k]['datoteke'],stats[k]['poti_v_obcini'],f(stats[k]['km']),f(stats[k]['km_v_obcini'])] for k,label in [('pohodnistvo','Pohodništvo'),('kolesarstvo','Kolesarstvo'),('skupaj','Skupaj')]])
    summary+=f'\n**To so vsote dolžin posameznih tras. Ponovni prehodi po odseku in skupni odseki več tras so šteti večkrat; {f(stats["skupaj"]["km_v_obcini"])} km ni dolžina edinstvenega omrežja ali zgrajenih ločenih poti.** Kolesarski GPX lahko poteka po navadni cesti, pohodni po kolovozu. Oblike infrastrukture iz same sledi ne ugotovimo. Dolžine so dvodimenzionalne in ne vključujejo višinske komponente. [1][2]\n'
    coverage=table(['Bližina trase','Pohodne: kraji','Kolesarske: kraji','Katerakoli: kraji','Delež ozemlja: pohodne / kolesarske / katerakoli'],[
        [f'{rad/1000:g} km'.replace('.',','),*[f'{stats[k]["pokritost"][i]["naselja"]}/{len(ns)} ({f(stats[k]["pokritost"][i]["naselja_delez"])} %)' for k in ['pohodnistvo','kolesarstvo','skupaj']],
        ' / '.join(f(stats[k]['pokritost'][i]['povrsina_delez'])+' %' for k in ['pohodnistvo','kolesarstvo','skupaj'])] for i,rad in enumerate([500,1000,2000])])
    coverage+='\nRazdalje 0,5 / 1 / 2 km so **analitični pragovi**, ne zdravstveni, evropski ali prometni standard. Delež ozemlja meri geometrijsko bližino, vključno z gozdovi in neposeljenimi območji. Pasovi so unija, prekrivanje se pri površini ne podvaja. Skupna bližina obeh vrst ne pomeni, da je kolesarska trasa primerna za pešce. [1][2]\n'
    worst=sorted(ns,key=lambda n:n['pohodnistvo_m'],reverse=True)[:8]
    gaps=table(['Kraj (točka OSM)','Do pohodne trase','Do kolesarske trase'],[[n['ime'],f(n['pohodnistvo_m']/1000)+' km',f(n['kolesarstvo_m']/1000)+' km'] for n in worst])
    gaps+='\n**Prednostna preverba za hojo:** Vranoviči, Ručetna vas, Zastava, Mihelja vas in Pavičiči. Razvrstitev je po oddaljenosti od predloženih pohodnih GPX, ne po številu prebivalcev, starosti ali prometni nevarnosti. Obstoječe lokalne poti, ki jih v zbirki ni, lahko sliko bistveno spremenijo. [1][2]\n\n**Pri kolesarjenju** sta najdlje Vranoviči (3,49 km) in Miliči (2,44 km). Vranoviči so edina od 111 zajetih točk več kot 2 km od katerekoli obravnavane trase znotraj občine. Za ukrepanje najprej preveriti, ali manjka GPX, označena povezava ali dejansko varna infrastruktura. [1][2]\n'
    short=[t for t in r if t['vrsta']=='pohodnistvo' and t['km']<=5 and t['delez_v_obcini']>=95]
    suitability='''### Možnosti za vsakodnevno gibanje in omejitve podatkov

V celoti oziroma vsaj 95-odstotno znotraj občine sta v zbirki **le dve celotni pohodniški trasi dolgi največ 5 km**: Ribja pot – srčna pot Svibnik (4,64 km) in Učna pot Grički kal (4,61 km). Prag 5 km je raziskovalni izbor krajših tras, **ne priporočena razdalja za vsakega uporabnika**. Podatki ne potrjujejo zahtevnosti, prehodnosti z vozičkom, klopi, sence, dostopa brez avtomobila ali dovoljenosti prehoda. [1][2]

Kolesarska krožna pot Črnomelj meri 10,39 km, od tega 10,39 km v občini. Druge lokalno prisotne kolesarske trase so daljše regionalne ture ali njihovi odseki. Za vsakodnevno preventivno vadbo je smiselno **preveriti in opisati krajše uporabne odseke**, ne vsake celotne ture predstavljati kot primerne za začetnike. Pot Dobličica je v mapi pohodnih poti, njeno interno ime GPX pa je »Morning Ride«; vrsta dejavnosti zato zahteva potrditev. [1][2]
'''
    methodology=f'''### Metoda izračuna in omejitve

| Korak | Postopek in omejitev |
| --- | --- |
| Vhod | Vseh 43 predloženih GPX, {f(sum(t['tocke'] for t in r),0)} trasnih točk; razvrstitev po mapah. Izračun ni dopolnjeval manjkajočih poti. |
| Razmejitev | OpenStreetMap, relacija 1685747, zajem 20. 9. 2026; izračunana površina približno {f(d['povrsina_obcine_km2'])} km². OSM ni uradna geodetska meja. |
| Dolžine | Vsak segment ločeno, brez povezovanja konca enega z začetkom naslednjega. Za lokalno dolžino je posebej obrezan vsak zaporedni par točk: ponovni prehodi so ohranjeni. WGS84 geodetska dolžina; preseki s poligonom občine v UTM 33N. |
| Kraji | {len(ns)} točk tipa town/village iz obstoječega OSM zajema. Brez zaselkov tipa hamlet, brez uteži prebivalstva in brez trditve, da gre za vsa uradna naselja. |
| Razdalja | Najkrajša zračna razdalja do črte **znotraj občine** v metrih, ne samo do najbližje shranjene točke. Zunajobčinski odseki niso uporabljeni za ta kazalnik. |
| Pasovi | Polmer 500 / 1.000 / 2.000 m, unija in presek z občino. Za površino so trase poenostavljene največ 5 m; loki imajo 16 odsekov na kvadrant. Zemljevid dodatno poenostavi pasove za 20 m, kar ne spremeni že izračunanih tabel. |
| Kakovost | {sum(t['neveljavne_tocke'] for t in r)} neveljavnih koordinat, {len(d['dvojniki'])} povsem enakih geometrij datotek. Največji razmik zaporednih točk je {f(max(t['max_razmik_m'] for t in r),0)} m: GPX med točkami predpostavlja ravno povezavo. Brez terenske potrditve. |
| Česa ne merimo | Prebivalcev v dosegu, časa hoje/vožnje, prometa, podlage, naklona, zapor, lastništva, oznak, stroškov, vzdrževanja in zdravstvenega učinka. Datumi v GPS posnetku niso datum terenske preverbe. |
'''
    solutions='''### Predlagani naslednji koraki

Ukrepi so raziskovalni predlogi. Okvir ur je orientacijska organizacijska ocena, ne ponudba ali potrjen občinski strošek.

| Rok | Ukrep in odgovorni | Viri / možno financiranje | Korist, tveganje in kazalnik |
| --- | --- | --- | --- |
| 0–3 mesece | RIC, občina in lokalna društva preverijo 43 vnosov, prvotni vir, upravljavca, označenost ter manjkajoče trase. Najprej razjasnijo 40 m mejnega stika Poti Gozdna železnica in vrsto poti Dobličica. | 20–40 ur pisarniškega dela; obstoječa sredstva upravljavcev. | Uporaben register; tveganje neodzivnosti. Delež poti s potrjenim upravljavcem in datumom preverbe. |
| 0–12 mesecev | Občina, KS in CKZ preverijo dostopne kratke odseke pri Vranovičih, Ručetni vasi in drugih oddaljenih krajih ter pri Svibniku/Griču opravijo ogled obstoječih krajših tras. | 5–8 terenskih ogledov po 2 osebi, približno 40–80 človek-ur; občinski program športa/turizma in sredstva partnerjev. | Loči vrzel podatkov od vrzeli dostopa; tveganje neurejenih pravic ali cestnih prehodov. Število opisov z varnim dostopom, podlago, ovirami in dolžino. |
| 1–3 leta | Na podlagi ogledov urediti prednostne manjkajoče povezave, označevanje in dogovorjeno vzdrževanje; odgovorni občina, upravljavci cest in lastniki. | Ločen popis del in projektantska ocena; možni občinski proračun, LAS ali namenski razpisi, upravičenost še ni preverjena. | Več uporabnih povezav; tveganje gradnje brez uporabnikov ali vzdrževanja. Število potrjenih dostopnih povezav in števci uporabe. |
| 1–3 leta | CKZ in društva preizkusijo redno vodeno hojo na preverjenih odsekih; spremljajo vključitev, vztrajanje in ovire dostopa. | Najprej dve skupini, okvirno 2–4 ure vodenja/koordinacije tedensko skupaj; sredstva programov izvajalcev. | Povezava poti z dejansko dejavnostjo; tveganje osipa. Udeležba po treh in šestih mesecih, ne samo število dogodkov. |
| 3–10 let | Vzpostaviti letno obnavljan register poti in dostopa iz naselij, povezan z uradnimi prostorskimi podatki, prebivalstvom in proračunom. | Letni načrt vzdrževanja in podatkov; obseg naložb šele po prioritetah. | Trajnejša dostopnost; tveganje zastarelih podatkov. Delež prebivalcev z dejansko varnim dostopom po mreži in pravočasno izvedeno vzdrževanje. |
'''
    mainmd=intro+'\n### Predložene trase in dolžine odsekov v občini\n\n'+summary+'\n### Bližina tras krajem in občinskemu ozemlju\n\n'+coverage+'\n### Prednostna območja za preverbo dostopa\n\n'+gaps+'\n'+suitability+'\n'+methodology+'\n'+solutions
    (P/'dokumentacija/poti-analiza.md').write_text('# Predložene pohodne in kolesarske trase: prostorska analiza občine\n\n'+mainmd+'\n## Literatura\n\n[1] Predložena zbirka GPX, naročnik poročila, obdelava 21. 9. 2026. Izvirniki: `viri/gpx/`; kontrolne vsote: `podatki/poti/poti-manifest.json`.\n\n[2] Meja Črnomlja in točke krajev, sodelavci OpenStreetMap, zajem 20. 9. 2026. https://www.openstreetmap.org/relation/1685747. Lokalna kopija: `viri/osm-crnomelj.json`; metodologija v wiki sintezi `pokritost-poti-crnomelj-2026.md`.\n',encoding='utf-8')
    rows=''.join(f'<tr data-id="{t["id"]}"><td><button type="button">{E(t["ime"])}</button></td><td>{"Pohodna" if t["vrsta"]=="pohodnistvo" else "Kolesarska"}</td><td>{f(t["km"],2)}</td><td>{f(t["km_v_obcini"],2)}</td><td>{f(t["delez_v_obcini"])} %</td><td><a href="{t["datoteka"]}" download>GPX</a></td></tr>' for t in r)
    cites=lambda s:s.replace('[1]','{{cite:poti-gpx}}').replace('[2]','{{cite:poti-osm}}')
    encoded_data=json.dumps(mapdata,ensure_ascii=False).replace('</','<\\/')
    out=f'''<section class="section" id="poti" data-title="Pohodne in kolesarske trase"><style>{(P/'vsebina/poti.css').read_text(encoding='utf-8')}</style>
<h2>Pohodne in kolesarske trase: zemljevid in prostorska bližina</h2>{render(cites(intro))}
<div class="poti-tools"><label><input id="poti-pes" type="checkbox" checked>Pohodne</label><label><input id="poti-kolo" type="checkbox" checked>Kolesarske</label><label><input id="poti-zunaj" type="checkbox" checked>Odseki zunaj občine</label><label><input id="poti-kraji" type="checkbox" checked>Kraji</label><label>Analitični pas vseh tras<select id="poti-pas"><option value="">Brez pasu</option><option value="500">500 m</option><option value="1000">1 km</option></select></label></div>
<div class="poti-legend"><span style="--key:#146e5c">Pohodne</span><span style="--key:#c1531e">Kolesarske</span><span style="--key:#5b7458">Meja občine</span><span style="--key:#b32639">Kraj več kot 1 km od katerekoli trase</span></div>
<div class="poti-layout"><div class="poti-mapbox">{svg}<div class="poti-zoom"><button type="button" data-action="in" aria-label="Približaj poti">+</button><button type="button" data-action="out" aria-label="Oddalji poti">−</button><button type="button" data-action="reset">Občina</button><button type="button" data-action="all">Vsa regija</button></div></div><aside class="poti-panel" aria-live="polite"><h3>Izberite traso ali kraj</h3><p>Klik na traso pokaže dolžino in izvirni GPX; klik na kraj pokaže oddaljenost od obeh vrst poti.</p><p>Približajte z gumboma ali dvoklikom, premaknite z vlečenjem. S tipkovnico: Tab, Enter, +/− in smerne tipke.</p><p class="subtle">Iskanje spodaj filtrira prikaz. Analitični pas vedno prikazuje vse trase iz zbirke, ne le trenutno vidnih.</p></aside></div>
<p class="subtle">Podlaga: © sodelavci OpenStreetMap, ODbL, zajem 20. 9. 2026; {{cite:poti-osm}}. GPX: datoteke naročnika; {{cite:poti-gpx}}. Zemljevid deluje brez omrežja. Črtkane, blede trase so zunaj občine; v kazalnikih niso upoštevane.</p>
<div class="poti-searchbox"><label>Iskanje trase <input id="poti-search" type="search" placeholder="Npr. Grički kal, Vinica, Mirna gora"></label><a class="btn" href="podatki/poti/poti.csv" download>Trase CSV</a><a class="btn" href="podatki/poti/poti-pokritost-naselij.csv" download>Oddaljenost krajev CSV</a><a class="btn" href="podatki/poti/poti.geojson" download>GeoJSON</a><a class="btn" href="podatki/poti/poti-zemljevid.svg" download>Zemljevid SVG</a></div>
<p id="poti-count"></p><details><summary>Seznam vseh 43 tras z dolžinami in prenosi</summary><div class="table-scroll"><table id="poti-tabela"><thead><tr><th>Trasa</th><th>Vrsta</th><th>Celotna (km)</th><th>V občini (km)</th><th>Delež v občini</th><th>Izvirnik</th></tr></thead><tbody>{rows}</tbody></table></div></details>
{render(cites(mainmd[len(intro):]))}
<script type="application/json" id="poti-data">{encoded_data}</script><script>{(P/'vsebina/poti.js').read_text(encoding='utf-8')}</script></section>'''
    # f-string je pri dvojnih oklepajih namenoma uporabljen le za statični del.
    out=re.sub(r'(?<!\{)\{cite:([^}]+)\}(?!\})',r'{{cite:\1}}',out)
    (P/'vsebina/poti.html').write_text(out,encoding='utf-8')
    standalone=svg.replace('<svg ', '<svg id="poti" ',1).replace('<title>','<style>'+(P/'vsebina/poti.css').read_text(encoding='utf-8').replace('#poti ','')+'</style><title>',1)
    (P/'podatki/poti/poti-zemljevid.svg').write_text(standalone,encoding='utf-8')
    write_wiki(d,mainmd,intro,summary,coverage,gaps,suitability,methodology,solutions)
    print('Poti: zemljevid, HTML, SVG in wiki sinteza pripravljeni.')

def write_wiki(d,mainmd,intro,summary,coverage,gaps,suitability,methodology,solutions):
    raw=ROOT/'viri/splet/poti-gpx-20260921-manifest.md'
    manifest=json.loads((P/'podatki/poti/poti-manifest.json').read_text(encoding='utf-8'))
    if not raw.exists():raw.write_text('# Predložena zbirka poti GPX\n\nDatum obdelave: 2026-09-21. Vir: naročnik; 43 izvirnih datotek v `viri/gpx/`. Izvorni avtorji in datum terenske preverbe niso potrjeni. To ni spletni zajem.\n\n'+table(['Datoteka','SHA-256'],[[t['datoteka'],t['sha256']] for t in manifest['datoteke']]),encoding='utf-8')
    osmraw=ROOT/'viri/splet/osm-crnomelj-poti-20260921.md';dest=ROOT/'viri/splet/priloge/osm-crnomelj-20260920.json'
    dest.parent.mkdir(exist_ok=True)
    if not dest.exists():shutil.copy2(P/'viri/osm-crnomelj.json',dest)
    if not osmraw.exists():osmraw.write_text('---\nurl: https://www.openstreetmap.org/relation/1685747\nnaslov: Meja Črnomlja in točke krajev – obstoječi zajem OpenStreetMap\nizdajatelj: Sodelavci OpenStreetMap\ndostopano: 2026-09-20\nmetoda zajema: WebFetch (Overpass, obstoječi zajem; ponovno lokalno analiziran 2026-09-21)\n---\n\nUporabljena relacija 1685747 (admin_level=8, Črnomelj), zunanja meja brez notranjih obročev, točke place=town/village, glavne ceste in reke. Čas podatkov '+d['osm_cas']+'. Celotna lokalna kopija: [[priloge/osm-crnomelj-20260920.json]]. Licenca podatkov: ODbL, © sodelavci OpenStreetMap.\n\nZajem ne vsebuje popolnega uradnega registra naselij, populacij ali omrežja za izračun dostopa. Meja je OSM, ne uradni katastrski/občinski prostorski akt.\n',encoding='utf-8')
    refs={'poti-gpx':{'title':'Predložena zbirka 43 poti GPX – manifest izvirnikov','publisher':'Naročnik poročila; izvirni avtorji niso potrjeni','date':'obdelava 21. september 2026','local':raw.relative_to(ROOT).as_posix(),'note':'Izvirniki v viri/gpx; kontrolne vsote v manifestu. Popolnost in terensko stanje nista potrjena.'},'poti-osm':{'title':'Meja Črnomlja, točke krajev in kartografska podlaga','publisher':'Sodelavci OpenStreetMap','date':'20. september 2026','access':'20. september 2026','url':'https://www.openstreetmap.org/relation/1685747','local':osmraw.relative_to(ROOT).as_posix(),'note':'Obstoječi zajem Overpass; © sodelavci OpenStreetMap, ODbL.'}}
    (P/'podatki/poti/poti-viri.json').write_text(json.dumps(refs,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    literature='''## Literatura

[1] »Predložena zbirka 43 poti GPX,« naročnik poročila, obdelava 21. septembra 2026. Lokalni izvirniki: `viri/gpx/`; [[../../../viri/splet/poti-gpx-20260921-manifest|manifest s kontrolnimi vsotami]]. Izračuni: [[../../../podatki/poti/poti-podatki.json]], [[../../../podatki/poti/poti-pokritost-naselij.csv]].

[2] »Meja Črnomlja in točke krajev,« sodelavci OpenStreetMap, 20. september 2026. [Na spletu]. Dostopno: https://www.openstreetmap.org/relation/1685747. [Dostopano: 20. september 2026]. Lokalna kopija: [[../../../viri/splet/osm-crnomelj-poti-20260921]]. © sodelavci OpenStreetMap, ODbL.
'''
    questions=table(['Naslovnik','Konkretno vprašanje'],[
    ['Občina / RIC','Kdo je upravljavec vsake od 43 predloženih tras in katere so uradno označene?'],
    ['Občina / geodetska služba','Ali približno 40 m Poti Gozdna železnica dejansko leži znotraj uradne občinske meje?'],
    ['Upravljavci poti','Katere sledi so bile nazadnje terensko preverjene in kdaj?'],
    ['Pristojne KS / RIC','Katere lokalne pohodne povezave manjkajo v zbirki pri Vranovičih in Ručetni vasi?'],
    ['Občina','Koliko prebivalcev po uradnih naslovnih podatkih nima varnega dostopa do poti brez avtomobila?'],
    ['CKZ','Kateri kratki odseki ustrezajo konkretnim skupinam uporabnikov in kdo potrdi primernost?'],
    ['Upravljavci cest','Kje GPX poteka po prometnih cestah brez ločene površine ali varnega prečkanja?'],
    ['Lastniki / upravljavci','Ali so urejene pravice prehoda, zapore in dovoljene vrste uporabe?'],
    ['RIC / društva','Ali je Dobličica pohodniška, kolesarska ali večnamenska trasa in od kod ime Morning Ride?'],
    ['Občina','Koliko znašajo stroški vzdrževanja in označevanja vsake poti ter kdo jih plača?'],
    ['CKZ / društva','Koliko različnih ljudi poti redno uporablja in koliko jih vztraja po šestih mesecih?'],
    ['Občina / RIC','Kdo bo vzdrževal javni register in objavil datum naslednjega pregleda?']])
    text='# Predložene pohodne in kolesarske trase GPX: prostorska analiza občine Črnomelj\n\n## Povzetek\n\n'+intro+'\n## Trenutno stanje\n\n'+summary+'\n## Ključna dejstva\n\n'+coverage+'\n### Prednostna območja preverbe\n\n'+gaps+'\n'+suitability+'\n## Viri\n\n'+methodology+'\n## Identificirani problemi\n\nZbirka je regionalna in njena popolnost ni potrjena. Pohodne trase so prostorsko slabše razporejene od kolesarskih; velika regionalna dolžina ne zagotavlja bližnje vsakodnevne vadbe. Podatki ne povedo, kdo je odločal o trasah, kdo nosi stroške in kakšen je izmerjeni učinek. Največjo korist od uporabnega registra imajo prebivalci, izvajalci vadbe in obiskovalci; posledice manjkajočih informacij nosijo predvsem uporabniki, ki se na sled zanesejo. Potrebna je preverba pravic uporabe in prometnih pogojev, ne sklep o ugotovljeni kršitvi.\n\n## Kritična vprašanja\n\n'+questions+'\n## Tveganja\n\nZračna bližina lahko prikrije reko, strm teren, prometno cesto ali nedovoljen prehod. Točke OSM lahko manjkajo ali niso središče poselitve. Meja in GPS imata prostorsko negotovost, posebej pri mejnih stikih. Skupna vsota dolžin se podvaja na skupnih odsekih. Brez terenskih in stroškovnih podatkov ni mogoče oceniti varnosti, gospodarnosti ali zdravstvenega učinka.\n\n## Možne rešitve\n\n'+solutions+'\n## Primerjave\n\nPrimerljiva je bližina obeh vrst tras v isti zbirki in na isti osnovi. Ni podatkov za pošteno lestvico občin ali primerjavo deležev prebivalstva. Naslednji korak je enaka analiza na uradnih mejah, naslovih in prometno preverjeni mreži za primerljive občine.\n\n## Odprta vprašanja\n\nStatus: Unverified — popolnost zbirke, aktualna prehodnost, prometna varnost, pravice prehoda, označenost, vzdrževalci, stroški, primernost za vozičke ali ranljive uporabnike in izmerjeni zdravstveni učinki. Sedmih vsebinskih ocen 1–5 iz same geometrije ni mogoče pošteno določiti; ne izdelamo navidezne skupne ocene kakovosti poti.\n\n## Povezane strani\n\npregled peš poti, kolesarskih poti in športnih objektov (stran nadrejenega vaulta, ni del tega projekta) · [[../../entities/institutions/ckz-crnomelj]] · [[zdravstveni-kader-in-sport-crnomelj-2026]] · [[../../sources/source-summaries/poti-gpx-pokritost-2026]]\n\n## Zadnja posodobitev\n\n2026-09-21 — izračun iz lokalnih virov, brez terenskega ogleda ali novega spletnega popisa poti.\n\n'+literature
    (ROOT/'wiki/analysis/synthesis/pokritost-poti-crnomelj-2026.md').write_text(text,encoding='utf-8')
    summarytext='# Vir: 43 tras GPX in prostorska pokritost občine\n\n## Povzetek\n\n'+intro+'\n## Izvor in zanesljivost\n\nGPX je zagotovil uporabnik. Zanesljivost je visoka za vsebino datotek in ponovljive izračune, neznana za aktualno stanje v naravi in popolnost. OSM je sekundarna kartografska osnova; uradne meje in naselja niso bili pridobljeni. Izvirne datoteke niso spremenjene. [1][2]\n\n'+methodology+'\n## Glavne ugotovitve\n\n'+summary+'\n## Povezane strani\n\n[[../../analysis/synthesis/pokritost-poti-crnomelj-2026]] · pregled peš poti, kolesarskih poti in športnih objektov (stran nadrejenega vaulta, ni del tega projekta)\n\n## Zadnja posodobitev\n\n2026-09-21.\n\n'+literature
    (ROOT/'wiki/sources/source-summaries/poti-gpx-pokritost-2026.md').write_text(summarytext,encoding='utf-8')
if __name__=='__main__':main()
