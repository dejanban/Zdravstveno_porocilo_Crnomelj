from pathlib import Path
import re
P=Path(__file__).resolve().parent;R=P.parents[1]
p=P/'pripravi_starost.py';s=p.read_text(encoding='utf-8')
s=s.replace('<svg viewBox="0 0 710 280"','<svg style="width:100%;height:auto" viewBox="0 0 710 280"')
s=s.replace('6,0 % v Sloveniji','5,8 % v Sloveniji (pri objavi na eno decimalko)')
s=s.replace('5,8 proti 6,0 %','5,8 proti 5,8 % (objavljeno na eno decimalko)')
s=s.replace('Preverjeno, da se vsota 86 starostnih razredov ujema s skupnim prebivalstvom za obe območji in vseh 19 let.','Vsota 86 starostnih razredov se ujema s skupnim prebivalstvom v 37 od 38 kombinacij območja in leta. Za Slovenijo 2008 je že v izvirniku razlika 2 oseb (skupaj 2.025.866, vsota 2.025.864); razlog ni ugotovljen. Glavni prikaz 2011–2026 nima tega neskladja.')
s=s.replace('Kontrole: 38 vsot starosti in 38 deležev 65+ uspešnih.','Kontrole: 37 vsot se ujema; Slovenija 2008 ima dokumentirano razliko 2 oseb. Vsi deleži 65+ preverjeni.')
p.write_text(s,encoding='utf-8')
p=P/'preveri_porocilo.py';s=p.read_text(encoding='utf-8').replace("'viri':33","'viri':len(json.loads((P/'literatura.json').read_text(encoding='utf-8')))")
s=s.replace("assert page.locator('.chart svg').count()==11","assert page.locator('.chart svg').count()==11\n    assert page.locator('#starost svg').count()==1\n    assert '2026' in page.locator('.readout').first.inner_text()")
p.write_text(s,encoding='utf-8')

marker='## Dopolnitev 2026-09-19 — starost prebivalcev'
for rel,text in [
('wiki/topics/social-affairs/zdravje-obcina-nijz-trendi.md','SURS na 1. 1. 2026 potrjuje povprečno starost 45,9 leta (Slovenija 44,6), 3.616 prebivalcev 65+ (25,5 %) in 2.052 otrok 0–14 let. Delež 80+ je po zaokroževanju 5,8 % na obeh ravneh, kar ne pomeni enake celotne starostne sestave. Celotna tabela, primarni viri IEEE in pojasnila: [[../../analysis/synthesis/starost-prebivalcev-crnomelj]].'),
('wiki/analysis/synthesis/zdravstvo-preventiva-ckz-2026.md','Dodana [[starost-prebivalcev-crnomelj|starostna sestava]]: povprečna starost 42,0 → 45,9 leta (2011–2026), število 65+ 2.420 → 3.616. Načrtovanje preventive in oskrbe naj upošteva starost ter dejanske funkcionalne potrebe; starost ni samostojna ocena kakovosti CKZ.'),
('wiki/index.md','- [[analysis/synthesis/starost-prebivalcev-crnomelj]] — sinteza; starost in število ljudi po letih 2011–2026 ter posamezne starosti za 2026, dva podatkovna vira SURS in metodološka pojasnila. Povezano z zdravstvenim poročilom in trendi NIJZ; zadnja posodobitev 2026-09-19.')]:
 p=R/rel;s=p.read_text(encoding='utf-8')
 if marker not in s:p.write_text(s+'\n\n'+marker+'\n\n'+text+'\n',encoding='utf-8')
p=R/'wiki/analysis/synthesis/pregled-za-kandidata.md';s=p.read_text(encoding='utf-8');anchor='- Zavod v letnem poročilu navaja pomanjkanje zdravnikov.'
if 'Starostna sestava (SURS, 1. 1. 2026)' not in s:
 s=s.replace(anchor,'- Starostna sestava (SURS, 1. 1. 2026): 45,9 leta v povprečju, 25,5 % prebivalcev je starih 65+. Število 65+ je od 2011 naraslo za 49,4 %. Načrtovati zmogljivosti preventive in oskrbe po dejanskih potrebah; [[starost-prebivalcev-crnomelj|podatki in omejitve]]. Status zdravstva ostaja nespremenjen.\n'+anchor)
 s+='\nZadnja dopolnitev zdravstvenega razdelka: 2026-09-19 — preverjena starostna sestava SURS in načrtovanje oskrbe.\n';p.write_text(s,encoding='utf-8')
p=R/'wiki/naslednji-koraki.md';s=p.read_text(encoding='utf-8');i=s.find('\n')
if '### Starost prebivalcev — končano' not in s:
 s=s[:i]+'''\n\n### Starost prebivalcev — končano 2026-09-19

Zdravstveno poročilo dopolnjeno s poglavjem `#starost`: SURS na 1. 1. 2026, letni prikaz 2011–2026, povprečna starost in skupine 0–14/15–64/65+/80+, petletni razredi ter posamezne starosti 0–84 in 85+. Podatki SURS JSON/CSV in poizvedbe v mapi poročila, IEEE kopije v raw/web. Vir vsebuje razliko dveh oseb pri vsoti starosti za Slovenijo 2008; glavni trend 2011–2026 se v celoti ujema. Delež 80+ je za obe območji po zaokroževanju 5,8 %, povprečna starost pa je različna (45,9/44,6).

Gradnja: `python -X utf8 pripravi_starost.py`, nato `python -X utf8 zgradi_porocilo.py` in `python -X utf8 preveri_porocilo.py` v mapi poročila. Enkratnega vzdrževalnega skripta `dopolni_starost.py` in starega `posodobi_wiki.py` ne zaganjajte za običajno gradnjo. Novi vir: [[analysis/synthesis/starost-prebivalcev-crnomelj]]. Iz grafov NIJZ so odstranjeni prazni repni stolpci XLSX, da drsnik pravilno privzeto kaže 2026. Nadaljnja naloga: starost po naseljih in dejanske potrebe po oskrbi.
'''+s[i:];p.write_text(s,encoding='utf-8')
p=R/'wiki/log.md';s=p.read_text(encoding='utf-8')
if 'query | Starost prebivalcev in spremembe skozi leta' not in s:
 with p.open('a',encoding='utf-8') as file:file.write('''\n\n## [2026-09-19] query | Starost prebivalcev in spremembe skozi leta

- Action: SURS neposredno preverjen za 2008–2026; zdravstveno poročilo dopolnjeno z letno tabelo 2011–2026, grafom povprečne starosti ter razdelitvijo po posameznih starostih za 2026. Ohranjeni izvori, poizvedbe in CSV. Popravljena obdelava praznih repnih stolpcev NIJZ.
- Sources used: SURS SiStat 05C4003S, 05C4008S in metodološka pojasnila; stanje 1. januar, oba spola skupaj, Črnomelj in Slovenija.
- Pages created: analysis/synthesis/starost-prebivalcev-crnomelj.
- Pages updated: zdravstveno poročilo HTML/PDF, trendi NIJZ, raziskovalna sinteza zdravstva, pregled-za-kandidata, index, naslednji-koraki.
- Open questions: Razlike med naselji, vzroki spremembe po starosti, potrebe po oskrbi. V izvornem prenosu Slovenije 2008 razlika 2 oseb med skupnim številom in vsoto starosti; razlog ni pojasnjen, glavni prikaz 2011–2026 ni prizadet.
- Follow-up tasks: Pridobiti starost po naseljih, selitveno strukturo ter agregate dostopnosti oskrbe in dosega CKZ.
''')
