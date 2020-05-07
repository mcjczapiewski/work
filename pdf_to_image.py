# -*- coding: utf-8 -*-

# import bibliotek
import os
import datetime

# import ctypes
from pdf2image import convert_from_path
from PIL import Image
from natsort import natsorted
from natsort import natsort_keygen
from pathlib import Path

nkey = natsort_keygen()

Image.MAX_IMAGE_PIXELS = None

# zmienna-licznik folderow
pdfs_counter = 0

# aktualna data i godzina
time_start = datetime.datetime.now()
print("~~~~~~START~~~~~~\t" + str(time_start).split(".")[0])

# deklaracja sciezki
print("\nPodaj ścieżkę głównego folderu, z którego chcesz konwertować PDFy:")
main_path = input()
print("\nPodaj lokalizację dla plików z błędami:")
error_files_path = input()
results_file = os.path.basename(os.path.normpath(error_files_path))
page_print_errors = (
    error_files_path
    + "\\"
    + results_file
    + "_bledy_druku_"
    + time_start.strftime("%Y-%m-%d")
    + ".txt"
)
not_printed = (
    error_files_path
    + "\\"
    + results_file
    + "_nie_utworzone_"
    + time_start.strftime("%Y-%m-%d")
    + ".txt"
)
# print("\nPodaj nazwę okna skryptu:")
# nazwaokna = input()
# ctypes.windll.kernel32.SetConsoleTitleW(nazwaokna)
# input("\nWciśnij ENTER aby kontynuować...\n")
print("\nTrwa liczenie PDFów, poczekaj chwilkę...\n")

# petla liczaca pdfy
for _, _, filenames in os.walk(main_path):
    for filename in filenames:
        if filename.endswith((".pdf", ".PDF")):
            pdfs_counter += 1

# glowna petla
for subdir, dirs, files in os.walk(main_path):
    dirs.sort(key=nkey)
    if "merge" not in subdir:
        continue
    # rozbija sciezke do folderu i bierze tylko
    # ostatni czlon jako numer operatu
    operat_number = os.path.basename(os.path.dirname(subdir))

    # poczatek petli skanujacej pliki pdf
    for file in natsorted(files):
        if file.endswith((".pdf", ".PDF")):

            # oddziela .pdf od nazwy pliku
            pdf_name, extension = os.path.splitext(file)
            page_number = 1

            # licznik petli, wskazujacy aktualny folder z PDFem
            print(f"{pdfs_counter}\t{operat_number}")
            pdfs_counter -= 1

            # tworzenie pelnej sciezki do rodzielanego pliku
            # na podstawie sciezki folderu i nazwy pliku
            filename = os.path.join(subdir, file)

            # konwertowanie PDF na pliki ppm
            try:
                images_from_path = convert_from_path(
                    filename, output_folder=subdir, dpi=300
                )
            except:
                with open(
                    page_print_errors, "a", encoding="utf-8"
                ) as errors_file:
                    errors_file.write(
                        "Otwarcie pliku się nie powiodło!:\t" + filename + "\n"
                    )
                break

            # konwertowanie ppm na jpg
            for page in images_from_path:

                # zfill dodaje zera wiodace
                jpg_page_number = str(page_number).zfill(3)
                jpg_name = os.path.join(
                    subdir, pdf_name + "__wpg_" + jpg_page_number + ".jpg"
                )
                try:
                    page.save(jpg_name, "JPEG", dpi=[300, 300])
                except MemoryError:
                    with open(
                        page_print_errors, "a", encoding="utf-8"
                    ) as errors_file:
                        errors_file.write(
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
                    with open(
                        page_print_errors, "a", encoding="utf-8"
                    ) as errors_file:
                        errors_file.write(
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
                page_number += 1

                # sprawdza czy na pewno plik sie utworzyl
                if Path(jpg_name).exists():
                    continue
                else:
                    with open(
                        page_print_errors, "a", encoding="utf-8"
                    ) as errors_file:
                        errors_file.write(
                            "Strona się nie wydrukowała!:\t"
                            + jpg_page_number
                            + "\t"
                            + jpg_name
                            + "\n"
                        )

            for entry in os.scandir(subdir):
                if entry.name.endswith(".ppm"):
                    try:
                        os.remove(entry)
                    except PermissionError:
                        with open(
                            page_print_errors, "a", encoding="utf-8"
                        ) as errors_file:
                            errors_file.write(
                                "PermissionError, możliwe że pliki \
                                ppm do usunięcia"
                                + " ręcznie w folderze!:\t"
                                + subdir
                                + "\n"
                            )
                        break
                    except:
                        with open(
                            page_print_errors, "a", encoding="utf-8"
                        ) as errors_file:
                            errors_file.write(
                                "Możliwe, że pliki ppm do usunięcia \
                                ręcznie w folderze!:\t"
                                + subdir
                                + "\n"
                            )
                        break

            if Path(os.path.join(subdir, pdf_name + "__wpg_001.jpg")).exists():
                continue
            else:
                with open(not_printed, "a", encoding="utf-8") as errors_file:
                    errors_file.write(filename + "\n")

# czas trwania calego skryptu
time_end = datetime.datetime.now()
time_delta = time_end - time_start
time_duration = time_delta.total_seconds() / 60
print("\nCałość zajęła (minuty):")
print("%.2f" % time_duration)
print("\n~~~~~~KONIEC~~~~~~\t" + str(time_end).split(".")[0])

input("Wciśnij ENTER aby wyjść...")
