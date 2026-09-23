from razisci_vire import *
import fitz

SOURCES = [
 ('nijz','https://obcine.nijz.si/obcine/crnomelj/','NIJZ','2026'),
 ('nijz2026','https://nijz.si/podatki/zdravje-v-obcini-2026/','NIJZ','2026'),
 ('metode','https://obcine.nijz.si/kazalniki/','NIJZ','2026'),
 ('zd2025','https://zd-crnomelj.si/wp-content/uploads/2026/03/Letno-porocilo-ZD-Crnomelj-2025.pdf','ZD Črnomelj','2026'),
 ('plan2025','https://zd-crnomelj.si/wp-content/uploads/2025/04/FINANCNI-NACRTI-2025.pdf','ZD Črnomelj','2025'),
 ('ckz','https://zd-crnomelj.si/ckz/','ZD Črnomelj','b.d.'),
 ('ckzdogodki','https://zd-crnomelj.si/ckz/dogodki/','ZD Črnomelj','b.d.'),
 ('urnik','https://zd-crnomelj.si/zvc/wp-content/uploads/sites/3/2025/03/Urnik-delavnic-APRIL-IN-MAJ-2025-5.pdf','ZD Črnomelj','2025'),
 ('slo-gibanje','https://pubmed.ncbi.nlm.nih.gov/36811242/','Obesity (Silver Spring) / PubMed','2023'),
 ('dpp','https://pubmed.ncbi.nlm.nih.gov/11832527/','New England Journal of Medicine / PubMed','2002'),
 ('hall','https://pubmed.ncbi.nlm.nih.gov/31105044/','Cell Metabolism / PubMed','2019'),
 ('sprint','https://pubmed.ncbi.nlm.nih.gov/26551272/','New England Journal of Medicine / PubMed','2015'),
 ('safer','https://www.who.int/initiatives/SAFER','WHO','b.d.'),
 ('live-life','https://www.who.int/initiatives/live-life-initiative-for-suicide-prevention','WHO','b.d.'),
 ('solska-prehrana','https://www.who.int/news-room/events/detail/2026/01/27/default-calendar/launch-of-the-who-guideline-on-policies-and-interventions-to-create-healthy-school-food-environments','WHO','2026-01-27'),
 ('predavanje','https://www.who.int/news-room/events/detail/2024/11/21/default-calendar/accelerating-childhood-overweight-reduction-lessons-learned-and-the-path-towards-2030','WHO','2024-11-21'),
 ('predavanje-prosojnice','https://cdn.who.int/media/docs/default-source/nutrition-and-food-safety/events/2024/webinar---accelerating-childhood-overweight-reduction---lessons-learned-and-the-path-towards-2030-presentation.pdf?sfvrsn=a331db34_5','WHO','2024-11-21'),
 ('oecd','https://www.oecd.org/content/dam/oecd/en/publications/reports/2025/12/country-health-profile-2025-country-notes_7e72146d/slovenia_27d174ae/4765833c-en.pdf','OECD / European Observatory','2025'),
 ('tobak','https://www.who.int/publications/i/item/9789240096431','WHO','2024'),
 ('neenakosti','https://www.who.int/publications/i/item/9789240107588','WHO','2025'),
]

def fetch(item):
    key,url,publisher,date=item
    r=get(url)
    if r.content.startswith(b'%PDF'):
        d=fitz.open(stream=r.content,filetype='pdf')
        text='\n\n'.join(f'## Stran PDF {i+1}\n'+p.get_text() for i,p in enumerate(d))
        title=d.metadata.get('title') or key
        (OUT/'viri').mkdir(exist_ok=True)
        (OUT/'viri'/f'{key}.pdf').write_bytes(r.content)
        links=[]
    else:
        s=BeautifulSoup(r.text,'html.parser')
        for x in s.select('script,style,header,footer,nav'): x.decompose()
        main=s.select_one('main') or s.select_one('#content') or s
        h=main.select_one('h1') or s.select_one('title')
        title=h.get_text(' ',strip=True) if h else key
        text=main.get_text('\n',strip=True)
        links=[{'title':a.get_text(' ',strip=True),'url':urljoin(url,a['href'])} for a in main.select('a[href]') if re.search('pdf|record|guideline|opisi|metodol|download|api/files',a['href']+' '+a.get_text(),re.I)]
    if 'One moment' in title or len(text)<150: raise RuntimeError('Zaščitna ali prazna stran: '+title)
    local=save(url,title,text,publisher,date,'primarni vir; izvirni dokument ali uradni povzetek')
    return {'key':key,'url':url,'publisher':publisher,'date':date,'title':title,'local':local,'links':links,'text':text}

if __name__=='__main__':
    records=[]; errors=[]
    with ThreadPoolExecutor(max_workers=4) as pool:
        fs={pool.submit(fetch,item):item for item in SOURCES}
        for f in as_completed(fs):
            try:
                x=f.result();records.append(x);print(x['key'],len(x['text']),flush=True)
            except Exception as e: errors.append({'key':fs[f][0],'url':fs[f][1],'error':str(e)});print('NAPAKA',fs[f][0],str(e),flush=True)
    (OUT/'literatura-zajem.json').write_text(json.dumps({'records':records,'errors':errors},ensure_ascii=False,indent=2),encoding='utf-8')
