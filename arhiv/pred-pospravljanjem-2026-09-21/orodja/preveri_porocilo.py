from pathlib import Path
import json
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import fitz
P = Path(__file__).resolve().parent.parent
with sync_playwright() as pw:
    browser=pw.chromium.launch(headless=True)
    page=browser.new_page(viewport={'width':1440,'height':1050},device_scale_factor=1)
    errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto((P/'porocilo.html').as_uri());page.wait_for_timeout(400)
    assert page.locator('.chart svg').count()==11
    assert page.locator('#starost svg').count()==1
    assert '2026' in page.locator('.readout').first.inner_text()
    page.screenshot(path=str(P/'preverjanje/namizje.png'))
    for width in [320,390,768,1440,1920]:
        page.set_viewport_size({'width':width,'height':950})
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'),width
    page.set_viewport_size({'width':390,'height':900});page.reload();page.screenshot(path=str(P/'preverjanje/telefon.png'))
    page.set_viewport_size({'width':1440,'height':1000});page.locator('#ckz').scroll_into_view_if_needed();page.screenshot(path=str(P/'preverjanje/ckz.png'))
    page.locator('input[type=range]').first.evaluate('(e)=>{e.value=0;e.dispatchEvent(new Event("input"))}')
    assert '2016' in page.locator('.readout').first.inner_text()
    page.locator('input[type=range]').first.evaluate('(e)=>{e.value=e.max;e.dispatchEvent(new Event("input"))}')
    page.emulate_media(media='print');page.pdf(path=str(P/'porocilo.pdf'),format='A4',print_background=True,prefer_css_page_size=True)
    page.emulate_media(media='screen');page.goto((P/'register-dogodkov.html').as_uri())
    expected=json.loads((P/'statistika-registra.json').read_text(encoding='utf-8'))['pripadnost']['Črnomelj']
    assert page.locator('#events-table tbody tr:visible').count()==expected
    page.locator('#event-search').fill('doblice');assert page.locator('#events-table tbody tr:visible').count()>0
    page.locator('#event-search').fill('xxxyyyzzz');assert page.locator('#events-table tbody tr:visible').count()==0
    page.locator('#reset-filters').click();assert page.locator('#events-table tbody tr:visible').count()==expected
    assert not errors,errors
    browser.close()
for name in ['porocilo.html','register-dogodkov.html']:
    soup=BeautifulSoup((P/name).read_text(encoding='utf-8'),'html.parser');ids={e['id'] for e in soup.select('[id]')}
    for a in soup.select('a[href]'):
        u=a['href']
        if u.startswith('#'):assert u[1:] in ids,(name,u)
        elif not u.startswith(('http:','https:','mailto:','tel:')):assert (P/u.split('#')[0]).exists(),(name,u)
d=fitz.open(P/'porocilo.pdf');print(json.dumps({'strani_pdf':len(d),'grafi':11,'viri':len(json.loads((P/'literatura.json').read_text(encoding='utf-8'))),'preverjanje':'Uspešno: povezave, 5 širin, JavaScript, filtri, drsnik.'},ensure_ascii=False));d.close()
