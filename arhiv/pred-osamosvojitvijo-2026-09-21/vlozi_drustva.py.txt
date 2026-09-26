from pathlib import Path
import re,json
P=Path(__file__).resolve().parent;R=P.parents[1]
refs=json.loads((P/'drustva-viri.json').read_text(encoding='utf-8'));ref=refs['drustva-ckz-imenik']
p=R/'wiki/entities/institutions/ckz-crnomelj.md';s=p.read_text(encoding='utf-8')
if '### Dopolnitev 2026-09-20 — javni imenik podpore' not in s:
 n=max(map(int,re.findall(r'\[(\d+)\]',s)))+1
 text=f'### Dopolnitev 2026-09-20 — javni imenik podpore\n\nCKZ je septembra 2025 izdal **Povezani za zdravje**, zbirnik z lokalnimi kontakti ustanov in društev. To dodatno podpira oceno njegovega obveščanja; cilj je posodabljanje obstoječega imenika. Ocena 3,4/5 ostaja, ker vir ne zapolnjuje vrzeli merjenja dosega in izidov. [{n}] Preverjeni dopolnjeni imenik: [[../associations/zdravstvena-podporna-mreza]].\n\n'
 s=s.replace('## Literatura',text+'## Literatura',1)
 entry=f'[{n}] »{ref["title"]},« ZD Črnomelj, september 2025. [Na spletu]. Dostopno: {ref["url"]}. [Dostopano: 20. september 2026]. Lokalna kopija: [[../../../{ref["local"]}]]. Natisnjene str. 33–34, 39–40.\n\n'
 s=s.replace('## Zadnja posodobitev',entry+'## Zadnja posodobitev',1)
 s+='\n2026-09-20 — pregledan zbirnik CKZ in dopolnjena podporna mreža; skupna ocena nespremenjena.\n';p.write_text(s,encoding='utf-8')
p=R/'wiki/entities/associations/pregled-drustev.md';s=p.read_text(encoding='utf-8')
old='vodi tudi **Program Mira**, območni center za duševno zdravje.'
if old in s:s=s.replace(old,'Prejšnja navedba, da vodi Program Mira oziroma območni center za duševno zdravje, ni potrjena in je umaknjena; Program MIRA je nacionalni okvir, ne dokaz take dejavnosti tega združenja. Glej popravek in primarni imenik v [[zdravstvena-podporna-mreza]].')
if '## Zdravstvena podporna mreža — 2026-09-20' not in s:s+='\n\n## Zdravstvena podporna mreža — 2026-09-20\n\n[[zdravstvena-podporna-mreza]] vsebuje 15 organizacij in povezav pomoči, kontakte, pogoje in omejitve, z 18 viri IEEE. [[sola-zdravja-crnomelj]] podrobneje obravnava deset skupin Šole zdravja v občini.\n'
p.write_text(s,encoding='utf-8')
p=R/'wiki/analysis/synthesis/pregled-za-kandidata.md';s=p.read_text(encoding='utf-8')
if 'CKZ že ima zbirnik »Povezani za zdravje«' not in s:
 start=s.find('### 🏥 Zdravstvo');target=s.find('#### ✅ Kar deluje',start)
 if target>=0:
  insert=s.find('\n',target);s=s[:insert]+ '\n\n- CKZ že ima zbirnik »Povezani za zdravje« (september 2025). Dopolnjeni [[../../entities/associations/zdravstvena-podporna-mreza|imenik]] povezuje 15 organizacij in mrež pomoči; Šola zdravja navaja deset skupin v občini. Priporočilo je redna preverba kontaktov in pomoč pri vključitvi. Ocena CKZ in status zdravstvene teme ostajata nespremenjena.'+s[insert:]
 s+='\nZadnja preverba zdravstvenega razdelka: 2026-09-20 — društva in podporna mreža.\n';p.write_text(s,encoding='utf-8')
p=R/'wiki/sources/source-summaries/drustva-zdravstvena-pomoc-2026-09-20.md'
p.write_text('''# Viri: društva in podporna pomoč za zdravje

## Povzetek

Preverjene so neposredne strani izvajalcev, območnih skupin in zvez ter zbirnik CKZ iz septembra 2025. Celotna sinteza s kontakti in 18 oštevilčenimi primarnimi oziroma neposrednimi institucionalnimi viri: [[../../entities/associations/zdravstvena-podporna-mreza]]. Ločen profil: [[../../entities/associations/sola-zdravja-crnomelj]].

## Zanesljivost in omejitve

Viri potrjujejo objavljeno ponudbo in kontakte, ne dejanske proste zmogljivosti. Nobeno društvo ni bilo kontaktirano. Starejši podatki so označeni; aktualna članarina in pogoji vključitve niso domnevani. Neposreden prenos Metuljčice vrne HTTP 403, zato je shranjen uporabljeni izvleček spletnega orodja. Stran RKS je imela TLS napako; uporabljeni vir je imenik CKZ, ne nedostopna stran. Stara podstran OZARE ni dostopna; lokalno delo potrjuje tudi Knjižnica Črnomelj.

## Uporaba

V zdravstvenem poročilu je dodano poglavje `#drustva`, na voljo je CSV. Možnosti sodelovanja so predlogi, ne že sklenjeni dogovori. Imenik CKZ dopolnjuje dokaz o javnem obveščanju, ne meritve zdravstvenega učinka.

## Zadnja posodobitev

2026-09-20.
''',encoding='utf-8')
p=R/'wiki/index.md';s=p.read_text(encoding='utf-8')
if '## Društva in zdravje — 2026-09-20' not in s:
 s+='''\n\n## Društva in zdravje — 2026-09-20

- [[entities/associations/zdravstvena-podporna-mreza]] — pregled društev; 15 organizacij in mrež pomoči, 18 virov, kontakti in omejitve; povezano s CKZ in zdravstvenim poročilom.
- [[entities/associations/sola-zdravja-crnomelj]] — društvo; deset skupin v občini, urnik na Gričku in pogoji za preverbo; 2 vira.
- [[sources/source-summaries/drustva-zdravstvena-pomoc-2026-09-20]] — povzetek zajema; uradni viri in omejitve preverbe kontaktov.

Zadnja posodobitev kazala: 2026-09-20.
''';p.write_text(s,encoding='utf-8')
p=R/'wiki/naslednji-koraki.md';s=p.read_text(encoding='utf-8');i=s.find('\n')
if '### Društva in zdravje — končano 2026-09-20' not in s:
 s=s[:i]+'''\n\n### Društva in zdravje — končano 2026-09-20

V zdravstveno poročilo dodano poglavje `#drustva`: 15 organizacij/mrež, kontakti, razlika med lokalno dejavnostjo, regionalno pokritostjo in možnostjo sodelovanja. Šola zdravja ima na svojem seznamu deset občinskih skupin. Pomemben novi vir: CKZ **Povezani za zdravje**, september 2025; imenik že obstaja, treba ga je vzdrževati. Ocena CKZ 3,4/5 ostaja. Novi wiki strani: [[entities/associations/zdravstvena-podporna-mreza]] in [[entities/associations/sola-zdravja-crnomelj]]. Popravljena neutemeljena stara navedba, da RK Črnomelj vodi Program MIRA.

Gradnja v mapi poročila: `python -X utf8 pripravi_drustva.py`, nato `python -X utf8 zgradi_porocilo.py`; PDF in preverba: `python -X utf8 preveri_porocilo.py`. Podatki v `drustva-pomoc.json/csv`, 18 virov v `drustva-viri.json`, izvirniki v `raw/web/zdravstvo-20260920-drustva-*`. Enkratne vložitvene skripte `vlozi_drustva.py` ni treba ponovno izvajati. Nove vire citirati z datumom dostopa 20. 9., stari viri ohranjajo 19. 9. Vse razpoložljivosti so spletno navedene, ne telefonsko potrjene. Nadalje: preveriti stroške, članstvo, termine, prevoze in zmogljivosti; nobeni organizaciji nismo poslali sporočila.
'''+s[i:];p.write_text(s,encoding='utf-8')
p=R/'wiki/log.md';s=p.read_text(encoding='utf-8')
if 'ingest | Društva in mreža podpore za zdravje' not in s:
 with p.open('a',encoding='utf-8') as file:file.write('''\n\n## [2026-09-20] ingest | Društva in mreža podpore za zdravje

- Action: Preverba 15 organizacij/mrež za lokalno in regionalno pomoč, 18 virov; dodana tabela v zdravstveno poročilo in CSV. Šola zdravja: deset skupin v občini. Najden obstoječi imenik CKZ Povezani za zdravje (september 2025); priznano dodatno delo pri obveščanju, ocena CKZ nespremenjena.
- Sources used: Uradne strani Šole zdravja, koronarnega društva/zveze, diabetikov, Europa Donna, Metuljčice, CVB, MS, Spominčice, Hospica, ŠENT, Slovenske filantropije; LU in Knjižnica Črnomelj; zbirnik CKZ.
- Pages created: entities/associations/zdravstvena-podporna-mreza; entities/associations/sola-zdravja-crnomelj; sources/source-summaries/drustva-zdravstvena-pomoc-2026-09-20.
- Pages updated: ckz-crnomelj, pregled-drustev, pregled-za-kandidata, index, naslednji-koraki, zdravstveno poročilo HTML/PDF. Umaknjena nepotrjena navedba o RK kot nosilcu Programa MIRA.
- Open questions: Dejanska razpoložljivost, članarine, termini, prevozi, dostopnost in dolgoročni izidi. Regionalno sodelovanje ni samodejno lokalna izvedba.
- Follow-up tasks: Po uporabnikovem naročilu preveriti konkretne pogoje vključitve pri izbranih izvajalcih; redno vzdrževati imenik, uskladiti morebitne stare skupne dokumente pred ponovno objavo.
''')
print('Predaja, kazalo, dnevnik in povezane strani posodobljeni.')
