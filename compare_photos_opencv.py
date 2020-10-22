# -*- coding: utf-8 -*-

import cv2
import os
import datetime
import fnmatch

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
print("\nTrwa liczenie folderów, poczekaj chwilkę...\n")

# petla liczaca foldery
for _, dirnames, _ in os.walk(sprawdzanie):
    # ^ this idiom means "we won't be using this value"
    countope += len(dirnames)
    wszystkieope = countope

# glowna petla
for subdir, dirs, files in os.walk(sprawdzanie):
    dirs.sort()
    folder_glowny = subdir
    plik_z_kolei = 1
    countpliki = przerwa = 0

    # rozbija sciezke do folderu i bierze
    # tylko ostatni czlon jako numer operatu
    nrope = os.path.basename(os.path.normpath(subdir))

    # ile minelo czasu od poczatku
    czastrwania = (datetime.datetime.now() - czasstart).total_seconds() / 60
    print("\nOd początku minęło: " + "%.2f" % czastrwania + "min")
    ten_folder_czas = datetime.datetime.now()

    # liczy pliki w danym folderze
    countpliki = len(
        fnmatch.filter(
            next(os.walk(folder_glowny))[2],
            "*.jpg" or "*.jepg" or "*.JPG" or "*.JPEG",
        )
    )

    # licznik petli, wskazujacy aktualnie skanowany folder z operatem
    print(str(countope) + " z " + str(wszystkieope) + "\t" + nrope)
    countope -= 1

    # petla dla plikow w folderze glownym
    for file in sorted(files):
        if (file.endswith(".jpg" or ".jpeg" or ".JPG" or ".JPEG")) and (
            plik_z_kolei
            in [1, countpliki // 3, int(countpliki // 1.5), countpliki - 1]
        ):
            pierwotne = file
            pierwsze = os.path.join(folder_glowny, pierwotne)
            countfiles = 0

            # proba otwarcia zdjecia
            try:
                original = cv2.imread(pierwsze)

            # jak nie otworzy to przechodzi do kolejnego
            # zdjecia w folderze (continue)
            except:
                with open(bledny, "a") as bl:
                    bl.write(pierwsze + "\tnie otworzyło się\tPIERWSZE\n")
                continue

            # petla dodatkowa, pliki do porownania z oryginalem
            for subdir, dirs, files in os.walk(sprawdzanie):
                dirs.sort()
                if folder_glowny in nie_powtarzaj and subdir in nie_powtarzaj:
                    continue
                else:
                    for file in sorted(files):

                        # czas od rozpoczecia tego folderu glownego
                        minelo = (
                            datetime.datetime.now() - uplynelo
                        ).total_seconds() / 60
                        countfiles += 1
                        if minelo >= 1:
                            czastrwania = (
                                datetime.datetime.now() - ten_folder_czas
                            ).total_seconds() / 60
                            print(
                                "Na tym folderze upłynęło: "
                                + "%.2f" % czastrwania
                                + "min\nAktualnie sprawdzany plik ("
                                + str(plik_z_kolei)
                                + " z "
                                + str(countpliki)
                                + " w tym folderze) porównano z "
                                + str(countfiles)
                                + " zdjęciami.\n"
                            )
                            uplynelo = datetime.datetime.now()

                        # kontynuacja petli
                        if file.endswith(
                            ".jpg" or ".jpeg" or ".JPG" or ".JPEG"
                        ):
                            porownane = file
                            drugie = os.path.join(subdir, porownane)

                            # aby mogly byc te same obrazy, w naszym przypadku
                            # beda tez te same nazwy plikow, a wiec:
                            if pierwotne == porownane:

                                # sprawdza czy plik oryginalny nie byl juz
                                # sprawdzany z drugim w# odwrotnej kolejnosci
                                # (a,b = b,a), jak byly to bierze kolejny plik
                                czy_bylo = str(drugie + "\t" + pierwsze)
                                if czy_bylo in lines_seen:
                                    continue

                                # jesli jeszcze nie byly to dodaje ta
                                # kombinacje do pamieci, zeby przy kolejnych
                                # plikach znow sprawdzic
                                else:
                                    line = str(pierwsze + "\t" + drugie)
                                    lines_seen.add(line)

                                    # jesli sciezka pierwszego pliku zgadza
                                    # sie ze sciezka drugiego
                                    # to ich nie powrownuje (ten sam plik)
                                    if pierwsze == drugie:
                                        continue

                                    # jesli jeszcze nie byly ze soba porownane,
                                    # to je porownuje
                                    else:
                                        try:
                                            image_to_compare = cv2.imread(
                                                drugie
                                            )

                                        # jak nie otworzy zdjecia to
                                        # przechodzi do kolejnego po
                                        # zapisaniu bledu do pliku tekstowego
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
                                                original.shape
                                                == image_to_compare.shape
                                            ):
                                                difference = cv2.subtract(
                                                    original, image_to_compare
                                                )
                                                b, g, r = cv2.split(difference)

                                                # jesli roznice w kanalach
                                                # wynosza 0 tzn. ze zdjecia
                                                # sa identyczne
                                                if (
                                                    cv2.countNonZero(b) == 0
                                                    and cv2.countNonZero(g)
                                                    == 0
                                                    and cv2.countNonZero(r)
                                                    == 0
                                                ):
                                                    with open(
                                                        plikwynik, "a"
                                                    ) as wynik:
                                                        wynik.write(
                                                            "IDENTYCZNE\t"
                                                            + pierwsze
                                                            + "\t"
                                                            + drugie
                                                            + "\n"
                                                        )
                                                    nie_powtarzaj.add(
                                                        folder_glowny
                                                    )
                                                    nie_powtarzaj.add(subdir)
                                                    przerwa = 1

                                                    # jesli znalazl w tym
                                                    # folderze odpowiadajaca
                                                    # pare, to konczy petle,
                                                    # bo jest duze
                                                    # prawdopodobiensto ze
                                                    # reszta tez bedzie tym
                                                    # samym wiec nie ma sensu
                                                    # sprawdzac wszystkiego
                                                    break

                                        # jak nie da sie ich otworzyc i
                                        # porownac nawet ksztaltow to
                                        # wypisze informacje do pliku
                                        except:
                                            with open(bledny, "a") as bl:
                                                bl.write(
                                                    pierwsze
                                                    + "\t"
                                                    + drugie
                                                    + "\tnie zostały \
                                                        porównane\n"
                                                )
                                            continue

        plik_z_kolei += 1
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
