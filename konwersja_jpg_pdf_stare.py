# -*- coding: utf-8 -*-

# import bibliotek
import os
import datetime
import img2pdf
import fnmatch as fn
from natsort import natsorted, natsort_keygen
nkey = natsort_keygen()

# aktualna data i godzina
czasstart = datetime.datetime.now()
print("~~~~~~START~~~~~~\t" + str(czasstart).split('.')[0])

# usunac jesli stosujemy rootdir a w os.walk() wstawic 'rootdir'
print('\nPodaj ścieżkę folderu ze zdjęciami:')
tutaj = input()
bledy = os.path.join(tutaj, 'BLEDY' + czasstart.strftime('%Y-%m-%d') + '.txt')
input("\nWciśnij ENTER aby kontynuować...")


# glowna petla
for subdir, dirs, files in os.walk(tutaj):
    dirs.sort(key=nkey)
    czyjpg = 0
    for file in natsorted(files):
        if file.endswith('.jpg'):
            czyjpg = 1
            break
    if czyjpg == 1:
        nrzm = os.path.basename(subdir)
        spispdf = os.path.join(subdir, nrzm.split('_')[0] + '_SPIS.pdf')
        zmpdf = os.path.join(subdir, nrzm + '.pdf')
        print(nrzm)
        try:
            with open(spispdf, 'wb') as sp:
                sp.write(img2pdf.convert([os.path.join(subdir, file) for file in natsorted(files)
                                         if fn.fnmatch(file, '*SPIS*')]))
        except:
            with open(bledy, 'a') as bl:
                bl.write(os.path.join(subdir, file) + '\tnie dodany do PDFa\n')
        try:
            with open(zmpdf, 'wb') as zp:
                zp.write(img2pdf.convert([os.path.join(subdir, file) for file in natsorted(files)
                                         if not fn.fnmatch(file, '*SPIS*')]))
        except:
            with open(bledy, 'a') as bl:
                bl.write(os.path.join(subdir, file) + '\tnie dodany do PDFa\n')

# czas trwania calego skryptu
czaskoniec = datetime.datetime.now()
roznicaczas = czaskoniec - czasstart
czastrwania = roznicaczas.total_seconds() / 60
print('\nCałość zajęła (minuty):')
print("%.2f" % czastrwania)
print("\n~~~~~~KONIEC~~~~~~\t" + str(czaskoniec).split('.')[0])

input('Wciśnij ENTER aby wyjść...')
