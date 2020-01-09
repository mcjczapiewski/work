import os
import shutil
from natsort import natsorted, natsort_keygen
nkey = natsort_keygen()

count = 1

print('\nUWAGA!\nPLIK Z EWENTUALNYMI BŁĘDAMI ZOSTANIE ZAPISANY W PODANEJ PONIŻEJ LOKALIZACJI!\n\n')
sciezka = input('Podaj ścieżkę WKT: ')
docelowa = input('Podaj ściezkę docelową: ')


for subdir, dirs, files in os.walk(sciezka):
    dirs.sort(key=nkey)
    glowny = subdir
    for file in natsorted(files):
        if file.upper().endswith('.WKT'):
            if '_' in file:
                nrope = file.split('_')[0]
            else:
                nrope = file.upper().split('.WKT')[0]
            for subdir, dirs, _ in os.walk(docelowa):
                dirs.sort(key=nkey)
                if not any(fname.upper().endswith(('.JPG', '.PDF')) for fname in os.listdir(subdir)):
                    continue
                folder = os.path.basename(subdir)
                doc = subdir
                if nrope == folder:
                    plik = os.path.join(glowny, file)
                    docplik = os.path.join(doc, file)
                    if os.path.exists(docplik):
                        with open(os.path.join(sciezka, 'juz_istnialy_nie_skopiowano.txt'), 'a') as bl:
                            bl.write(plik + '\t' + docplik + '\n')
                        continue
                    else:
                        try:
                            shutil.copy(plik, docplik)
                            print(count)
                            count += 1

                        except:
                            with open(os.path.join(sciezka, 'bledy.txt'), 'a') as bl:
                                bl.write(plik + '\n')

input('KONIEC.')
