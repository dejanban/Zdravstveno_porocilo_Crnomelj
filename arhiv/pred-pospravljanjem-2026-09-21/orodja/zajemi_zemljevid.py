"""Enkratni zajem OSM osnove za zemljevid defibrilatorjev (meja občine, Kolpa, ceste, naselja)."""
import requests, json
from pathlib import Path
P = Path(__file__).resolve().parent.parent
Q = '''[out:json][timeout:120];
rel["boundary"="administrative"]["admin_level"="8"]["name"="Črnomelj"]->.c;
.c map_to_area->.a;
(.c; way(r.c);
 way["waterway"="river"](area.a);
 way["highway"~"^(motorway|trunk|primary|secondary)$"](area.a);
 node["place"~"^(town|village)$"](area.a););
out geom;'''
r = requests.post('https://overpass-api.de/api/interpreter', data={'data': Q}, headers={'User-Agent': 'ObcinaCrnomeljVault/1.0 (raziskava)', 'Accept': 'application/json'}, timeout=150)
print(r.status_code, len(r.content))
(P / 'viri' / 'osm-crnomelj.json').write_bytes(r.content)
d = r.json()
from collections import Counter
print(Counter((e['type'], (e.get('tags') or {}).get('boundary') or (e.get('tags') or {}).get('waterway') or (e.get('tags') or {}).get('highway') or (e.get('tags') or {}).get('place')) for e in d['elements']))
