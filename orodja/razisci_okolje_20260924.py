from pathlib import Path
import requests, fitz, json, hashlib, re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'viri/okolje-2026-09-24'
OUT.mkdir(exist_ok=True)
ledger=json.loads((OUT/'manifest.json').read_text(encoding='utf-8')) if (OUT/'manifest.json').exists() else []
def save(url,slug):
    r=requests.get(url,timeout=60); r.raise_for_status()
    pdf=r.content.startswith(b'%PDF')
    p=OUT/(slug+('.pdf' if pdf else '.html')); p.write_bytes(r.content)
    if pdf:
        doc=fitz.open(p); txt='\n'.join(f'\n--- Stran PDF {i+1} ---\n'+page.get_text(sort=True) for i,page in enumerate(doc))
    else:
        txt=BeautifulSoup(r.content,'html.parser').get_text('\n',strip=True)
    (OUT/(slug+'.md')).write_text(f'url: {url}\nnaslov: {slug}\nizdajatelj: {requests.utils.urlparse(url).netloc}\ndostopano: 2026-09-24\nmetoda zajema: HTTP; celoten besedilni izvleček BeautifulSoup/PyMuPDF\n\n'+txt,encoding='utf-8')
    ledger.append(dict(url=url,path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(r.content).hexdigest()))
    (OUT/'manifest.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2),encoding='utf-8')
    return BeautifulSoup(r.content,'html.parser') if not pdf else None

if __name__=='__main__':
    url='https://www.komunala-crnomelj.si/novica/kakovost-pitne-vode'
    soup=save(url,'komunala-kakovost')
    links=[(a.get_text(' ',strip=True),urljoin(url,a['href'])) for a in soup.select('a[href]')]
    for title,u in links:
        if re.search(r'(kakovost|poročil)',title,re.I) and '.pdf' in u.lower():
            years=re.findall(r'20\d\d',title)
            if years:
                slug='voda-'+years[-1]+'-'+str(len(ledger))
                try: save(u,slug); print(slug,title,flush=True)
                except Exception as e: print('NAPAKA',u,str(e),flush=True)
    url='https://www.arso.gov.si/zrak/kakovost%20zraka/poro%C4%8Dila%20in%20publikacije/kakovost_letna.html'
    soup=save(url,'arso-letna-kazalo')
    for a in soup.select('a[href]'):
        title=a.get_text(' ',strip=True)
        if any(str(y) in title for y in [2022,2023,2024,2025]):
            year=re.search(r'20\d\d',title).group()
            try: save(urljoin(url,a['href']),'zrak-'+year); print('zrak',year,flush=True)
            except Exception as e: print('NAPAKA',str(e),flush=True)
    for slug,u in [('arso-podatki','https://www.arso.gov.si/zrak/kakovost%20zraka/podatki/'),('arso-arhiv','https://www.arso.gov.si/zrak/kakovost%20zraka/podatki/arhiv.html'),('who-determinante','https://www.who.int/news-room/fact-sheets/detail/social-determinants-of-health'),('who-stres','https://www.who.int/news-room/questions-and-answers/item/stress'),('who-prehrana','https://www.who.int/news-room/fact-sheets/detail/healthy-diet'),('who-zrak','https://www.who.int/news-room/fact-sheets/detail/ambient-(outdoor)-air-quality-and-health')]:
        try: save(u,slug); print(slug,flush=True)
        except Exception as e: print('NAPAKA',str(e),flush=True)
