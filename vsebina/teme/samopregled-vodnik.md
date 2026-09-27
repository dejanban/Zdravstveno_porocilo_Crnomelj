# Vodnik: kateri pregledi so za vas

## Povzetek

Nekatere pogoste bolezni dolgo ne bolijo. Zvišan krvni tlak, sladkorna bolezen tipa 2 ter predrakave spremembe na debelem črevesu in materničnem vratu lahko leta napredujejo brez težav. Svetovna zdravstvena organizacija ocenjuje, da 44 % odraslih z zvišanim krvnim tlakom za to ne ve. [@who-hipertenzija-2025] Tudi v Črnomlju je tako: preventivni pregledi v ambulantah družinske medicine ZD Črnomelj so leta 2025 med 1.366 pregledanimi na novo odkrili 236 oseb z zvišanim krvnim tlakom in 144 s sladkorno boleznijo. [@ref:vir-5]

Ta zavihek zbira uradna navodila za preglede, ki jih lahko opravite sami, in za preglede, na katere vas povabijo. Pove tudi, kaj kažejo raziskave o njihovi koristi. Vodnik ne nadomešča posveta z zdravnikom. Če se že zdravite, veljajo navodila vašega zdravnika.

<p class="callout warning">Če imate nenadne težave, kot so bolečina v prsih, povešen ustni kot, šibka roka ali nerazumljiv govor, ne merite in ne čakajte: pokličite 112. Znaki so opisani v poglavju <a href="#samopregled-nujno">Znaki, ob katerih ne čakajte</a>.</p>

### Štirje načini, kako pravočasno odkriti težavo

| Način | Kaj pomeni | Primeri |
|---|---|---|
| Meritev ali samopregled doma | Sami opazujete in merite. Sprememba je razlog za obisk pri zdravniku, ne diagnoza. | [Krvni tlak](#samopregled-tlak), [obseg pasu in vprašalnik o sladkorni bolezni](#samopregled-sladkor), [dojke, moda in koža](#samopregled-telo) |
| Državni presejalni program | Po pošti prejmete vabilo. Pregled je za zavarovane osebe brezplačen. | [Svit, Zora in Dora](#samopregled-presejanje) |
| Preventivni pregled v ambulanti družinske medicine | Diplomirana medicinska sestra povabi odrasle od 30. leta dalje vsakih pet let: krvne preiskave, meritve, pogovor o navadah in vprašalnik o počutju. [@nijz-preventivni-pregled] | Odkrije zvišan tlak, sladkor in maščobe v krvi, depresijo. [Več o rezultatih v Črnomlju](#referencne-ambulante) |
| Znaki, ob katerih ne čakate | Nekatere težave zahtevajo takojšnjo pomoč. | [Možganska kap, srčni infarkt, nepravilen utrip](#samopregled-nujno) |

### Poiščite preglede za svojo starost

Vpišite starost in izberite spol. Preglednica pokaže, kaj velja za vas. Brez izbire so prikazani vsi pregledi. Podatki veljajo za septembra 2026; spremembe programa Zora začnejo veljati 1. 1. 2027.

<div class="samopregled-filter no-print" hidden><label>Starost (leta)<input id="samopregled-starost" type="number" min="15" max="100" inputmode="numeric" placeholder="npr. 52"></label><label>Spol<select id="samopregled-spol"><option value="">Vsi</option><option value="z">Ženska</option><option value="m">Moški</option></select></label><button type="button" id="samopregled-pocisti">Počisti</button></div>
<p class="subtle no-print" id="samopregled-stevec" role="status"></p>
<table id="samopregled-tabela"><thead><tr><th>Pregled</th><th>Komu</th><th>Kako pogosto</th><th>Kako in kje</th></tr></thead><tbody>
<tr data-spol="vsi" data-od="18" data-do="120"><td><a href="#samopregled-tlak">Krvni tlak</a></td><td>Vsi odrasli</td><td>Pri normalnem tlaku brez zdravil zadošča enkrat na leto. Pri zdravljenju po dogovoru z zdravnikom. [@hipertenzija-merjenje-doma]</td><td>Doma z validiranim merilnikom na nadlakti ali v ambulanti.</td></tr>
<tr data-spol="vsi" data-od="18" data-do="120"><td><a href="#samopregled-sladkor">Obseg pasu</a></td><td>Vsi odrasli</td><td>Občasno; pomembno je, da se obseg ne povečuje. [@nijz-obseg-pasu]</td><td>Doma s šiviljskim metrom v višini popka.</td></tr>
<tr data-spol="vsi" data-od="18" data-do="120"><td><a href="#samopregled-sladkor">Vprašalnik o tveganju za sladkorno bolezen (FINDRISK)</a></td><td>Vsi odrasli</td><td>Kadar koli. Pri 15 točkah ali več obiščite zdravnika. [@nijz-findrisk-2026]</td><td>Na papirju ali v spletni različici NIJZ; izračun je tudi v tem poročilu.</td></tr>
<tr data-spol="vsi" data-od="30" data-do="120"><td><a href="#referencne-ambulante">Preventivni pregled v ambulanti družinske medicine</a></td><td>Odrasli od 30. leta</td><td>Vsakih pet let; ob večjem tveganju prej. [@nijz-preventivni-pregled]</td><td>Pri diplomirani medicinski sestri v ambulanti vašega izbranega zdravnika.</td></tr>
<tr data-spol="z" data-od="20" data-do="64"><td><a href="#samopregled-presejanje">Zora: rak materničnega vratu</a></td><td>Ženske 20–64 let; od 1. 1. 2027 25–64 let</td><td>Na tri leta; po negativnem testu HPV na pet let. [@zora-nadgradnja-2026]</td><td>Pri izbranem ginekologu.</td></tr>
<tr data-spol="z" data-od="50" data-do="69"><td><a href="#samopregled-presejanje">Dora: rak dojk</a></td><td>Ženske 50–69 let</td><td>Vsaki dve leti na vabilo. [@dora-vprasanja]</td><td>Slikanje v ZD Novo mesto, Kandijska cesta 4; naročanje 080 27 28. [@dora-oe-novo-mesto]</td></tr>
<tr data-spol="vsi" data-od="50" data-do="74"><td><a href="#samopregled-presejanje">Svit: rak debelega črevesa in danke</a></td><td>Moški in ženske 50–74 let</td><td>Vsaki dve leti na vabilo. [@nijz-svit]</td><td>Test blata doma, vzorec pošljete po pošti.</td></tr>
<tr data-spol="z" data-od="18" data-do="120"><td><a href="#samopregled-telo">Dojke: pozornost na spremembe</a></td><td>Vse odrasle ženske</td><td>Redno; program Dora svetuje enkrat mesečno, tudi med dvema slikanjema. [@oi-priporocila-rak-dojk-2021] [@dora-vprasanja]</td><td>Ogled in otip doma; spremembo pokažite osebnemu zdravniku ali ginekologu.</td></tr>
<tr data-spol="m" data-od="15" data-do="120"><td><a href="#samopregled-telo">Moda</a></td><td>Moški, zlasti mlajši (rak mod je najpogostejši rak moških, starih 20–40 let)</td><td>Društvo onkoloških bolnikov svetuje enkrat mesečno. [@dobs-samopregled-mod] [@oi-rak-mod]</td><td>Otip med kopanjem ali po njem.</td></tr>
<tr data-spol="vsi" data-od="15" data-do="120"><td><a href="#samopregled-telo">Koža in znamenja</a></td><td>Vsi</td><td>Društvo onkoloških bolnikov svetuje enkrat mesečno. [@dobs-melanom]</td><td>Pred velikim ogledalom v dobro osvetljeni sobi.</td></tr>
<tr data-spol="m" data-od="50" data-do="69"><td><a href="#samopregled-presejanje">Test PSA (prostata)</a></td><td>Moški 50–69 let</td><td>Državnega programa ni. Raziskava PRO-PETER vabi naključno izbrane moške. [@oi-pro-peter]</td><td>Odločitev po pogovoru z osebnim zdravnikom o koristih in slabostih.</td></tr>
<tr data-spol="vsi" data-od="18" data-do="120"><td><a href="#samopregled-presejanje">Pljuča</a></td><td>Kadilci in nekdanji kadilci</td><td>Presejalnega programa še ni; projekt LUKA pripravlja strokovne podlage. [@oi-sola-pljucnega-raka-2025]</td><td>Najbolj učinkovit korak je opustitev kajenja; CKZ Črnomelj navaja delavnico svetovanja za opuščanje kajenja. [@ckz-delavnice-odrasli]</td></tr>
</tbody></table>

Brez JavaScripta in v PDF so prikazani vsi pregledi. Starostne meje v stolpcu »Komu« so iz navedenih virov; pri samopregledih brez uradne starostne meje preglednica uporablja 15 ali 18 let le za prikaz.

## Povezane strani

Krvni tlak, sladkorna bolezen, dojke, moda in koža, presejalni programi, nujni znaki, referenčne ambulante.

## Zadnja posodobitev

27. september 2026.
