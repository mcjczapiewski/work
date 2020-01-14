# -*- coding: utf-8 -*-

# import bibliotek
import os
import datetime
from natsort import natsorted, natsort_keygen

nkey = natsort_keygen()

# zmienna-licznik przeskanowanych folderow i separator
countope = 0
separ = "\t"

# aktualna data i godzina
czasstart = datetime.datetime.now()
print("~~~~~~START~~~~~~\t" + str(czasstart).split(".")[0])

# usunac jesli stosujemy rootdir a w os.walk() wstawic 'rootdir'
print("\nPodaj dokładną ścieżkę folderu, z którego chcesz liczyć zdjęcia:")
liczenie = input()
print("\nPodaj ścieżkę dla pliku wynikowego:")
sciezka = input()
wynikowy = os.path.basename(os.path.normpath(sciezka))
bledny = (
    sciezka + "\\" + wynikowy + "_" + czasstart.strftime("%Y-%m-%d") + ".txt"
)
print("\nPlik zostanie umieszczony w:\n" + bledny)
input("\nWciśnij ENTER aby kontynuować...")

# glowna petla
for subdir, dirs, files in os.walk(liczenie):
    dirs.sort(key=nkey)
    zdjecia = 0
    # rozbija sciezke do folderu i bierze tylko
    # ostatni czlon jako numer operatu
    nrope = os.path.basename(os.path.normpath(subdir))
    folder_name = os.path.join(subdir, nrope)

    # licznik petli, wskazujacy aktualnie skanowany folder z operatem
    countope += 1
    print(countope, separ, nrope)

    # poczatek petli skanujacej pliki jpg
    for file in natsorted(files):
        nowego = file.upper()
        if nowego.endswith((".JPG", ".JPEG")):
            zdjecia += 1
    with open(bledny, "a") as wynik:
        wynik.write(subdir + "\t" + str(zdjecia) + "\n")

# czas trwania calego skryptu
czaskoniec = datetime.datetime.now()
roznicaczas = czaskoniec - czasstart
czastrwania = roznicaczas.total_seconds() / 60
print("\nCałość zajęła (minuty):")
print("%.2f" % czastrwania)
print("\n~~~~~~KONIEC~~~~~~\t" + str(czaskoniec).split(".")[0])

input("Wciśnij ENTER aby wyjść...")
