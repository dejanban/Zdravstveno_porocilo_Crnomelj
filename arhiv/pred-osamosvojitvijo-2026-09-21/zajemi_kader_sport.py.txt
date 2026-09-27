"""Zajem javnih virov za datirani pregled kadra in športa; obstoječih kopij ne prepisuje."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json, requests, fitz
from bs4 import BeautifulSoup
from urllib.parse import urljoin
P=Path(__file__).resolve().parent
ROOT=P.parents[1]
def fetch(item):
    key,r=item
    dst=ROOT/r['local']
    if dst.exists(): return key,'že shranjeno'
    try:
        response=requests.get(r['url'],timeout=35)
        response.raise_for_status()
        if response.content.startswith(b'%PDF'):
            pdf=P/'viri'/f'kader-sport-{key}.pdf'
            pdf.write_bytes(response.content)
            with fitz.open(pdf) as d:
                body='\n\n'.join(f'## Stran PDF {i+1}\n\n'+page.get_text() for i,page in enumerate(d))
        elif key == 'zzzsdata':
            import openpyxl, io
            (P/'viri'/'kader-sport-zzzs.xlsx').write_bytes(response.content)
            wb=openpyxl.load_workbook(io.BytesIO(response.content),data_only=True)
            parts=[]
            for sh in wb:
                rows=list(sh.values)
                selected=[row for i,row in enumerate(rows) if i<10 or any('rnomelj' in str(v) or 'UKOVI' in str(v) or 'JERCIN' in str(v) for v in row)]
                parts.append('## '+sh.title+'\n\n'+'\n'.join(' | '.join(str(v) if v is not None else '' for v in row) for row in selected))
            body='Izvleček za Črnomelj; celotni izvirnik je shranjen v mapi poročila.\n\n'+'\n\n'.join(parts)
        else:
            response.encoding=response.apparent_encoding
            s=BeautifulSoup(response.text,'html.parser')
            if s.title and any(x in s.title.get_text().lower() for x in ['one moment','just a moment','access denied']):
                return key,'zaščitna stran; ni shranjeno'
            for t in s.select('script,style,nav,header,footer'):t.decompose()
            body=s.get_text('\n',strip=True)
            links=[(a.get_text(' ',strip=True),urljoin(response.url,a['href'])) for a in s.select('a[href]') if a.get_text(' ',strip=True)]
            body+='\n\n## Povezave iz vira\n\n'+'\n'.join(f'- {t}: {u}' for t,u in links)
        head='---\n'+f'url: {r["url"]}\nnaslov: {json.dumps(r["title"],ensure_ascii=False)}\nizdajatelj: {r["publisher"]}\ndostopano: 2026-09-21\nmetoda zajema: WebFetch (requests; izvirno besedilo)\n---\n\n'
        dst.write_text(head+body,encoding='utf-8')
        return key,f'{len(body)} znakov'
    except Exception as e:return key,str(e)
if __name__=='__main__':
    refs=json.loads((P/'kader-sport-viri.json').read_text(encoding='utf-8'))
    with ThreadPoolExecutor(max_workers=6) as pool:
        for key,result in pool.map(fetch,refs.items()):print(key,result,flush=True)
