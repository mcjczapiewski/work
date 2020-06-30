# -*- coding: utf-8 -*-
import os
import datetime
import fitz
import regex
import io
from natsort import natsorted, natsort_keygen

nkey = natsort_keygen()

###########################################################

czasstart = datetime.datetime.now()
print("~~~~~~START~~~~~~\t" + str(czasstart).split(".")[0])
print("\nPodaj ścieżkę do liczenia:")
tutaj = input()
print("\nPodaj ścieżkę do folderu od pliku wynikowego:")
sciezka = input()
wynikowy = os.path.basename(os.path.normpath(sciezka))
plikwynik = (
    sciezka
    + "\\"
    + wynikowy
    + "_strony_"
    + czasstart.strftime("%Y-%m-%d")
    + ".txt"
)
bledny = (
    sciezka
    + "\\"
    + wynikowy
    + "_BLEDY_"
    + czasstart.strftime("%Y-%m-%d")
    + ".txt"
)
countope = 1
ile = 1

###########################################################

with open(r"\\waw-dt1407\I\04_KOPIA_PLIKOWA\kontrole_2020-06-30\sciezki.txt", "r") as sciezki:
    for line in sciezki:
        tutaj = line.strip()

        for subdir, dirs, files in os.walk(tutaj):
            dirs.sort(key=nkey)
            if not any(fname.upper().endswith(".PDF") for fname in os.listdir(subdir)):
                continue
            nrope = (
                os.path.basename(os.path.dirname(subdir))
                + "_"
                + os.path.basename(subdir)
            )
            print(str(countope) + "\t" + nrope)
            # print(str(ile) + "_" + str(countope) + "\t" + nrope)
            countope += 1
            for file in natsorted(files):
                if file.upper().endswith(".PDF") and regex.match(
                    r"^.+(-SZK-|-M-|-Z-).+\.PDF", file.upper()
                ):
                    plik = os.path.join(subdir, file)
                    try:
                        doc = fitz.open(plik)
                        strony = doc.pageCount
                        # for page in doc:
                        #     x = str(page.MediaBox).split(" ")[2].split(",")[0]
                        #     y = str(page.MediaBox).split(" ")[3].split(")")[0]
                        #     area = (float(x) * float(y)) / (72 * 72)
                        if not strony == 1:
                            with io.open(
                                plikwynik, "a", encoding="utf-8"
                            ) as wynik:
                                wynik.write(str(strony) + "\t" + plik + "\n")
                            continue
                    except:
                        with io.open(bledny, "a", encoding="utf-8") as bl:
                            bl.write("Nie udało się otworzyć:\t" + plik + "\n")
                        continue
# ile += 1

czaskoniec = datetime.datetime.now()
roznicaczas = czaskoniec - czasstart
czastrwania = roznicaczas.total_seconds() / 60
print("Czas trwania (min):")
print("%.2f" % czastrwania)
input("THE END. Press something...")
