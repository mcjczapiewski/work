# -*- coding: utf-8 -*-

# import bibliotek
import os
import datetime
from natsort import natsort_keygen
from natsort import natsorted

nkey = natsort_keygen()

# zmienna-licznik przeskanowanych folderow i separator
count = 1
separ = "\t"

# aktualna data i godzina
czasstart = datetime.datetime.now()
print("~~~~~~START~~~~~~\t" + str(czasstart).split(".")[0])

# usunac jesli stosujemy rootdir a w os.walk() wstawic 'rootdir'
print("\nScieżka do plików pierwotnych:")
pierwotne = input()

print("\nPodaj ścieżkę dla ew. pliku z błędami:")
sciezka = input()
bledny = (
    sciezka
    + "\\"
    + os.path.basename(os.path.normpath(sciezka))
    + "_bledy_"
    + czasstart.strftime("%Y-%m-%d")
    + ".txt"
)
plikwynik = (
    sciezka
    + "\\"
    + os.path.basename(os.path.normpath(sciezka))
    + "_wynik_"
    + czasstart.strftime("%Y-%m-%d")
    + ".txt"
)
print("\nPlik zostanie umieszczony w:\n" + bledny)
input("\nWciśnij ENTER aby kontynuować...")

for subdir, dirs, files in os.walk(pierwotne):
    dirs.sort(key=nkey)
    lista = set()
    nrope = os.path.basename(subdir)
    print(str(count) + "\t" + nrope)
    count += 1
    for file in natsorted(files):
        if os.path.isdir(os.path.join(subdir, file)):
            continue
        lista.add(file)
    if lista:
        porownaj = subdir.replace(
            r"I:\skany\N", r"P:\cyfryzacja_powiat_wloclawski\WERSJA_NA_DYSKU\N"
        )
        for _, _, files in os.walk(porownaj):
            for file in natsorted(files):
                if file not in lista:
                    with open(plikwynik, "a") as pw:
                        pw.write(subdir + "\n")

# czas trwania calego skryptu
czaskoniec = datetime.datetime.now()
roznicaczas = czaskoniec - czasstart
czastrwania = roznicaczas.total_seconds() / 60
print("\nCałość zajęła (minuty):")
print("%.2f" % czastrwania)
print("\n~~~~~~KONIEC~~~~~~\t" + str(czaskoniec).split(".")[0])

input("Wciśnij ENTER aby wyjść...")
