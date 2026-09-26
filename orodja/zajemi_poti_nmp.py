"""Zajem cestnih poti OSRM med ZD Črnomelj in 111 naselji (omrežje; ni del običajne gradnje).

Za vsako naselje dve poizvedbi na javni strežnik OSRM (router.project-osrm.org, profil avto, cestna mreža OSM):
- smer ZD -> naselje: geometrija poti in čas po odsekih (za zemljevid in oceno vožnje reševalcev),
- smer naselje -> ZD: čas in dolžina vožnje prebivalca.
Rezultat: viri/teme-2026-09-25/osrm-poti.json. Obstoječa datoteka se ne prepiše brez --osvezi.
"""
from pathlib import Path
import json, sys, time, urllib.request

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'viri/teme-2026-09-25/osrm-poti.json'
ZD = (15.1875308, 45.5754632)
UA = {'User-Agent': 'zdravje-crnomelj-raziskava/1.0'}


def route(a, b, annotations):
    url = (f'https://router.project-osrm.org/route/v1/driving/{a[0]:.6f},{a[1]:.6f};{b[0]:.6f},{b[1]:.6f}'
           f'?overview=full&geometries=geojson' + ('&annotations=duration' if annotations else ''))
    for poskus in range(4):
        try:
            d = json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read())
            if d.get('code') == 'Ok':
                return d['routes'][0]
        except Exception:
            pass
        time.sleep(2 + 3 * poskus)
    raise RuntimeError(url)


def main():
    if OUT.exists() and '--osvezi' not in sys.argv:
        print('Obstaja; za ponovni zajem uporabi --osvezi.'); return
    naselja = json.loads((ROOT / 'arhiv/izvirnik-0dc0bd4/podatki/poti/poti-podatki.json').read_text(encoding='utf-8'))['naselja']
    out = {'datum': time.strftime('%Y-%m-%d'), 'izhodisce': {'ime': 'ZD Črnomelj', 'lon': ZD[0], 'lat': ZD[1]},
           'vir': 'OSRM demo strežnik, profil driving, podatki © sodelavci OpenStreetMap (ODbL)', 'naselja': []}
    for n in naselja:
        p = (n['lon'], n['lat'])
        tja = route(ZD, p, True)
        nazaj = route(p, ZD, False)
        leg = tja['legs'][0]
        out['naselja'].append({'ime': n['ime'], 'lon': n['lon'], 'lat': n['lat'],
                               'zd_naselje_s': tja['duration'], 'zd_naselje_m': tja['distance'],
                               'naselje_zd_s': nazaj['duration'], 'naselje_zd_m': nazaj['distance'],
                               'geometrija': [[round(x, 5), round(y, 5)] for x, y in tja['geometry']['coordinates']],
                               'odseki_s': [round(v, 1) for v in leg['annotation']['duration']]})
        time.sleep(1.1)
        print(n['ime'], round(tja['duration'] / 60, 1), round(nazaj['duration'] / 60, 1), flush=True)
    OUT.write_text(json.dumps(out, ensure_ascii=False), encoding='utf-8')


if __name__ == '__main__':
    main()
