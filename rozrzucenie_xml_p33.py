# -*- coding: utf-8 -*-

# import bibliotek
import os
import datetime
import shutil
from natsort import natsorted
from natsort import natsort_keygen
nkey = natsort_keygen()
byly = set()
stare_xml = set()
nowe_xml = set()
count = 1

# aktualna data i godzina
czasstart = datetime.datetime.now()
print("~~~~~~START~~~~~~\t" + str(czasstart).split('.')[0])

print('\n\nUWAGA! W folderze z xmlami mogą pojawić się 4 pliki tekstowe:\n- bledy\n- \
      podmienione\n- brak_odpowiednika_dla_xmla\n- brak_nowego_xmla_dla_operatu\n\n')

tusaxml = input('Podaj ścieżkę do folderu z plikami xml: ')
tusaoperaty = input('Podaj ścieżkę do folderu z operatami: ')

for subdir, dirs, _ in os.walk(tusaoperaty):
    dirs.sort(key=nkey)
    operat = subdir
    stare_xml.add(operat)
    for subdir, dirs, files in os.walk(tusaxml):
        dirs.sort(key=nkey)
        for file in natsorted(files):
            if file.endswith(('.xml', '.XML')):
                if os.path.splitext(file)[0] == os.path.basename(operat):
                    print(count)
                    count += 1
                    if not os.path.exists(os.path.join(operat, file)):
                        try:
                            shutil.copy(os.path.join(subdir, file), os.path.join(operat, file))
                        except:
                            with open(os.path.join(tusaxml, 'bledy.txt'), 'a') as bledy:
                                bledy.write(os.path.join(subdir, file) + '\tNie udało się skopiować.\n')
                    else:
                        try:
                            shutil.copy(os.path.join(subdir, file), os.path.join(operat, file))
                            with open(os.path.join(tusaxml, 'podmienione.txt'), 'a') as bledy:
                                bledy.write(os.path.join(operat, file) + '\n')
                        except:
                            with open(os.path.join(tusaxml, 'bledy.txt'), 'a') as bledy:
                                bledy.write(os.path.join(subdir, file) + '\tNie udało się skopiować.\n')
                    byly.add(os.path.join(subdir, file))
                    nowe_xml.add(operat)


for subdir, dirs, files in os.walk(tusaxml):
    dirs.sort(key=nkey)
    for file in natsorted(files):
        if file.upper().endswith('.XML'):
            if os.path.join(subdir, file) not in byly:
                with open(os.path.join(tusaxml, 'brak_odpowiednika_dla_xmla.txt'), 'a') as bledy:
                    bledy.write(os.path.join(subdir, file) + '\n')

for i in natsorted(stare_xml):
    if i not in nowe_xml:
        with open(os.path.join(tusaxml, 'brak_nowego_xmla_dla_operatu.txt'), 'a') as bledy:
            bledy.write(os.path.join(i) + '\n')

# czas trwania calego skryptu
czaskoniec = datetime.datetime.now()
roznicaczas = czaskoniec - czasstart
czastrwania = roznicaczas.total_seconds() / 60
print('\nCałość zajęła (minuty):')
print("%.2f" % czastrwania)
print("\n~~~~~~KONIEC~~~~~~\t" + str(czaskoniec).split('.')[0])

input('Wciśnij ENTER aby wyjść...')
