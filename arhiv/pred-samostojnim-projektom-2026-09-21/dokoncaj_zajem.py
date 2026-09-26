"""Počasen zaporedni zaključek iskanja, s spoštovanjem HTTP 429."""
from razisci_vire import *
import razisci_vire

def slow_get(url):
    for attempt in range(4):
        time.sleep(2.5)
        r=requests.get(url,timeout=40)
        if r.status_code==429:
            delay=r.headers.get('Retry-After','12')
            delay=min(50,max(12,int(delay) if delay.isdigit() else 12))
            time.sleep(delay)
            continue
        r.raise_for_status();r.encoding=r.apparent_encoding;return r
    raise RuntimeError('HTTP 429 tudi po počasnem ponovnem poskusu')

if __name__=='__main__':
    razisci_vire.get=slow_get
    p=OUT/'zajem-odeon.json';d=json.loads(p.read_text(encoding='utf-8')); known={r['url']:r for r in d['records']}
    pending={e['url'] for e in d['failures']};done=set();errors=[];new=set()
    # Tudi strani, ki jih zaradi vrzeli pri paginaciji še ni bilo v prvotnem obhodu.
    pending.update(BASE+f'/iskanje/page{i}?q=krepitev' for i in range(1,46) if BASE+f'/iskanje/page{i}?q=krepitev' not in d['search_pages'])
    pending.discard(BASE+'/iskanje/page1?q=krepitev')
    while pending:
        u=sorted(pending)[0];pending.remove(u);done.add(u)
        try:
            if '/iskanje/' in u:
                links,pages,_=search_page(u);new.update(links-set(known));pending.update(pages-set(d['search_pages'])-done)
            else:new.add(u)
        except Exception as e:errors.append({'url':u,'error':str(e)})
        print('Iskanje',len(done),'preostalo',len(pending),'novih',len(new),flush=True)
    for i,u in enumerate(sorted(new)):
        try:r=detail(u);known[u]=r
        except Exception as e:errors.append({'url':u,'error':str(e)})
        if i%20==0:print('Nove objave',i+1,'/',len(new),flush=True)
    d.update(records=list(known.values()),failures=errors,search_pages=sorted(set(d['search_pages'])|done),candidate_count=len(known)+len([e for e in errors if '/iskanje/' not in e['url']]))
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8');print('KONČANO',len(known),'napak',len(errors),flush=True)
