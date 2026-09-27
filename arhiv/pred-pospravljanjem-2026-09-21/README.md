# Zdravje v Občini Črnomelj — samostojen raziskovalni projekt

Ta mapa je samostojen projekt: javno poročilo o zdravju v Občini Črnomelj, lokalna knjižnica vseh uporabljenih virov in wiki, ki ga vzdržuje raziskovalni agent. Mapo lahko prekopirate kamorkoli in jo odprete kot nov projekt (Claude Code ali Codex); nič v njej ne kaže izven mape.

## Kaj odpreti

| Datoteka | Vsebina |
|---|---|
| `porocilo.html` | Poročilo z interaktivnimi grafi, zemljevidi (defibrilatorji, poti), starostjo prebivalcev, oceno CKZ in literaturo. Deluje brez omrežja; odprite ga neposredno v brskalniku. |
| `porocilo.pdf` | Enako poročilo za tisk. |
| `register-dogodkov.html` | Iskalni register 1.068 objav Radia Odeon o dejavnostih CKZ. |
| `viri/index.html` | Lokalna knjižnica: vsi viri, ki jih poročilo navaja, z lokalno kopijo. |
| `wiki/index.md` | Zemljevid wikija (strani v slovenščini). |

## Navodila za agenta

Agent dela po `AGENTS.md` (za Claude Code tudi `CLAUDE.md`): kot neodvisen raziskovalec zdravja v občini, po enaki shemi kot agent nadrejenega vaulta (viri, wiki, `index.md`, `log.md`, `naslednji-koraki.md`, kritična vprašanja, rešitve, ocene, citiranje IEEE). Ob začetku seje mora prebrati `AGENTS.md`, nato `wiki/naslednji-koraki.md`.

## Namestitev in gradnja

```powershell
python -m pip install -r requirements.txt
python -m playwright install chromium
$env:PYTHONIOENCODING='utf-8'
python -X utf8 zazeni.py zgradi     # obnovi poročilo in knjižnico virov
python -X utf8 zazeni.py preveri    # preveri povezave, širine, JavaScript in izdela PDF
python -X utf8 zazeni.py vse        # oboje
python -X utf8 zazeni.py postrezi   # http://127.0.0.1:8000/porocilo.html
```

Izračun GPX poti (neobvezno): `python -m pip install --target .python-deps -r requirements-poti.txt`, nato `python -X utf8 zazeni.py zgradi --preracunaj-poti`.

## Zgradba mape

| Mapa | Namen |
|---|---|
| `wiki/` | Vzdrževani wiki (slovenščina). |
| `viri/` | Vsi viri: `splet/` shranjene spletne strani, `nijz/` časovni nizi NIJZ, PDF-ji, GPX, karte, AED. |
| `orodja/` | Skripte za zajem, gradnjo in preverjanje. |
| `arhiv/` | Prejšnje različice in enkratne skripte (ne zaganjati ponovno). |
| `preverjanje/` | Posnetki zaslona in rezultati preverjanja. |
| koren | Vhodi gradnje (`vsebina.html`, `slog.css`, JSON/CSV podatki) in izdelki (`porocilo.*`). Izdelkov ne urejajte ročno. |

## Omejitve

Podatki so presek 19.–21. 9. 2026. Ocena CKZ (3,4/5) je uredniška ocena javno dokumentiranega dela, ne klinična ali finančna presoja. Lokacije defibrilatorjev in razpoložljivost društev so navedene po spletnih virih in datoteki naročnika, ne terensko ali telefonsko potrjene.
