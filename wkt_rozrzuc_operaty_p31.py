# -*- coding: utf-8 -*-

# import bibliotek
import os
import datetime
import shutil
import re
from natsort import natsorted
from natsort import natsort_keygen

nkey = natsort_keygen()

separ = "\t"


def sciezki():

    print("\nScieżka do folderów operatów:")
    tusapdfy = input()
    print("\nScieżka do plików WKT:")
    tusawkt = input()
    print("\nPodaj ścieżkę dla ew. pliku z błędami:")
    sciezka = input()
    bledny = (
        sciezka
        + "\\"
        + os.path.basename(os.path.normpath(sciezka))
        + "_"
        + czasstart.strftime("%Y-%m-%d")
        + ".txt"
    )
    resztawkt = (
        sciezka
        + "\\"
        + os.path.basename(os.path.normpath(sciezka))
        + "_nieskopiowane_"
        + czasstart.strftime("%Y-%m-%d")
        + ".txt"
    )
    print("\nPlik zostanie umieszczony w:\n" + bledny)
    input("\nWciśnij ENTER aby kontynuować...")
    return tusapdfy, tusawkt, bledny, resztawkt


def skladowe():
    # pobiera elementy z innej funkcji
    tusapdfy, tusawkt, bledny, resztawkt = sciezki()
    countope = 1
    listawkt = set()

    # glowna petla
    for subdir, dirs, _ in os.walk(tusapdfy):
        dirs.sort(key=nkey)

        # rozbija sciezke do folderu i bierze tylko
        # ostatni czlon jako numer operatu
        nrope = os.path.basename(subdir)
        folderpdf = subdir

        # licznik petli, wskazujacy aktualnie skanowany folder z operatem
        print(countope, separ, nrope)
        countope += 1

        # szuka odpowiadajacego pliku o tym samym nr w WKT
        for subdir, dirs, files in os.walk(tusawkt):
            dirs.sort(key=nkey)

            for file in natsorted(files):
                if file.endswith(".wkt") and re.match(
                    "^" + nrope + r"(_|-| |\.wkt)", file
                ):

                    wktpath = os.path.join(folderpdf, file)
                    plikwkt = os.path.join(subdir, file)

                    # sprawdzenie czy przypadkiem taki wkt juz
                    # nie istnieje, aby go nie nadpisać
                    if os.path.exists(wktpath):
                        with open(bledny, "a") as bl:
                            bl.write(
                                "Taki plik już istnieje:\t" + plikwkt + "\n"
                            )
                    else:
                        # jak nie istnieje to kopiuje wkt
                        # do lokalizacji z operatem
                        try:
                            shutil.copy(plikwkt, folderpdf)
                            listawkt.add(plikwkt)
                        except:
                            with open(bledny, "a") as bl:
                                bl.write(
                                    "Nie udało się skopiować pliku:\t"
                                    + plikwkt
                                    + "\n"
                                )

    # sprawdza, czy wszystkie pliki WKT znalazły swoje
    # odpowiedniki w folderach z operatami
    for subdir, dirs, files in os.walk(tusawkt):
        dirs.sort(key=nkey)
        for file in natsorted(files):
            if file.endswith(".wkt"):
                plikwkt = os.path.join(subdir, file)
                if plikwkt not in listawkt:
                    with open(resztawkt, "a") as rw:
                        rw.write(plikwkt + "\n")


def operaty():
    tusapdfy, tusawkt, bledny, resztawkt = sciezki()
    countope = 1
    listawkt = set()

    # glowna petla
    for subdir, dirs, _ in os.walk(tusapdfy):
        dirs.sort(key=nkey)

        # rozbija sciezke do folderu i bierze tylko
        # ostatni czlon jako numer operatu
        nrope = os.path.basename(subdir)
        folderpdf = subdir

        # licznik petli, wskazujacy aktualnie skanowany folder z operatem
        print(countope, separ, nrope)
        countope += 1

        # szuka odpowiadajacego folderu z operatem o tym samym nr w WKT
        for subdir, dirs, files in os.walk(tusawkt):
            dirs.sort(key=nkey)

            for file in natsorted(files):
                if file.endswith(".wkt") and re.match(
                    "^" + nrope + r"(_|-| |\.wkt)", file
                ):
                    wktpath = os.path.join(folderpdf, file)
                    plikwkt = os.path.join(subdir, file)
                    if os.path.exists(wktpath):
                        with open(bledny, "a") as bl:
                            bl.write(
                                "Taki plik już istnieje:\t" + plikwkt + "\n"
                            )
                    else:
                        try:
                            shutil.copy(plikwkt, folderpdf)
                            listawkt.add(plikwkt)
                        except:
                            with open(bledny, "a") as bl:
                                bl.write(
                                    "Nie udało się skopiować pliku:\t"
                                    + plikwkt
                                    + "\n"
                                )

        # jeśli nie znajdzie w folderze z operatem żadnego wkt,
        # tzn. że wkt dla danego operatu nie istnieje
        if not any(fname.endswith(".wkt") for fname in os.listdir(folderpdf)):
            with open(bledny, "a") as bl:
                bl.write("WKT dla operatu nie istnieje:\t" + folderpdf + "\n")

        # sprawdza czy istnieje plik wkt główny dla operatu
        plikwkt = os.path.join(folderpdf, nrope + ".wkt")
        if not os.path.exists(plikwkt):
            with open(bledny, "a") as bl:
                bl.write(
                    "WKT dla operatu nie istnieje więc nie skopiowano go \
                        na m-wyn, m-wyw itd.:\t"
                    + folderpdf
                    + "\n"
                )

        # jeśli tak, to kopiuje go dla map i szkiców
        else:
            for _, _, files in os.walk(folderpdf):
                for file in natsorted(files):
                    if re.match(
                        "(.*M-WYW.*)|(.*M-WYN.*)|(.*SZK-POL.*)", file
                    ) and file.endswith((".PDF", ".pdf")):
                        newwkt = os.path.join(
                            folderpdf, os.path.splitext(file)[0] + ".wkt"
                        )

                        # upewnia się, że wkt dla danej mapy/szkicu jeszcze
                        # nie istnieje, jesli nie to tworzy z głównego pliku
                        if not os.path.exists(newwkt):
                            try:
                                shutil.copy(plikwkt, newwkt)
                            except:
                                with open(bledny, "a") as bl:
                                    bl.write(
                                        "Nie udało się skopiować pliku:\t"
                                        + plikwkt
                                        + "\n"
                                    )

            # jeżeli nie ma w danym folderze wkt dla mapy wywiadu, wynikowej
            # bądź żadnego szkicu (bo nie ma dla nich pdf)
            # to tworzy wkt dla mapy uzupełniającej (jeśli istnieje)
            if not any(
                re.match(
                    "(.*M-WYW.*wkt)|(.*M-WYN.*wkt)|(.*SZK-POL.*wkt)", fname
                )
                for fname in os.listdir(folderpdf)
            ):
                for _, _, files in os.walk(folderpdf):
                    for file in natsorted(files):
                        if re.match(".*M-UZ.*", file) and file.endswith(
                            (".PDF", ".pdf")
                        ):
                            newwkt = os.path.join(
                                folderpdf, os.path.splitext(file)[0] + ".wkt"
                            )
                            if not os.path.exists(newwkt):
                                try:
                                    shutil.copy(plikwkt, newwkt)
                                except:
                                    with open(bledny, "a") as bl:
                                        bl.write(
                                            "Nie udało się skopiować pliku:\t"
                                            + plikwkt
                                            + "\n"
                                        )

    # sprawdza, które pliki wkt nie znalazły odpowienika
    # w folderach z operatami
    for subdir, dirs, files in os.walk(tusawkt):
        dirs.sort(key=nkey)
        for file in natsorted(files):
            if file.endswith(".wkt"):
                plikwkt = os.path.join(subdir, file)
                if plikwkt not in listawkt:
                    with open(resztawkt, "a") as rw:
                        rw.write(plikwkt + "\n")


# aktualna data i godzina
czasstart = datetime.datetime.now()
print("~~~~~~START~~~~~~\t" + str(czasstart).split(".")[0])

co_robic = 0
while co_robic != 1:
    co_robic = input(
        """\n\nKopiowanie dokumentów składowych wciśnij 1
        Kopiowanie wkt operatów wciśnij 2:\n"""
    )
    if co_robic == "1":
        co_robic = 1
        skladowe()
    elif co_robic == "2":
        co_robic = 1
        operaty()


# czas trwania calego skryptu
czaskoniec = datetime.datetime.now()
roznicaczas = czaskoniec - czasstart
czastrwania = roznicaczas.total_seconds() / 60
print("\nCałość zajęła (minuty):")
print("%.2f" % czastrwania)
print("\n~~~~~~KONIEC~~~~~~\t" + str(czaskoniec).split(".")[0])

input("Wciśnij ENTER aby wyjść...")
