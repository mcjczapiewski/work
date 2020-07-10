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
separ = "\t"
lista = set()

# aktualna data i godzina
czasstart = datetime.datetime.now()
print("~~~~~~START~~~~~~\t" + str(czasstart).split(".")[0])

# usunac jesli stosujemy rootdir a w os.walk() wstawic 'rootdir'
print("\nPodaj ścieżkę folderu, z którego chcesz rozrzucić pliki:")
tutaj = input()
input("\nWciśnij ENTER aby kontynuować...")

# glowna petla
for subdir, dirs, files in os.walk(tutaj):
    dirs.sort(key=nkey)
    oklad = subdir

    for file in natsorted(files):
        czlony = file.rsplit("_")
        if fnmatch.fnmatch(file, "*kladk*"):
            okladka = os.path.join(oklad, file)
            if okladka not in lista:
                for subdir, dirs, _ in os.walk(oklad):
                    if fnmatch.fnmatch(os.path.basename(subdir), "19*"):
                        shutil.copy2(os.path.join(oklad, file), subdir)
                        lista.add(os.path.join(subdir, file))

        elif re.match("^.+SPI.*", file):
            spis = os.path.join(oklad, file)
            if spis not in lista:
                newdest = os.path.join(oklad, czlony[0])
                for subdir, dirs, _ in os.walk(newdest):
                    if fnmatch.fnmatch(os.path.basename(subdir), "19*"):
                        shutil.copy2(os.path.join(oklad, file), subdir)
                        lista.add(os.path.join(subdir, file))

# czas trwania calego skryptu
czaskoniec = datetime.datetime.now()
roznicaczas = czaskoniec - czasstart
czastrwania = roznicaczas.total_seconds() / 60
print("\nCałość zajęła (minuty):")
print("%.2f" % czastrwania)
print("\n~~~~~~KONIEC~~~~~~\t" + str(czaskoniec).split(".")[0])

input("Wciśnij ENTER aby wyjść...")
