"""Poti samostojnega projekta; nikoli ne išče nad njegovim korenom."""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json, re, html

BASE=Path(__file__).resolve().parent.parent
POTI=json.loads((BASE/'podatki/projekt-poti.json').read_text(encoding='utf-8'))

def datoteka(ime):
    ime=str(ime).replace('\\','/')
    if Path(ime).is_absolute():
        p=Path(ime).resolve()
    else:
        mapped=POTI.get(ime)
        if mapped is None:
            for prefix in sorted(POTI,key=len,reverse=True):
                if ime.startswith(prefix+'/'):
                    mapped=POTI[prefix]+ime[len(prefix):]
                    break
        p=(BASE/(mapped or ime)).resolve()
    if not p.is_relative_to(BASE):raise ValueError('Pot zapušča samostojni projekt: '+str(ime))
    return p

def lokalni_vir(ime):
    p=datoteka(ime)
    if p.suffix=='.md':p=p.with_suffix('.html')
    elif p.is_dir():p=p/'index.html'
    return p.relative_to(BASE).as_posix()

def lokalne_povezave(besedilo):
    def replace(m):
        u=html.unescape(m[2])
        if u.startswith(('#','http:','https:','mailto:','tel:','data:')):return m[0]
        path,sep,fragment=u.partition('#')
        path=unquote(path)
        while path.startswith('../'):path=path[3:]
        new=datoteka(path).relative_to(BASE).as_posix() if path else ''
        if new.endswith('.md') and new.startswith('viri/'):new=new[:-3]+'.html'
        elif new and datoteka(new).is_dir():new+='/index.html'
        return m[1]+html.escape(new+(sep+fragment if sep else ''),quote=True)+m[3]
    return re.sub(r'((?:href|src)=["\'])([^"\']+)(["\'])',replace,besedilo)

def lokalna_analiza(text):
    def link(m):
        original,_,label=m[1].partition('|');name=original.split('#')[0]
        while name.startswith('../'):name=name[3:]
        dest=POTI.get(name)
        if not dest:
            dest=next((v for k,v in POTI.items() if k.startswith('wiki/') and Path(k).stem==Path(name).stem),None)
        if not dest and name.startswith(('raw/','porocila/')):
            prefix='porocila/zdravstvo-obcina-crnomelj/'
            name=name.removeprefix(prefix)
            dest=POTI.get(name) or POTI.get(name+'.md')
        if dest:return '['+(label or Path(original).stem)+'](../'+dest+')'
        return label or Path(original).stem
    text=re.sub(r'\[\[([^\]]+)\]\]',link,text)
    text=text.replace('../../../porocila/zdravstvo-obcina-crnomelj/porocilo.html','../porocilo.html')
    return text
