import io
import os
import regex
from natsort import natsorted, natsort_keygen

nkey = natsort_keygen()

count = 1

print(
    "\nUWAGA! W folderze, we wskazanej przez użytkownika lokalizacji, \
może pojawić się plik bledy.txt!\n\n"
)
sciezka = input("Podaj ścieżkę do folderu: ")

for subdir, dirs, files in os.walk(sciezka):
    dirs.sort(key=nkey)
    # pomija foldery bez zdjec
    if (
        not any(fname.upper().endswith(".JPG") for fname in os.listdir(subdir))
        # or "ponad" in subdir
    ):
        continue
    kolejny = kolejna = ten_sam = numerek = taki_sam = podaj_ope = 0
    okladka = stara_nazwa = 0
    # zmienna dla zfill, jak wiecej niz 1000 skanow w folderze
    dopelnij = 3
    if any(
        regex.match("^.+_[0-9][0-9][0-9][0-9]_.+", fname)
        for fname in os.listdir(subdir)
    ):
        dopelnij = 4
    # jak nie ma okladki to pierwszy plik zaczyna sie od 01_001
    for file in natsorted(files):
        if file.upper().endswith(".JPG") and "okładka" not in file:
            kolejny = kolejna = 1
        break
    # petla glowna na plikach
    for file in natsorted(files):
        if file.upper().endswith(".JPG") and regex.match("^.+_.+_.+", file):
            nr_tomu = zmien = 0
            # poczatek nazwy nowego pliku
            poczatek = "nn_"
            tom = ""
            plik = os.path.join(subdir, file)
            # jak numer tomu w nazwie to dzieli inaczej
            if regex.match("^T.+", file):
                nr_tomu = 1
                try:
                    tom = regex.match("(^T.*?[.])([0-9])", file)[1]
                except:
                    tom = regex.match("(^T.*?[_])([0-9])", file)[1]
                poczatek = "nn_" + tom
                try:
                    file = regex.match("^T.*?[.]([0-9].+$)", file)[1]
                except:
                    file = regex.match("^T.*?[_]([0-9].+$)", file)[1]
            # podzial nazwy na czesci
            dokument = int(file.split("_")[0])
            strona = int(file.split("_")[1])
            nazwa = str(file.split("_")[2])
            # jak zmienila sie nazwa dokumentu, a numer zostal ten sam, to
            # zeby zmienic nr dla kolejnego dokumentu potrzeba 'oszukac
            # program'
            if kolejny != 0:
                if nazwa != stara_nazwa:
                    ten_sam += 100000
            stara_nazwa = nazwa
            # jesli dolejny numer dokumentu nie jest tak na prawde kolejnym,
            # to nalezy zmienic nazwe
            if not dokument == kolejny:
                # a dodatkowo nie jest to ten sam numer i nazwa co poprzedni
                if not dokument == ten_sam:
                    zmien = 1
            ten_sam = dokument

            if zmien == 1:
                # jak kolejny numer strony nie jest kolejnym w ciagu
                if not strona == kolejna:
                    strona = kolejna
                # nowa nazwa dokumentu
                nowy = (
                    poczatek
                    + str(kolejny).zfill(2)
                    + "_"
                    + str(strona).zfill(dopelnij)
                    + "_"
                    + file.split("_")[2]
                )
                # drukuje sciezke do operatu, if po to, zeby nie robil tego
                # wiecej niz raz na folder
                if podaj_ope == 0:
                    print("\n\n" + subdir)
                    podaj_ope = 1
                print(tom + file + "\t" + nowy)
                # podjecie proby zmiany nazwy, inaczej do tekstowego
                try:
                    os.rename(plik, os.path.join(subdir, nowy))
                except:
                    with io.open(
                        os.path.join(sciezka, "bledy_nazywania.txt"),
                        "a",
                        encoding="utf-8",
                    ) as blad:
                        blad.write(plik + "\n")
                # zmienne dla zachowania aktualnych numerow do sprawdzenia
                # poprawnosci w kolejnej iteracji petli
                numerek = kolejny
                taki_sam = dokument
                kolejny += 1

            # jak zmiana nie jest podyktowana roznicami w nr dokumentu to
            # sprawdza czy numer powinien sie zmienic i ew zmienia
            if dokument == taki_sam and zmien != 1 and kolejny != 0:
                if not strona == kolejna:
                    strona = kolejna
                nowy = (
                    poczatek
                    + str(numerek).zfill(2)
                    + "_"
                    + str(strona).zfill(dopelnij)
                    + "_"
                    + file.split("_")[2]
                )
                if podaj_ope == 0:
                    print("\n\n" + subdir)
                    podaj_ope = 1
                print(tom + file + "\t" + nowy)
                try:
                    os.rename(plik, os.path.join(subdir, nowy))
                except:
                    with io.open(
                        os.path.join(sciezka, "bledy_nazywania.txt"),
                        "a",
                        encoding="utf-8",
                    ) as blad:
                        blad.write(plik + "\n")
                zmien = 1

            # jezli zmiany w numerze dokumentu nie powinny zajść to sprawdza
            # czy numer strony powienien sie zminic
            if not strona == kolejna and zmien != 1:
                strona = kolejna
                nowy = (
                    poczatek
                    + str(dokument).zfill(2)
                    + "_"
                    + str(strona).zfill(dopelnij)
                    + "_"
                    + file.split("_")[2]
                )
                if podaj_ope == 0:
                    print("\n\n" + subdir)
                    podaj_ope = 1
                print(tom + file + "\t" + nowy)
                try:
                    os.rename(plik, os.path.join(subdir, nowy))
                except:
                    with io.open(
                        os.path.join(sciezka, "bledy_nazywania.txt"),
                        "a",
                        encoding="utf-8",
                    ) as blad:
                        blad.write(plik + "\n")

            if dokument == kolejny and zmien != 1:
                kolejny += 1
            kolejna += 1

    # czysci nn_ z nowych nazw
    for _, _, files in os.walk(subdir):
        for file in natsorted(files):
            if file.startswith("nn_"):
                plik = os.path.join(subdir, file)
                try:
                    os.rename(plik, os.path.join(subdir, file.split("nn_")[1]))
                except:
                    with io.open(
                        os.path.join(sciezka, "bledy_usun_nn.txt"),
                        "a",
                        encoding="utf-8",
                    ) as blad:
                        blad.write(plik + "\n")

input("\nTHE END. Press something...")
