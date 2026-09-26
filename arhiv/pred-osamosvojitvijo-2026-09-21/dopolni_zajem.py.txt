from razisci_vire import *

if __name__=='__main__':
    p=OUT/'zajem-odeon.json'; d=json.loads(p.read_text(encoding='utf-8'))
    known={r['url']:r for r in d['records']}; candidates=set(); searched=set(d['search_pages']); errors=[]
    # Enobesedne poizvedbe zajamejo sklanjane nazive in starejši naziv ZVC.
    for q in ['krepitev','ZVC','zdravstvenovzgojni','zdravstveno-vzgojni']:
        pending={BASE+'/iskanje/?q='+quote(q)}; done=set()
        while pending:
            batch=sorted(pending-done); pending=set()
            if not batch: break
            with ThreadPoolExecutor(max_workers=3) as pool:
                fs={pool.submit(search_page,u):u for u in batch}
                for f in as_completed(fs):
                    u=fs[f];done.add(u);searched.add(u)
                    try:
                        links,pages,_=f.result();candidates.update(links);pending.update(pages-done)
                    except Exception as e: errors.append({'url':u,'error':str(e)})
        print(q,len(done),len(candidates),flush=True)
    # Ponovni poskus vseh neuspelih iskalnih strani iz prvega prehoda.
    for err in d['failures']:
        if '/iskanje/' in err['url']:
            try:
                links,pages,_=search_page(err['url']); candidates.update(links)
            except Exception as e: errors.append({'url':err['url'],'error':str(e)})
        else: candidates.add(err['url'])
    with ThreadPoolExecutor(max_workers=4) as pool:
        fs={pool.submit(detail,u):u for u in sorted(candidates-set(known))}
        for i,f in enumerate(as_completed(fs)):
            try:
                r=f.result(); known[r['url']]=r
            except Exception as e: errors.append({'url':fs[f],'error':str(e)})
            if i%40==0: print('Dopolnjeno',i+1,'/',len(fs),flush=True)
    d.update(records=list(known.values()),search_pages=sorted(searched),failures=errors,candidate_count=len(set(known)|candidates))
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
    print('KONČANO',len(known),'napak',len(errors),flush=True)
