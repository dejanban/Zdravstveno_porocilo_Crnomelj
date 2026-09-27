"""Natisljiva različica vprašalnika o izkušnjah pacientov (HTML in PDF A4).

Vir besedila: razdelek »## Vprašalnik« v vsebina/teme/vprasalnik-pacienti.md.
Izhod: podatki/vprasalnik/vprasalnik-izkusnje-pacientov.html in .pdf (PDF z Microsoft Edge prek Playwright).
Zagon: python -X utf8 orodja/pripravi_vprasalnik.py (ni del običajne gradnje, ker potrebuje brskalnik).
"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tmp/okolje-runtime'))
import markdown

CSS = '''@page{size:A4;margin:14mm 13mm}body{font:10.5pt/1.4 "Segoe UI",Arial,sans-serif;color:#17202a;margin:0}
h1{font-size:16pt;margin:0 0 4px}p{margin:0 0 8px}table{width:100%;border-collapse:collapse;margin:8px 0 12px;page-break-inside:auto}
tr{page-break-inside:avoid}th,td{border:1px solid #9aa5b1;padding:5px 6px;vertical-align:top;text-align:left}th{background:#e9eef2;font-size:9.5pt}
table:first-of-type td:first-child{width:5%;text-align:center}table:first-of-type td:nth-child(2){width:38%}td:first-child{white-space:nowrap}.meta{font-size:8.5pt;color:#4a5968;border-top:1px solid #c5cdd4;margin-top:10px;padding-top:6px}
.skrinja{border:1.5px dashed #6b7a88;padding:6px 8px;font-size:9.5pt}'''


def main():
    text = (ROOT / 'vsebina/teme/vprasalnik-pacienti.md').read_text(encoding='utf-8')
    del_ = text.split('## Vprašalnik\n', 1)[1].split('\n## ', 1)[0]
    del_ = '\n'.join(l for l in del_.splitlines() if not l.startswith('Natisljiva različica'))
    del_ = del_.replace('**Vprašalnik o vašem obisku v Zdravstvenem domu Črnomelj**', '# Vprašalnik o vašem obisku v Zdravstvenem domu Črnomelj')
    body = markdown.markdown(del_, extensions=['tables'])
    html = (f'<!doctype html><html lang="sl"><head><meta charset="utf-8"><title>Vprašalnik o izkušnjah pacientov</title><style>{CSS}</style></head><body>'
            f'{body}<p class="meta">Delovna predloga 1.0 · 26. september 2026 · neodvisni predlog raziskovalnega poročila o zdravju v Občini Črnomelj; ZD vprašalnika ni potrdil. '
            'Izpolnjuje se enkrat v letnem obdobju zbiranja, anonimno.</p></body></html>')
    out = ROOT / 'podatki/vprasalnik'; out.mkdir(parents=True, exist_ok=True)
    (out / 'vprasalnik-izkusnje-pacientov.html').write_text(html, encoding='utf-8')
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(channel='msedge', headless=True)
        pg = b.new_page(); pg.goto((out / 'vprasalnik-izkusnje-pacientov.html').as_uri())
        pg.pdf(path=str(out / 'vprasalnik-izkusnje-pacientov.pdf'), format='A4', print_background=True, prefer_css_page_size=True)
        b.close()
    import pymupdf
    print('PDF strani:', len(pymupdf.open(out / 'vprasalnik-izkusnje-pacientov.pdf')))


if __name__ == '__main__':
    main()
