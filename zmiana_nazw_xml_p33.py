import os
import regex
from natsort import natsorted, natsort_keygen
nkey = natsort_keygen()

count = 1
print('\nTYLKO DO ZMIANY NAZW PLIKOW XML ZAWIERAJĄCYCH W POLU "nazwaPliku" ROZSZERZENIE .tif\n\n')
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
            with open(xml, 'r') as plik:
                for line in plik:
                    if regex.match(r'^.+?nazwaPliku.*', line):
                        nazwa = regex.sub(r'^.+?nazwaPliku>(.+)\.tif.+$', '\\1', line)
                        nowy_xml = os.path.join(subdir, nazwa.split('\n')[0] + '.xml')
                        print(str(count) + '\t' + nowy_xml)
                        count += 1
                        break
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
