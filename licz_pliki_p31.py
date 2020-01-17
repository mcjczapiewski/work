import os, io
from natsort import natsorted, natsort_keygen
nkey = natsort_keygen()

count = 1
print('\nUWAGA!\nW podanej ścieżce utworzy się plik txt z danymi.\n')
sciezka = input('Podaj ścieżkę: ')

for subdir, dirs, files in os.walk(sciezka):
    dirs.sort(key=nkey)
    liczba = 0
    if not any(fname.upper().endswith(('.PDF', '.JPG', '.JPEG', '.XML', '.WKT', '.TXT')) for fname in os.listdir(subdir)):
        continue
    for file in natsorted(files):
        if not file.upper().endswith(('.WKT', '.XML')):
            liczba += 1

    with io.open(os.path.join(sciezka, 'liczba_plikow.txt'), 'a', encoding = 'utf-8') as pisz:
        pisz.write(subdir+'\t'+str(liczba)+'\n')
    print(count)
    count += 1

input('KONIEC.')
