from pathlib import Path
import requests,json,concurrent.futures
from bs4 import BeautifulSoup
import fitz
P=Path(__file__).resolve().parent.parent;R=P
sources={
'sz':('https://solazdravja.com/skupina/crnomelj/','Društvo Šola zdravja'),
'sz-skupine':('https://solazdravja.com/obcina/crnomelj/','Društvo Šola zdravja'),
'koronarni':('https://zkdks.si/kontakt/','Zveza koronarnih društev in klubov Slovenije'),
'koronarni-lokalno':('https://koronarnodrustvo-dbk.si/rehabilitacijska-vadba-koronarnih-bolnikov-poslej-tudi-v-crnomlju/','Društvo koronarnih bolnikov Dolenjske in Bele krajine'),
'diabetiki':('https://diabetiki-metlika.org/','Društvo diabetikov Metlika'),
'diabetiki-kontakt':('https://diabetiki-metlika.org/kontakt/','Društvo diabetikov Metlika'),
'donna':('https://europadonna.si/skupnost-europa-donna/skupine/podruznica-bela-krajina/','Europa Donna Slovenija'),
'metuljcica':('https://www.metuljcica.si/srecanja/','Društvo Metuljčica'),
'metuljcica-delo':('https://www.metuljcica.si/kategorija/zanimivost/','Društvo Metuljčica'),
'ckz-imenik':('https://zd-crnomelj.si/wp-content/uploads/2025/10/zbirnik-informacij-CKZ-crnomelj_cistopis.pdf','ZD Črnomelj, CKZ'),
'cvb':('https://www.zdruzenjecvb.com/klubi.html','Združenje bolnikov s cerebrovaskularno boleznijo Slovenije'),
'ms':('https://www.zdruzenje-ms.si/podruznice/dolenjska/','Združenje multiple skleroze Slovenije'),
'spomincica':('https://www.spomincica.si/demenci-prijazne-tocke/','Spominčica – Alzheimer Slovenija'),
'dpt':('https://www.zik-crnomelj.eu/en/projekti/demenci-prijazna-tocka-dpt/','Ljudska univerza Črnomelj'),
'hospic':('https://hospic.si/kontakti/','Slovensko društvo Hospic'),
'hospic-regija':('https://hospic.si/wp-content/uploads/2023/01/Seznam-vseh-obmocnih-odborov-s-kontakti.pdf','Slovensko društvo Hospic'),
'sent':('https://www.sent.si/index.php?m_id=dnevni_center_enota_sent_novo_mesto','ŠENT'),
'filantropija':('https://www.filantropija.org/hisa-sadezi-druzbe-crnomelj/','Slovenska filantropija'),
'rk':('https://rksozcrnomelj.com/prva-pomoc','RKS – Območno združenje Črnomelj'),
'ozara':('https://knjiznica-crnomelj.si/zgodilo-se-je/skupaj-za-dusevno-zdravje/','Knjižnica Črnomelj'),
}
def get(item):
 key,(url,publisher)=item;r=requests.get(url,timeout=40);r.raise_for_status()
 if r.content.startswith(b'%PDF'):
  file=P/'viri'/f'drustva-{key}.pdf';file.write_bytes(r.content);d=fitz.open(file);content='\n\n'.join(f'## Stran PDF {i+1}\n\n'+page.get_text() for i,page in enumerate(d));title='Povezani za zdravje: zbirnik informacij za krepitev zdravja v lokalni skupnosti' if key=='ckz-imenik' else 'Seznam območnih odborov s kontakti';d.close()
 else:
  soup=BeautifulSoup(r.content,'html.parser');title=soup.title.get_text(' ',strip=True) if soup.title else key
  for el in soup(['script','style','nav','header','footer']):el.decompose()
  main=soup.find('main') or soup.find('article') or soup;content=main.get_text('\n',strip=True)
 local=f'viri/splet/zdravstvo-20260920-drustva-{key}.md'
 (R/local).write_text(f'---\nurl: {url}\nnaslov: "{title.replace(chr(34),chr(39))}"\nizdajatelj: {publisher}\ndostopano: 2026-09-20\nmetoda zajema: WebFetch (javni spletni vir; PDF tudi lokalno)\n---\n\n'+content,encoding='utf-8')
 return key,{'title':title,'publisher':publisher,'date':'september 2025' if key=='ckz-imenik' else 'b.d.','url':url,'local':local,'access':'20. september 2026','note':'Preverjena spletna navedba; kontakt ni telefonsko potrjen.'}
if __name__=='__main__':
 refs={};errors=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
  jobs={pool.submit(get,x):x[0] for x in sources.items()}
  for job in concurrent.futures.as_completed(jobs):
   try:k,r=job.result();refs['drustva-'+k]=r;print(k,'OK',flush=True)
   except Exception as e:errors.append({'key':jobs[job],'error':str(e)})
 (P/'podatki/drustva/drustva-viri.json').write_text(json.dumps(refs,ensure_ascii=False,indent=2),encoding='utf-8');print('Napake',errors,flush=True)
