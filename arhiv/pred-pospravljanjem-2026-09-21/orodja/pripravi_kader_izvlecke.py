from pathlib import Path
import json,openpyxl
P=Path(__file__).resolve().parent.parent; ROOT=P
refs=json.loads((P/'kader-sport-viri.json').read_text(encoding='utf-8'))
def save(key,original,title,body):
    r=dict(refs[original]);r['title']=title;r['local']=f'viri/splet/kader-sport-20260921-{key}.md'
    dst=ROOT/r['local']
    if not dst.exists():
        dst.write_text(f'---\nurl: {r["url"]}\nnaslov: {title}\nizdajatelj: {r["publisher"]}\ndostopano: 2026-09-21\nmetoda zajema: WebFetch; lokalni izvleček iz prenesenega izvirnika\n---\n\n'+body,encoding='utf-8')
    refs[key]=r
w=openpyxl.load_workbook(P/'viri/kader-sport-zzzs.xlsx',data_only=True)
rows=[list(row) for row in w.active.values if any('ČRNOMELJ' in str(v).upper() for v in row)]
head=['zdravnik','izvajalec','dejavnost','timi','opredeljeni','GK_na_tim','sprejema']
data=[{k:row[i] for k,i in zip(head,[7,3,9,10,11,14,18])} for row in rows]
(P/'kader-zzzs-20260901.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
body='Stanje 1. 9. 2026. Naslov izvajalca ni nujno lokacija ambulante: Gabrijela Plut dela v Semiču; Valerija Šimec v Vinici. Enoličnost preverjena po šifri zdravnika.\n\n| '+' | '.join(head)+' |\n|'+' --- |'*len(head)+'\n'
body+='\n'.join('| '+' | '.join(str(d[k]) for k in head)+' |' for d in data)
body+='\n\nCelotna preglednica: viri/kader-sport-zzzs.xlsx. Uporabljene izvirne vrstice 1330–1338. Izvirna glava in pojasnila tudi v kader-sport-20260921-zzzsdata.md. GK pomeni glavarinski količnik, ne števila ljudi.\n'
save('zzzsizvlecek','zzzsdata','Aktivni zdravniki ZZZS: preverjeni izvleček za Črnomelj in Semič',body)
body='## Preverjeni prepis iz tabele 11.2, str. 43–44\n\nTabela ima stolpca 31. 12. 2024 in 31. 12. 2025. Vizualno preverjena oba lista. Za 31. 12. 2025: fizioterapevt – 1 delavka; dietetik VII/1 (II) – pripravnik – 1 delavka; delovni terapevt – 3 delavke. Delovnih terapevtov ne šteti med psihoterapevte.\n\n## OCR uporabljenih strani (možne napake prepoznave)\n\n'
for n in [43,44]:body+=f'### Stran {n}\n\n'+(P/f'preverjanje/dso2025-{n}.txt').read_text(encoding='utf-8')+'\n'
save('dsokader','dso2025','DSO Črnomelj 2025: kadrovska tabela, str. 43–44',body)
(P/'kader-sport-viri.json').write_text(json.dumps(refs,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('ZZZS:',len(data),'enoličnih zdravnikov za izvajalce s sedežem Črnomelj; od tega ena ambulanta v Semiču. DSO: vizualno preverjen izvleček shranjen.')
