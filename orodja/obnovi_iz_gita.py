"""Obnovi prazne (0 B) datoteke iz prvega commita 0dc0bd4.

Commit d96d620 je po nesreči izpraznil 1.087 datotek; njihove izvirne vsebine so
ohranjene v commitu 0dc0bd4. Skripta prepiše samo datoteke, ki imajo danes 0 bajtov,
in to s surovim git blobom (brez pretvorbe koncev vrstic), zato se izvirni SHA-256
ujemajo z manifestom iz 0dc0bd4. Neprazne datoteke se nikoli ne prepišejo.
Rezultat: preverjanje/obnova-iz-gita.json.
"""
from pathlib import Path
import hashlib, json, subprocess

P = Path(__file__).resolve().parents[1]
COMMIT = '0dc0bd4'


def git(*a):
    return subprocess.run(['git', '-c', 'core.quotepath=off', *a], cwd=P, capture_output=True, check=True).stdout


def main():
    rows = git('ls-tree', '-r', '-l', COMMIT).decode('utf-8').splitlines()
    obnovljeno, preskoceno = [], 0
    for line in rows:
        meta, path = line.split('\t', 1)
        _, typ, blob, size = meta.split()
        if typ != 'blob' or size == '-' or int(size) == 0 or path.startswith('tmp/'):
            continue
        f = P / path
        if not f.is_file() or f.stat().st_size != 0:
            preskoceno += 1
            continue
        data = git('cat-file', 'blob', blob)
        f.write_bytes(data)
        obnovljeno.append({'path': path, 'bajti': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
    rep = {'commit': COMMIT, 'obnovljeno': len(obnovljeno), 'preskoceno_neprazno_ali_manjkajoce': preskoceno,
           'datoteke': obnovljeno}
    (P / 'preverjanje/obnova-iz-gita.json').write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'Obnovljeno {len(obnovljeno)} datotek iz {COMMIT}.')


if __name__ == '__main__':
    main()
