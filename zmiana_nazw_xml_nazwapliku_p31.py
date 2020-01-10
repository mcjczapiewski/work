import os
import regex
import io
from natsort import natsorted, natsort_keygen
nkey = natsort_keygen()

count = 1
print('\nTYLKO DO ZMIANY NAZW PLIKOW XML ZAWIERAJĄCYCH POLE "nazwaPliku"\nUWAGA! \
    W folderze z plikami XML może pojawić się plik BLEDY_XML.\n\n')
sciezka = input('Podaj ścieżkę do folderu z plikami XML: ')
czy = input('Aktualne rozszerzenie plików to txt czy xml? Wpisz "txt" lub "xml": ')
if '"' in czy:
    czy = regex.sub('"(.+)"', '\\1', czy)
rozszerzenie = '.' + czy

for subdir, dirs, files in os.walk(sciezka):
    dirs.sort(key=nkey)
    for file in natsorted(files):
        if (file.lower()).endswith(rozszerzenie):
            xml = os.path.join(subdir, file)
            with io.open(xml, 'r', encoding='utf-8') as plik:
                nowy_xml = 'nic'
                for line in plik:
                    if regex.match('^.+?nazwaPliku.*', line):
                        nazwa = regex.sub('^.+?nazwaPliku>(.+)</nazwa.+$', '\\1', line)
                        if any(i in nazwa for i in (('.PDF', '.pdf', '.tif', '.TIF', '.tiff', '.TIFF'))):
                            nazwa_n = os.path.splitext(nazwa)[0]
                            nowy_xml = os.path.join(subdir, nazwa_n.split('\n')[0] + '.xml')
                        else:
                            nowy_xml = os.path.join(subdir, nazwa.split('\n')[0] + '.xml')
                        print(str(count) + '\t' + nowy_xml)
                        count += 1
                        break
            if not nowy_xml == 'nic':
                if not os.path.exists(nowy_xml):
                    try:
                        os.rename(xml, nowy_xml)
                    except:
                        raise
                        with open(os.path.join(sciezka, 'BLEDY_XML.txt'), 'a') as bledy:
                            bledy.write(xml + '\tNie można zmienić nazwy.\n')
                else:
                    with open(os.path.join(sciezka, 'BLEDY_XML.txt'), 'a') as bledy:
                        bledy.write(xml + '\t' + nowy_xml + '\tPlik o tej nazwie juz istnieje.\n')

input('\nWciśnij ENTER żeby zamknąć...')
