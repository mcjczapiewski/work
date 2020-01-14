# -*- coding: utf-8 -*-

# import bibliotek
import os
import datetime
import fnmatch
from natsort import natsorted

# zmienna-licznik przeskanowanych folderow i separator
countope = 0

# aktualna data i godzina
czasstart = datetime.datetime.now()
print("~~~~~~START~~~~~~\t" + str(czasstart).split(".")[0])

# usunac jesli stosujemy rootdir a w os.walk() wstawic 'rootdir'
print("\nPodaj ścieżkę do sprawdzania numeracji szkiców:")
sprnr = input()
print("\nPodaj ścieżkę dla ew. pliku z błędami:")
sciezka = input()
bledny = (
    sciezka
    + "\\"
    + os.path.basename(os.path.normpath(sciezka))
    + "_BLEDY_"
    + czasstart.strftime("%Y-%m-%d")
    + ".txt"
)
zmienione = (
    sciezka
    + "\\"
    + os.path.basename(os.path.normpath(sciezka))
    + "_zmienione_"
    + czasstart.strftime("%Y-%m-%d")
    + ".txt"
)
print("\nPlik zostanie umieszczony w:\n" + bledny)
print("\nPlik ze zmianami zostanie umieszczony w:\n" + zmienione)
input("\nWciśnij ENTER aby kontynuować...")
print("\nLiczę foldery...")

# liczy foldery
for _, dirnames, _ in os.walk(sprnr):
    countope += len(dirnames)

# glowna petla
for subdir, dirs, files in os.walk(sprnr):
    dirs.sort()

    # deklaracja zbiorow danych
    usun_a = set()
    usun_b = set()
    nrstr = sciezkapisz = 1

    # wyciaga nr operatu ze sciezki
    nrope = os.path.basename(subdir)

    # licznik
    print(str(countope) + "\t" + nrope)
    countope -= 1

    # sortowanie plikow w odpowiedniej kolejnosci
    for file in natsorted(files):
        if file.endswith(".jpg" or ".JPG" or ".jpeg" or ".JPEG"):

            # jesli okladka/spis tresci to bierz kolejny plik
            if fnmatch.fnmatch(file, "00_*"):
                continue
            elif fnmatch.fnmatch(file, "*_*_*"):
                # rozdziela nazwe pliku po _
                a = str.split(file, "_")

                # nowa nazwa pliku zawierajaca nowy numer strony
                newname = a[0] + "_" + str(nrstr).zfill(3) + "_" + a[2]

                if newname == file:
                    nrstr += 1
                    continue

                else:

                    # podjecie proby zmiany nazwy
                    try:
                        os.rename(
                            os.path.join(subdir, file),
                            os.path.join(subdir, newname),
                        )
                        with open(zmienione, "a") as zm:
                            if sciezkapisz == 1:
                                zm.write("\n\n\n\n" + subdir + "\n\n")
                            zm.write(file + "\t\t" + newname + "\n")
                        sciezkapisz = 0

                    # jesli podczas proby okazalo sie, ze taka nazwa juz
                    # istnieje, to tworzy kolejna nazwe dodajac do numeru
                    # strony 'a'
                    except FileExistsError:
                        subnewname = (
                            a[0] + "_" + str(nrstr).zfill(3) + "a_" + a[2]
                        )

                        # przenazwnie z nowa nazwa
                        os.rename(
                            os.path.join(subdir, file),
                            os.path.join(subdir, subnewname),
                        )
                        with open(zmienione, "a") as zm:
                            if sciezkapisz == 1:
                                zm.write("\n\n\n\n" + subdir + "\n\n")
                            zm.write(file + "\t\t" + subnewname + "\n")
                        sciezkapisz = 0

                        # dodanie sciezki do przenazwanego pliku z 'a' zeby
                        # na koniec to 'a' usunac
                        usun_a.add(os.path.join(subdir, subnewname))

                    # jesli nie przenazwal nawet po dodaniu 'a' to
                    # wpisuje blad do pliku
                    except:
                        with open(bledny, "a") as bl:
                            bl.write(
                                "Jakiś inny błąd w:\t"
                                + os.path.join(subdir, file)
                                + "\n"
                            )

                    nrstr += 1

            else:
                with open(bledny, "a") as bl:
                    bl.write(
                        "Nie zmieniono nazwy, bo nie odpowiada wzorcowi:\t"
                        + os.path.join(subdir, file)
                        + "\n"
                    )

    # jesli lista od usun_a nie jest pusta to usuwa
    # a z plikow tam wystepujacych
    if usun_a:
        with open(zmienione, "a") as zm:
            zm.write("\n\n\n\n")

        # usuniecie 'a' dla kazdego pliku z listy
        for line in natsorted(usun_a):
            wyczysc = os.path.basename(line)
            b = str.split(wyczysc, "a_")
            czysty = b[0] + "_" + b[1]
            try:
                os.rename(line, os.path.join(os.path.dirname(line), czysty))
                with open(zmienione, "a") as zm:
                    zm.write(os.path.basename(line) + "\t\t" + czysty + "\n")
            except FileExistsError:
                subnewname = b[0] + "b_" + b[1]
                os.rename(
                    line, os.path.join(os.path.dirname(line), subnewname)
                )
                with open(zmienione, "a") as zm:
                    zm.write(
                        os.path.basename(line) + "\t\t" + subnewname + "\n"
                    )
                usun_b.add(os.path.join(os.path.dirname(line), subnewname))
            except:
                with open(bledny, "a") as bl:
                    bl.write(
                        "Jakiś inny błąd w:\t" + os.path.join(subdir, file)
                    )

        with open(zmienione, "a") as zm:
            zm.write("\n\n\n\n")

    # jesli lista od usun_b nie jest pusta to ją wpisuje w plik
    if usun_b:
        with open(bledny, "a") as bl:
            bl.write('Dopisane litery "b":\t' + usun_b + "\n")

# czas trwania calego skryptu
czaskoniec = datetime.datetime.now()
roznicaczas = czaskoniec - czasstart
czastrwania = roznicaczas.total_seconds() / 60
print("\nCałość zajęła (minuty):")
print("%.2f" % czastrwania)
print("\n~~~~~~KONIEC~~~~~~\t" + str(czaskoniec).split(".")[0])

input("Wciśnij ENTER aby wyjść...")
