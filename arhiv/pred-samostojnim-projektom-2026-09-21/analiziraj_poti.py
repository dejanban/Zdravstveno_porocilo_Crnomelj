"""GPX + obstoječi zajem OSM -> sledljiv prostorski popis; brez omrežja."""
from pathlib import Path
import sys,json,xml.etree.ElementTree as ET,hashlib,csv,math
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P/'.python-deps'))
import shapely,numpy as np
from shapely.geometry import LineString,MultiLineString,Polygon,Point,mapping
from shapely.ops import transform,unary_union
from pyproj import Transformer,Geod
from pripravi_aed import stitch
F=Transformer.from_crs(4326,32633,always_xy=True).transform
B=Transformer.from_crs(32633,4326,always_xy=True).transform
G=Geod(ellps='WGS84')
NAMES={
'credniska_pot':'Čredniška pot','grajska_gozdna_ucna_pot_obrh':'Grajska gozdna učna pot Obrh',
'jozefov_pohod':'Jožefov pohod','kraska_ucna_pot_od_lebice_do_krupe':'Kraška učna pot od Lebice do Krupe',
'krupa_moverna_vas':'Krupa–Moverna vas','martinov_pohod':'Martinov pohod','mlinarska_pot':'Mlinarska pot',
'najjuznejsa_slovenska_pespot_od_radencev_do_damlja':'Najjužnejša slovenska pešpot Radenci–Damelj',
'obkolpska_grajska_pot':'Obkolpska grajska pot','pastirska_pot':'Pastirska pot','planinska_krozna_pot':'Planinska krožna pot',
'pot_gozdna_zeleznica':'Pot Gozdna železnica','pot_na_smuk_gornje_laze':'Pot na Smuk – Gornje Laze',
'ribja-pot':'Ribja pot – srčna pot Svibnik','sejemska_pespot_vinica_zunici':'Sejemska pešpot Vinica–Žuniči',
'trdinova_pot':'Trdinova pot','trska_pespot':'Trška pešpot','ucna-pot':'Učna pot – srčna pot Svibnik',
'ucna_pot_divji_potok':'Učna pot Divji potok','ucna_pot_gricki_kal':'Učna pot Grički kal',
'ucna_pot_kucar_kolpa':'Učna pot Kučar–Kolpa','ucna_pot_mirna_gora':'Učna pot Mirna gora',
'ucna_pot_zdenc_vidovec':'Učna pot Zdenc–Vidovec','ucno_rekreacijska_pot_doblicica':'Učno-rekreacijska pot Dobličica',
'urbanova_pot':'Urbanova pot','zupanciceva_pot':'Župančičeva pot',
'belokranjska_kolesarska_proga':'Belokranjska kolesarska proga',
'kolesarska_krozna_pot_crnomelj':'Kolesarska krožna pot Črnomelj','kolesarska_krozna_pot_metlika':'Kolesarska krožna pot Metlika',
'kolesarska_pot_damelj':'Kolesarska pot Damelj','kolesarska_pot_gace':'Kolesarska pot Gače',
'kolesarska_pot_gradnik':'Kolesarska pot Gradnik','kolesarska_pot_krasnji_vrh':'Kolesarska pot Krašnji vrh',
'kolesarska_pot_krupa':'Kolesarska pot Krupa','kolesarska_pot_kucar':'Kolesarska pot Kučar',
'kolesarska_pot_mirna_gora':'Kolesarska pot Mirna gora','kolesarska_pot_mirna_gora_semic':'Kolesarska pot Mirna gora – Semič',
'kolesarska_pot_ravnace':'Kolesarska pot Ravnače','kolesarska_pot_vidosici':'Kolesarska pot Vidošiči',
'poljanska_kolesarska_pot':'Poljanska kolesarska pot','zupanciceva_kolesarska_pot':'Župančičeva kolesarska pot',
'turnokolesarska_3048_stkp_etapa_22_planinski_dom_na_mirni_gori_planinski_dom_pri_gospodicni_na_gorjancih':'STKP etapa 22: Mirna gora–Gospodična',
'turnokolesarska_3049_stkp_etapa_21_koca_pri_jelenovem_studencu_planinski_dom_na_mirni_gori':'STKP etapa 21: Jelenov studenec–Mirna gora'}
def lines(g):
    if g.is_empty:return []
    if g.geom_type=='LineString':return [g]
    if hasattr(g,'geoms'):return [s for part in g.geoms for s in lines(part)]
    return []
def km(g):
    return sum(G.line_length(*zip(*transform(B,x).coords)) for x in lines(g))/1000
def clipped_km(geom,boundary):
    # Presek cele samoprekrivajoče trase bi izgubil ponovne prehode.
    # Vsak izvorni par točk obrežemo ločeno in geodetsko seštejemo dele.
    edges=np.array([[a,b] for line in lines(geom) for a,b in zip(list(line.coords),list(line.coords)[1:])])
    parts=shapely.get_parts(shapely.intersection(shapely.linestrings(edges),boundary))
    parts=parts[shapely.get_type_id(parts)==1]
    if not len(parts):return 0.0
    counts=shapely.get_num_coordinates(parts)
    if not np.all(counts==2):return sum(km(line) for line in parts)
    xy=shapely.get_coordinates(parts);lon,lat=B(xy[:,0],xy[:,1])
    return float(np.sum(G.inv(lon[::2],lat[::2],lon[1::2],lat[1::2])[2])/1000)

def coords(g):return [[[round(x,7),round(y,7)] for x,y in transform(B,z).coords] for z in lines(g)]
def read_gpx(path):
    root=ET.parse(path).getroot(); segs=root.findall('.//{*}trkseg')
    typ='trkpt'
    if not segs:segs=root.findall('.//{*}rte');typ='rtept'
    out=[];elev=[];bad=0;maxgap=0;times=[]
    for seg in segs:
        pts=[]
        for pt in seg.findall('{*}'+typ):
            try:
                lon,lat=float(pt.attrib['lon']),float(pt.attrib['lat'])
                assert math.isfinite(lon) and math.isfinite(lat) and -180<=lon<=180 and -90<=lat<=90
            except (ValueError,KeyError,AssertionError):
                bad+=1
                if len(pts)>1:out.append(pts)
                pts=[];continue
            if pts:
                gap=G.inv(*pts[-1],lon,lat)[2];maxgap=max(maxgap,gap)
            pts.append((lon,lat))
            t=pt.findtext('{*}time')
            if t:times.append(t)
            try:
                v=float(pt.findtext('{*}ele'))
                if math.isfinite(v):elev.append(v)
            except (TypeError,ValueError):pass
        if len(pts)>1:out.append(pts)
    if not out:raise ValueError('Ni uporabne trase: '+str(path))
    return root,out,elev,bad,maxgap,times

def main():
    osm=json.loads((P/'viri/osm-crnomelj.json').read_text(encoding='utf-8'))
    rel=next(e for e in osm['elements'] if e['type']=='relation' and e.get('tags',{}).get('name')=='Črnomelj')
    assert not any(m.get('role')=='inner' for m in rel['members'])
    ring=stitch([[(p['lon'],p['lat']) for p in m['geometry']] for m in rel['members'] if m['type']=='way' and m.get('role')=='outer'])
    boundary=transform(F,Polygon(ring));assert boundary.is_valid
    route_geoms={};data=[];manifest=[];groups={'pohodnistvo':[],'kolesarstvo':[]};features=[]
    for i,path in enumerate(sorted((P/'viri/gpx').rglob('*.gpx'))):
        root,segs,elev,bad,gap,times=read_gpx(path)
        geom=transform(F,MultiLineString(segs));inner=geom.intersection(boundary);outer=geom.difference(boundary)
        length=km(geom);local=clipped_km(geom,boundary);kind=path.parent.name
        slug=path.stem;assert slug in NAMES,slug
        canon=sorted(min(tuple(s),tuple(reversed(s))) for s in segs)
        row={'id':i,'ime':NAMES[slug],'vrsta':kind,'datoteka':path.relative_to(P).as_posix(),
             'gpx_ime':root.findtext('.//{*}trk/{*}name') or root.findtext('.//{*}rte/{*}name') or '',
             'km':length,'km_v_obcini':local,'delez_v_obcini':local/length*100 if length else 0,
             'v_obcini':local>0.001,'segmenti':len(segs),'tocke':sum(map(len,segs)),
             'max_razmik_m':gap,'neveljavne_tocke':bad,'visina_min':min(elev) if elev else None,
             'visina_max':max(elev) if elev else None,'cas_prvi':min(times) if times else None,'cas_zadnji':max(times) if times else None,
             'zacetek_konec_m':G.inv(*segs[0][0],*segs[-1][-1])[2] if len(segs)==1 else None,
             'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
             'geometrija_hash':hashlib.sha256(repr(canon).encode()).hexdigest(),
             'trasa':segs,'znotraj':coords(inner),'zunaj':coords(outer)}
        data.append(row);route_geoms[i]=inner
        if not inner.is_empty:groups[kind].extend(lines(inner))
        manifest.append({k:v for k,v in row.items() if k not in ['trasa','znotraj','zunaj']})
        features.append({'type':'Feature','properties':manifest[-1],'geometry':mapping(MultiLineString(segs))})
    # Za razdalje ni potrebno drago vozliščenje vseh prekrivajočih se odsekov.
    unions={k:MultiLineString(v) for k,v in groups.items()};unions['skupaj']=MultiLineString(groups['pohodnistvo']+groups['kolesarstvo'])
    ns=[]
    for e in osm['elements']:
        if e['type']!='node' or e.get('tags',{}).get('place') not in ('town','village'):continue
        pt=transform(F,Point(e['lon'],e['lat']))
        if not boundary.covers(pt):continue
        distances={k:pt.distance(g) for k,g in unions.items()}
        nearest=min((pt.distance(g),i) for i,g in route_geoms.items() if not g.is_empty)
        ns.append({'osm_id':e['id'],'ime':e['tags'].get('name',''),'lon':e['lon'],'lat':e['lat'],
                   **{k+'_m':v for k,v in distances.items()},'najblizja_pot_id':nearest[1]})
    ns.sort(key=lambda n:n['ime'])
    buffers={};stats={};area=boundary.area/1e6
    cached_buffers={}
    for key,net in unions.items():
        bins=[];buffers[key]={}
        for radius in [500,1000,2000]:
            if key=='skupaj':
                buf=unary_union([cached_buffers[(k,radius)] for k in groups])
            else:
                buf=unary_union([line.simplify(5).buffer(radius,quad_segs=16) for line in groups[key]]).intersection(boundary)
                cached_buffers[(key,radius)]=buf
            print('Pas',key,radius,'m izračunan',flush=True)
            n=sum(x[key+'_m']<=radius for x in ns)
            bins.append({'razdalja_m':radius,'naselja':n,'naselja_delez':n/len(ns)*100,'povrsina_km2':buf.area/1e6,'povrsina_delez':buf.area/boundary.area*100})
            if radius<=1000:buffers[key][str(radius)]=mapping(transform(B,buf.simplify(20,preserve_topology=True)))
        subset=data if key=='skupaj' else [r for r in data if r['vrsta']==key]
        stats[key]={'datoteke':len(subset),'poti_v_obcini':sum(r['v_obcini'] for r in subset),
                    'km':sum(r['km'] for r in subset),'km_v_obcini':sum(r['km_v_obcini'] for r in subset),'pokritost':bins}
    hashes={}
    for r in data:hashes.setdefault(r['geometrija_hash'],[]).append(r['id'])
    result={'datum':'2026-09-21','crs_analize':'EPSG:32633','meja_osm_id':rel['id'],'osm_cas':osm['osm3s']['timestamp_osm_base'],
            'povrsina_obcine_km2':area,'stevilo_naselij_osm':len(ns),'statistika':stats,'poti':data,'naselja':ns,
            'meja':ring,'pasovi':buffers,'dvojniki':[v for v in hashes.values() if len(v)>1],
            'metoda':'Dolžine WGS84 geodetsko; preseki, zračne razdalje in površine UTM 33N. Vsak zaporedni par točk se za dolžino obreže ločeno; ponovni prehodi znotraj iste trase in skupni odseki različnih tras se pri seštevku dolžin ponovijo. Pasovi so unija in se pri površini ne seštevajo. Samo odseki znotraj občine. Dolžine in razdalje: vse veljavne točke. Za površino pasov trase poenostavljene s toleranco 5 m in krožni loki s 16 odseki na kvadrant; prikaz pasov dodatno poenostavljen 20 m. OSM town/village točke, ne popoln uradni seznam naselij ali prebivalstveno utežena pokritost.'}
    (P/'poti-podatki.json').write_text(json.dumps(result,ensure_ascii=False),encoding='utf-8')
    (P/'poti.geojson').write_text(json.dumps({'type':'FeatureCollection','features':features},ensure_ascii=False),encoding='utf-8')
    (P/'poti-manifest.json').write_text(json.dumps({'datum':'2026-09-21','datoteke':manifest,'metoda':result['metoda']},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for filename,rows in [('poti.csv',manifest),('poti-pokritost-naselij.csv',ns)]:
        with (P/filename).open('w',encoding='utf-8-sig',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=';');w.writeheader();w.writerows(rows)
    short=[r for r in data if r['vrsta']=='pohodnistvo' and r['km']<=5 and r['delez_v_obcini']>=95]
    print(json.dumps({'povrsina':area,'naselja':len(ns),'statistika':stats,'kratke_pes':[r['ime'] for r in short],
                      'oddaljena':sorted(ns,key=lambda n:n['skupaj_m'],reverse=True)[:12],
                      'dvojniki':result['dvojniki'],'max_razmik':max(r['max_razmik_m'] for r in data)},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
