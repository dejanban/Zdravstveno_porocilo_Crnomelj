"""Ponovljiv javni zajem za poročilo; obstoječih surovih virov ne prepisuje."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin, urlparse, quote
import requests, re, json, hashlib, time
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent.parent
RAW = ROOT / 'viri/splet'
DATE = '2026-09-19'
BASE = 'https://www.radio-odeon.com'

def get(url):
    for attempt in range(3):
        try:
            r = requests.get(url, timeout=35)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            return r
        except Exception:
            if attempt == 2: raise
            time.sleep(1)

def save(url, title, text, publisher='Radio Odeon', date='', kind='sekundarni vir'):
    slug = 'zdravstvo-20260919-' + re.sub('[^a-zA-Z0-9-]', '-', urlparse(url).path.strip('/'))[-100:] + '-' + hashlib.sha1(url.encode()).hexdigest()[:9]
    p = RAW / (slug + '.md')
    if not p.exists():
        p.write_text('---\n' + '\n'.join(f'{k}: {json.dumps(v,ensure_ascii=False)}' for k,v in {'url':url,'naslov':title,'izdajatelj':publisher,'dostopano':DATE,'datum objave':date or 'b.d.','metoda zajema':'WebFetch (requests; javna stran)','vrsta':kind}.items()) + '\n---\n\n# '+title+'\n\n## Zajeto besedilo\n\n'+text+'\n',encoding='utf-8')
    return p.relative_to(ROOT).as_posix()

def search_page(url):
    s = BeautifulSoup(get(url).text,'html.parser')
    main = s.select_one('main') or s
    urls = {urljoin(BASE, h.find_parent('a')['href']) for h in main.select('h2') if h.find_parent('a') and h.find_parent('a').find_parent(class_='border-b')}
    pages = {urljoin(BASE,a['href']) for a in main.select('a[href]') if '/iskanje/' in a['href']}
    return urls, pages, save(url,'Iskanje: '+url, '\n'.join(sorted(urls)), kind='iskalni indeks; seznam zadetkov')

def detail(url):
    s = BeautifulSoup(get(url).text,'html.parser')
    main = s.select_one('main') or s
    h = main.select_one('h1')
    title = h.get_text(' ',strip=True) if h else ''
    content = main.select_one('.prose')
    text = content.get_text('\n',strip=True) if content else ''
    heading = main.select_one('.show-item__heading')
    if heading: text = heading.get_text('\n',strip=True)+'\n'+text
    dates = [t.get('datetime') for t in main.select('time') if t.get('datetime')]
    ld = [x.get_text() for x in s.select('script[type="application/ld+json"]')]
    local = save(url,title,text+'\n\n## Strojni datumi\n'+json.dumps({'time':dates,'json_ld':ld},ensure_ascii=False),date=dates[0] if dates else '')
    return {'url':url,'title':title,'text':text,'dates':dates,'json_ld':ld,'local':local}

def run():
    candidates = set(); searched=set(); failures=[]; local_count=0; local_hits=0
    # Celotna lokalna zbirka, brez stranskih koledarjev in priporočil.
    for p in (ROOT/'viri/radio-odeon').rglob('*.md'):
        local_count+=1
        t=p.read_text(encoding='utf-8',errors='replace')
        m=re.search(r'^source:\s*"?([^"\n]+)',t,re.M)
        if not m: continue
        u=m[1].strip()
        if not any(x in u for x in ['/novice/','/koledar-dogodkov/','/nasveti/','/sport/']): continue
        body=re.split(r'\n(?:##? (?:Galerija|Ne zamudite|Zadnji blogi|Poglejte tudi)|\*\*Galerija)',t)[0]
        if re.search(r'\bCKZ\b|krepitev zdravja|zdravstvenovzgojn',body,re.I):
            candidates.add(u.replace('https://radio-odeon.com','https://www.radio-odeon.com')); local_hits+=1
    print(f'Lokalno pregledano {local_count}, kandidati {local_hits}',flush=True)
    for q in ['CKZ','krepitev zdravja','zdravstvenovzgojni','ZVC','Tatjana Gregorič']:
        pending={BASE+'/iskanje/?q='+quote(q)}
        while pending:
            batch=sorted(pending-searched)
            if not batch: break
            pending=set()
            with ThreadPoolExecutor(max_workers=3) as pool:
                futures={pool.submit(search_page,u):u for u in batch}
                for f in as_completed(futures):
                    u=futures[f]; searched.add(u)
                    try:
                        links,pages,_=f.result(); candidates.update(links); pending.update(pages-searched)
                    except Exception as e: failures.append({'url':u,'error':str(e)})
        print(f'Iskanje {q}: skupaj {len(searched)} strani, {len(candidates)} kandidatov',flush=True)
    records=[]
    cache=OUT/'podatki/register/zajem-odeon.json'
    previous=json.loads(cache.read_text(encoding='utf-8')).get('records',[]) if cache.exists() else []
    known={x['url']:x for x in previous}
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures={pool.submit(detail,u):u for u in sorted(candidates) if u not in known}
        records=list(known.values())
        for i,f in enumerate(as_completed(futures)):
            try: records.append(f.result())
            except Exception as e: failures.append({'url':futures[f],'error':str(e)})
            if i%50==0: print(f'Prebrano {len(records)}/{len(candidates)}',flush=True)
    payload={'accessed':DATE,'local_files_scanned':local_count,'search_pages':sorted(searched),'candidate_count':len(candidates),'failures':failures,'records':records}
    cache.write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'KONČANO: {len(records)} strani, {len(failures)} napak',flush=True)

if __name__=='__main__': run()
