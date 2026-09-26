"""Zajem virov za nove teme (25. 9. 2026): register podatki/teme/teme-viri.json.

Izvirnik gre v viri/teme-2026-09-25/<file>, izvleček z metapodatki v viri/splet/teme-20260925-<slug>.md,
SHA-256 obeh v viri/manifest.json. Obstoječih izvirnikov ne prenaša znova (razen z --osvezi),
zato je ponovni zagon brez omrežja varen. Omrežni del ni del običajne gradnje.
"""
from pathlib import Path
import hashlib, json, re, sys, urllib.request

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tmp/okolje-runtime'))
D = ROOT / 'viri/teme-2026-09-25'
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128 Safari/537.36'}


def besedilo(path):
    ext = path.suffix.lower()
    if ext == '.pdf':
        import pymupdf
        return '\n'.join(f'--- Stran {i + 1} ---\n' + p.get_text() for i, p in enumerate(pymupdf.open(path)))
    if ext in ('.html', '.htm'):
        from bs4 import BeautifulSoup
        s = BeautifulSoup(path.read_text(encoding='utf-8', errors='replace'), 'html.parser')
        for t in s(['script', 'style', 'nav', 'header', 'footer', 'noscript', 'form', 'aside']):
            t.decompose()
        main = s.find('article') or s.find('main') or s.body
        txt = re.sub(r'\n\s*\n+', '\n\n', main.get_text('\n', strip=True))
        if len(txt) < 300 and s.body:  # stran se izrisuje z JavaScriptom: vzemi celotno telo
            txt = re.sub(r'\n\s*\n+', '\n\n', s.body.get_text('\n', strip=True))
        return txt
    if ext == '.xlsx':
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        out = []
        for ws in wb.worksheets:
            out.append(f'## List {ws.title}')
            for i, row in enumerate(ws.iter_rows(values_only=True)):
                vals = [str(v) for v in row if v is not None]
                keep = i < 40 or any(k in ' '.join(vals).upper() for k in ('NOVO MESTO', 'METLIKA', 'ČRNOMELJ'))
                if vals and keep:
                    out.append(' | '.join(vals))
        return '\n'.join(out)
    if ext == '.json':
        return path.read_text(encoding='utf-8-sig')[:20000]
    return path.read_text(encoding='utf-8', errors='replace')


def main():
    recs = json.loads((ROOT / 'podatki/teme/teme-viri.json').read_text(encoding='utf-8'))
    D.mkdir(parents=True, exist_ok=True)
    m = json.loads((ROOT / 'viri/manifest.json').read_text(encoding='utf-8'))
    known = {r['path']: r for r in m['files']}
    for r in recs:
        src = ROOT / r.get('dir', 'viri/teme-2026-09-25') / r['file']
        src.parent.mkdir(parents=True, exist_ok=True)
        if '--osvezi' in sys.argv or not src.exists():
            url = r.get('download', r['url'])
            src.write_bytes(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read())
        txt = besedilo(src)
        md = (f"---\nurl: {r['url']}\nnaslov: {r['title']}\nizdajatelj: {r['publisher']}\navtorji: {r['authors']}\n"
              f"datum objave: {r['date']}\ndostopano: {r.get('accessed', '2026-09-25')}\n"
              f"metoda zajema: prenos izvirnika ({src.relative_to(ROOT).as_posix()}), strojni izvleček besedila\n"
              f"obseg branja: {r['scope']}\nzanesljivost: {r['reliability']}\n---\n\n{txt}\n")
        out = ROOT / f"viri/splet/teme-20260925-{r['slug']}.md"
        out.write_text(md, encoding='utf-8')
        r['local'] = out.relative_to(ROOT).as_posix()
        r['path'] = src.relative_to(ROOT).as_posix()
        for p in (r['local'], r['path']):
            h = hashlib.sha256((ROOT / p).read_bytes()).hexdigest()
            if p in known:
                known[p]['sha256'] = h
            else:
                known[p] = {'path': p, 'sha256': h}
                m['files'].append(known[p])
        print(f"{r['slug']}: {len(txt)} znakov")
    (ROOT / 'podatki/teme/teme-viri.json').write_text(json.dumps(recs, ensure_ascii=False, indent=1), encoding='utf-8')
    (ROOT / 'viri/manifest.json').write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
