# -*- coding: utf-8 -*-

# import bibliotek
import os
import datetime
import shutil
import fnmatch
import re
from natsort import natsorted, natsort_keygen
nkey = natsort_keygen()

# zmienna-licznik przeskanowanych folderow i separator
countope = 0
separ = '\t'

# aktualna data i godzina
czasstart = datetime.datetime.now()
print("~~~~~~START~~~~~~\t" + str(czasstart).split('.')[0])

# usunac jesli stosujemy rootdir a w os.walk() wstawic 'rootdir'
print('\nPodaj ścieżkę folderu, z którego chcesz rozrzucić pliki:')
tutaj = input()
input("\nWciśnij ENTER aby kontynuować...")

# glowna petla
for subdir, dirs, files in os.walk(tutaj):
    dirs.sort(key=nkey)

    for file in natsorted(files):
        czlony = re.split(';|_', file)
        if (not fnmatch.fnmatch(file, '*SPIS*') and not fnmatch.fnmatch(file, '*kladk*')
                and file.endswith('.pdf')):
            newdest = os.path.join(subdir, czlony[2])
            if not os.path.exists(newdest):
                os.mkdir(newdest)
                newdest = os.path.join(newdest, czlony[4])
                if os.path.exists(newdest):
                    shutil.move(os.path.join(subdir, file), newdest)
                else:
                    os.mkdir(newdest)
                    shutil.move(os.path.join(subdir, file), newdest)
            else:
                newdest = os.path.join(newdest, czlony[4])
                if os.path.exists(newdest):
                    shutil.move(os.path.join(subdir, file), newdest)
                else:
                    os.mkdir(newdest)
                    shutil.move(os.path.join(subdir, file), newdest)

# czas trwania calego skryptu
czaskoniec = datetime.datetime.now()
roznicaczas = czaskoniec - czasstart
czastrwania = roznicaczas.total_seconds() / 60
print('\nCałość zajęła (minuty):')
print("%.2f" % czastrwania)
print("\n~~~~~~KONIEC~~~~~~\t" + str(czaskoniec).split('.')[0])

input('Wciśnij ENTER aby wyjść...')
