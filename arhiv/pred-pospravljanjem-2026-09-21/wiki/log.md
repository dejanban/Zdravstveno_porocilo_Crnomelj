# Dnevnik (log)

Kronološki, samo-dodajajoč zapisnik. Format vsakega vnosa: `## [LETO-MESEC-DAN] tip | Naslov`.

Starejša zgodovina dela (poročilo o zdravstvu, CKZ, starost, društva, kader in šport, poti, defibrilatorji, 19.–21. 9. 2026) je v dnevniku nadrejenega vaulta `Obcina_Crnomelj_Vault/wiki/log.md`; ta dnevnik se začne z ustanovitvijo samostojnega projekta.

## [2026-09-21] update | Ustanovitev samostojnega raziskovalnega projekta o zdravju

- Action: Mapa `porocila/zdravstvo-obcina-crnomelj` je pripravljena kot samostojen projekt. Skripte so v `orodja/` (koren = mapa projekta), poti do virov so projektno relativne (`raw/web/` → `viri/splet/`, `raw/Zdravje_kraja` → `viri/nijz`), v `viri/` je lokalna kopija vseh virov, ki jih poročilo navaja (93 citiranih virov, 1.068 objav registra Radia Odeon, 54 nizov NIJZ, PDF-ji, GPX, AED), dodan je `viri/manifest.json` s SHA-256. V `wiki/` je prenesen izbor zdravstvenih strani (27 datotek), s povezavami preusmerjenimi v projekt; povezave na strani, ki niso del projekta, so pretvorjene v navadno besedilo. Dodani so `AGENTS.md` (navodila agenta kot raziskovalca zdravja), `CLAUDE.md`, `README.md`, `requirements.txt`, `wiki/index.md`, `log.md`, `naslednji-koraki.md` in zdravstveni `pregled-za-kandidata.md`. Enkratne skripte (`dokoncaj_zajem`, `dopolni_*`, `posodobi_wiki`, `vlozi_*`) so premaknjene v `arhiv/enkratne-skripte/`; izvirna besedila pred preusmeritvijo poti so v `arhiv/pred-samostojnim-projektom-2026-09-21/`.
- Sources used: obstoječi viri in izdelki mape; kopije iz `raw/web/` in `raw/Zdravje_kraja` nadrejenega vaulta.
- Pages created: `AGENTS.md`, `CLAUDE.md`, `README.md`, `wiki/index.md`, `wiki/log.md`, `wiki/naslednji-koraki.md`, `wiki/analysis/synthesis/pregled-za-kandidata.md`, `viri/manifest.json`, 26 prenesenih wiki strani in infografik.
- Pages updated: vse podatkovne datoteke in skripte s potmi do virov.
- Open questions: nekatere strani prenesenega wikija (npr. starejši povzetki virov NIJZ) vsebujejo starejše formulacije, ki jih poročilo popravlja; pred uporabo preveriti proti `porocilo.html`, razdelek »Sled sprememb«.
- Follow-up tasks: pri prvi seji v novem projektu zagnati `python -X utf8 zazeni.py vse` in preveriti rezultat; nadaljevati odprte raziskave iz `naslednji-koraki.md`.
