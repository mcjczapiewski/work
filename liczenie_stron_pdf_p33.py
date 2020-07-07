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
# print("\nPodaj ścieżkę do liczenia:")
# tutaj = input()
# print("\nPodaj ścieżkę do folderu od pliku wynikowego:")
# sciezka = input()
# wynikowy = os.path.basename(os.path.normpath(sciezka))
# plikwynik = (
#     sciezka
#     + "\\"
#     + wynikowy
#     + "_strony_"
#     + czasstart.strftime("%Y-%m-%d")
#     + ".txt"
# )
# bledny = (
#     sciezka
#     + "\\"
#     + wynikowy
#     + "_BLEDY_"
#     + czasstart.strftime("%Y-%m-%d")
#     + ".txt"
# )
countope = 1
ile = 1

###########################################################

plikwynik = r"I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614\ZADANIE 4\kontrole_2020-07-06\wiecej_niz_1_strona.txt"  # noqa
bledny = r"I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614\ZADANIE 4\kontrole_2020-07-06\nie_udalo_sie_policzyc_stron.txt"  # noqa
with open(
    r"I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614\ZADANIE 4\kontrole_2020-07-06\sciezki.txt",  # noqa
    "r",
    encoding="utf-8",
) as sciezki:
    for line in sciezki:
        tutaj = line.strip()

        for subdir, dirs, files in os.walk(tutaj):
            dirs.sort(key=nkey)
            if not any(
                fname.upper().endswith(".PDF") for fname in os.listdir(subdir)
            ):
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
                        if not strony == 1:
                            with io.open(
                                plikwynik, "a", encoding="utf-8"
                            ) as wynik:
                                wynik.write(str(strony) + "\t" + plik + "\n")
                            continue
                    except:
                        with io.open(bledny, "a", encoding="utf-8") as bl:
                            bl.write(plik + "\n")
                        continue
# ile += 1

czaskoniec = datetime.datetime.now()
roznicaczas = czaskoniec - czasstart
czastrwania = roznicaczas.total_seconds() / 60
print("Czas trwania (min):")
print("%.2f" % czastrwania)
input("THE END. Press something...")
