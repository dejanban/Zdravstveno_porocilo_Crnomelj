"""Preveri obnovljeni obseg arhiva; ne potrjuje izgubljenih starih virov."""
from pathlib import Path
import json, hashlib
P=Path(__file__).resolve().parents[1]
m=json.loads((P/'viri/manifest.json').read_text(encoding='utf-8'))
known_path=P/'podatki/spanje/podedovana-neskladja.json'
known={r['path']:r for r in json.loads(known_path.read_text(encoding='utf-8'))} if known_path.exists() else {}
report={'exact':0,'line_ending_equivalent':0,'inherited_unresolved':[],'new_source_failures':[]}
for r in m['files']:
    p=(P/r['path']).resolve()
    assert p.is_relative_to(P) and p.is_file(),r['path']
    raw=p.read_bytes();actual=hashlib.sha256(raw).hexdigest()
    if actual==r['sha256']:report['exact']+=1
    elif hashlib.sha256(raw.replace(b'\n',b'\r\n')).hexdigest()==r['sha256']:
        report['line_ending_equivalent']+=1
    elif r['path'] in known and actual==known[r['path']]['observed_sha256'] and r['sha256']==known[r['path']]['expected_sha256']:
        report['inherited_unresolved'].append(r['path'])
    else:raise AssertionError('Nova ali nepojasnjena sprememba: '+r['path'])
# Izvirni manifest (commit 0dc0bd4): vsebine obnovljene z orodja/obnovi_iz_gita.py.
izv=m.get('izvorni_manifest',{}).get('datoteke',[])
izv_known={r['path'] for r in m.get('izvorna_neskladja',[])}
report['izvorni_manifest']={'skupaj':len(izv),'exact':0,'line_ending_equivalent':0,'znana_neskladja':[]}
for r in izv:
    p=(P/r['lokalna_pot']).resolve()
    assert p.is_relative_to(P) and p.is_file(),r['lokalna_pot']
    raw=p.read_bytes()
    if hashlib.sha256(raw).hexdigest()==r['sha256']:report['izvorni_manifest']['exact']+=1
    elif hashlib.sha256(raw.replace(b'\r\n',b'\n').replace(b'\n',b'\r\n')).hexdigest()==r['sha256']:
        report['izvorni_manifest']['line_ending_equivalent']+=1
    elif r['lokalna_pot'] in izv_known:report['izvorni_manifest']['znana_neskladja'].append(r['lokalna_pot'])
    else:raise AssertionError('Nepojasnjena sprememba izvirnega vira: '+r['lokalna_pot'])
report['status']='opozorilo: podedovana neskladja' if report['inherited_unresolved'] or report['izvorni_manifest']['znana_neskladja'] else 'uspesno'
(P/'preverjanje/kontrolne-vsote.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
print('Podedovana neskladja niso potrjeni izvirniki. Stari viri so obnovljeni iz commita 0dc0bd4 in preverjeni proti izvirnemu manifestu.')
