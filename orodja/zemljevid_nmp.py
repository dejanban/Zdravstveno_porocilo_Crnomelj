"""Interaktivni zemljevid dostopnosti ZD Črnomelj (SVG brez zunanjih zahtev).

Vhodi: viri/teme-2026-09-25/osrm-poti.json (orodja/zajemi_poti_nmp.py), meja/ceste/reke OSM iz
arhiv/izvirnik-0dc0bd4/podatki/aed/aed.json, prebivalci SURS 2026 iz podatki/teme/dostopnost-naselij.csv.
Ocena reševalcev (PREDPOSTAVKE, enake kot v orodja/analiziraj_dostopnost_nmp.py):
  nujna vožnja = 0,8 × modelski čas vožnje ZD -> naselje,
  dostopni čas NMP = 1 min obdelava klica + 1 min izvoz + nujna vožnja (razpon zgoraj: 1,5 + 1 + 1,0 × vožnja).
Barvna lestvica: divergentna, temno zelena (hitro) -> siva pri 15 min (cilj povprečnega dostopnega časa po
pravilniku NMP) -> temno rdeča (počasi, 40 min in več).
"""
from pathlib import Path
import csv, html, json, math

ROOT = Path(__file__).resolve().parents[1]
STOPS = [(0, (15, 92, 58)), (7.5, (96, 158, 120)), (15, (189, 184, 174)), (25, (210, 122, 92)), (40, (142, 27, 27))]
KLIC, IZVOZ, NUJNA = 1.0, 1.0, 0.8
KLIC_Z, FAKTOR_Z = 1.5, 1.0


def barva(t):
    t = max(0, min(40, t))
    for (a, ca), (b, cb) in zip(STOPS, STOPS[1:]):
        if t <= b:
            f = (t - a) / (b - a)
            return '#%02x%02x%02x' % tuple(round(x + (y - x) * f) for x, y in zip(ca, cb))
    return '#%02x%02x%02x' % STOPS[-1][1]


def okl_l(hexc):
    r, g, b = [int(hexc[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    lin = [c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4 for c in (r, g, b)]
    l = .4122214708 * lin[0] + .5363325363 * lin[1] + .0514459929 * lin[2]
    m = .2119034982 * lin[0] + .6806995451 * lin[1] + .1073969566 * lin[2]
    s = .0883024619 * lin[0] + .2817188376 * lin[1] + .6299787005 * lin[2]
    return .2104542553 * l ** (1 / 3) + .7936177850 * m ** (1 / 3) - .0040720468 * s ** (1 / 3)


def fmt(x, d=1):
    return f'{x:.{d}f}'.replace('.', ',')


def build():
    # Lestvica mora biti svetlostno monotona od obeh koncev proti sredini (berljivo tudi pri barvni slepoti).
    Ls = [okl_l(barva(t)) for t in (0, 5, 10, 15, 20, 30, 40)]
    assert Ls[0] < Ls[1] < Ls[2] < Ls[3] and Ls[3] > Ls[4] > Ls[5] > Ls[6], Ls
    osrm = json.loads((ROOT / 'viri/teme-2026-09-25/osrm-poti.json').read_text(encoding='utf-8'))
    osm = json.loads((ROOT / 'arhiv/izvirnik-0dc0bd4/podatki/aed/aed.json').read_text(encoding='utf-8'))
    preb = {r['naselje']: r for r in csv.DictReader((ROOT / 'podatki/teme/dostopnost-naselij.csv').open(encoding='utf-8-sig'))}
    meja = osm['meja']
    lon0 = sum(p[0] for p in meja) / len(meja); lat0 = sum(p[1] for p in meja) / len(meja)
    kx = math.cos(math.radians(lat0))
    okvir = meja + [c for n in osrm['naselja'] for c in n['geometrija']]  # tudi poti, ki gredo čez mejo
    xs = [(p[0] - lon0) * kx for p in okvir]; ys = [(lat0 - p[1]) for p in okvir]
    W = 900; pad = 16
    sc = (W - 2 * pad) / (max(xs) - min(xs)); H = round((max(ys) - min(ys)) * sc + 2 * pad)
    minx, miny = min(xs), min(ys)

    def P(lon, lat):
        return ((lon - lon0) * kx - minx) * sc + pad, ((lat0 - lat) - miny) * sc + pad

    def path(coords, step=1):
        pts = [P(*c) for c in coords[::step]] + ([P(*coords[-1])] if step > 1 else [])
        return 'M' + 'L'.join(f'{x:.1f} {y:.1f}' for x, y in pts)

    svg = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-labelledby="zemljevid-nmp-title zemljevid-nmp-desc" class="nmp-map">',
           '<title id="zemljevid-nmp-title">Čas do ZD Črnomelj in ocenjeni čas nujne pomoči po naseljih</title>',
           '<desc id="zemljevid-nmp-desc">Zemljevid Občine Črnomelj s 111 naselji in cestnimi potmi od zdravstvenega doma. Barva kaže ocenjeni čas: temno zelena najhitreje, siva okoli 15 minut, temno rdeča najpočasneje. Vse vrednosti so tudi v preglednici pod zemljevidom.</desc>',
           f'<path d="{path(meja)}Z" class="nmp-meja"/>']
    for c in osm['reke']:
        svg.append(f'<path d="{path(c)}" class="nmp-reka"/>')
    for c in osm['ceste']:
        svg.append(f'<path d="{path(c)}" class="nmp-cesta"/>')
    # Časi: z umerjanjem na Google (orodja/kalibracija_casov.py) ali, dokler ga ni, razpon OSRM–Valhalla.
    import kalibracija_casov as K
    modeli = K.modeli()
    kal = json.loads(K.REZ.read_text(encoding='utf-8')) if K.REZ.exists() else {}
    umerjeno = bool(kal.get('uporabljeno'))
    casi = {}
    for n in osrm['naselja']:
        mm = modeli[n['ime']]
        if umerjeno:
            pr = K.umerjen_cas(n['ime'], 'prebivalec')[0]; nb = K.umerjen_cas(n['ime'], 'nmp')[0]
            casi[n['ime']] = dict(pr=pr, pr_lo=pr, pr_hi=pr, nb=nb, nb_lo=nb, nb_hi=nb)
        else:
            prs = [mm['osrm_min'], mm['valhalla_min'] or mm['osrm_min']]; nbs = [mm['osrm_nmp_min'], mm['valhalla_nmp_min'] or mm['osrm_nmp_min']]
            casi[n['ime']] = dict(pr=sum(prs) / 2, pr_lo=min(prs), pr_hi=max(prs), nb=sum(nbs) / 2, nb_lo=min(nbs), nb_hi=max(nbs))
    # Barve cest: kumulativni čas OSRM, preračunan na osrednjo oceno z enim skupnim razmerjem.
    razmerje = sum(c['nb'] for c in casi.values()) / sum(n['zd_naselje_s'] / 60 for n in osrm['naselja'])
    # Obarvane poti: vsak odsek enkrat (prvi prihod), razdeljeno na polilinije po polminutnih razredih.
    seen = set(); segs = []
    for n in osrm['naselja']:
        g = n['geometrija']; cum = 0.0; cur = None
        for (a, b, d) in zip(g, g[1:], n['odseki_s']):
            t_mid = razmerje * (cum + d / 2) / 60; cum += d
            key = (tuple(a), tuple(b)); rkey = (tuple(b), tuple(a))
            if key in seen or rkey in seen or a == b:
                cur = None; continue
            seen.add(key)
            razred = round(t_mid * 2) / 2
            if cur and cur['razred'] == razred and cur['pts'][-1] == a:
                cur['pts'].append(b)
            else:
                cur = {'razred': razred, 'pts': [a, b]}; segs.append(cur)
    segs.sort(key=lambda s: -s['razred'])
    for s in segs:
        t = s['razred']
        svg.append(f'<path d="{path(s["pts"])}" class="nmp-pot" data-t="{t}" stroke="{barva(KLIC + IZVOZ + NUJNA * t)}"/>')
    # Poudarjene poti posameznih naselij (skrite, prikaz ob izbiri).
    rows = []
    for i, n in enumerate(osrm['naselja']):
        c = casi[n['ime']]; mm = modeli[n['ime']]
        r = preb.get(n['ime'], {})
        pop = int(r['prebivalci_2026']) if r.get('prebivalci_2026') else None
        p65 = int(r['prebivalci_65_2026']) if r.get('prebivalci_65_2026') else None
        km = [round(mm['osrm_km'], 1), round(mm['valhalla_km'] or mm['osrm_km'], 1)]
        rows.append({'i': i, 'ime': n['ime'], 'pop': pop, 'p65': p65,
                     'pr_min': round(c['pr'], 1), 'pr_lo': round(c['pr_lo'], 1), 'pr_hi': round(c['pr_hi'], 1),
                     'pr_km': km[0], 'km_razlika': (not umerjeno) and abs(km[0] - km[1]) > 0.15 * max(km),
                     'nujna_lo': round(NUJNA * c['nb_lo'], 1), 'nujna_hi': round(NUJNA * c['nb_hi'], 1),
                     'nujna_min': round(NUJNA * c['nb'], 1),
                     'nmp_min': round(KLIC + IZVOZ + NUJNA * c['nb'], 1), 'nmp_lo': round(KLIC + IZVOZ + NUJNA * c['nb_lo'], 1),
                     'nmp_zg': round(KLIC_Z + IZVOZ + FAKTOR_Z * c['nb_hi'], 1),
                     'lon': n['lon'], 'lat': n['lat']})
        svg.append(f'<path d="{path(n["geometrija"], 3)}" class="nmp-hl" id="nmp-hl-{i}"/>')
    # Naselja: velikost po prebivalcih, barva po oceni NMP, bel obroč.
    for r in sorted(rows, key=lambda r: -(r['pop'] or 0)):
        x, y = P(r['lon'], r['lat'])
        rad = 4 if not r['pop'] else 3.5 + 8.5 * math.sqrt(r['pop'] / 5432)  # ploščina ~ prebivalci; Črnomelj = 12
        status = 'pod 15 min' if r['nmp_min'] <= 15 else 'nad 15 min'
        label = (f"{r['ime']}: vožnja prebivalca do ZD {fmt(r['pr_lo'])}–{fmt(r['pr_hi'])} min; ocenjeni dostopni čas nujne pomoči "
                 f"{fmt(r['nmp_lo'])}–{fmt(r['nmp_zg'])} min, osrednja ocena {status}")
        svg.append(f'<g class="nmp-naselje" tabindex="0" data-i="{r["i"]}" aria-label="{html.escape(label, quote=True)}">'
                   f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rad + 6:.1f}" class="nmp-hit"/>'
                   f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rad:.1f}" fill="{barva(r["nmp_min"])}" data-nmp="{r["nmp_min"]}" data-pr="{r["pr_min"]}" class="nmp-pika"/>'
                   f'<title>{html.escape(label)}</title></g>')
    for ime in ['Vinica', 'Dragatuš', 'Stari trg ob Kolpi', 'Adlešiči', 'Griblje', 'Tribuče', 'Preloka', 'Sinji Vrh']:
        r = next((r for r in rows if r['ime'] == ime), None)
        if r:
            x, y = P(r['lon'], r['lat'])
            svg.append(f'<text x="{x + 9:.1f}" y="{y - 8:.1f}" class="nmp-label">{html.escape(ime)}</text>')
    zx, zy = P(osrm['izhodisce']['lon'], osrm['izhodisce']['lat'])
    svg.append(f'<g class="nmp-zd" aria-label="Zdravstveni dom Črnomelj, izhodišče nujne medicinske pomoči"><rect x="{zx - 10:.1f}" y="{zy - 10:.1f}" width="20" height="20" rx="4"/>'
               f'<path d="M{zx - 5:.1f} {zy:.1f}H{zx + 5:.1f}M{zx:.1f} {zy - 5:.1f}V{zy + 5:.1f}"/><title>Zdravstveni dom Črnomelj, Delavska pot 4</title></g>'
               f'<text x="{zx + 14:.1f}" y="{zy + 22:.1f}" class="nmp-label nmp-label-zd">ZD Črnomelj</text>')
    svg.append('</svg>')
    data = [{k: r[k] for k in ('ime', 'pop', 'p65', 'pr_min', 'pr_lo', 'pr_hi', 'pr_km', 'km_razlika', 'nujna_lo', 'nujna_hi', 'nmp_min', 'nmp_lo', 'nmp_zg')} for r in rows]
    vir_casov = (f"umerjeno na čase Google Maps za {kal['izpolnjeno']} naselij (model {kal['model'].upper()}, povprečna napaka ±{fmt(kal['modeli'][kal['model']]['mae_cv_min'])} min)"
                 if umerjeno else 'razpon dveh odprtokodnih modelov (OSRM in Valhalla), še neumerjeno na Google Maps')
    # CSV za prenos.
    with (ROOT / 'podatki/teme/zemljevid-dostopnost.csv').open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(['naselje', 'prebivalci_2026', 'prebivalci_65_2026', 'voznja_prebivalca_min_spodaj', 'voznja_prebivalca_min_zgoraj', 'razdalja_km_OSRM', 'modela_izbereta_razlicni_poti', 'nujna_voznja_min_spodaj', 'nujna_voznja_min_zgoraj', 'dostopni_cas_NMP_min_spodaj', 'dostopni_cas_NMP_osrednja', 'dostopni_cas_NMP_min_zgoraj', 'vir_casov'])
        for r in sorted(data, key=lambda r: r['nmp_min']):
            w.writerow([r['ime'], r['pop'], r['p65'], r['pr_lo'], r['pr_hi'], r['pr_km'], 'da' if r['km_razlika'] else 'ne', r['nujna_lo'], r['nujna_hi'], r['nmp_lo'], r['nmp_min'], r['nmp_zg'], vir_casov])
    grad = ','.join(f'{barva(t)} {t / 40 * 100:.0f}%' for t in range(0, 41, 5))
    ticks = ''.join(f'<span style="left:{t / 40 * 100:.1f}%">{t if t < 40 else "40+"}</span>' for t in (0, 5, 10, 15, 20, 30, 40))
    tabela = ''.join(f'<tr><td>{html.escape(r["ime"])}</td><td>{r["pop"] if r["pop"] is not None else "ni podatka"}</td><td>{fmt(r["pr_lo"])}–{fmt(r["pr_hi"])}</td><td>{fmt(r["nujna_lo"])}–{fmt(r["nujna_hi"])}</td><td>{fmt(r["nmp_lo"])}–{fmt(r["nmp_zg"])}</td></tr>'
                     for r in sorted(data, key=lambda r: r['nmp_min']))
    nad15 = sum(r['pop'] or 0 for r in data if r['nmp_min'] > 15); vsi = sum(r['pop'] or 0 for r in data)
    body = f'''<p class="no-print">Premaknite miško nad naselje ali ga izberite s tipkovnico (tabulator). Prikaže se čas vožnje prebivalca do zdravstvenega doma in ocenjeni čas, v katerem pride ekipa nujne medicinske pomoči. Poudari se tudi pot, po kateri bi vozila. Barva cest pove, koliko časa ekipa potrebuje do tiste točke.</p>
<div class="nmp-controls" role="group" aria-label="Barva zemljevida"><button type="button" data-nmp-mode="nmp" aria-pressed="true">Ocena nujne pomoči</button><button type="button" data-nmp-mode="pr" aria-pressed="false">Vožnja prebivalca do ZD</button></div>
<figure class="nmp-figure"><div class="nmp-wrap">{''.join(svg)}<div class="nmp-tip" role="status" hidden></div></div>
<div class="nmp-legend" aria-hidden="true"><div class="nmp-legend-title">Minute (<span data-nmp-legend>ocenjeni dostopni čas nujne pomoči</span>)</div><div class="nmp-bar" style="background:linear-gradient(90deg,{grad})"><i style="left:37.5%"></i></div><div class="nmp-ticks">{ticks}</div><div class="nmp-legend-note">Siva ≈ 15 minut: cilj povprečnega dostopnega časa po pravilniku NMP. Pika = naselje (velikost po številu prebivalcev), kvadrat = ZD Črnomelj.</div></div>
<figcaption><b>Vir časov: {vir_casov}.</b> Po osrednji oceni ima {fmt(100 * nad15 / vsi)} % prebivalcev povezanih naselij dostopni čas nad 15 minut. Oba modela računata z isto cestno mrežo OpenStreetMap, a z različnimi hitrostmi, zato se razlikujeta. Primer so Griblje: OSRM izbere enopasovno lokalno cesto z vpisano omejitvijo 90 km/h (10 min), Valhalla pa drugo pot (22 min). Primerjava z Google Maps je pokazala, da se modela od njega razlikujeta. Zato vozne čase umerjamo na Googlove vrednosti za izbrana naselja (predloga <a href="podatki/teme/kalibracija-google.csv">kalibracija-google.csv</a>). Vožnja prebivalca je čas običajne vožnje od naselja do ZD. Nujna vožnja reševalcev je <b>predpostavka</b>: 0,8 × modelski čas, ker se vozilo z modrimi lučmi ne drži omejitev. Ocenjeni dostopni čas prišteje 1 minuto obdelave klica in 1 minuto izvoza (pravilnik dovoljuje največ 1 minuto). Zgornja meja razpona je 1,5 + 1 minuti in vožnja brez pospeška. To ni izmerjeni dostopni čas: model ne pozna zasedenosti ekipe, vremena in iskanja naslova, točka naselja pa je ena koordinata. <a class="citation" href="#tema-osrm-poti">[vir]</a><a class="citation" href="#tema-valhalla-casi">[vir]</a><a class="citation" href="#tema-surs-naselja-2026">[vir]</a><a class="citation" href="#tema-pravilnik-nmp-2026">[vir]</a> <a href="podatki/teme/zemljevid-dostopnost.csv" download>Prenesi podatke (CSV)</a>.</figcaption></figure>
<details class="content-layer"><summary>Preglednica: vsa naselja, razvrščena po oceni nujne pomoči</summary><div class="table-scroll"><table><thead><tr><th>Naselje</th><th>Prebivalci 2026</th><th>Vožnja prebivalca do ZD (min)</th><th>Nujna vožnja reševalcev, ocena (min)</th><th>Dostopni čas NMP, ocena (min)</th></tr></thead><tbody>{tabela}</tbody></table></div></details>
<script type="application/json" id="nmp-data">{json.dumps(data, ensure_ascii=False)}</script>
<script type="application/json" id="nmp-scale">{json.dumps(STOPS)}</script>'''
    return body


CSS = '''
.nmp-controls{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0}.nmp-controls button{border:1px solid #9fb0bf;background:#fff;border-radius:999px;padding:7px 14px;font:inherit;cursor:pointer;color:#19334b}.nmp-controls button[aria-pressed=true]{background:#19334b;color:#fff;border-color:#19334b}
.nmp-figure{margin:0}.nmp-wrap{position:relative;border:1px solid var(--line,#d6dde2);border-radius:12px;background:#fbfaf7;overflow:hidden}
.nmp-map{display:block;width:100%;height:auto}.nmp-meja{fill:#f1eee6;stroke:#8b8173;stroke-width:1.5}.nmp-reka{fill:none;stroke:#8fb3cc;stroke-width:1.4}.nmp-cesta{fill:none;stroke:#d9d4ca;stroke-width:1}
.nmp-pot{fill:none;stroke-width:2.4;stroke-linecap:round;stroke-linejoin:round}.nmp-hl{fill:none;stroke:#10212f;stroke-width:4.5;stroke-linecap:round;stroke-linejoin:round;opacity:0;pointer-events:none}.nmp-hl.on{opacity:.85}
.nmp-naselje{cursor:pointer;outline:none}.nmp-hit{fill:transparent}.nmp-pika{stroke:#fff;stroke-width:2}.nmp-naselje:hover .nmp-pika,.nmp-naselje:focus .nmp-pika{stroke:#10212f;stroke-width:2.5}
.nmp-zd rect{fill:#19334b;stroke:#fff;stroke-width:2}.nmp-zd path{stroke:#fff;stroke-width:2.4}.nmp-label{font-size:12px;fill:#2b3d4d;paint-order:stroke;stroke:#fbfaf7;stroke-width:3px}.nmp-label-zd{font-weight:700;font-size:13px}
.nmp-tip{position:absolute;z-index:3;min-width:220px;max-width:280px;background:#fff;border:1px solid #c9d2da;border-radius:10px;box-shadow:0 6px 18px #10212f22;padding:10px 12px;font-size:13.5px;line-height:1.45;color:#19334b;pointer-events:none}
.nmp-tip b{display:block;font-size:14.5px;margin-bottom:4px}.nmp-tip .row{display:flex;justify-content:space-between;gap:12px}.nmp-tip .row span:last-child{font-weight:700;white-space:nowrap}.nmp-tip .sw{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px;vertical-align:middle}.nmp-tip small{display:block;color:#526270;margin-top:5px}
.nmp-legend{margin:12px 2px 6px;max-width:560px}.nmp-legend-title{font-size:13px;color:#445669;margin-bottom:6px}.nmp-bar{position:relative;height:12px;border-radius:6px}.nmp-bar i{position:absolute;top:-4px;bottom:-4px;width:2px;background:#10212f}.nmp-ticks{position:relative;height:18px;font-size:12px;color:#445669}.nmp-ticks span{position:absolute;transform:translateX(-50%);top:3px}.nmp-legend-note{font-size:12.5px;color:#526270;margin-top:4px}
@media print{.nmp-controls,.nmp-tip{display:none!important}.nmp-hl{display:none}}
'''

JS = r'''(()=>{const wrap=document.querySelector('.nmp-wrap');if(!wrap)return;
const data=JSON.parse(document.getElementById('nmp-data').textContent),stops=JSON.parse(document.getElementById('nmp-scale').textContent);
const tip=wrap.querySelector('.nmp-tip');let mode='nmp';
const col=t=>{t=Math.max(0,Math.min(40,t));for(let k=1;k<stops.length;k++){const[a,ca]=stops[k-1],[b,cb]=stops[k];if(t<=b){const f=(t-a)/(b-a);return'rgb('+ca.map((x,i)=>Math.round(x+(cb[i]-x)*f)).join(',')+')';}}return'rgb('+stops[stops.length-1][1].join(',')+')';};
const f1=x=>x.toFixed(1).replace('.',','),rg=(a,b)=>Math.abs(a-b)<0.05?f1(a):f1(a)+'–'+f1(b);
function show(g,ev){const r=data[+g.dataset.i];const hl=document.getElementById('nmp-hl-'+g.dataset.i);wrap.querySelectorAll('.nmp-hl.on').forEach(e=>e.classList.remove('on'));hl&&hl.classList.add('on');
tip.innerHTML='<b>'+r.ime+'</b>'+(r.pop!=null?'<div class="row"><span>Prebivalci (65+)</span><span>'+r.pop+' ('+r.p65+')</span></div>':'')+
'<div class="row"><span><i class="sw" style="background:'+col(r.pr_min)+'"></i>Vožnja prebivalca do ZD</span><span>'+rg(r.pr_lo,r.pr_hi)+' min</span></div>'+
'<div class="row"><span>Nujna vožnja reševalcev</span><span>≈ '+rg(r.nujna_lo,r.nujna_hi)+' min</span></div>'+
'<div class="row"><span><i class="sw" style="background:'+col(r.nmp_min)+'"></i>Dostopni čas NMP</span><span>'+f1(r.nmp_lo)+'–'+f1(r.nmp_zg)+' min</span></div>'+
'<small>'+(r.nmp_min<=15?'✓ Osrednja ocena je znotraj 15 minut.':'⚠ Osrednja ocena presega 15 minut.')+' Razdalja po cesti '+f1(r.pr_km)+' km.'+(r.km_razlika?' Modela izbereta različni poti, zato je razpon širok.':'')+' Modelska ocena, ne meritev.</small>';
tip.hidden=false;const box=wrap.getBoundingClientRect();let x,y;if(ev&&ev.clientX!=null){x=ev.clientX-box.left;y=ev.clientY-box.top;}else{const c=g.querySelector('.nmp-pika').getBoundingClientRect();x=c.left-box.left+c.width/2;y=c.top-box.top+c.height/2;}
const w=tip.offsetWidth,h=tip.offsetHeight;tip.style.left=Math.max(6,Math.min(box.width-w-6,x+14))+'px';tip.style.top=(y-h-14>6?y-h-14:Math.min(box.height-h-6,y+16))+'px';}
function hide(){tip.hidden=true;wrap.querySelectorAll('.nmp-hl.on').forEach(e=>e.classList.remove('on'));}
wrap.querySelectorAll('.nmp-naselje').forEach(g=>{g.addEventListener('pointermove',e=>show(g,e));g.addEventListener('pointerleave',hide);g.addEventListener('focus',()=>show(g));g.addEventListener('blur',hide);g.addEventListener('keydown',e=>{if(e.key==='Escape'){hide();g.blur();}});});
document.querySelectorAll('[data-nmp-mode]').forEach(b=>b.addEventListener('click',()=>{mode=b.dataset.nmpMode;document.querySelectorAll('[data-nmp-mode]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));
wrap.querySelectorAll('.nmp-pot').forEach(p=>{const t=+p.dataset.t;p.setAttribute('stroke',col(mode==='nmp'?2+0.8*t:t));});
wrap.querySelectorAll('.nmp-pika').forEach(c=>c.setAttribute('fill',col(+(mode==='nmp'?c.dataset.nmp:c.dataset.pr))));
const lg=document.querySelector('[data-nmp-legend]');if(lg)lg.textContent=mode==='nmp'?'ocenjeni dostopni čas nujne pomoči':'vožnja prebivalca do ZD';}));})();'''
