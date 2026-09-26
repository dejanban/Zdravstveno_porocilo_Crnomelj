"""Funkcionalna in vizualna preverba zavihkov; izvedba tudi iz file://."""
from pathlib import Path
import sys,json,re,hashlib
from urllib.parse import unquote
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tmp/okolje-runtime'))
from playwright.sync_api import sync_playwright,expect
from bs4 import BeautifulSoup
import fitz

def main():
 result={'viewports':[],'errors':[],'external_requests':[],'checks':[]}
 source=(ROOT/'porocilo.html').read_text(encoding='utf-8');s=BeautifulSoup(source,'html.parser')
 ids=[x['id'] for x in s.select('[id]')];assert len(ids)==len(set(ids)),'Podvojeni ID'
 assert not re.search(r'\[@[^\]]+\]',source)
 for table in s.select('.sleep table'):
  n=len(table.select('thead th'))
  assert all(len(row.find_all('td',recursive=False))==n for row in table.select('tbody tr')),'Poškodovane celice raziskovalne tabele'
 visible=BeautifulSoup(source,'html.parser')
 for el in visible(['script','style']):el.decompose()
 assert not re.search(r'<a\s+(?:class|href)=',visible.get_text()),'Napačno izpisana koda navedbe'
 for a in s.select('a[href]'):
  href=a['href']
  if href.startswith('#'):assert href[1:] in ids,href
  elif not re.match(r'^(https?:|mailto:|tel:|data:)',href):
   p=(ROOT/unquote(href.split('#')[0])).resolve();assert p.is_relative_to(ROOT) and p.is_file() and p.stat().st_size>0,href
 old=BeautifulSoup((ROOT/'vsebina/obnovljena-osnova-20260924.html').read_text(encoding='utf-8'),'html.parser')
 assert all(s.find(id=x['id']) for x in old.select('main > section')),'Izgubljeno poglavje'
 result['checks']+=['Enolična sidra in veljavne lokalne povezave','Ohranjena vsa stara poglavja']
 result['missing_legacy_files']=len(json.loads((ROOT/'preverjanje/manjkajoci-prenosi.json').read_text(encoding='utf-8')))
 with sync_playwright() as p:
  b=p.chromium.launch(channel='msedge',headless=True)
  page=b.new_page();page.on('pageerror',lambda e:result['errors'].append(str(e)))
  page.on('request',lambda r:result['external_requests'].append(r.url) if r.url.startswith(('http:','https:')) else None)
  page.emulate_media(reduced_motion='reduce')
  url=(ROOT/'porocilo.html').as_uri()
  panels=[x['id'] for x in s.select('.report-panel')]
  for width in [1440,1024,768,390,360]:
   page.set_viewport_size({'width':width,'height':1000});page.goto(url,wait_until='load')
   for panel in panels:
    page.evaluate('(id)=>window.__reportReveal("#"+id)',panel)
    assert page.locator('.report-panel:visible').count()==1,panel
    dims=page.evaluate('({width:innerWidth,scroll:document.documentElement.scrollWidth})');assert dims['scroll']<=width+1,(panel,dims)
   result['viewports'].append({'width':width,'tabs':len(panels),'horizontal_overflow':False})
   if width in [1440,390]:
    for panel in ['pregled','spanje','poti','sport','aed','stevilke']:
     page.evaluate('(id)=>window.__reportReveal("#zavihek-"+id)',panel)
     page.screenshot(path=str(ROOT/f'preverjanje/prenova-{panel}-{width}.png'))
  page.set_viewport_size({'width':1440,'height':1000});page.goto(url)
  page.locator('#tab-spanje').click();page.wait_for_url('**#zavihek-spanje');expect(page.locator('#spanje-povzetek')).to_be_visible()
  page.locator('#tab-aed').click();page.go_back();expect(page.locator('#spanje-povzetek')).to_be_visible()
  page.locator('#tab-spanje').focus();page.keyboard.press('ArrowDown');expect(page.locator('#zavihek-poti')).to_be_visible()
  page.keyboard.press('Home');expect(page.locator('#zavihek-pregled')).to_be_visible()
  result['checks'].append('Klik, tipkovnica, neposredna povezava in zgodovina Nazaj')
  page.locator('#report-search').fill('metaanaliza');assert page.locator('#report-results a').count()>0
  page.locator('#report-results a').filter(has_text='Kaj kažejo raziskave').click();expect(page.locator('#spanje-raziskave')).to_be_visible()
  page.locator('#clear-report-search').click();assert page.locator('#report-results').is_hidden()
  page.goto(url+'#pitna-voda');expect(page.locator('#pitna-voda')).to_be_visible()
  result['checks'].append('Iskanje v skritih zavihkih in stara sidra')
  page.evaluate('window.__reportReveal("#zavihek-stevilke")')
  slider=page.locator('#zavihek-stevilke .chart input[type=range]').first
  slider.evaluate('(e)=>{e.value=e.min||0;e.dispatchEvent(new Event("input",{bubbles:true}))}')
  assert 'Izdaja' in page.locator('#zavihek-stevilke .chart .readout').first.inner_text()
  result['checks'].append('Drsnik ohranjenih grafov NIJZ')
  page.evaluate('window.__reportReveal("#zavihek-sport")');page.locator('#sport-search').fill('Rokomet');assert page.locator('#sport-table tbody tr:visible').count()==1
  page.locator('#sport-search').fill('');page.locator('#sport-type').select_option(label='Tenis');assert page.locator('#sport-table tbody tr:visible').count()==1
  page.locator('#sport-type').select_option('');result['checks'].append('Iskanje in filter športnih dejavnosti')
  page.evaluate('window.__reportReveal("#zavihek-poti")');page.locator('[data-mode=pes]').click()
  assert page.locator('#poti-pes').is_checked() and not page.locator('#poti-kolo').is_checked()
  page.locator('[data-mode=kolo]').click();assert not page.locator('#poti-pes').is_checked() and page.locator('#poti-kolo').is_checked()
  page.locator('[data-mode=vse]').click();page.locator('#poti-aed').check();assert page.locator('#poti-aed-layer').is_visible()
  first=page.locator('#poti-aed-layer a').first;first.evaluate('(e)=>e.dispatchEvent(new MouseEvent("click",{bubbles:true,cancelable:true}))');expect(page.locator('#zavihek-aed')).to_be_visible()
  page.locator('#aed-search').fill('Dobliče');assert page.locator('#aed-table tbody tr:visible').count()>0
  page.locator('#aed-table tbody tr:visible').first.click();assert 'časovna dostopnost' in page.locator('#aed-panel').inner_text().lower()
  result['checks'].append('Peš/kolesarski pogled, sloj AED, prehod na lokacijo in filter AED')
  page.goto(url+'#poti');old_view=page.locator('#poti svg').get_attribute('viewBox');page.locator('.poti-zoom [data-action=in]').click();assert page.locator('#poti svg').get_attribute('viewBox')!=old_view
  page.locator('#poti-tabela').evaluate('(e)=>{let p=e.parentElement;while(p){if(p.tagName==="DETAILS")p.open=true;p=p.parentElement;}}')
  page.locator('#poti-tabela tbody tr:visible button').first.click();expect(page.locator('.poti-panel')).to_contain_text('Nadmorska višina')
  result['checks'].append('Približevanje zemljevida in podrobnosti poti')
  # Register mora ostati delujoč in brez zunanjega nalaganja.
  page.goto((ROOT/'register-dogodkov.html').as_uri());search=page.locator('#event-search')
  if search.count():search.fill('spanje');assert page.locator('#event-count').inner_text()
  result['checks'].append('Ohranjen register objav CKZ')
  # Brez JavaScripta je celotno poročilo dostopno.
  ctx=b.new_context(java_script_enabled=False);plain=ctx.new_page();plain.goto(url);assert plain.locator('.report-panel:visible').count()==len(panels);ctx.close()
  result['checks'].append('Celotna vsebina dostopna brez JavaScripta')
  page.goto(url+'#zavihek-spanje');page.evaluate('document.querySelectorAll("details").forEach(e=>e.open=true)')
  page.pdf(path=str(ROOT/'porocilo.pdf'),format='A4',print_background=True,prefer_css_page_size=True)
  b.close()
 assert not result['errors'],result['errors'];assert not result['external_requests'],result['external_requests']
 doc=fitz.open(ROOT/'porocilo.pdf');full='\n'.join(p.get_text() for p in doc)
 for text in ['Spanje in digitalne navade','Športne dejavnosti','AED-ji','Pitna voda','Kritična vprašanja','Carter','Lemahieu','Literatura']:
  assert text in full,('Manjka v PDF',text)
 result['pdf_pages']=len(doc);rendered=[]
 for i,pg in enumerate(doc):
  if i==0 or any(x in pg.get_text() for x in ['Kaj kažejo raziskave','Lokalna vprašanja, ukrepi','Peš in kolesarske poti','Športne dejavnosti','AED-ji','Pregled ključnih raziskav','Uredniška ocena dokumentiranosti']):
   pg.get_pixmap(matrix=fitz.Matrix(1.2,1.2)).save(ROOT/f'preverjanje/prenova-pdf-{i+1}.png');rendered.append(i+1)
 result['rendered_pdf_pages']=rendered;result['references']=len(s.select('#literatura p[id]'));result['checks'].append('PDF vključuje vse zavihke in razširjene podrobnosti')
 (ROOT/'preverjanje/prenova-porocilo.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
