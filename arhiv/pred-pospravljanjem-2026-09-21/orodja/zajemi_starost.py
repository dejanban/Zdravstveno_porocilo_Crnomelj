from pathlib import Path
import requests,json,csv
from bs4 import BeautifulSoup
P=Path(__file__).resolve().parent.parent;R=P
for table in ['05C4003S','05C4008S']:
    meta=json.loads((P/f'surs-{table}-meta.json').read_text(encoding='utf-8'));query=[]
    for v in meta['variables']:
        if v['code']=='OBČINE':values=[a for a,b in zip(v['values'],v['valueTexts']) if b in ['Črnomelj','SLOVENIJA']]
        elif v['code']=='POLLETJE':values=[a for a in v['values'] if a.endswith('H1') and a>='2008H1']
        elif v['code']=='SPOL':values=[v['values'][0]]
        else:values=v['values']
        query.append({'code':v['code'],'selection':{'filter':'item','values':values}})
    payload={'query':query,'response':{'format':'json'}}
    url=f'https://pxweb.stat.si/SiStatData/api/v1/sl/Data/{table}.px'
    result=requests.post(url,json=payload,timeout=60);result.raise_for_status();data=result.json()
    (P/f'surs-{table}-podatki.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    (P/f'surs-{table}-poizvedba.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
    labels={v['code']:dict(zip(v['values'],v['valueTexts'])) for v in meta['variables']}
    codes=[c['code'] for c in data['columns'] if c['type']!='c'];rows=[]
    for d in data['data']:rows.append([labels[c].get(k,k) for c,k in zip(codes,d['key'])]+d['values'])
    with (P/f'surs-{table}.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f,delimiter=';');w.writerow(codes+['vrednost']);w.writerows(rows)
    text=f'---\nurl: https://pxweb.stat.si/SiStatData/pxweb/sl/Data/-/{table}.px\nnaslov: "{meta["title"]}"\nizdajatelj: Statistični urad Republike Slovenije\ndostopano: 2026-09-19\nmetoda zajema: WebFetch (API PxWeb, javna podatkovna poizvedba)\n---\n\n# {meta["title"]}\n\nStanje H1 pomeni 1. januar. Zajem: Slovenija in Črnomelj, 2008–2026, oba spola skupaj. Podatki izvirnega odgovora API so ohranjeni v JSON in CSV ob poročilu. Poizvedba je shranjena za ponovljivost.\n\n'+' | '.join(codes+['vrednost'])+'\n\n'+'\n'.join(' | '.join(row) for row in rows)+'\n'
    (R/f'viri/splet/zdravstvo-20260919-surs-{table.lower()}.md').write_text(text,encoding='utf-8')
    print(table,len(rows),codes,rows[-3:])
url='https://pxweb.stat.si/SiStatData/pxweb/sl/Data/-/05C4008S.px'
r=requests.get(url,timeout=45);r.raise_for_status();s=BeautifulSoup(r.content,'html.parser')
for n in s(['script','style']):n.decompose()
(R/'viri/splet/zdravstvo-20260919-surs-starost-metodologija.md').write_text(f'---\nurl: {url}\nnaslov: "Prebivalstvo — izbrani kazalniki: pojasnila"\nizdajatelj: SURS\ndostopano: 2026-09-19\nmetoda zajema: WebFetch\n---\n\n'+s.get_text('\n',strip=True),encoding='utf-8')
