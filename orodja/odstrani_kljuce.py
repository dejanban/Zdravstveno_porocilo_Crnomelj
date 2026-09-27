"""Odstrani javne API ključe tretjih oseb iz shranjenih kopij spletnih strani v viri/.

Shranjene strani lahko vsebujejo ključe, ki jih spletišče pošilja vsakemu obiskovalcu (npr. Google Maps,
Firebase). Niso naši in niso zaupni, a jih ne razširjamo naprej, GitHub pa jih pri pushu lahko zavrne.
Ključ se zamenja z oznako; prvotna in nova SHA-256 se zapišeta v viri/manifest.json (razdelek
»redakcije«), nova vsota nadomesti staro v seznamu »files«. Zagon je idempotenten.
"""
from pathlib import Path
import hashlib, json, re, subprocess

ROOT = Path(__file__).resolve().parents[1]
VZOREC = re.compile(rb'AIza[0-9A-Za-z_-]{35}')
OZNAKA = b'ODSTRANJEN-JAVNI-KLJUC-TRETJE-OSEBE'


def main():
    files = subprocess.run(['git', '-c', 'core.quotepath=off', 'ls-files', '-z', '--', 'viri', 'arhiv'],
                           cwd=ROOT, capture_output=True).stdout.decode('utf-8').split('\0')
    m = json.loads((ROOT / 'viri/manifest.json').read_text(encoding='utf-8'))
    red = {r['path']: r for r in m.setdefault('redakcije', [])}
    for f in filter(None, files):
        p = ROOT / f
        if not p.is_file():
            continue
        raw = p.read_bytes()
        n = len(VZOREC.findall(raw))
        if not n:
            continue
        novo = VZOREC.sub(OZNAKA, raw)
        stara, nova = hashlib.sha256(raw).hexdigest(), hashlib.sha256(novo).hexdigest()
        p.write_bytes(novo)
        for r in m['files']:
            if r['path'] == f and r['sha256'] == stara:
                r['sha256'] = nova
        red[f] = {'path': f, 'sha256_pred_redakcijo': red.get(f, {}).get('sha256_pred_redakcijo', stara), 'sha256_po_redakciji': nova,
                  'odstranjeno': f'{n} javni API ključ(i) tretje osebe (vzorec AIza…)', 'datum': '2026-09-26',
                  'razlog': 'Ključ spletišča, viden vsakemu obiskovalcu; ne razširjamo ga naprej. Vsebina strani sicer nespremenjena.'}
        print(f'{f}: odstranjenih {n}')
    m['redakcije'] = list(red.values())
    (ROOT / 'viri/manifest.json').write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
