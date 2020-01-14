# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# import bibliotek
from PIL import Image
import os
import datetime
# import ctypes

# root jesli chcemy wrzucac plik pythona do foleru, w ktorym jest
# folder do sprawdzenia rootdir = 'PARTIA 1.0'

Image.MAX_IMAGE_PIXELS = None

# zmienna-licznik przeskanowanych folderow i separator
countope = 0
separ = "\t"

# aktualna data i godzina
czasstart = datetime.datetime.now()
print("~~~~~~START~~~~~~\t" + str(czasstart).split(".")[0])

# usunac jesli stosujemy rootdir a w os.walk() wstawic 'rootdir'
print("\nPodaj ścieżkę, w której znajduje się plik zmien_dpi.txt :")
plik_lista = input()
textfile = plik_lista + "\\zmien_dpi.txt"
print("\nPodaj ścieżkę dla pliku wynikowego:")
sciezka = input()
wynikowy = os.path.basename(os.path.normpath(sciezka))
bledny = (
    sciezka
    + "\\"
    + wynikowy
    + "_BLEDY_zmien_dpi_"
    + czasstart.strftime("%Y-%m-%d")
    + ".txt"
)
print("\nPlik zostanie umieszczony w:\n" + bledny)
# print('\nPodaj nazwę okna skryptu:')
# nazwaokna = input()
# ctypes.windll.kernel32.SetConsoleTitleW(nazwaokna)

alllines = 0

with open(textfile, "r") as otxtl:
    for line in otxtl:
        alllines += 1

input(
    "\nPlików do przekonwertowania: "
    + str(alllines)
    + "\n\nWciśnij ENTER aby kontynuować..."
)

# glowna petla
with open(textfile, "r") as otxt:
    for line in otxt:

        # przypisuje do zmiennej adres jednego pliku
        zmiana = line.rstrip("\n")

        # nazwa dla nowotworzonego pliku z wyzszym dpi
        nazwa_n = "nowy_" + os.path.basename(os.path.normpath(zmiana))

        # wyciaga sciezke do folderu, w ktorym ma zostac zapisany plik
        rozdziel = os.path.split(zmiana)

        # zmienna zawierajaca koncowy adres z nazwa dla nowego pliku
        zapisz = os.path.join(rozdziel[0], nazwa_n)

        # odlicza do konca
        print(str(alllines) + separ + zmiana)
        alllines -= 1

        # proba otwarcia i zapisu zdjecia z wyzszym DPI
        try:
            img = Image.open(zmiana)
            img.save(zapisz, dpi=(300, 300))

        # jak sie nie uda to wpisuje sciezke problematycznego
        # pliku do pliku tekstowego
        except:
            with open(bledny, "a") as bl:
                bl.write(zmiana + "\n")

# czas trwania calego skryptu
czaskoniec = datetime.datetime.now()
roznicaczas = czaskoniec - czasstart
czastrwania = roznicaczas.total_seconds() / 60
print("\nCałość zajęła (minuty):")
print("%.2f" % czastrwania)
print("\n~~~~~~KONIEC~~~~~~\t" + str(czaskoniec).split(".")[0])

input("Wciśnij ENTER aby wyjść...")
