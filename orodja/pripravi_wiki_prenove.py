"""Povzetki novih virov in dokumentirana povezava s CKZ; brez novih trditev."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
def write(name,text):
 p=ROOT/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8')
def main():
 records=json.loads((ROOT/'podatki/spanje/spanje-viri.json').read_text(encoding='utf-8'))
 text=(ROOT/'vsebina/spanje-digitalne-navade.md').read_text(encoding='utf-8')
 research=text.split('### Pregled ključnih raziskav')[1].split('### Facebook')[0]
 aggregate='# Spanje in digitalne navade: pregled virov\n\nPreverjeno 25. septembra 2026. Usmerjeni izbor osmih raziskav in dveh objav NIJZ, ne izčrpen sistematični pregled. Glavna sinteza: [[../../topics/social-affairs/spanje-digitalne-navade.md]].\n\n| Vir | Vrsta in obseg | Lokalni povzetek |\n|---|---|---|\n'
 for r in records:
  slug=r['slug'];row=next((line for line in research.splitlines() if '[@'+slug+']' in line),'')
  cols=row.strip('|').split('|') if row else []
  finding=cols[2].strip() if cols else ('NIJZ opisuje okvir za usklajeno obravnavo zaslonov in vsebin pri otrocih.' if slug=='nijz-zasloni' else 'NIJZ povezuje spanje s šolskimi obveznostmi, večernimi navadami, gibanjem in podporo ob težavah.')
  limitation=cols[3].strip() if cols else 'Uradno strokovno sporočilo; ne vsebuje ocene potreb ali učinka programa v Črnomlju.'
  body=f'# {r["title"]}\n\n## Vir in zanesljivost\n\n| Podatek | Vrednost |\n|---|---|\n| Izdajatelj in leto | {r["publisher"]}; {r["date"]} |\n| Vrsta | '+('Uradna strokovna spletna objava' if slug.startswith('nijz') else 'Recenzirana raziskovalna objava')+f' |\n| Prebrano | {r["scope"]} |\n| Zanesljivost | Srednja za prenos ugotovitev; omejitve spodaj. NIJZ ima visoko zanesljivost za vsebino lastnih priporočil. |\n| Dostop | 25. september 2026 |\n\n## Ključna ugotovitev\n\n{finding} [1]\n\n## Omejitve\n\n{limitation} [1] To ni lokalna meritev za Črnomelj.\n\n## Povezane strani\n\n[[../../topics/social-affairs/spanje-digitalne-navade.md]]; [[spanje-digitalni-viri.md]].\n\n## Literatura\n\n[1] »{r["title"]},« {r["publisher"]}, {r["date"]}. [Na spletu]. Dostopno: {r["url"]}. [Dostopano: 25. september 2026]. Lokalna kopija: [[../../../{r["local"]}]]. Izvirni prenos: [[../../../{r["path"]}]].\n'
  body=re.sub(r'\[@[^\]]+\]','[1]',body)
  write('wiki/sources/source-summaries/spanje-'+slug+'.md',body)
  safe_title=r['title'].replace('|','\\|')
  aggregate+=f'| {safe_title} | {r["scope"]} | [[spanje-{slug}.md]] |\n'
 aggregate+='\n## Metoda in omejitve\n\nIskanje preko primarnih objav, PubMed/Europe PMC in NIJZ. Iskalni izrazi in obseg so zapisani na tematski strani. Štirje povzetki omejujejo presojo metod; polnih besedil ni dopustno predstavljati kot prebranih. Dodatne priloge niso vključene. Vsak vir ima zajem, kontrolno vsoto ter lastni povzetek z literaturo.\n'
 write('wiki/sources/source-summaries/spanje-digitalni-viri.md',aggregate)
 print('Pripravljenih',len(records),'posamičnih povzetkov in kazalo virov.')
if __name__=='__main__':main()
