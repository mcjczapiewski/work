import os, shutil, regex
from natsort import natsort_keygen, natsorted
nkey = natsort_keygen()

count = 1
przeniesione = set()
nieprzeniesione = set()

stad = r'I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614\DĄBROWA BISKUPIA\metadane_gogolewski'
tu = r'I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614\DĄBROWA BISKUPIA'

for subdir, dirs, files in os.walk(stad):
    dirs.sort(key=nkey)
    if not any(fname.upper().endswith('.PDF') for fname in os.listdir(subdir)):
        continue
    else:
        glowny = subdir
        szukaj = regex.escape(stad) + r'\\(.+$)'
        pierwotny = regex.match(szukaj, subdir)[1]
        docelowy = os.path.join(tu, pierwotny)
        if os.path.exists(docelowy):
            for file in natsorted(files):
                if file.upper().endswith('.PDF'):
                    plik = os.path.join(glowny, file)
                    print(str(count)+'\t'+plik)
                    count += 1
                    if os.path.exists(os.path.join(docelowy, file)):
                        try:
                            os.remove(os.path.join(docelowy, file))
                        except:
                            with open(r'D:\_MACIEK_\python_proby\nie_da_sie_usunac.txt', 'a') as nie:
                                nie.write(os.path.join(docelowy, file)+'\n')
                    try:
                        shutil.move(plik, docelowy)
                        przeniesione.add(plik)
                    except:
                        with open(r'D:\_MACIEK_\python_proby\nie_da_sie_przeniesc.txt', 'a') as nie_p:
                            nie_p.write(plik+'\t'+docelowy+'\n')
                        nieprzeniesione.add(plik)
        else:
            with open(r'D:\_MACIEK_\python_proby\brak_odpowiednika_folderu.txt', 'a') as brak:
                brak.write(glowny+'\n')

