"""Preveri obnovljeni obseg arhiva; ne potrjuje izgubljenih starih virov."""
from pathlib import Path
import json, hashlib
P=Path(__file__).resolve().parents[1]
m=json.loads((P/'viri/manifest.json').read_text(encoding='utf-8'))
for r in m['files']:
    p=(P/r['path']).resolve()
    assert p.is_relative_to(P) and p.is_file(),r['path']
    assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256'],r['path']
print(f"Kontrolne vsote: {len(m['files'])} datotek ustreza obnovljenemu manifestu. Stari prazni viri niso potrjeni.")
