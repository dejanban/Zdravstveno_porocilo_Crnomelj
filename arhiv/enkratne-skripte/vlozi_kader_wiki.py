"""Enkratna vključitev popisa v obstoječe povezane strani in evidenco dela."""
from pathlib import Path
import re,json,os
P=Path(__file__).resolve().parent; ROOT=P.parents[1]
refs=json.loads((P/'kader-sport-viri.json').read_text(encoding='utf-8'))
def read(p):return p.read_text(encoding='utf-8')
def write(p,s):p.write_text(s,encoding='utf-8')
def before(p,marker,text):
 s=read(p)
 if text.strip() not in s:
  assert marker in s,(p,marker)
  write(p,s.replace(marker,text+'\n\n'+marker,1))

topic=ROOT/'wiki/topics/social-affairs/zd-crnomelj-pregled.md'
new='### Dopolnitev kadrovske slike, 21. 9. 2026\n\nProgram ZD 2026 konkretizira vrzel družinske medicine: **7,53 priznanega in 5,53 zagotovljenega tima**, razlika **2,00 tima** za območje ZD, vključno s Semičem. [1] Seznam ZZZS na 1. 9. 2026 po preverbi lokacij pokaže **6 družinskih zdravnikov in 2 pediatrinji na območju občine Črnomelj** v dejavnostih opredeljevanja; to ni celoten zdravniški kader vseh specialnosti. [2] Pri treh imenovanih psihologinjah je Sabina Prah odsotna do nadaljnjega; objavljeni urniki in kratkotrajne odsotnosti ne dokazujejo treh hkrati razpoložljivih izvajalk. [3]\n\nRazčlenitev javne in zasebne ponudbe, DSO, psihiatrije, prehrane, fizioterapije, kineziologije ter športa je v [[../../analysis/synthesis/zdravstveni-kader-in-sport-crnomelj-2026]]. Evropsko povprečje zdravnikov ni občinski normativ. Prednostni ukrepi so zapolnitev priznanega programa, jasna pot odraslih do duševnozdravstvene obravnave in datiran imenik dejanskih lokalnih zmogljivosti. Obstoječa ocena širše zdravstvene teme ostaja.\n'
before(topic,'## Ključna dejstva',new)
s=read(topic)
if '## Literatura' not in s:
 s+='\n## Literatura\n\n'
 for i,key in enumerate(['plan2026','zzzsizvlecek','dmz'],1):
  r=refs[key];local=Path(os.path.relpath(ROOT/r['local'],topic.parent)).as_posix()
  s+=f'[{i}] »{r["title"]},« {r["publisher"]}, {r["date"]}. [Na spletu]. Dostopno: {r["url"]}. [Dostopano: 21. september 2026]. Lokalna kopija: [[{local}]].\n\n'
 write(topic,s)
for rel in ['wiki/entities/institutions/ckz-crnomelj.md','wiki/entities/institutions/zd-crnomelj.md','wiki/topics/tourism/pesposti-kolesarske-poti-sportni-objekti.md']:
 p=ROOT/rel
 text='**Dopolnitev 21. 9. 2026:** [[../../analysis/synthesis/zdravstveni-kader-in-sport-crnomelj-2026|Zdravstveni kader, duševno zdravje in šport]] vsebuje datiran popis javne in zasebne ponudbe, ločuje osebe od obsega dela ter dokumentirano vadbo od imenikov društev. Prejšnjih številk in seznamov ne uporabljati kot popoln popis trenutno aktivnih izvajalcev.'
 before(p,'## Povezane strani',text)
 s=read(p)
 if '2026-09-21 — povezana' not in s:s+='\n2026-09-21 — povezana nova sinteza kadra in športne ponudbe; osnovna ocena nespremenjena.\n'
 write(p,s)

candidate=ROOT/'wiki/analysis/synthesis/pregled-za-kandidata.md';s=read(candidate)
old='- Zavod v letnem poročilu navaja pomanjkanje zdravnikov. Manjka primerljiv celovit pregled dosega, stroškov in izidov CKZ.'
new='- Program ZD 2026 konkretizira primanjkljaj **2,00 tima družinske medicine** za območje ZD, tudi Semič. Pri psihološki pomoči zaposlenih ne smemo enačiti s prisotnimi izvajalci; odrasli potrebujejo jasno pot od CKZ do specialistične obravnave. [[zdravstveni-kader-in-sport-crnomelj-2026|Preverjeni popis kadra, zasebnikov in športa]]. Manjka primerljiv celovit pregled dosega, stroškov in izidov CKZ.'
if old in s:s=s.replace(old,new,1)
old='**Takoj / prvo leto:** občina in ZD naj objavita kadrovski načrt, CKZ pa agregat uporabnikov, izvedb, stroškov in izhodiščnih rezultatov; s šolami vzpostaviti redno gibanje in izboljševanje prehranskega okolja.'
new='**Takoj / prvo leto:** ZD naj pripravi načrt zapolnitve priznanega programa po lokacijah in pot do psihološke/psihiatrične pomoči odraslim. Občina in CKZ naj s klubi objavita preverjen imenik vadb, cen in prostih mest; CKZ naj poroča o uporabnikih, stroških in izidih. S šolami ohranjati redno gibanje in izboljševati prehransko okolje.'
if old in s:s=s.replace(old,new,1)
line='Zadnja preverba zdravstvenega razdelka: 2026-09-21 — kadrovski program, psihološka pomoč, zasebniki in šport; status ❌ širše zdravstvene teme ostaja, ocena CKZ ostaja 3,4/5. Druge teme niso bile ponovno vsebinsko preverjene.'
if line not in s:s+='\n'+line+'\n'
write(candidate,s)

idx=ROOT/'wiki/index.md';s=read(idx)
s=re.sub(r'^Zadnja posodobitev:.*$', 'Zadnja posodobitev: 2026-09-21 — zdravstveni kader, psihološka pomoč in šport: 38 virov, ZZZS 1. 9. 2026, vrzel 2,00 tima in omejitve zasebnega popisa; dopolnjeno samostojno zdravstveno poročilo.',s,count=1,flags=re.M)
insert='\n| Nova stran | Kategorija in povzetek |\n| --- | --- |\n| [[analysis/synthesis/zdravstveni-kader-in-sport-crnomelj-2026]] | Sinteza; 38 virov; psihološka pomoč, javni in zasebni kader, dejanske lokacije, zdravniki in šport; 21. 9. 2026. |\n| [[sources/source-summaries/kader-sport-crnomelj-2026]] | Povzetek virov; datum, zanesljivost in dokazna sled popisa; povezano z ZD, CKZ in športom. |\n'
if '[[analysis/synthesis/zdravstveni-kader-in-sport-crnomelj-2026]]' not in s:
 m=re.search(r'^Zadnja posodobitev:.*$',s,re.M);s=s[:m.end()]+'\n'+insert+s[m.end():]
write(idx,s)

handoff=ROOT/'wiki/naslednji-koraki.md';s=read(handoff)
block='### Kader, psihološka pomoč in šport — 21. 9. 2026\n\nDokončan spletni dokazni popis v [[analysis/synthesis/zdravstveni-kader-in-sport-crnomelj-2026]] in [[sources/source-summaries/kader-sport-crnomelj-2026]] (38 uporabljenih virov). Glavne ugotovitve: 3 zaposlene psihologinje konec 2025, dve z urnikom in ena odsotna do nadaljnjega; DSO ima gostujočega nevropsihiatra. ZD 6 fizioterapevtov, DSO še 1; skupina dietetikov/kineziologov v ZD skupaj 4. ZZZS 1. 9. 2026: v občini 6 izbranih družinskih zdravnikov in 2 pediatrinji; Gabrijela Plut v Semiču izločena, zasebnika Suzana Milenković in Miro Vuković vključena. Vrzel programa ZD je 2,00 tima, vključuje tudi Semič. Ni evropskega občinskega normativa, iz katerega bi smeli izračunati navidezno natančen primanjkljaj. Zasebni kader in trenerji niso v celoti prešteti; navedeni so potrjeni deli in minimumi, ne ničle. Športna ponudba ločuje dokumentirano vadbo 2025, ponudbo ob zajemu in imenik klubov.\n\nV `` je izvorni dokument `kader-sport-vsebina.md`; ponovljiva gradnja: `python -X utf8 pripravi_kader_sport.py`, nato `python -X utf8 zgradi_porocilo.py` in `python -X utf8 preveri_porocilo.py`. Prvi skript izdela wiki sintezo, povzetek virov in HTML razdelke; vsebino zato urejaj v izvornem dokumentu. Skripta `vlozi_kader_wiki.py` je enkratna vključitev, ne del običajne gradnje. Podatki ZZZS v `kader-zzzs-20260901.json`, izvirni XLSX in PDF v `viri/`, spletne kopije `viri/splet/kader-sport-20260921-*`. DSO tabela str. 43–44 vizualno preverjena; celotni skenirani PDF še ni OCR-an.\n\nOdprto: z izvajalci potrditi točno lokalno prisotnost, kvalifikacije, ure in prosta mesta; pridobiti število prebivalcev brez izbranega zdravnika ter polni register treningov 2026/27. Noben izvajalec ni bil kontaktiran. Popis ne obravnava zaključka postopka nekdanjega direktorja; stare navedbe v zgodovinskih delih niso nova preverba vodstva.\n\n'
if '### Kader, psihološka pomoč in šport — 21. 9. 2026' not in s:
 s=s.replace('# Naslednji koraki in trenutno stanje seje\n\n','# Naslednji koraki in trenutno stanje seje\n\n'+block,1)
write(handoff,s)
print('Povezane strani, kandidat, kazalo in predaja posodobljeni.')
