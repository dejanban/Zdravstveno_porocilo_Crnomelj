"""Umerjanje modelskih časov vožnje na Googlove čase, ki jih vpiše uporabnik.

Vhod: podatki/teme/kalibracija-google.csv (stolpca google_min in google_km izpolni človek iz Google Maps;
izhodišče Delavska pot 4, Črnomelj; cilj središče naselja; običajni promet, brez zastojev).
Modela: OSRM (viri/teme-2026-09-25/osrm-poti.json) in Valhalla (viri/teme-2026-09-25/valhalla-casi.json).
Za vsak model se z metodo najmanjših kvadratov oceni google = a + b * model; izbere se model z manjšo
povprečno absolutno napako (MAE) v navzkrižnem preverjanju (izpusti enega). Rezultat:
podatki/teme/kalibracija-rezultat.json. Brez vsaj 6 izpolnjenih vrstic kalibracija ni uporabljena.
Zagon brez argumentov ustvari ali dopolni predlogo in izpiše stanje.
"""
from pathlib import Path
import csv, json, statistics

ROOT = Path(__file__).resolve().parents[1]
PREDLOGA = ROOT / 'podatki/teme/kalibracija-google.csv'
REZ = ROOT / 'podatki/teme/kalibracija-rezultat.json'
NASELJA = ['Griblje', 'Tribuče', 'Dragatuš', 'Adlešiči', 'Vinica', 'Preloka', 'Učakovci', 'Stari trg ob Kolpi',
           'Sinji Vrh', 'Dolenja Podgora', 'Petrova vas', 'Zilje', 'Dobliče', 'Talčji Vrh']
MIN_TOCK = 6


def modeli():
    osrm = {n['ime']: n for n in json.loads((ROOT / 'viri/teme-2026-09-25/osrm-poti.json').read_text(encoding='utf-8'))['naselja']}
    val = json.loads((ROOT / 'viri/teme-2026-09-25/valhalla-casi.json').read_text(encoding='utf-8'))['naselja']
    out = {}
    for ime, n in osrm.items():
        v = val.get(ime, {})
        out[ime] = {'osrm_min': n['naselje_zd_s'] / 60, 'osrm_km': n['naselje_zd_m'] / 1000,
                    'osrm_nmp_min': n['zd_naselje_s'] / 60,
                    'valhalla_min': v.get('naselje_zd_min'), 'valhalla_km': v.get('naselje_zd_km'),
                    'valhalla_nmp_min': v.get('zd_naselje_min')}
    return out


def fit(xs, ys):
    mx, my = statistics.mean(xs), statistics.mean(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx if sxx else 1.0
    return my - b * mx, b


def predloga(m):
    obstojece = {}
    if PREDLOGA.exists():
        obstojece = {r['naselje']: r for r in csv.DictReader(PREDLOGA.open(encoding='utf-8-sig'))}
    with PREDLOGA.open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(['naselje', 'osrm_min', 'osrm_km', 'valhalla_min', 'valhalla_km', 'google_min', 'google_km', 'google_datum', 'opomba'])
        for ime in NASELJA + [i for i in obstojece if i not in NASELJA]:
            r = obstojece.get(ime, {}); x = m[ime]
            w.writerow([ime, f"{x['osrm_min']:.1f}", f"{x['osrm_km']:.1f}", f"{x['valhalla_min']:.1f}", f"{x['valhalla_km']:.1f}",
                        r.get('google_min', ''), r.get('google_km', ''), r.get('google_datum', ''), r.get('opomba', '')])


def main():
    m = modeli()
    predloga(m)
    tocke = []
    for r in csv.DictReader(PREDLOGA.open(encoding='utf-8-sig')):
        try:
            g = float(r['google_min'].replace(',', '.'))
        except ValueError:
            continue
        gkm = float(r['google_km'].replace(',', '.')) if r['google_km'].strip() else None
        tocke.append((r['naselje'], g, gkm))
    rez = {'izpolnjeno': len(tocke), 'uporabljeno': False, 'metoda': __doc__.strip().splitlines()[0]}
    if len(tocke) >= MIN_TOCK:
        ocene = {}
        for model in ('osrm', 'valhalla'):
            xs = [m[t[0]][model + '_min'] for t in tocke]; ys = [t[1] for t in tocke]
            napake = []
            for i in range(len(xs)):  # navzkrižno preverjanje: izpusti enega
                a, b = fit(xs[:i] + xs[i + 1:], ys[:i] + ys[i + 1:])
                napake.append(abs(a + b * xs[i] - ys[i]))
            a, b = fit(xs, ys)
            ocene[model] = {'a': round(a, 3), 'b': round(b, 3), 'mae_cv_min': round(statistics.mean(napake), 2),
                            'mae_brez_umerjanja_min': round(statistics.mean(abs(x - y) for x, y in zip(xs, ys)), 2)}
        izbran = min(ocene, key=lambda k: ocene[k]['mae_cv_min'])
        rez.update({'uporabljeno': True, 'model': izbran, 'modeli': ocene,
                    'razlike_poti': [{'naselje': t[0], 'google_km': t[2], 'model_km': round(m[t[0]][izbran + '_km'], 1)}
                                     for t in tocke if t[2] and abs(t[2] - m[t[0]][izbran + '_km']) > 0.15 * t[2]],
                    'google': {t[0]: t[1] for t in tocke}})
    REZ.write_text(json.dumps(rez, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps(rez, ensure_ascii=False, indent=1))


def umerjen_cas(ime, smer='prebivalec'):
    """Umerjen čas vožnje (min) za naselje; brez veljavne kalibracije vrne OSRM."""
    m = modeli()[ime]
    rez = json.loads(REZ.read_text(encoding='utf-8')) if REZ.exists() else {}
    if smer == 'prebivalec' and ime in rez.get('google', {}):
        return rez['google'][ime], 'Google (vpisano)'
    if not rez.get('uporabljeno'):
        return (m['osrm_min'] if smer == 'prebivalec' else m['osrm_nmp_min']), 'OSRM (neumerjeno)'
    k = rez['model']; o = rez['modeli'][k]
    x = m[k + '_min'] if smer == 'prebivalec' else m[k + '_nmp_min']
    return max(1.0, o['a'] + o['b'] * x), f'{k.upper()} umerjen na Google'


if __name__ == '__main__':
    main()
