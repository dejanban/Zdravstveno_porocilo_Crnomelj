from razisci_okolje_20260924 import *
for slug,u in [('vrtovi-rct','https://pmc.ncbi.nlm.nih.gov/articles/PMC9936951/'),('zrak-februar-2025','https://arso.si/o%20agenciji/knji%C5%BEnica/mese%C4%8Dni%20bilten/Nase%20okolje%20-%20februar%202025.pdf')]:
    try: save(u,slug); print(slug,flush=True)
    except Exception as e: print(str(e),flush=True)
base='https://www.arso.gov.si/zrak/kakovost%20zraka/podatki/'
soup=BeautifulSoup((OUT/'arso-podatki.html').read_bytes(),'html.parser')
for a in soup.select('a[href]'):
    title=a.get_text(' ',strip=True)
    if ('mesečne' in title and ('PM10' in title or 'PM2' in title)) or ('Preseganj' in title and 'PM10' in title) or ('Črnomlju' in title and ('kovin' in title or 'ogljikovodikov' in title)):
        u=urljoin(base,a['href']); slug='zrak-podatki-'+str(len(ledger))
        try: save(u,slug); print(slug,title,flush=True)
        except Exception as e: print(str(e),flush=True)
