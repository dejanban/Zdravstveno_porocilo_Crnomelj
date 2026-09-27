from pathlib import Path
import sys,json,re,hashlib
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tmp/okolje-runtime'))
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import fitz

def main():
    results={'viewports':[],'errors':[],'requests':[]}
    s=BeautifulSoup((ROOT/'porocilo.html').read_text(encoding='utf-8'),'html.parser')
    ids=[x['id'] for x in s.select('[id]')]
    assert len(ids)==len(set(ids)), 'Podvojeni HTML id'
    bad=[a['href'] for a in s.select('a[href^="#"]') if a['href'][1:] and a['href'][1:] not in ids]
    assert not bad,bad
    assert not re.search(r'\[@[^\]]+\]',str(s)), 'Nerazrešene navedbe'
    results['references']=len(s.select('#literatura p[id]'))
    with sync_playwright() as p:
        b=p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True)
        page=b.new_page()
        page.on('pageerror',lambda e:results['errors'].append(str(e)))
        page.on('request',lambda r: results['requests'].append(r.url) if r.url.startswith(('http:','https:')) else None)
        for width in [1440,1024,768,390,360]:
            page.set_viewport_size({'width':width,'height':1000})
            page.goto((ROOT/'porocilo.html').as_uri(),wait_until='load')
            page.emulate_media(reduced_motion='reduce')
            dims=page.evaluate('({width:innerWidth,scroll:document.documentElement.scrollWidth})')
            assert dims['scroll']<=width+1, dims
            assert page.locator('#pitna-voda').count()==1
            # Obstoječi drsnik mora še vedno posodabljati izpis.
            slider=page.locator('.chart input[type=range]').first
            if slider.count():
                slider.evaluate('(e)=>{e.value=e.min||0;e.dispatchEvent(new Event("input",{bubbles:true}))}')
                assert 'Izdaja' in page.locator('.chart .readout').first.inner_text()
            for sid in ['okolje-zdravje','pitna-voda','zrak']:
                if width in [1440,390]:
                    page.locator('#'+sid).scroll_into_view_if_needed()
                    page.evaluate('(id)=>document.getElementById(id).scrollIntoView({block:"start"})',sid)
                    page.screenshot(path=str(ROOT/f'preverjanje/{sid}-{width}.png'))
            results['viewports'].append(dims)
        page.set_viewport_size({'width':1440,'height':1000})
        page.goto((ROOT/'porocilo.html').as_uri(),wait_until='load')
        page.evaluate('document.querySelectorAll("details").forEach(x=>x.open=true)')
        page.pdf(path=str(ROOT/'porocilo.pdf'),format='A4',print_background=True,prefer_css_page_size=True)
        b.close()
    assert not results['errors'],results['errors']
    assert not results['requests'],results['requests']
    d=fitz.open(ROOT/'porocilo.pdf');results['pdf_pages']=len(d)
    relevant=[]
    for i,p in enumerate(d):
        t=p.get_text()
        if any(q in t for q in ['Razvitost, dohodki, stres','Pitna voda: pregled','Kakovost zraka: meritve','Benzo(a)piren in kovine','Kaj se je zgodilo v Adlešičih','Uredniška ocena javno']):
            p.get_pixmap(matrix=fitz.Matrix(1.2,1.2)).save(ROOT/f'preverjanje/okolje-pdf-{i+1}.png');relevant.append(i+1)
    results['rendered_pages']=relevant
    (ROOT/'preverjanje/okolje-porocilo.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(results,ensure_ascii=False,indent=2))
if __name__=='__main__':
    from preveri_prenovo import main as preveri_prenovo
    preveri_prenovo()
