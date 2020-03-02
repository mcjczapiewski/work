import os
import regex
import io
from natsort import natsorted, natsort_keygen

nkey = natsort_keygen()

count = 1

print(
    "\nUWAGA! W folderze, we wskazanej przez użytkownika lokalizacji,\n\
    może pojawić się plik bledy.txt!\n\n"
)
sciezka = input("Podaj ścieżkę do folderu: ")
write_out = r"I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614\ZADANIE 2\GNIEWKOWO\Kontrole\Kontrola nazw plikow"  # noqa

for subdir, dirs, files in os.walk(sciezka):
    dirs.sort(key=nkey)
    if not any(
        fname.upper().endswith(".PDF") for fname in os.listdir(subdir)
    ) or not os.path.basename(subdir).startswith("P"):
        continue
    print(str(count) + "\t" + subdir)
    count += 1
    kolejny = 1
    for file in natsorted(files):
        if file.upper().endswith(".PDF") and file.upper().startswith("P."):
            plik = os.path.join(subdir, file)
            try:
                bez_ope = file.split(os.path.basename(subdir))[1]
            except IndexError:
                with io.open(
                    os.path.join(write_out, "nieprawidlowy_nr_operatu.txt"),
                    "a",
                    encoding="utf-8",
                ) as bl_nazwy:
                    bl_nazwy.write(plik + "\n")
                break
            nr_tomu = myslnik = 0
            if regex.match(r"^.T.+", bez_ope):
                nr_tomu = 1
                tom = regex.match(r"^.(T.*?)(_[1-9]|-[1-9])", bez_ope)[1]
                bez_ope = regex.match(
                    r"^.T.*?((_[1-9].+$)|-[1-9].+$)", bez_ope
                )[1]
            try:
                if bez_ope.startswith("-"):
                    myslnik = 1
                    numer = int(bez_ope.split("-", 1)[1].split("-")[0])
                else:
                    numer = int(bez_ope.split("_")[1].split("-")[0])
            except IndexError:
                with io.open(
                    os.path.join(write_out, "bledy_w_nazwach_plikow.txt"),
                    "a",
                    encoding="utf-8",
                ) as bl_nazwy:
                    bl_nazwy.write(plik + "\n")
                continue
            if not numer == kolejny:
                if nr_tomu == 1:
                    if regex.match(
                        os.path.basename(subdir) + "-T[0-9].+", file
                    ):
                        operat = os.path.basename(subdir) + "-" + tom + "_"
                    elif myslnik == 1:
                        operat = os.path.basename(subdir) + "_" + tom + "-"
                    else:
                        operat = os.path.basename(subdir) + "_" + tom + "_"
                else:
                    operat = os.path.basename(subdir) + "_"
                if (
                    regex.match(os.path.basename(subdir) + "-T[0-9].+", file)
                    or myslnik == 1
                ):
                    dokument = "-" + file.split("-", 2)[2]
                else:
                    dokument = "-" + file.split("-", 1)[1]
                nazwa = os.path.join(subdir, operat + str(kolejny) + dokument)
                with io.open(
                    os.path.join(write_out, "bledny_nr_dokumentu.txt"),
                    "a",
                    encoding="utf-8",
                ) as dokumentu:
                    dokumentu.write(plik + "\t" + nazwa + "\n")

            kolejny += 1

    duble = {}
    for _, _, files in os.walk(subdir):
        for file in natsorted(files):
            if file.upper().endswith(".PDF") and file.upper().startswith("P."):
                nazwa = file.split(os.path.basename(subdir))[1]
                typ = regex.match(
                    r".+?([A-Z].*[A-Z])", str(os.path.splitext(nazwa)[0])
                )[1]
                if typ not in duble:
                    duble[typ] = 1
                elif typ in duble:
                    do_tego = duble[typ]
                    do_tego += 1
                    duze_litery = file.upper()
                    pierwotna = regex.match(r"^.+-(.+)\.PDF", duze_litery)[
                        1
                    ].zfill(3)
                    if not str(pierwotna) == str(do_tego).zfill(3):
                        bylo = file.split(pierwotna)[0]
                        rozszerzenie = os.path.splitext(file)[1]
                        bedzie = bylo + str(do_tego).zfill(3) + rozszerzenie
                        with io.open(
                            os.path.join(write_out, "bledny_numer_strony.txt"),
                            "a",
                            encoding="utf-8",
                        ) as strony:
                            strony.write(os.path.join(subdir, file) + "\n")

                    duble[typ] = do_tego

input("\nTHE END. Press something...")
