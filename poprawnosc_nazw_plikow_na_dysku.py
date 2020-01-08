import os, regex
from natsort import natsorted, natsort_keygen
nkey = natsort_keygen()

nazwy = ('decyzja', 'dokumentacja przejściowa', 'dziennik pomiarowy', 'inny', 'mapa', 'okładka', 'opis topograficzny', 'protokół', 'spis treści', 'sprawozdanie techniczne', 'szkic', 'wykaz współrzędnych')
sciezka = input('Podaj ścieżkę: ')

count = 1

for subdir, dirs, files in os.walk(sciezka):
    dirs.sort(key=nkey)

    if not any(fname.upper().endswith('.JPG') for fname in os.listdir(subdir)):
        with open(r'D:\_MACIEK_\python_proby\foldery_bez_JPG.txt', 'a') as np:
            np.write(os.path.join(subdir)+'\n')
        continue

    print(str(count)+'\t'+os.path.basename(os.path.dirname(subdir))+'\\'+os.path.basename(subdir))
    count += 1
    
    for file in natsorted(files):
        if file.upper().endswith('.JPG'):
            nazwa = regex.match('^.+_(.+)\.jpg', file.lower())[1]
            if nazwa not in nazwy:
                with open(r'D:\_MACIEK_\python_proby\niepoprawne_nazwy.txt', 'a') as np:
                    np.write(os.path.join(subdir, file)+'\n')
