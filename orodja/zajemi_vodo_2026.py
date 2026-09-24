from razisci_okolje_20260924 import *
soup=BeautifulSoup((OUT/'komunala-vzorci-crnomelj.html').read_bytes(),'html.parser')
seen=set()
for a in soup.select('a[href]'):
    title=a.get_text(' ',strip=True)
    if '.pdf' not in a['href'] or '2026' not in title: continue
    u=urljoin('https://www.komunala-crnomelj.si',a['href'])
    if u in seen: continue
    seen.add(u)
    slug='vzorec-2026-'+str(len(seen))
    try: save(u,slug)
    except Exception as e: print('NAPAKA',str(e),flush=True)
print('Prenesenih povezav',len(seen),flush=True)
