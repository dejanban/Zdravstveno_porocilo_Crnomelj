# Zdravje v Občini Črnomelj — samostojen raziskovalni projekt

Ta mapa je samostojen projekt: javno poročilo o zdravju v Občini Črnomelj, lokalna knjižnica vseh uporabljenih virov in wiki, ki ga vzdržuje raziskovalni agent. Mapo lahko prekopirate kamorkoli in jo odprete kot nov projekt (Claude Code ali Codex); nič v njej ne kaže izven mape.

## Kaj odpreti

| Datoteka | Vsebina |
|---|---|
| `porocilo.html` | Enajst povezanih zavihkov, iskanje po vseh vsebinah, grafi, zemljevidi in raziskave spanja. Modra/jesenska oblika; deluje neposredno v brskalniku brez omrežja. |
| `porocilo.pdf` | Enako poročilo za tisk. |
| Obrazci CKZ | Prejšnji prenosi so del poškodovanega arhiva. Ohranjeno besedilo je v zavihku CKZ; veljavne predloge v tej prenovi niso ponovno izdelane. |
| `register-dogodkov.html` | Iskalni register 1.068 objav Radia Odeon o dejavnostih CKZ. |
| `viri/index.html` | Lokalna knjižnica s stanjem kopij in označenimi manjkajočimi podedovanimi viri. |
| `wiki/index.md` | Zemljevid wikija (strani v slovenščini). |

## Navodila za agenta

Agent dela po `AGENTS.md` (za Claude Code tudi `CLAUDE.md`): kot neodvisen raziskovalec zdravja v občini, po enaki shemi kot agent nadrejenega vaulta (viri, wiki, `index.md`, `log.md`, `naslednji-koraki.md`, kritična vprašanja, rešitve, ocene, citiranje IEEE). Ob začetku seje mora prebrati `AGENTS.md`, nato `wiki/naslednji-koraki.md`.

## Namestitev in gradnja

```powershell
python -m pip install --target tmp/okolje-runtime -r requirements.txt
$env:PYTHONIOENCODING='utf-8'
python -X utf8 zazeni.py zgradi     # obnovi poročilo in knjižnico virov
python -X utf8 zazeni.py preveri    # preveri povezave, širine, JavaScript in izdela PDF
python -X utf8 zazeni.py vse        # oboje
python -X utf8 zazeni.py postrezi   # http://127.0.0.1:8000/porocilo.html
```

Trenutno preverjanje uporablja Python 3.11, projektne odvisnosti v `tmp/okolje-runtime` in nameščeni Microsoft Edge prek Playwrighta. Zaganjalnik sam nastavi pot do projektnih odvisnosti. Gradnja ne obnavlja izgubljenih izvirnih Excelov ali obrazcev CKZ.

`--preracunaj-poti` se v obnovljenem projektu izrecno ustavi, ker prvotni generator in del GPX nista ohranjena. Uporabljeni so podatki, dejansko vgrajeni v staro poročilo. Podrobnosti: [dokumentacija prenove](dokumentacija/prenova-20260925.md).

## Zgradba mape

| Mapa | Namen |
|---|---|
| `wiki/` | Vzdrževani wiki (slovenščina). |
| `viri/` | Vsi viri: `splet/` shranjene spletne strani, `nijz/` časovni nizi NIJZ, PDF-ji, GPX, karte, AED. |
| `orodja/` | Skripte za zajem, gradnjo in preverjanje. |
| `arhiv/` | Prejšnje različice in enkratne skripte (ne zaganjati ponovno). |
| `preverjanje/` | Posnetki zaslona in rezultati preverjanja. |
| `vsebina/` | Vhodi gradnje: razdelki poročila, slogi in skripte (`vsebina.html`, `slog.css` …). |
| `podatki/` | Podatkovne in bibliografske datoteke po temah (`ckz`, `aed`, `starost`, `drustva`, `kader`, `poti`, `register`, `nijz`, `literatura`). |
| `dokumentacija/` | Opombe k analizi poti. |
| koren | Izdelki (`porocilo.html`, `porocilo.pdf`, `register-dogodkov.html`, `index.html`), `zazeni.py`, `AGENTS.md`, `README.md`. Izdelkov ne urejajte ročno. |

## Omejitve

Prenova 25. 9. 2026 vključuje osem raziskav in dve objavi NIJZ o spanju, zaslonih in družbenih omrežjih; štirje članki so prebrani samo kot povzetki. Vsi novi zajemi imajo preverjene kontrolne vsote. V podedovanem arhivu ostaja šest nepojasnjenih neskladij HTML-kopij in 77 manjkajočih ali praznih ciljev povezav iz poročila. Pri 313 datotekah je potrjena ekvivalentnost po pretvorbi koncev vrstic. Poročilo te omejitve izrecno označuje; prenova ne potrjuje znova vseh starejših trditev.

Osnovni podatki imajo presek 19.–21. 9. 2026; obrazci CKZ in ponovna preverba strani NIJZ o spremljanju so z 22. 9. 2026. Predloga je avtorska, brez potrditve uvedbe v CKZ. Ocena CKZ (3,4/5) je uredniška ocena javno dokumentiranega dela, ne klinična ali finančna presoja. Lokacije defibrilatorjev in razpoložljivost društev so navedene po spletnih virih in datoteki naročnika, ne terensko ali telefonsko potrjene.
