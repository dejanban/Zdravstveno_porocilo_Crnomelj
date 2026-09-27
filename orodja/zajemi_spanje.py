"""Ponovljiv zajem izbranih raziskav; brez spreminjanja starega arhiva."""
from pathlib import Path
import sys, json, hashlib, concurrent.futures
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tmp/okolje-runtime'))
import requests
from bs4 import BeautifulSoup

SOURCES=[
 ('chang-2015','https://doi.org/10.1073/pnas.1418490112','https://elib.dlr.de/94985/1/Chang%20et%20al%20-%20Evening%20Use%20of%20eReaders%20-%20PNAS%202014.pdf','PNAS','2015','10.1073/pnas.1418490112'),
 ('carter-2016','https://pubmed.ncbi.nlm.nih.gov/27802500/','27802500','JAMA Pediatrics','2016','10.1001/jamapediatrics.2016.2341'),
 ('lund-2021','https://pmc.ncbi.nlm.nih.gov/articles/PMC8482627/','https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8482627/fullTextXML','BMC Public Health','2021','10.1186/s12889-021-11640-9'),
 ('spanje-pregled-2022','https://pmc.ncbi.nlm.nih.gov/articles/PMC8811149/','https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8811149/fullTextXML','Frontiers in Medicine','2022',''),
 ('ahmed-2024','https://pubmed.ncbi.nlm.nih.gov/39242043/','39242043','Journal of Affective Disorders','2024','10.1016/j.jad.2024.08.193'),
 ('ahmed-2025','https://pubmed.ncbi.nlm.nih.gov/40782602/','40782602','Computers in Human Behavior','2025',''),
 ('itani-2017','https://pubmed.ncbi.nlm.nih.gov/27743803/','27743803','Sleep Medicine','2017','10.1016/j.sleep.2016.08.006'),
 ('odklop-2025','https://www.nature.com/articles/s41598-025-90984-3','https://www.nature.com/articles/s41598-025-90984-3','Scientific Reports','2025','10.1038/s41598-025-90984-3'),
 ('nijz-zasloni','https://nijz.si/zivljenjski-slog/nekemicne-zasvojenosti/zasloni/','https://nijz.si/zivljenjski-slog/nekemicne-zasvojenosti/zasloni/','NIJZ','2021; posodobitev 17. 7. 2025',''),
 ('nijz-spanje-2026','https://nijz.si/zivljenjski-slog/nazaj-v-solski-ritem-kako-urediti-spanje-otrok-in-mladostnikov/','https://nijz.si/zivljenjski-slog/nazaj-v-solski-ritem-kako-urediti-spanje-otrok-in-mladostnikov/','NIJZ','26. 8. 2026; posodobitev 27. 8. 2026',''),
]

def capture(row):
 slug,url,fetch,publisher,date,doi=row
 ext='xml' if fetch.endswith('XML') else 'pdf' if fetch.endswith('.pdf') else 'html'
 title='';authors='';scope='celotno glavno besedilo; dodatne priloge niso vključene'
 if fetch.isdigit():
  fetch='https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:'+fetch+'%20AND%20SRC:MED&format=json&resultType=core'
  ext='json';scope='bibliografski zapis in povzetek; celotno besedilo ni prebrano'
 r=requests.get(fetch,timeout=75,headers={'User-Agent':'Mozilla/5.0'})
 if r.status_code>=400 and slug in ['chang-2015','carter-2016']:
  fetch=url;ext='html';r=requests.get(fetch,timeout=75,headers={'User-Agent':'Mozilla/5.0'})
 r.raise_for_status()
 if ext=='pdf':
  import fitz
  doc=fitz.open(stream=r.content,filetype='pdf');body='\n'.join(f'Stran {i+1}\n'+p.get_text() for i,p in enumerate(doc));title='Evening use of light-emitting eReaders negatively affects sleep, circadian timing, and next-morning alertness';authors='Anne-Marie Chang; Daniel Aeschbach; Jeanne F. Duffy; Charles A. Czeisler';scope=f'celotno glavno besedilo PDF, {len(doc)} strani; dodatne priloge niso vključene'
 elif ext=='json':
  item=r.json()['resultList']['result'][0];title=item['title'];authors=item.get('authorString','');doi=item.get('doi',doi);publisher=item['journalInfo']['journal']['title']
  body=BeautifulSoup(item.get('abstractText',''),'html.parser').get_text(' ',strip=True)
 else:
  s=BeautifulSoup(r.content,'html.parser')
  for el in s(['script','style','nav','footer','header']):el.decompose()
  if ext=='xml':
   title=s.find('article-title').get_text(' ',strip=True)
   authors='; '.join(x.get_text(' ',strip=True) for x in s.find_all('contrib',{'contrib-type':'author'}))
   ids=s.find_all('article-id',{'pub-id-type':'doi'})
   if ids:doi=ids[0].text
   body=s.get_text('\n',strip=True)
  else:
   title=(s.find('h1') or s.find('title')).get_text(' ',strip=True)
   body=(s.find('article') or s.find('main') or s).get_text('\n',strip=True)
 if len(body)<400:raise ValueError('Nezadosten zajem '+slug)
 folder=ROOT/'viri/spanje-2026-09-25';folder.mkdir(parents=True,exist_ok=True)
 raw=folder/(slug+'.'+ext);raw.write_bytes(r.content)
 local='viri/splet/spanje-20260925-'+slug+'.md'
 meta=f'url: {url}\nnaslov: {title}\nizdajatelj: {publisher}\ndatum objave: {date}\ndostopano: 2026-09-25\nmetoda zajema: HTTP GET; {fetch}; izluščeno besedilo\nobseg: {scope}\nvrsta: '+('uradna strokovna objava' if slug.startswith('nijz') else 'recenzirana raziskava')+'\nzanesljivost: srednja; pri raziskavah omejena prenosljivost na Črnomelj\n'
 (ROOT/local).write_text(meta+'\n# Zajeto besedilo\n\n'+body,encoding='utf-8')
 return dict(id='sleep-'+slug,slug=slug,title=title,authors=authors,publisher=publisher,date=date,doi=doi,url=url,fetch_url=fetch,accessed='2026-09-25',scope=scope,local=local,path=raw.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(r.content).hexdigest())

def main():
 records=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
  for row,result in zip(SOURCES,pool.map(lambda r:safe(r),SOURCES)):
   if isinstance(result,dict):records.append(result);print(result['slug'],result['title'],flush=True)
   else:print('NAPAKA',row[0],result,flush=True)
 out=ROOT/'podatki/spanje';out.mkdir(parents=True,exist_ok=True)
 (out/'spanje-viri.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
def safe(row):
 try:return capture(row)
 except Exception as e:return str(e)
if __name__=='__main__':main()
