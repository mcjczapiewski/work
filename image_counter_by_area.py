# -*- coding: cp1250 -*-

# import bibliotek
from PIL import Image
import os
import math
import datetime
import ctypes

Image.MAX_IMAGE_PIXELS = None

# zmienna-licznik przeskanowanych folderow i separator
countope = 0
separ = "\t"

# aktualna data i godzina
czasstart = datetime.datetime.now()
print("~~~~~~START~~~~~~\t" + str(czasstart).split(".")[0])

# usunac jesli stosujemy rootdir a w os.walk() wstawic 'rootdir'
print(
    "\nPodaj dokładną ścieżkę folderu, \
        z którego chcesz liczyć strony:"
)
liczenie = input()
print("\nPodaj ścieżkę dla pliku wynikowego:")
sciezka = input()
wynikowy = os.path.basename(os.path.normpath(sciezka))
plikwynik = (
    sciezka
    + "\\"
    + wynikowy
    + "_zliczone_strony_"
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
print("\nPodaj nazwę okna skryptu:")
nazwaokna = input()
ctypes.windll.kernel32.SetConsoleTitleW(nazwaokna)
input("\nWciśnij ENTER aby kontynuować...")
print("\nTrwa liczenie folderów, poczekaj chwilkę...\n")

# petla liczaca foldery
for _, dirnames, _ in os.walk(liczenie):
    # ^ this idiom means "we won't be using this value"
    countope += len(dirnames)

# utworzenie wynikowego pliku tekstowego z pierwsza
# linijka zawierajaca opisy kolumn
with open(plikwynik, "a") as wynik:
    wynik.write(
        "Numer operatu\tA0\tA1\tA2\tA3\tA4\tniewymiarowe \
            przeliczone na A4\tSUMA A4\n"
    )

# glowna petla
for subdir, dirs, files in os.walk(liczenie):
    dirs.sort()

    # rozbija sciezke do folderu i bierze tylko
    # ostatni czlon jako numer operatu
    nrope = os.path.basename(os.path.normpath(subdir))

    # deklaracja zmiennych
    A0 = A1 = A2 = A3 = A4 = A4r = resized = 0

    # licznik petli, wskazujacy aktualnie skanowany folder z operatem
    print(countope, separ, nrope)
    countope -= 1

    # poczatek petli skanujacej pliki jpg
    for file in sorted(files):
        if (
            file.endswith(".jpg")
            or file.endswith(".JPG")
            or file.endswith(".jpeg")
            or file.endswith(".JPEG")
        ):

            # tworzenie pelnej sciezki do skanowanego pliku
            # na podstawie sciezki folderu i nazwy pliku
            filename = os.path.join(subdir, file)

            try:
                # otwarcie zdjecia
                img = Image.open(filename)

                # czy jest informacja o DPI zdjecia
                if img.info.get("dpi"):

                    # odczytanie i spisanie wartosci pikseli i dpi
                    width, height = img.size
                    xdpi, ydpi = img.info["dpi"]

                    # obliczenie ;pola powierzchni; danego zdjecia
                    imagearea = float(((width * height) / (xdpi * ydpi)))

                    # zalozenia typu ;co jesli zdjecie ma wymiar;
                    if imagearea < 97:
                        A4 += 1
                    elif 192 < imagearea < 195:
                        A3 += 1
                    elif 385 < imagearea < 388:
                        A2 += 1
                    elif 773 < imagearea < 776:
                        A1 += 1
                    elif 1548 < imagearea < 1551:
                        A0 += 1

                    # jesli nie miesci sie w zadnym przedziale, to suma
                    # powierzchni dzielona przez pole powierzchni kartki A4
                    else:
                        resized = float(resized + imagearea)

                # jesli zdjecie nie ma DPI zapisz komunikat
                else:
                    with open(bledny, "a") as bl:
                        bl.write("Zdjęcie nie ma DPI: " + filename + "\n")

            except:
                with open(bledny, "a") as bl:
                    bl.write(
                        "Nie udało się otworzyć zdjęcia: "
                        + filename
                        + "\n"
                    )

    # math.ceil zaokragla zawsze w gore
    A4r = int(math.ceil(float(resized / 96.665)))
    A4sum = A4 + (A3 * 2) + (A2 * 4) + (A1 * 8) + (A0 * 16) + A4r

    # zapis otrzymanych wynikow z danego folderu do wskazanego pliku wynikowego
    with open(plikwynik, "a") as wynik:
        wynik.write(
            nrope
            + "\t"
            + str(A0)
            + "\t"
            + str(A1)
            + "\t"
            + str(A2)
            + "\t"
            + str(A3)
            + "\t"
            + str(A4)
            + "\t"
            + str(A4r)
            + "\t"
            + str(A4sum)
            + "\n"
        )

# czas trwania calego skryptu
czaskoniec = datetime.datetime.now()
roznicaczas = czaskoniec - czasstart
czastrwania = roznicaczas.total_seconds() / 60
print("\nCałość zajęła (minuty):")
print("%.2f" % czastrwania)
print("\n~~~~~~KONIEC~~~~~~\t" + str(czaskoniec).split(".")[0])

input("Wciśnij ENTER aby wyjść...")
