from pathlib import Path
import json,re,unicodedata,csv
P=Path(__file__).resolve().parent
def norm(s): return ''.join(c for c in unicodedata.normalize('NFD',s.lower()) if unicodedata.category(c)!='Mn')
def process():
    d=json.loads((P/'zajem-odeon.json').read_text(encoding='utf-8')); rows=[]
    overrides=json.loads((P/'pregled-registra.json').read_text(encoding='utf-8')) if (P/'pregled-registra.json').exists() else {}
    for r in d['records']:
        text=' '.join(r['text'].split()); t=norm(r['title']+' '+text)
        local=re.search(r'(?:ckz|czk|cent\w* za krepitev zdravja|zdravstveno.?vzgojn\w* centr\w*|zvc).{0,65}(?:crnomelj|bela krajina|bele krajine)',t)
        explicit_local=re.search(r'(?:ckz|czk|cent\w* za krepitev zdravja|zvc).{0,25}crnomelj',t)
        other=re.search(r'(?:ckz|cent\w* za krepitev zdravja).{0,65}metlik',t)
        if other and not explicit_local: local=None
        if local: affiliation='Črnomelj'; reason='V besedilu je izrecno naveden črnomaljski CKZ oziroma nekdanji naziv Bela krajina.'
        elif other: affiliation='Drug center';reason='CKZ Metlika oziroma drug izvajalec; ni dokaza vloge CKZ Črnomelj.'
        elif re.search(r'krepitev zdravja|\bckz\b|\bzvc\b',t): affiliation='Nejasno';reason='Povezava s CKZ Črnomelj ni dovolj izrecna; ne vključujemo v njegovo oceno.'
        else: affiliation='Izločeno';reason='Iskalni zadetek brez potrjene relevantnosti za CKZ.'
        if any(w in t for w in ['preklic dejavnosti','dejavnosti odpadejo','odpovedan']): status='Odpoved / preklic'
        elif '/koledar-dogodkov/' in r['url']: status='Vabilo'
        elif re.search(r'vabimo|vabljeni|bo potekal|bodo potekal|bo jutri|bo v soboto',t) and not re.search('smo izvedli|smo pripravili|je potekal|so izvedl|uspesno zakljuc',t):status='Vabilo'
        elif re.search(r'potekal|izvedl|obiskali|smo|udelezili|zakljuc|pripravili|odprtje',t):status='Poročilo / novica'
        else:status='Informativna objava'
        date=r['dates'][0][:10] if r['dates'] else ''
        eventdate=''
        for ld in r['json_ld']:
            try:
                j=json.loads(ld)
                if isinstance(j,dict) and j.get('@type')=='Event' and j.get('startDate'):eventdate=j['startDate'][:10]
            except (ValueError,TypeError):pass
        category='Skupnost in splošno zdravje'
        for pattern,label in [(r'zob|ustn|higien','Ustno zdravje'),(r'prehran|huj|vitamin|zdravo jem|sladoled','Prehrana in telesna masa'),(r'tesnob|depres|stres|sprosc|odnosi|dusevn','Duševno zdravje'),(r'sladkor|krvni tlak|mascobe v krvi','Presnovno in srčno-žilno zdravje'),(r'kajenj|alkohol|odvisnost','Tvegana vedenja'),(r'roznat|brkat|rak|samopregled','Ozaveščanje o raku'),(r'porod|starsevstvo|nosec','Starši in otroci'),(r'gib|hoj|pohod|sport|vadb|rolanj|vodne|vodni','Gibanje')]:
            if re.search(pattern,t):category=label;break
        excerpt=''
        m=local or other or re.search('krepitev zdravja|ckz',t)
        if m:excerpt=text[max(0,m.start()-len(r['title'])-50):m.end()+120][:280]
        else:excerpt=text[:230]
        row={'url':r['url'],'naslov':r['title'],'pripadnost':affiliation,'vrsta':status,'datum_objave':date,'datum_dogodka':eventdate,'tema':category,'razlog':reason,'izsek':excerpt,'lokalna_kopija':r['local']}
        row.update(overrides.get(r['url'],{}))
        if (row['datum_objave'] or row['datum_dogodka'])>'2026-09-19':row['pripadnost']='Po presečnem datumu';row['razlog']='Ne šteje v retrospektivno oceno do 19. 9. 2026.'
        rows.append(row)
    rows.sort(key=lambda r:(r['datum_objave'] or r['datum_dogodka'] or '0000',r['naslov']),reverse=True)
    (P/'register-dogodkov.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    with (P/'register-dogodkov.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=';');w.writeheader();w.writerows(rows)
    from collections import Counter
    stats={'pregledane_objave':len(rows),'lokalne_datoteke':d['local_files_scanned'],'iskalne_strani':len(d['search_pages']),'napake':d['failures'],'pripadnost':dict(Counter(r['pripadnost'] for r in rows)),'vrste_crnomelj':dict(Counter(r['vrsta'] for r in rows if r['pripadnost']=='Črnomelj'))}
    (P/'statistika-registra.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Objave:',len(rows),'nere?eni zajemi:',len(stats['napake']))
    return rows
if __name__=='__main__':process()
