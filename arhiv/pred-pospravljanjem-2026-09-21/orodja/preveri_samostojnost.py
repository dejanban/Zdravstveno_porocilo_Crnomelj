"""Preverba virov, SHA-256 ter povezav, ki ne smejo zapuščati projekta."""
import hashlib,json,re
from pathlib import Path
from urllib.parse import unquote,urlsplit
from bs4 import BeautifulSoup
from projekt import BASE,datoteka

def main():
    manifest=json.loads((BASE/'viri/manifest.json').read_text(encoding='utf-8'))
    for r in manifest['datoteke']:
        p=datoteka(r['lokalna_pot'])
        assert p.is_file(),p
        assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256'],p
    refs=json.loads(datoteka('literatura.json').read_text(encoding='utf-8'))
    assert len(refs)==93
    rows=json.loads(datoteka('register-dogodkov.json').read_text(encoding='utf-8'))
    assert len(rows)==1068
    for r in refs:assert datoteka(r['local']).exists(),r['local']
    for r in rows:assert datoteka(r['lokalna_kopija']).is_file(),r['lokalna_kopija']
    documents=[BASE/'porocilo.html',BASE/'porocilo-print.html',BASE/'register-dogodkov.html',BASE/'index.html',*sorted((BASE/'viri').rglob('*.html'))]
    n=0
    for p in documents:
        soup=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser');ids={x['id'] for x in soup.select('[id]')}
        for e in soup.select('[href],[src]'):
            u=e.get('href') or e.get('src');parts=urlsplit(u)
            if parts.scheme in ['https','http','mailto','tel','data']:continue
            assert not parts.scheme,(p,u)
            target=(p.parent/unquote(parts.path)).resolve() if parts.path else p.resolve()
            assert target.is_relative_to(BASE),(p,u,'zunaj projekta')
            assert target.exists(),(p,u,'manjka')
            if not parts.path and parts.fragment:assert unquote(parts.fragment) in ids,(p,u,'sidro')
            n+=1
    result={'viri_porocila':len(refs),'objave_registra':len(rows),'izvirniki_sha256':len(manifest['datoteke']),'preverjene_strani':len(documents),'lokalne_povezave':n,'status':'uspešno'}
    (BASE/'preverjanje').mkdir(exist_ok=True)
    (BASE/'preverjanje/samostojnost.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()
