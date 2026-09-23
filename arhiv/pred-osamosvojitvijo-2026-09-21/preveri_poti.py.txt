"""Preverba prostorske obdelave, izvornih datotek in uporabniškega zemljevida."""
from pathlib import Path
import json,hashlib,math,re,xml.etree.ElementTree as ET
from analiziraj_poti import F,B,G,km,clipped_km
from shapely.geometry import LineString,MultiLineString,Polygon,Point
from shapely.ops import transform
from playwright.sync_api import sync_playwright
P=Path(__file__).resolve().parent
d=json.loads((P/'poti-podatki.json').read_text(encoding='utf-8'))
manifest=json.loads((P/'poti-manifest.json').read_text(encoding='utf-8'))['datoteke']
assert len(d['poti'])==len(list((P/'viri/gpx').rglob('*.gpx')))==len(manifest)
boundary=transform(F,Polygon(d['meja']))
tolerant=boundary.buffer(.03)
from shapely.prepared import prep
tolerant=prep(tolerant)
for r in d['poti']:
    assert hashlib.sha256((P/r['datoteka']).read_bytes()).hexdigest()==r['sha256']
    assert 0<=r['km_v_obcini']<=r['km']+.000001
    assert r['neveljavne_tocke']==0
    for seg in r['znotraj']:
        # Zaokrožitev izvoza na 7 decimalk lahko premakne točko za nekaj mm.
        assert all(tolerant.covers(transform(F,Point(c))) for c in seg)
for k,s in d['statistika'].items():
    assert all(a['naselja']<=b['naselja'] and a['povrsina_km2']<=b['povrsina_km2'] for a,b in zip(s['pokritost'],s['pokritost'][1:]))
    assert all(0<=b['naselja']<=d['stevilo_naselij_osm'] and b['povrsina_delez']<=100 for b in s['pokritost'])
# Neodvisen primer: linija skozi kvadrat in oddaljen ločen segment.
square=Polygon([(0,0),(1000,0),(1000,1000),(0,1000)])
cross=LineString([(-1000,500),(2000,500)])
assert cross.intersection(square).length==1000
assert Point(500,1000).distance(cross)==500
a=LineString([F(15.1,45.5),F(15.101,45.5)]);b=LineString([F(15.9,45.5),F(15.901,45.5)])
assert abs(km(MultiLineString([a,b]))-(km(a)+km(b)))<1e-9
# Ponovljeni prehod mora ostati v dolžini tudi po obrezovanju.
repeat=LineString([F(15.1,45.5),F(15.101,45.5),F(15.1,45.5)])
assert abs(clipped_km(repeat,repeat.buffer(100))-km(repeat))<1e-8
ET.parse(P/'poti-zemljevid.svg')
errors=[];requests=[]
with sync_playwright() as pw:
    browser=pw.chromium.launch()
    page=browser.new_page(viewport={'width':1440,'height':1050})
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('request',lambda r:requests.append(r.url))
    page.goto((P/'porocilo.html').as_uri())
    page.locator('#poti').scroll_into_view_if_needed()
    assert page.locator('#poti .pot-route').count()==len(d['poti'])
    assert page.locator('#poti .pot-place').count()==d['stevilo_naselij_osm']
    default=page.locator('#poti svg').get_attribute('viewBox')
    page.locator('#poti .poti-zoom [data-action=in]').click()
    assert page.locator('#poti svg').get_attribute('viewBox')!=default
    page.locator('#poti .poti-zoom [data-action=reset]').click()
    assert page.locator('#poti svg').get_attribute('viewBox')==default
    page.locator('#poti-search').fill('gricki kal')
    assert '1 od 43' in page.locator('#poti-count').inner_text()
    page.locator('#poti details summary').click()
    assert page.locator('#poti-tabela tbody tr:visible').count()==1
    page.locator('#poti-tabela tbody tr:visible button').click()
    assert 'Grički kal' in page.locator('#poti .poti-panel').inner_text()
    assert '4,6 km' in page.locator('#poti .poti-panel').inner_text()
    page.locator('#poti-search').fill('')
    page.locator('#poti-kolo').uncheck()
    assert '26 od 43' in page.locator('#poti-count').inner_text()
    page.locator('#poti-zunaj').uncheck()
    assert '14 od 43' in page.locator('#poti-count').inner_text()
    page.locator('#poti-kolo').check();page.locator('#poti-zunaj').check()
    page.locator('#poti-pas').select_option('1000')
    assert page.locator('#poti .pot-buffer[data-radius="1000"]').evaluate('(e)=>getComputedStyle(e).display')!='none'
    page.locator('#poti .poti-zoom [data-action=reset]').click()
    page.locator('#poti .poti-layout').scroll_into_view_if_needed()
    page.screenshot(path=str(P/'preverjanje/poti-namizje.png'))
    for width in [320,390,768,1440,1920]:
        page.set_viewport_size({'width':width,'height':950})
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),width
    page.set_viewport_size({'width':390,'height':900})
    page.locator('#poti .poti-layout').scroll_into_view_if_needed()
    page.screenshot(path=str(P/'preverjanje/poti-telefon.png'))
    # Tisk vedno obnovi celoten občinski prikaz; po tisku vrne uporabnikove filtre.
    page.locator('#poti-kolo').uncheck();page.locator('#poti-search').fill('gricki')
    page.evaluate("window.dispatchEvent(new Event('beforeprint'))")
    assert page.locator('#poti-kolo').is_checked() and page.locator('#poti-search').input_value()==''
    page.evaluate("window.dispatchEvent(new Event('afterprint'))")
    assert not page.locator('#poti-kolo').is_checked() and page.locator('#poti-search').input_value()=='gricki'
    assert not errors,errors
    assert not any(u.startswith(('https:','http:')) for u in requests),requests
    browser.close()
print(json.dumps({'izvirniki':'kontrolne vsote ustrezajo','geometrija':'preseki, razdalje, segmenti in monotoni pasovi preverjeni','zemljevid':'filtri, iskanje brez šumnikov, izbor, povečava, izvoz SVG, tisk, 5 širin, brez omrežja in napak JavaScript'},ensure_ascii=False))
