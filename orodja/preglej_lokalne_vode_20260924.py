from pathlib import Path
import fitz,hashlib,json,re
ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'viri/okolje-2026-09-24/lokalni-izvlecki';out.mkdir(exist_ok=True)
rows=[]; seen={}
for p in (ROOT/'viri/Komunala_Crnomelj').rglob('*.pdf'):
    if not p.stat().st_size: continue
    sha=hashlib.sha256(p.read_bytes()).hexdigest()
    if sha in seen:
        rows.append(dict(path=p.relative_to(ROOT).as_posix(),sha256=sha,duplicate=seen[sha]));continue
    doc=fitz.open(p); txt='\n'.join(f'\nStran {i+1}\n'+page.get_text(sort=True) for i,page in enumerate(doc))
    seen[sha]=p.relative_to(ROOT).as_posix()
    (out/(sha[:16]+'.txt')).write_text(txt,encoding='utf-8')
    rows.append(dict(path=p.relative_to(ROOT).as_posix(),sha256=sha,extract=(out/(sha[:16]+'.txt')).relative_to(ROOT).as_posix(),pages=len(doc),chars=len(txt),flags=[line for line in txt.splitlines() if re.search(r'nesklad|neustre|Datum.+odv|Mesto odv|Escherichia|Giardia|Cryptospor',line,re.I)]))
(ROOT/'podatki/okolje/lokalni-vzorci-20260924.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print('Datoteke',len(rows),'Enolične',len(seen))
for r in rows:
    if '2026' in r['path'] and 'duplicate' not in r: print(r['extract'],r['path'].split('/')[-1],r['flags'])
