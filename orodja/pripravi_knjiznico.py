"""Lokalni bralnik virov in kazalo izvirnikov; brez omrežja."""
from pathlib import Path
import json, html, hashlib
from projekt import BASE, datoteka, lokalna_analiza

def page(title,body):
    return '<!doctype html><html lang="sl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+html.escape(title)+'</title><style>body{font:16px/1.6 system-ui;color:#173c32;background:#f7f8f2;max-width:1100px;margin:35px auto;padding:0 20px}a{color:#086c60}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:white;padding:22px;border:1px solid #dde5d8}table{width:100%;border-collapse:collapse}td,th{padding:9px;border-bottom:1px solid #cdd8ca;text-align:left}input{padding:10px;width:90%;margin:12px 0}nav{margin-bottom:20px}.scroll{overflow-x:auto}</style><body>'+body+'</body></html>'

def main():
    root=BASE/'viri'
    for p in root.rglob('*.md'):
        title=p.stem
        body='<nav><a href="'+('../'*len(p.relative_to(root).parts[:-1]))+'index.html">Knjižnica virov</a> · <a href="'+html.escape(p.name)+'" download>Izvirna shranjena datoteka</a></nav><h1>Shranjeni vir</h1><pre>'+html.escape(p.read_text(encoding='utf-8-sig'))+'</pre>'
        p.with_suffix('.html').write_text(page(title,body),encoding='utf-8')
    for folder in ['nijz','dokumenti','kartografija','aed','gpx']:
        p=root/folder
        rows=''.join('<tr><td><a href="'+html.escape(f.relative_to(p).as_posix(),quote=True)+'">'+html.escape(f.relative_to(p).as_posix())+'</a></td><td>'+str(f.stat().st_size)+'</td></tr>' for f in sorted(p.rglob('*')) if f.is_file() and f.name!='index.html' and f.suffix!='.html')
        (p/'index.html').write_text(page('Izvirniki: '+folder,'<a href="../index.html">Knjižnica virov</a><h1>Izvirniki: '+folder+'</h1><div class="scroll"><table><tr><th>Datoteka</th><th>Bajti</th></tr>'+rows+'</table></div>'),encoding='utf-8')
    refs=json.loads(datoteka('podatki/literatura/literatura.json').read_text(encoding='utf-8'))
    rows=''
    for i,r in enumerate(refs,1):
        p=datoteka(r['local']);target=p.with_suffix('.html') if p.suffix=='.md' else p/'index.html' if p.is_dir() else p
        rows+='<tr><td>'+str(i)+'</td><td>'+html.escape(r['title'])+'<br><small>'+html.escape(r.get('publisher',''))+'</small></td><td><a href="'+html.escape(target.relative_to(root).as_posix(),quote=True)+'">Shranjeni vir</a>'+((' · <a href="'+html.escape(r['url'],quote=True)+'">Izvorni URL</a>') if r.get('url') else '')+'</td></tr>'
    body='<nav><a href="../porocilo.html">Poročilo</a> · <a href="../register-dogodkov.html">Register 1.068 objav</a></nav><h1>Lokalna knjižnica virov</h1><p>Vseh '+str(len(refs))+' virov, citiranih v poročilu. Shranjeni so uporabljeni zajemi in izvlečki ter razpoložljivi izvirniki. Kjer je raziskava podprta samo s povzetkom, arhiv tega ne predstavlja kot celotno besedilo raziskave. Izvorni datumi zajema ostajajo ohranjeni.</p><p><a href="dokumenti/index.html">PDF in drugi dokumenti</a> · <a href="nijz/index.html">NIJZ</a> · <a href="aed/index.html">AED</a> · <a href="kartografija/index.html">Kartografija</a> · <a href="gpx/index.html">GPX</a> · <a href="manifest.json">Manifest izvirnikov SHA-256</a></p><label>Iskanje po naslovu ali izdajatelju<br><input id="iskanje" type="search"></label><div class="scroll"><table><thead><tr><th>Št.</th><th>Vir</th><th>Dostop</th></tr></thead><tbody>'+rows+'</tbody></table></div><script>document.querySelector("#iskanje").addEventListener("input",e=>{const q=e.target.value.toLocaleLowerCase("sl");document.querySelectorAll("tbody tr").forEach(r=>r.hidden=!r.textContent.toLocaleLowerCase("sl").includes(q))})</script>'
    (root/'index.html').write_text(page('Lokalna knjižnica virov',body),encoding='utf-8')
    for p in (BASE/'analize').glob('*.md'):p.write_text(lokalna_analiza(p.read_text(encoding='utf-8')),encoding='utf-8')
    landing=('<h1>Zdravje v Občini Črnomelj</h1><p>Samostojen raziskovalni projekt: javno poročilo, lokalna knjižnica vseh uporabljenih virov in wiki. Vse deluje brez omrežja.</p>'
        '<div class="scroll"><table><tr><th>Kaj</th><th>Kje</th></tr>'
        '<tr><td>Poročilo z grafi in zemljevidi</td><td><a href="porocilo.html">porocilo.html</a> · <a href="porocilo.pdf">PDF</a></td></tr>'
        '<tr><td>Register objav o dejavnostih CKZ (Radio Odeon)</td><td><a href="register-dogodkov.html">register-dogodkov.html</a></td></tr>'
        '<tr><td>Lokalna knjižnica virov</td><td><a href="viri/index.html">viri/index.html</a></td></tr>'
        '<tr><td>Wiki (slovenščina)</td><td><a href="wiki/index.md">wiki/index.md</a></td></tr>'
        '<tr><td>Navodila za agenta in namestitev</td><td><a href="AGENTS.md">AGENTS.md</a> · <a href="README.md">README.md</a></td></tr></table></div>')
    (BASE/'index.html').write_text(page('Zdravje v Občini Črnomelj',landing),encoding='utf-8')
    print('Knjižnica:',len(refs),'citiranih virov in vsi shranjeni izvlečki registra.')

if __name__=='__main__':main()
