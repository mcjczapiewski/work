# -*- coding: utf-8 -*-

import os
import datetime
from PIL import Image

# zmienne i przechowywanie linii
lines_seen = set()
nie_powtarzaj = set()
countope = 0

# aktualna data i godzina
czasstart = datetime.datetime.now()
print("~~~~~~START~~~~~~\t" + str(czasstart).split(".")[0])
uplynelo = datetime.datetime.now()

# sciezki do plikow
print("\nPodaj dokładną ścieżkę folderu, w którym chcesz porównywać:")
sprawdzanie = input()
print("\nPodaj dokładną ścieżkę folderu, w którym chcesz porównywać 2:")
porownanie = input()
print("\nPodaj ścieżkę dla pliku wynikowego:")
sciezka = input()
wynikowy = os.path.basename(os.path.normpath(sciezka))
plikwynik = (
    sciezka
    + "\\"
    + wynikowy
    + "_identyczne_"
    + czasstart.strftime("%Y-%m-%d")
    + ".txt"
)
print("\nPlik zostanie umieszczony w:\n" + plikwynik)
bledny = (
    sciezka
    + "\\"
    + wynikowy
    + "_BLEDY_"
    + czasstart.strftime("%Y-%m-%d")
    + ".txt"
)
input("\nWciśnij ENTER aby kontynuować...")

# glowna petla
for subdir, dirs, files in os.walk(sprawdzanie):
    dirs.sort()
    folder_glowny = subdir

    # rozbija sciezke do folderu i bierze tylko
    # ostatni czlon jako numer operatu
    nrope = os.path.basename(os.path.normpath(subdir))
    print(countope)
    countope += 1

    # petla dla plikow w folderze glownym
    for file in sorted(files):
        przerwa = 0

        if file.endswith((".jpg", ".jpeg", ".JPG", ".JPEG")):
            pierwotne = file
            pierwsze = os.path.join(folder_glowny, pierwotne)

            # proba otwarcia zdjecia
            try:
                original = Image.open(pierwsze)

            # jak nie otworzy to przechodzi do kolejnego
            # zdjecia w folderze (continue)
            except:
                with open(bledny, "a") as bl:
                    bl.write(pierwsze + "\tnie otworzyło się\tPIERWSZE\n")
                continue

            # petla dodatkowa, pliki do porownania z oryginalem
            for subdir, dirs, files in os.walk(porownanie):
                dirs.sort()
                for file in sorted(files):

                    # kontynuacja petli
                    if file.endswith((".jpg", ".jpeg", ".JPG", ".JPEG")):
                        porownane = file
                        drugie = os.path.join(subdir, porownane)

                        # aby mogly byc te same obrazy, w naszym przypadku
                        # beda tez te same nazwy plikow, a wiec:
                        if (nrope + pierwotne) == (
                            os.path.basename(subdir) + porownane
                        ):
                            print("NAZWY TE SAME")

                            # sprawdza czy plik oryginalny nie byl juz
                            # sprawdzany z drugim w odwrotnej kolejnosci
                            # (a,b = b,a), jak byly to bierze kolejny plik
                            czy_bylo = str(drugie + "\t" + pierwsze)
                            if czy_bylo in lines_seen:
                                continue

                            # jesli jeszcze nie byly to dodaje ta kombinacje
                            # do pamieci, zeby przy
                            # kolejnych plikach znow sprawdzic
                            else:
                                line = str(pierwsze + "\t" + drugie)
                                lines_seen.add(line)

                                # jesli sciezka pierwszego pliku zgadza sie ze
                                # sciezka drugiego to ich nie powrownuje
                                # (ten sam plik)
                                if pierwsze == drugie:
                                    continue

                                # jesli jeszcze nie byly ze soba porownane,
                                # to je porownuje
                                else:
                                    try:
                                        image_to_compare = Image.open(drugie)

                                    # jak nie otworzy zdjecia to przechodzi do
                                    # kolejnego po zapisaniu bledu do pliku
                                    # tekstowego
                                    except:
                                        with open(bledny, "a") as bl:
                                            bl.write(
                                                drugie
                                                + "\tnie otworzyło \
                                                    się\tDRUGIE\n"
                                            )
                                        continue

                                    # podejmuje probe porownania
                                    try:
                                        # jesli ksztalty sa identyczne to
                                        # sprawdza roznice w kanalach RGB
                                        if (
                                            len(original.fp.read())
                                            == len(image_to_compare.fp.read())
                                            and original.size
                                            == image_to_compare.size
                                        ):
                                            with open(plikwynik, "a") as wynik:
                                                wynik.write(
                                                    "IDENTYCZNE\t"
                                                    + pierwsze
                                                    + "\t"
                                                    + drugie
                                                    + "\n"
                                                )
                                            przerwa = 1
                                            break

                                        else:
                                            with open(bledny, "a") as bl:
                                                bl.write(
                                                    pierwsze
                                                    + "\t"
                                                    + drugie
                                                    + "\trozne\n"
                                                )
                                            continue

                                    # jak nie da sie ich otworzyc i porownac
                                    # nawet ksztaltow to wypisze informacje
                                    # do pliku
                                    except:
                                        with open(bledny, "a") as bl:
                                            bl.write(
                                                pierwsze
                                                + "\t"
                                                + drugie
                                                + "\tnie zostały porównane\n"
                                            )
                                        continue

                if przerwa == 1:
                    break

# czas trwania calego skryptu
czaskoniec = datetime.datetime.now()
roznicaczas = czaskoniec - czasstart
czastrwania = roznicaczas.total_seconds() / 60
print("\nCałość zajęła (minuty):")
print("%.2f" % czastrwania)
print("\n~~~~~~KONIEC~~~~~~\t" + str(czaskoniec).split(".")[0])

input("Wciśnij ENTER aby wyjść...")
