# -*- coding: utf-8 -*-

# import bibliotek
import os
import datetime

# zmienna-licznik przeskanowanych folderow i separator
countope = 0

# aktualna data i godzina
czasstart = datetime.datetime.now()
print("~~~~~~START~~~~~~\t" + str(czasstart).split(".")[0])

# usunac jesli stosujemy rootdir a w os.walk() wstawic 'rootdir'
print("\nPodaj ścieżkę do sprawdzania numeracji szkiców:")
sprnr = input()
input("\nWciśnij ENTER aby kontynuować...")
file = r"D:\python_proby\spis_arkuszy.txt"

lines_seen = set(line.strip() for line in open(file))


# glowna petla
for subdir, dirs, files in os.walk(sprnr):
    dirs.sort()

    # wyciaga nr operatu ze sciezki
    nrope = str.split(os.path.basename(subdir), ";")

    # licznik
    # print(str(countope)+'\t'+nrope)
    # countope += 1

    if not nrope[0] in lines_seen:
        print(nrope)

# czas trwania calego skryptu
czaskoniec = datetime.datetime.now()
roznicaczas = czaskoniec - czasstart
czastrwania = roznicaczas.total_seconds() / 60
print("\nCałość zajęła (minuty):")
print("%.2f" % czastrwania)
print("\n~~~~~~KONIEC~~~~~~\t" + str(czaskoniec).split(".")[0])

input("Wciśnij ENTER aby wyjść...")
