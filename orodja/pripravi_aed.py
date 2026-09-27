"""Zemljevid defibrilatorjev: viri/AEDs.xlsx + viri/osm-crnomelj.json -> podatki/aed/aed.json, podatki/aed/aed.csv, vsebina/aed.html (razdelek poročila)."""
import json, csv, math, html
from pathlib import Path
import openpyxl
P = Path(__file__).resolve().parent.parent
E = lambda v: html.escape(str(v), quote=True)
HALL = ['Črnomelj', 'Vinica', 'Dragatuš', 'Adlešiči', 'Stari trg ob Kolpi', 'Dobliče', 'Griblje', 'Kanižarica', 'Tanča Gora', 'Talčji Vrh', 'Sinji Vrh', 'Petrova vas', 'Butoraj', 'Tribuče', 'Zilje', 'Preloka', 'Loka', 'Grič']
EXTRA = [('Metlika', 15.3167, 45.6483), ('Semič', 15.1825, 45.6528), ('Predgrad (Kočevje)', 15.055, 45.505)]


def stitch(ways):
    segs = [list(map(tuple, w)) for w in ways]
    ring = segs.pop(0)
    while segs:
        for i, s in enumerate(segs):
            if s[0] == ring[-1]: ring += s[1:]
            elif s[-1] == ring[-1]: ring += s[::-1][1:]
            elif s[-1] == ring[0]: ring = s[:-1] + ring
            elif s[0] == ring[0]: ring = s[::-1][:-1] + ring
            else: continue
            segs.pop(i); break
        else:
            raise SystemExit('meje ni mogoče sestaviti v en obroč')
    return ring


def inside(pt, ring):
    x, y = pt; c = False
    for (x1, y1), (x2, y2) in zip(ring, ring[1:] + ring[:1]):
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1: c = not c
    return c


def hav(a, b):
    p1, p2 = math.radians(a[1]), math.radians(b[1])
    d = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(math.radians(b[0] - a[0]) / 2) ** 2
    return 2 * 6371.0 * math.asin(math.sqrt(d))


def vrsta(name):
    return 'Gasilski dom ali vozilo' if 'gasil' in name.lower() else 'Druga lokacija'


def podatki():
    osm = json.loads((P / 'viri' / 'osm-crnomelj.json').read_text(encoding='utf-8'))['elements']
    rel = next(e for e in osm if e['type'] == 'relation')
    ring = stitch([[(p['lon'], p['lat']) for p in m['geometry']] for m in rel['members'] if m['type'] == 'way' and m.get('role') == 'outer'])
    ws = openpyxl.load_workbook(P / 'viri' / 'AEDs.xlsx', data_only=True).active
    aed = []
    for r in list(ws.iter_rows(values_only=True))[1:]:
        if not r[1]: continue
        lon, lat = float(r[1]), float(r[2])
        name = (r[3] or '').strip()
        name = name[4:].strip() if name.upper().startswith('AED ') else name
        aed.append({'ime': name, 'naslov': (r[4] or '').strip(), 'lon': lon, 'lat': lat, 'vObcini': inside((lon, lat), ring)})
    tag = lambda e, k: (e.get('tags') or {}).get(k)
    d = {'meja': ring,
         'ceste': [[(p['lon'], p['lat']) for p in e['geometry']] for e in osm if e['type'] == 'way' and tag(e, 'highway')],
         'reke': [[(p['lon'], p['lat']) for p in e['geometry']] for e in osm if e['type'] == 'way' and tag(e, 'waterway')],
         'naselja': [{'ime': e['tags'].get('name', ''), 'lon': e['lon'], 'lat': e['lat'], 'tip': e['tags']['place']} for e in osm if e['type'] == 'node'],
         'aed': aed, 'vir': 'AEDs.xlsx (naročnik, 2026-09-20); OpenStreetMap (ODbL): meja, ceste, reke, naselja'}
    (P / 'podatki/aed/aed.json').write_text(json.dumps(d, ensure_ascii=False), encoding='utf-8')
    with (P / 'podatki/aed/aed.csv').open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f, delimiter=';'); w.writerow(['ime', 'naslov', 'lon', 'lat', 'v_obcini_crnomelj'])
        for a in aed: w.writerow([a['ime'], a['naslov'], a['lon'], a['lat'], 'da' if a['vObcini'] else 'ne'])
    return d


def zgradi(d):
    ring, aed = d['meja'], d['aed']
    lo0 = min(x for x, _ in ring) - .015; lo1 = max(x for x, _ in ring) + .015
    la0 = min(y for _, y in ring) - .012; la1 = max(y for _, y in ring) + .012
    for a in aed:
        lo0 = min(lo0, a['lon'] - .01); lo1 = max(lo1, a['lon'] + .01); la0 = min(la0, a['lat'] - .01); la1 = max(la1, a['lat'] + .01)
    k = 2600; c = math.cos(math.radians((la0 + la1) / 2))
    W = round((lo1 - lo0) * c * k); H = round((la1 - la0) * k)
    X = lambda lon: round((lon - lo0) * c * k, 1); Y = lambda lat: round((la1 - lat) * k, 1)
    path = lambda pts: 'M' + 'L'.join(f'{X(x)} {Y(y)}' for x, y in pts)
    km5 = round(5 / (111.32 * c) * c * k)
    svg = f'<svg class="aed-svg" viewBox="0 0 {W} {H}" role="group" aria-label="Zemljevid defibrilatorjev v Občini Črnomelj in sosednjih občinah"><rect width="{W}" height="{H}" fill="#f7f8f2"/>'
    svg += f'<path class="mj" d="{path(ring)}Z" fill="#e4edce" stroke="#4a7a66" stroke-dasharray="7 4"/>'
    svg += ''.join(f'<path class="rd" d="{path(r)}" fill="none" stroke="#c9a56a" opacity=".85"/>' for r in d['ceste'])
    svg += ''.join(f'<path class="rv" d="{path(r)}" fill="none" stroke="#6a9ccf" opacity=".9"/>' for r in d['reke'])
    for n in d['naselja']:
        if n['ime'] in HALL or n['tip'] == 'town':
            svg += f'<text x="{X(n["lon"])}" y="{Y(n["lat"]) - 10}" class="pl" text-anchor="middle">{E(n["ime"])}</text>'
    for nm, lo, la in EXTRA:
        svg += f'<text x="{X(lo)}" y="{Y(la) - 16}" class="pl out" text-anchor="middle">{E(nm)}</text>'
    for i in sorted(range(len(aed)), key=lambda i: aed[i]['vObcini']):
        a = aed[i]; cls = 'in' if a['vObcini'] else 'out'
        t = E(a['ime']) + (' · ' + E(a['naslov']) if a['naslov'] else '')
        svg += f'<circle class="aed {cls}" data-i="{i}" cx="{X(a["lon"])}" cy="{Y(a["lat"])}" r="{7 if a["vObcini"] else 5.5}" tabindex="0" role="button" aria-label="{t}"><title>{t}</title></circle>'
    svg += f'<g transform="translate({W - km5 - 24} {H - 22})"><line class="sc" x1="0" x2="{km5}" y1="0" y2="0" stroke="#163632"/><text x="{km5 / 2}" y="-7" class="pl" text-anchor="middle">5 km</text></g></svg>'
    n_in = sum(a['vObcini'] for a in aed)
    gas_in = sum(a['vObcini'] and vrsta(a['ime']) == 'Gasilski dom ali vozilo' for a in aed)
    pts_in = [a for a in aed if a['vObcini']]
    kraji = [n for n in d['naselja'] if inside((n['lon'], n['lat']), ring)]
    dist = sorted((min(hav((n['lon'], n['lat']), (a['lon'], a['lat'])) for a in aed), n['ime']) for n in kraji)
    share = lambda t: round(100 * sum(1 for m, _ in dist if m <= t) / len(dist))
    far = sorted(dist, reverse=True)[:6]
    order = sorted(range(len(aed)), key=lambda i: (not aed[i]['vObcini'], aed[i]['ime']))
    rows = ''.join(f'<tr data-i="{i}" data-in="{1 if aed[i]["vObcini"] else 0}"><td>{E(aed[i]["ime"])}</td><td>{E(aed[i]["naslov"]) or "—"}</td><td>{vrsta(aed[i]["ime"])}</td><td>{"Občina Črnomelj" if aed[i]["vObcini"] else "Sosednja občina"}</td><td class="num">{aed[i]["lat"]:.5f}, {aed[i]["lon"]:.5f}</td></tr>' for i in order)
    stat = ('<div class="table-scroll"><table><thead><tr><th>Kazalnik</th><th>Vrednost</th><th>Pomen</th></tr></thead><tbody>'
            f'<tr><td>Defibrilatorji v datoteki</td><td>{len(aed)}</td><td>Datoteka zajema tudi sosednje občine (Metlika, Semič, Predgrad).</td></tr>'
            f'<tr><td>Znotraj meje Občine Črnomelj</td><td><b>{n_in}</b></td><td>Razvrščeno po meji občine iz OpenStreetMap, ne po naslovu.</td></tr>'
            f'<tr><td>Od tega v gasilskih domovih ali gasilskih vozilih</td><td>{gas_in} od {n_in}</td><td>Dostopnost izven delovnega časa je odvisna od gasilcev; datoteka je ne navaja.</td></tr>'
            f'<tr><td>Naselja (OSM) v občini z defibrilatorjem znotraj 1 / 3 / 5 km zračne črte</td><td>{share(1)} % / {share(3)} % / {share(5)} %</td><td>Od {len(dist)} naselij v občini, upoštevani so vsi defibrilatorji iz datoteke, tudi v sosednjih občinah; zračna razdalja, ne čas vožnje ali odzivnost reševalcev.</td></tr>'
            f'<tr><td>Naselja najdlje od najbližjega defibrilatorja</td><td>{"; ".join(f"{n} ({m:.1f} km)" for m, n in far)}</td><td>Kandidati za preverjanje potrebe, ne dokaz vrzeli.</td></tr>'
            '</tbody></table></div>')
    data = json.dumps([{'i': i, 'ime': a['ime'], 'naslov': a['naslov'], 'lat': a['lat'], 'lon': a['lon'], 'in': a['vObcini'], 'v': vrsta(a['ime'])} for i, a in enumerate(aed)], ensure_ascii=False).replace('</', '<\\/')
    out = f'''<section class="section" id="aed" data-title="Defibrilatorji na zemljevidu">
<h2>Lokacije defibrilatorjev (AED) in dostopnost</h2>
<p>Zemljevid prikazuje {len(aed)} lokacij avtomatskih zunanjih defibrilatorjev iz datoteke, ki jo je dodal naročnik poročila. Znotraj meje Občine Črnomelj jih je <b>{n_in}</b>; ostale so v sosednjih občinah in so prikazane zbledelo. Pri srčnem zastoju je odločilen čas do prvega defibrilatorja, zato ni pomembno le število naprav, ampak tudi to, ali so v resnici dosegljive.</p>
<div class="aed-tools"><label><input type="checkbox" id="aed-neighbours" checked> Pokaži sosednje občine ({len(aed) - n_in})</label><span class="aed-legend"><i class="dot in"></i> Občina Črnomelj <i class="dot out"></i> sosednje občine <i class="rv"></i> Kolpa <i class="rd"></i> glavne ceste</span></div>
<div class="aed-layout"><div class="aed-mapbox">{svg}<div class="aed-zoom" role="group" aria-label="Povečava zemljevida"><button type="button" data-z="in" aria-label="Približaj">+</button><button type="button" data-z="out" aria-label="Oddalji">−</button><button type="button" data-z="reset" aria-label="Celoten prikaz">⤢</button></div></div><aside class="aed-panel" id="aed-panel" aria-live="polite"><h3>Izberite točko na zemljevidu</h3><p class="subtle">Kliknite ali s tipko Enter izberite defibrilator. V središču Črnomlja so točke blizu skupaj: približajte z gumbom + ali z dvoklikom, premik z vlečenjem. Podrobnosti so tudi v tabeli spodaj.</p></aside></div>
<p class="subtle">Meja občine, Kolpa, glavne ceste in naselja: OpenStreetMap (ODbL), lokalna kopija viri/osm-crnomelj.json. Lokacije defibrilatorjev: viri/AEDs.xlsx. Zemljevid deluje brez omrežja.</p>
<h3>Kako dobra je pokritost?</h3>
{stat}
<div class="callout"><b>Omejitve.</b> Podatkov ta pregled ni preveril na terenu: datoteka ne navaja delovanja naprave, datuma servisa, ur dostopa ali kdo ima ključ. Pri nekaterih vnosih je lokacija zasebna hiša, podjetje ali gasilsko vozilo, zato prebivalec zunaj delovnega časa morda ne more do naprave. Razdalje so zračne in ne upoštevajo terena ali cest. Ob srčnem zastoju najprej pokličite 112; reševalec lahko usmeri do najbližjega defibrilatorja.</div>
<details><summary>Seznam vseh {len(aed)} lokacij (iskanje in prenos)</summary>
<div class="aed-filter"><label>Iskanje<input type="search" id="aed-search" placeholder="Npr. Vinica, šola, gasilski"></label> <a class="btn" href="podatki/aed/aed.csv" download>Prenesi CSV</a></div>
<div class="table-scroll"><table id="aed-table"><thead><tr><th>Lokacija</th><th>Naslov</th><th>Vrsta</th><th>Občina</th><th>Koordinate</th></tr></thead><tbody>{rows}</tbody></table></div></details>
<script type="application/json" id="aed-data">{data}</script>
<script>{JS}</script>
</section>'''
    (P / 'vsebina/aed.html').write_text(out, encoding='utf-8')
    print('skupaj', len(aed), '| v občini', n_in, '| gasilski', gas_in, '| naselij', len(dist), '| pokritost 1/3/5 km', share(1), share(3), share(5), '| najdlje', far[:3])


JS = """(()=>{const d=JSON.parse(document.getElementById('aed-data').textContent),panel=document.getElementById('aed-panel'),svg=document.querySelector('.aed-svg'),rows=[...document.querySelectorAll('#aed-table tbody tr')];
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
function pick(i){const a=d[i];svg.querySelectorAll('.aed.sel').forEach(c=>c.classList.remove('sel'));svg.querySelector('.aed[data-i="'+i+'"]')?.classList.add('sel');rows.forEach(r=>r.classList.toggle('sel',+r.dataset.i===i));
panel.innerHTML='<h3>'+esc(a.ime)+'</h3><p>'+(a.naslov?esc(a.naslov)+'<br>':'')+'<span class="subtle">'+esc(a.v)+' · '+(a.in?'Občina Črnomelj':'sosednja občina')+'</span></p><p class="num">'+a.lat.toFixed(5)+', '+a.lon.toFixed(5)+'</p><a href="https://www.openstreetmap.org/?mlat='+a.lat+'&mlon='+a.lon+'#map=17/'+a.lat+'/'+a.lon+'" rel="noopener">Odpri v OpenStreetMap ↗</a>';}
svg.addEventListener('click',e=>{const c=e.target.closest('.aed');if(c)pick(+c.dataset.i);});
svg.addEventListener('keydown',e=>{if((e.key==='Enter'||e.key===' ')&&e.target.classList&&e.target.classList.contains('aed')){e.preventDefault();pick(+e.target.dataset.i);}});
const nb=document.getElementById('aed-neighbours'),q=document.getElementById('aed-search');
const norm=s=>s.normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').toLowerCase();
function apply(){const show=nb.checked;svg.querySelectorAll('.aed.out').forEach(c=>c.style.display=show?'':'none');const t=norm(q.value);rows.forEach(r=>{const out=r.dataset.in==='0';r.hidden=(!show&&out)||(t&&!norm(r.textContent).includes(t));});}
nb.addEventListener('change',apply);q.addEventListener('input',apply);
const vb0=svg.viewBox.baseVal,W=vb0.width,H=vb0.height;let v={x:0,y:0,w:W,h:H};
function draw(){const s=v.w/W;svg.setAttribute('viewBox',v.x+' '+v.y+' '+v.w+' '+v.h);svg.querySelectorAll('.aed').forEach(c=>c.setAttribute('r',(c.classList.contains('in')?7:5.5)*Math.max(s,.12)));svg.querySelectorAll('.pl').forEach(t=>t.style.fontSize=(13*Math.max(s,.2))+'px');svg.style.setProperty('--sw',Math.max(s,.2));}
function zoom(f,cx,cy){const nw=Math.min(W,Math.max(W/40,v.w*f)),nh=nw*H/W;cx=cx??v.x+v.w/2;cy=cy??v.y+v.h/2;v={x:cx-(cx-v.x)*nw/v.w,y:cy-(cy-v.y)*nh/v.h,w:nw,h:nh};clamp();draw();}
function clamp(){v.x=Math.min(Math.max(v.x,0),W-v.w);v.y=Math.min(Math.max(v.y,0),H-v.h);}
function pt(e){const r=svg.getBoundingClientRect();return[v.x+(e.clientX-r.left)/r.width*v.w,v.y+(e.clientY-r.top)/r.height*v.h];}
document.querySelector('.aed-zoom').addEventListener('click',e=>{const z=e.target.dataset.z;if(z==='in')zoom(.5);else if(z==='out')zoom(2);else if(z==='reset'){v={x:0,y:0,w:W,h:H};draw();}});
svg.addEventListener('dblclick',e=>{const[x,y]=pt(e);zoom(.4,x,y);});
let drag=null,moved=false;svg.addEventListener('pointerdown',e=>{drag={x:e.clientX,y:e.clientY,vx:v.x,vy:v.y};moved=false;});
window.addEventListener('pointermove',e=>{if(!drag)return;const r=svg.getBoundingClientRect(),dx=e.clientX-drag.x,dy=e.clientY-drag.y;if(Math.abs(dx)+Math.abs(dy)>4)moved=true;if(moved){v.x=drag.vx-dx/r.width*v.w;v.y=drag.vy-dy/r.height*v.h;clamp();draw();}});
window.addEventListener('pointerup',()=>{drag=null;});svg.addEventListener('click',e=>{if(moved){e.stopImmediatePropagation();moved=false;}},true);
const cx=i=>+svg.querySelector('.aed[data-i="'+i+'"]').getAttribute('cx'),cy=i=>+svg.querySelector('.aed[data-i="'+i+'"]').getAttribute('cy');
window.__aedFocus=i=>{v.w=W/8;v.h=H/8;v.x=cx(i)-v.w/2;v.y=cy(i)-v.h/2;clamp();draw();pick(i);};
rows.forEach(r=>r.addEventListener('click',()=>window.__aedFocus(+r.dataset.i)));})();"""

if __name__ == '__main__':
    zgradi(podatki())
