# -*- coding: utf-8 -*-

# import bibliotek
import os
import datetime
import ctypes
from pdf2image import convert_from_path
from PIL import Image
from natsort import natsorted
from natsort import natsort_keygen
from pathlib import Path

nkey = natsort_keygen()

Image.MAX_IMAGE_PIXELS = None

# zmienna-licznik folderow i separator
countope = 0
separ = "\t"

# aktualna data i godzina
czasstart = datetime.datetime.now()
print("~~~~~~START~~~~~~\t" + str(czasstart).split(".")[0])

# deklaracja sciezki
print("\nPodaj ścieżkę głównego folderu, z którego chcesz konwertować PDFy:")
rozdziel = input()
print("\nPodaj lokalizację dla plików z błędami:")
sciezka = input()
wynikowy = os.path.basename(os.path.normpath(sciezka))
bledy_druku = (
    sciezka
    + "\\"
    + wynikowy
    + "_bledy_druku_"
    + czasstart.strftime("%Y-%m-%d")
    + ".txt"
)
nie_utworzone = (
    sciezka
    + "\\"
    + wynikowy
    + "_nie_utworzone_"
    + czasstart.strftime("%Y-%m-%d")
    + ".txt"
)
print("\nPodaj nazwę okna skryptu:")
nazwaokna = input()
ctypes.windll.kernel32.SetConsoleTitleW(nazwaokna)
input("\nWciśnij ENTER aby kontynuować...\n")
print("\nTrwa liczenie PDFów, poczekaj chwilkę...\n")

# petla liczaca pdfy
for _, _, filenames in os.walk(rozdziel):
    # ^ this idiom means "we won't be using this value"
    for filename in filenames:
        if filename.endswith((".pdf", ".PDF")):
            countope += 1

# glowna petla
for subdir, dirs, files in os.walk(rozdziel):
    dirs.sort(key=nkey)

    # rozbija sciezke do folderu i bierze tylko
    # ostatni czlon jako numer operatu
    nrope = os.path.basename(os.path.normpath(subdir))

    # poczatek petli skanujacej pliki pdf
    for file in natsorted(files):
        if file.endswith((".pdf", ".PDF")):

            # oddziela .pdf od nazwy pliku
            nazwa_pdf, rozszerzenie = os.path.splitext(file)
            nrstr = 1

            # licznik petli, wskazujacy aktualny folder z PDFem
            print(countope, separ, nrope)
            countope -= 1

            # tworzenie pelnej sciezki do rodzielanego pliku
            # na podstawie sciezki folderu i nazwy pliku
            filename = os.path.join(subdir, file)

            # konwertowanie PDF na pliki ppm
            try:
                images_from_path = convert_from_path(
                    filename, output_folder=subdir, dpi=300
                )
            except:
                with open(bledy_druku, "a") as bd:
                    bd.write(
                        "Otwarcie pliku się nie powiodło!:\t" + filename + "\n"
                    )
                break

            # konwertowanie ppm na jpg
            for page in images_from_path:

                # zfill dodaje zera wiodace
                strona = str(nrstr).zfill(3)
                nazwa = os.path.join(
                    subdir, nazwa_pdf + "__wpg_" + strona + ".jpg"
                )
                try:
                    page.save(nazwa, "JPEG", dpi=[300, 300])
                except MemoryError:
                    with open(bledy_druku, "a") as bd:
                        bd.write(
                            "PDF do rozbicia PDFillem, memoryerror!:\t"
                            + filename
                            + "\nSprawdzić pliki PDFa po nim, prawdopodobnie \
                              także trzeba poprawić.\n"
                        )
                    print(
                        "MEMORYERROR\tPlik musi zostać rozbity pdfillem\n"
                        + filename
                        + "\nSprawdzić pliki PDFa po nim, prawdopodobnie także trzeba \
                          poprawić.\nPrzechodzę do kolejnego pliku."
                    )
                    break
                except:
                    with open(bledy_druku, "a") as bd:
                        bd.write(
                            "PDF do rozbicia PDFillem, nieokreślony bład!:\t"
                            + filename
                            + "\nSprawdzić pliki PDFa po nim, prawdopodobnie \
                              także trzeba poprawić.\n"
                        )
                    print(
                        "Nieznany błąd.\tPlik musi zostać rozbity pdfillem\n"
                        + filename
                        + "\nSprawdzić pliki PDFa po nim, prawdopodobnie także trzeba \
                          poprawić.\nPrzechodzę do kolejnego pliku."
                    )
                    break
                nrstr += 1

                # sprawdza czy na pewno plik sie utworzyl
                if Path(nazwa).exists():
                    continue
                else:
                    with open(bledy_druku, "a") as bd:
                        bd.write(
                            "Strona się nie wydrukowała!:\t"
                            + strona
                            + "\t"
                            + nazwa
                            + "\n"
                        )

            for entry in os.scandir(subdir):
                if entry.name.endswith(".ppm"):
                    try:
                        os.remove(entry)
                    except PermissionError:
                        with open(bledy_druku, "a") as bd:
                            bd.write(
                                "PermissionError, możliwe że pliki \
                                ppm do usunięcia"
                                + " ręcznie w folderze!:\t"
                                + subdir
                                + "\n"
                            )
                        break
                    except:
                        with open(bledy_druku, "a") as bd:
                            bd.write(
                                "Możliwe, że pliki ppm do usunięcia \
                                ręcznie w folderze!:\t"
                                + subdir
                                + "\n"
                            )
                        break

            if Path(
                os.path.join(subdir, nazwa_pdf + "__wpg_001.jpg")
            ).exists():
                continue
            else:
                with open(nie_utworzone, "a") as nu:
                    nu.write(filename + "\n")

# czas trwania calego skryptu
czaskoniec = datetime.datetime.now()
roznicaczas = czaskoniec - czasstart
czastrwania = roznicaczas.total_seconds() / 60
print("\nCałość zajęła (minuty):")
print("%.2f" % czastrwania)
print("\n~~~~~~KONIEC~~~~~~\t" + str(czaskoniec).split(".")[0])

input("Wciśnij ENTER aby wyjść...")
