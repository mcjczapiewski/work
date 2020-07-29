# -*- coding: utf-8 -*-

import os
import re
import shutil
import datetime
# import ctypes
from pathlib import Path

# aktualna data i godzina
czasstart = datetime.datetime.now()
print("~~~~~~START~~~~~~\t" + str(czasstart).split(".")[0])

textfile = r"D:\_MACIEK_\python_proby\polaczone.txt"
bledny = r"D:\_MACIEK_\python_proby\polaczone_bledy.txt"

alllines = 0
line_nb = 1

# liczy ilosc plikow do skopiowania na podstawie
# ilosci wierszy w pliku tekstowym
with open(textfile, "r", encoding="utf-8") as otxtl:
    for line in otxtl:
        alllines += 1

input(
    "\nPlików do przeniesienia: "
    + str(alllines)
    + "\n\nWciśnij ENTER aby kontynuować..."
)

# glowna petla
with open(textfile, "r", encoding="utf-8") as otxt:
    for line in otxt:

        # odlicza do konca
        print(str(alllines))
        alllines -= 1

        # regex rozdzielajacy sciezke z ktorej
        # kopiowac od sciezki DO ktorej kopiowac
        sourcefile, destpath = line.strip().split("\t")

        # wykona tylko, jesli plik do skopiowania wciaz istnieje
        if Path(sourcefile).exists():
            try:
                shutil.copy2(sourcefile, destpath)
            except:
                with open(bledny, "a") as bl:
                    bl.write(
                        "Wystąpił nieokreślony błąd w linii:\t"
                        + str(line_nb)
                        + "\r\n"
                    )
                    continue
        else:
            with open(bledny, "a") as bl:
                bl.write(
                    "Plik z linii nr ~~"
                    + str(line_nb)
                    + "~~ już nie istnieje!\r\n"
                )
        line_nb += 1

# czas trwania calego skryptu
czaskoniec = datetime.datetime.now()
roznicaczas = czaskoniec - czasstart
czastrwania = roznicaczas.total_seconds() / 60
print("\nCałość zajęła (minuty):")
print("%.2f" % czastrwania)
print("\n~~~~~~KONIEC~~~~~~\t" + str(czaskoniec).split(".")[0])

if Path(bledny).exists():
    print("\n!PRZEANALIZUJ PLIK Z BŁĘDAMI!")

input("Wciśnij ENTER aby wyjść...")
