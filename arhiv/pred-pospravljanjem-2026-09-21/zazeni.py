"""Zagon: python zazeni.py [zgradi|preveri|vse|postrezi]."""
from pathlib import Path
import argparse,subprocess,sys

P=Path(__file__).resolve().parent
def run(name):subprocess.run([sys.executable,'-X','utf8',str(P/'orodja'/name)],cwd=P,check=True)
def main():
    parser=argparse.ArgumentParser(description='Samostojno zdravstveno poročilo Črnomelj')
    parser.add_argument('ukaz',choices=['zgradi','preveri','vse','postrezi'],nargs='?',default='zgradi')
    parser.add_argument('--preracunaj-poti',action='store_true',help='Ponovno izračunaj GPX; sicer uporabi priložene rezultate.')
    parser.add_argument('--port',type=int,default=8000)
    args=parser.parse_args()
    if args.ukaz=='postrezi':
        print(f'Odpri http://127.0.0.1:{args.port}/porocilo.html',flush=True)
        subprocess.run([sys.executable,'-m','http.server',str(args.port),'--bind','127.0.0.1','--directory',str(P)],check=True);return
    if args.ukaz in ['zgradi','vse']:
        run('pripravi_aed.py')
        if args.preracunaj_poti:run('analiziraj_poti.py')
        for name in ['pripravi_starost.py','pripravi_drustva.py','pripravi_kader_sport.py','pripravi_poti.py','zgradi_porocilo.py','pripravi_knjiznico.py']:run(name)
    if args.ukaz in ['preveri','vse']:
        for name in ['preveri_samostojnost.py','preveri_poti.py','preveri_porocilo.py']:run(name)
    print('Končano. Odpri porocilo.html. PDF se obnovi z ukazom preveri ali vse.')
if __name__=='__main__':main()
