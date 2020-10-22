# -*- coding: utf-8 -*-

# import bibliotek
import os
import datetime
import img2pdf
import fnmatch as fn
from natsort import natsorted, natsort_keygen
from PIL import Image

nkey = natsort_keygen()

Image.MAX_IMAGE_PIXELS = None
countope = 1

# aktualna data i godzina
czasstart = datetime.datetime.now()
print("~~~~~~START~~~~~~\t" + str(czasstart).split(".")[0])

# usunac jesli stosujemy rootdir a w os.walk() wstawic 'rootdir'
print("\nPodaj ścieżkę folderu ze zdjęciami:")
tutaj = input()
bledy = os.path.join(tutaj, "BLEDY" + czasstart.strftime("%Y-%m-%d") + ".txt")
input("\nWciśnij ENTER aby kontynuować...")

for subdir, dirs, files in os.walk(tutaj):
    zbior_spis = []
    zbior = []
    aktualizuj = 1

    czyjpg = 0
    for file in files:
        if file.endswith(".jpg"):
            czyjpg = 1
            break
    if czyjpg == 1:

        pdf_spis = os.path.join(subdir, "SPIS.pdf")
        dirs.sort(key=nkey)
        print(str(countope) + "\t" + os.path.normpath(subdir))
        countope += 1

        for file in natsorted(files):
            if file.endswith(".jpg") and fn.fnmatch(file, "*klad*"):
                zbior_spis.append(os.path.join(subdir, file))

        for file in natsorted(files):
            if file.endswith(".jpg") and fn.fnmatch(file, "*SPIS*"):
                zbior_spis.append(os.path.join(subdir, file))
            elif file.endswith(".jpg") and not fn.fnmatch(file, "*klad*"):
                czlony = file.rsplit("_")
                if aktualizuj == 1:
                    c2 = czlony[2]
                    aktualizuj = 0
                if czlony[2] == c2:
                    zbior.append(os.path.join(subdir, file))
                else:
                    try:
                        with open(
                            os.path.join(subdir, c2 + ".pdf"), "wb"
                        ) as nowepdf:
                            assert nowepdf.write(
                                img2pdf.convert([i for i in zbior])
                            )
                    except:
                        with open(bledy, "a") as bl:
                            bl.write(
                                os.path.join(subdir, c2 + ".pdf")
                                + "\tSprawdz PDFa\n"
                            )
                    c2 = czlony[2]
                    zbior = []
                    zbior.append(os.path.join(subdir, file))

        try:
            with open(pdf_spis, "wb") as nowepdf:
                nowepdf.write(img2pdf.convert([i for i in zbior_spis]))
        except:
            with open(bledy, "a") as bl:
                bl.write(pdf_spis + "\tSprawdz PDFa\n")
        try:
            with open(os.path.join(subdir, c2 + ".pdf"), "wb") as nowepdf:
                nowepdf.write(img2pdf.convert([i for i in zbior]))
        except:
            with open(bledy, "a") as bl:
                bl.write(
                    os.path.join(subdir, c2 + ".pdf") + "\tSprawdz PDFa\n"
                )

# czas trwania calego skryptu
czaskoniec = datetime.datetime.now()
roznicaczas = czaskoniec - czasstart
czastrwania = roznicaczas.total_seconds() / 60
print("\nCałość zajęła (minuty):")
print("%.2f" % czastrwania)
print("\n~~~~~~KONIEC~~~~~~\t" + str(czaskoniec).split(".")[0])

input("Wciśnij ENTER aby wyjść...")
