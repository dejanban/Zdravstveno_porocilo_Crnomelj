"""Dostopnost naselij do NMP: modelski scenariji dostopnega časa.

Vhodi: točke naselij OSM (arhiv/izvirnik-0dc0bd4/podatki/poti/poti-podatki.json, zajem 20. 9. 2026),
prebivalstvo po naseljih SURS 05C5003S za 2026 (viri/teme-2026-09-25/surs-05C5003S-crnomelj-2026.json),
AED iz podatki/aed/aed.json in modelski časi vožnje OSRM (viri/teme-2026-09-25/osrm-tabela.json).
Z --osvezi se tabela OSRM ponovno pridobi z javnega strežnika (potrebno omrežje).

Dostopni čas po pravilniku (Uradni list RS 666/2026) teče od dviga slušalke v dispečerski službi do prihoda
ekipe. Model ga ocenjuje kot: obdelava klica (PREDPOSTAVKA 1–2 min) + izvoz (največ 1 min po 7. členu) +
vožnja OSRM × faktor (PREDPOSTAVKA 0,8 = hitrejša nujna vožnja, 1,0 = običajna vožnja, 1,2 = slabše razmere).
Scenarij B predpostavlja, da je ekipa ZD Črnomelj zasedena in pride najbližja druga ekipa (ZD Metlika ali
UC Novo mesto). Model ne pozna dejanske zasedenosti ekip, vremena, pešpoti do bolnika ali iskanja naslova.
Izhodi: podatki/teme/dostopnost-naselij.csv in dostopnost-naselij.json.
"""
from pathlib import Path
import csv, json, math, sys, urllib.request

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'viri/teme-2026-09-25'
TOCKE = {'ZD Črnomelj': (15.1875308, 45.5754632), 'SB Novo mesto (UC)': (15.1638289, 45.7999676),
         'ZD Metlika': (15.3180735, 45.6484141)}
PASOVI = [(0, 10), (10, 15), (15, 20), (20, 30), (30, 999)]
SCENARIJI = {  # (izhodišča, obdelava klica min, izvoz min, faktor vožnje)
    'A_srednji': (['ZD Črnomelj'], 1.5, 1.0, 1.0),
    'A_hitra_voznja': (['ZD Črnomelj'], 1.0, 1.0, 0.8),
    'A_pocasna_voznja': (['ZD Črnomelj'], 2.0, 1.0, 1.2),
    'B_druga_ekipa': (['ZD Metlika', 'SB Novo mesto (UC)'], 1.5, 1.0, 1.0),
}


def haversine(a, b):
    lon1, lat1, lon2, lat2 = map(math.radians, (*a, *b))
    h = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    return 2 * 6371.0088 * math.asin(math.sqrt(h))


def nalozi_surs():
    d = json.loads((SRC / 'surs-05C5003S-crnomelj-2026.json').read_text(encoding='utf-8-sig'))
    dim = d['dimension']
    kraji = dim['OBČINA/NASELJE']['category']
    meritve = list(dim['MERITVE']['category']['index'])
    n_m = len(meritve)
    out = {}
    for code, i in kraji['index'].items():
        vals = dict(zip(meritve, d['value'][i * n_m:(i + 1) * n_m]))
        out[code] = {'ime': kraji['label'][code].split(' ', 1)[1], 'skupaj': vals['0'] or 0, '65+': vals['65_'] or 0}
    return out


def main():
    naselja = json.loads((ROOT / 'arhiv/izvirnik-0dc0bd4/podatki/poti/poti-podatki.json').read_text(encoding='utf-8'))['naselja']
    imena = list(TOCKE)
    osrm_path = SRC / 'osrm-tabela.json'
    if '--osvezi' in sys.argv or not osrm_path.exists():
        pts = list(TOCKE.values()) + [(n['lon'], n['lat']) for n in naselja]
        url = ('https://router.project-osrm.org/table/v1/driving/' + ';'.join(f'{x:.6f},{y:.6f}' for x, y in pts)
               + '?sources=' + ';'.join(str(i) for i in range(len(TOCKE))) + '&annotations=duration,distance')
        req = urllib.request.Request(url, headers={'User-Agent': 'zdravje-crnomelj-raziskava/1.0'})
        osrm_path.write_bytes(urllib.request.urlopen(req, timeout=60).read())
    osrm = json.loads(osrm_path.read_text(encoding='utf-8'))
    assert osrm['code'] == 'Ok' and len(osrm['durations']) == len(TOCKE), 'Tabela OSRM ne ustreza izhodiščem; zaženi z --osvezi.'
    surs = nalozi_surs()
    po_imenu = {v['ime']: v for k, v in surs.items() if len(k) == 6}
    aed = [(r['lon'], r['lat']) for r in json.loads((ROOT / 'podatki/aed/aed.json').read_text(encoding='utf-8')) if r.get('in')]
    off = len(TOCKE)
    rows = []
    for j, n in enumerate(naselja, start=off):
        p = (n['lon'], n['lat'])
        s = po_imenu.get(n['ime'])
        voz = {ime: osrm['durations'][k][j] / 60 for k, ime in enumerate(imena) if osrm['durations'][k][j] is not None}
        r = {'naselje': n['ime'], 'prebivalci_2026': s['skupaj'] if s else None, 'prebivalci_65_2026': s['65+'] if s else None,
             'zracno_zd_km': round(haversine(p, TOCKE['ZD Črnomelj']), 2),
             'cesta_zd_km': round(osrm['distances'][0][j] / 1000, 1),
             'voznja_zd_min': round(voz['ZD Črnomelj'], 1),
             'voznja_metlika_min': round(voz['ZD Metlika'], 1),
             'voznja_sbnm_min': round(voz['SB Novo mesto (UC)'], 1),
             'zracno_najblizji_aed_km': round(min(haversine(p, a) for a in aed), 2) if aed else None}
        for sc, (izh, klic, izvoz, f) in SCENARIJI.items():
            r['dostopni_' + sc + '_min'] = round(klic + izvoz + f * min(voz[i] for i in izh), 1)
        rows.append(r)
    rows.sort(key=lambda r: -r['voznja_zd_min'])
    cols = list(rows[0])
    with (ROOT / 'podatki/teme/dostopnost-naselij.csv').open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f); w.writerow(cols); w.writerows([[r[c] for c in cols] for r in rows])
    znani = [r for r in rows if r['prebivalci_2026'] is not None]
    vsi = sum(r['prebivalci_2026'] for r in znani)
    vsi65 = sum(r['prebivalci_65_2026'] for r in znani)

    def pasovi(polje):
        out = []
        for a, b in PASOVI:
            sel = [r for r in znani if a <= r[polje] < b]
            out.append({'pas_min': f'{a}–{b}' if b < 999 else f'{a}+', 'naselja': len(sel),
                        'prebivalci': sum(r['prebivalci_2026'] for r in sel), 'prebivalci_65': sum(r['prebivalci_65_2026'] for r in sel)})
        return out

    scen = {}
    for sc in SCENARIJI:
        polje = 'dostopni_' + sc + '_min'
        nad15 = [r for r in znani if r[polje] > 15]
        scen[sc] = {'pasovi': pasovi(polje), 'nad_15_prebivalci': sum(r['prebivalci_2026'] for r in nad15),
                    'nad_15_delez': round(100 * sum(r['prebivalci_2026'] for r in nad15) / vsi, 1),
                    'nad_15_65plus': sum(r['prebivalci_65_2026'] for r in nad15),
                    'utezeno_povprecje_min': round(sum(r[polje] * r['prebivalci_2026'] for r in znani) / vsi, 1)}
    rep = {'datum': '2026-09-26', 'izhodisca': TOCKE, 'scenariji_opis': {k: {'izhodisca': v[0], 'obdelava_klica_min': v[1], 'izvoz_min': v[2], 'faktor_voznje': v[3]} for k, v in SCENARIJI.items()},
           'naselja_osm': len(rows), 'naselja_surs': len(po_imenu), 'ujemanje_imen': len(znani), 'prebivalci_zajeti': vsi,
           'prebivalci_65_zajeti': vsi65, 'prebivalci_obcina_2026': surs['017']['skupaj'],
           'brez_ujemanja_osm': [r['naselje'] for r in rows if r['prebivalci_2026'] is None],
           'voznja_zd_pasovi': pasovi('voznja_zd_min'), 'scenariji': scen,
           'omejitev': 'Model OSRM (OSM cestna mreža) in predpostavke o obdelavi klica ter hitrosti nujne vožnje. To ni izmerjeni dostopni čas NMP. Zračna razdalja do AED ni čas do uporabe AED.',
           'najdlje_10': rows[:10]}
    (ROOT / 'podatki/teme/dostopnost-naselij.json').write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: rep[k] for k in ['ujemanje_imen', 'prebivalci_zajeti', 'prebivalci_65_zajeti', 'voznja_zd_pasovi']}, ensure_ascii=False))
    for sc, v in scen.items():
        print(sc, 'nad 15 min:', v['nad_15_prebivalci'], f"({v['nad_15_delez']} %), 65+:", v['nad_15_65plus'], 'povprečje', v['utezeno_povprecje_min'], [(p['pas_min'], p['prebivalci']) for p in v['pasovi']])
    for r in rows[:8]:
        print(r['naselje'], r['prebivalci_2026'], r['voznja_zd_min'], r['voznja_metlika_min'], r['dostopni_A_srednji_min'], r['dostopni_B_druga_ekipa_min'])


if __name__ == '__main__':
    main()
