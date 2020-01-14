import os
import regex
from natsort import natsorted, natsort_keygen

nkey = natsort_keygen()

count = 1

print(
    "\nUWAGA! W folderze, we wskazanej przez użytkownika lokalizacji,\n\
        może pojawić się plik bledy.txt!\n\n"
)
sciezka = input("Podaj ścieżkę do folderu: ")

for subdir, dirs, files in os.walk(sciezka):
    dirs.sort(key=nkey)
    aa = set()
    bb = set()
    if not any(fname.upper().endswith(".PDF") for fname in os.listdir(subdir)):
        continue
    kolejny = 1
    for file in natsorted(files):
        if file.upper().endswith(".PDF"):
            bez_ope = file.split(os.path.basename(subdir))[1]
            nr_tomu = myslnik = 0
            if regex.match(r"^.T.+", bez_ope):
                nr_tomu = 1
                tom = regex.match(r"^.(T.*?)(_[1-9]|-[1-9])", bez_ope)[1]
                bez_ope = regex.match(
                    r"^.T.*?((_[1-9].+$)|-[1-9].+$)", bez_ope
                )[1]
            if bez_ope.startswith("-"):
                myslnik = 1
                numer = int(bez_ope.split("-", 1)[1].split("-")[0])
            else:
                numer = int(bez_ope.split("_")[1].split("-")[0])
            if not numer == kolejny:
                print(str(count) + "\t" + file)
                count += 1
                plik = os.path.join(subdir, file)
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
                try:
                    os.rename(plik, nazwa)
                except:
                    try:
                        aa_nazwa = os.path.join(
                            subdir, operat + str(kolejny) + "aaa" + dokument
                        )
                        os.rename(plik, aa_nazwa)
                        aa.add(aa_nazwa)
                    except:
                        try:
                            bb_nazwa = os.path.join(
                                subdir,
                                operat + str(kolejny) + "bbb" + dokument,
                            )
                            os.rename(plik, bb_nazwa)
                            bb.add(bb_nazwa)
                        except:
                            with open(
                                os.path.join(sciezka, "bledy.txt"), "a"
                            ) as bl:
                                bl.write(
                                    plik
                                    + "\t"
                                    + nazwa
                                    + "\tNie udało się zmienić nazwy pliku.\n"
                                )

                wkt = os.path.join(subdir, os.path.splitext(file)[0] + ".wkt")
                if os.path.exists(wkt) and any(
                    i in wkt for i in (("SZK-POL", "M-WYN", "M-WYW", "M-UZ"))
                ):
                    print(str(count) + "\t" + os.path.basename(wkt))
                    count += 1
                    try:
                        os.rename(wkt, os.path.splitext(nazwa)[0] + ".wkt")
                    except:
                        try:
                            aa_nazwa = os.path.join(
                                subdir,
                                operat
                                + str(kolejny)
                                + "aaa"
                                + os.path.splitext(dokument)[0]
                                + ".wkt",
                            )
                            os.rename(plik, aa_nazwa)
                            aa.add(aa_nazwa)
                        except:
                            try:
                                bb_nazwa = os.path.join(
                                    subdir,
                                    operat
                                    + str(kolejny)
                                    + "bbb"
                                    + os.path.splitext(dokument)[0]
                                    + ".wkt",
                                )
                                os.rename(plik, bb_nazwa)
                                bb.add(bb_nazwa)
                            except:
                                with open(
                                    os.path.join(sciezka, "bledy.txt"), "a"
                                ) as bl:
                                    bl.write(
                                        wkt
                                        + "\t"
                                        + os.path.splitext(nazwa)[0]
                                        + ".wkt"
                                        + "\tNie udało się zmienić \
                                            nazwy pliku.\n"
                                    )
            kolejny += 1
    for i in aa:
        try:
            os.rename(i, i.split("aaa")[0] + i.split("aaa")[1])
        except:
            with open(os.path.join(sciezka, "bledy.txt"), "a") as bl:
                bl.write(
                    i
                    + "\t"
                    + i.split("aaa")[0]
                    + i.split("aaa")[1]
                    + "\tNie udało się zmienić nazwy pliku.\n"
                )

    for i in bb:
        try:
            os.rename(i, i.split("bbb")[0] + i.split("bbb")[1])
        except:
            with open(os.path.join(sciezka, "bledy.txt"), "a") as bl:
                bl.write(
                    i
                    + "\t"
                    + i.split("bbb")[0]
                    + i.split("bbb")[1]
                    + "\tNie udało się zmienić nazwy pliku.\n"
                )

    aa = set()
    bb = set()
    duble = {}
    for _, _, files in os.walk(subdir):
        for file in natsorted(files):
            if file.upper().endswith(".PDF"):
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
                        print(str(count) + "\t" + file)
                        count += 1
                        bylo = file.split(pierwotna)[0]
                        rozszerzenie = os.path.splitext(file)[1]
                        bedzie = bylo + str(do_tego).zfill(3) + rozszerzenie
                        try:
                            os.rename(
                                os.path.join(subdir, file),
                                os.path.join(subdir, bedzie),
                            )
                        except:
                            try:
                                aa_nazwa = os.path.join(
                                    subdir,
                                    bylo
                                    + "aaa"
                                    + str(do_tego).zfill(3)
                                    + rozszerzenie,
                                )
                                os.rename(plik, aa_nazwa)
                                aa.add(aa_nazwa)
                            except:
                                try:
                                    bb_nazwa = os.path.join(
                                        subdir,
                                        bylo
                                        + "bbb"
                                        + str(do_tego).zfill(3)
                                        + rozszerzenie,
                                    )
                                    os.rename(plik, bb_nazwa)
                                    bb.add(bb_nazwa)
                                except:
                                    with open(
                                        os.path.join(sciezka, "bledy.txt"), "a"
                                    ) as bl:
                                        bl.write(
                                            os.path.join(subdir, file)
                                            + "\t"
                                            + os.path.join(subdir, bedzie)
                                            + "\tNie udało się zmienić \
                                                nazwy pliku.\n"
                                        )
                        wkt = os.path.join(
                            subdir, os.path.splitext(file)[0] + ".wkt"
                        )
                        if os.path.exists(wkt):
                            print(str(count) + "\t" + os.path.basename(wkt))
                            count += 1
                            rozszerzenie = ".wkt"
                            bedzie = (
                                bylo + str(do_tego).zfill(3) + rozszerzenie
                            )
                            try:
                                os.rename(wkt, os.path.join(subdir, bedzie))
                            except:
                                try:
                                    aa_nazwa = os.path.join(
                                        subdir,
                                        bylo
                                        + "aaa"
                                        + str(do_tego).zfill(3)
                                        + rozszerzenie,
                                    )
                                    os.rename(plik, aa_nazwa)
                                    aa.add(aa_nazwa)
                                except:
                                    try:
                                        bb_nazwa = os.path.join(
                                            subdir,
                                            bylo
                                            + "bbb"
                                            + str(do_tego).zfill(3)
                                            + rozszerzenie,
                                        )
                                        os.rename(plik, bb_nazwa)
                                        bb.add(bb_nazwa)
                                    except:
                                        with open(
                                            os.path.join(sciezka, "bledy.txt"),
                                            "a",
                                        ) as bl:
                                            bl.write(
                                                wkt
                                                + "\t"
                                                + os.path.join(subdir, bedzie)
                                                + "\tNie udało się zmienić \
                                                    nazwy pliku.\n"
                                            )
                    duble[typ] = do_tego

    for i in aa:
        try:
            os.rename(i, i.split("aaa")[0] + i.split("aaa")[1])
        except:
            with open(os.path.join(sciezka, "bledy.txt"), "a") as bl:
                bl.write(
                    i
                    + "\t"
                    + i.split("aaa")[0]
                    + i.split("aaa")[1]
                    + "\tNie udało się zmienić nazwy pliku.\n"
                )

    for i in bb:
        try:
            os.rename(i, i.split("bbb")[0] + i.split("bbb")[1])
        except:
            with open(os.path.join(sciezka, "bledy.txt"), "a") as bl:
                bl.write(
                    i
                    + "\t"
                    + i.split("bbb")[0]
                    + i.split("bbb")[1]
                    + "\tNie udało się zmienić nazwy pliku.\n"
                )

    aa = set()
    bb = set()
    for _, _, files in os.walk(subdir):
        for file in natsorted(files):
            if file.upper().endswith((".TXT", ".KCD", ".DXF", ".DWG")):
                bez_ope = file.split(os.path.basename(subdir))[1]
                nr_tomu = myslnik = 0
                if regex.match(r"^.T.+", bez_ope):
                    nr_tomu = 1
                    tom = regex.match(r"^.(T.*?)(_[1-9]|-[1-9])", bez_ope)[1]
                    bez_ope = regex.match(
                        r"^.T.*?((_[1-9].+$)|-[1-9].+$)", bez_ope
                    )[1]
                if bez_ope.startswith("-"):
                    myslnik = 1
                    numer = int(bez_ope.split("-", 1)[1].split("-")[0])
                else:
                    numer = int(bez_ope.split("_")[1].split("-")[0])
                if not numer == kolejny:
                    print(str(count) + "\t" + file)
                    count += 1
                    plik = os.path.join(subdir, file)
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
                        regex.match(
                            os.path.basename(subdir) + "-T[0-9].+", file
                        )
                        or myslnik == 1
                    ):
                        dokument = "-" + file.split("-", 2)[2]
                    else:
                        dokument = "-" + file.split("-", 1)[1]
                    nazwa = os.path.join(
                        subdir, operat + str(kolejny) + dokument
                    )
                    try:
                        os.rename(plik, nazwa)
                    except:
                        try:
                            aa_nazwa = os.path.join(
                                subdir,
                                operat + str(kolejny) + "aaa" + dokument,
                            )
                            os.rename(plik, aa_nazwa)
                            aa.add(aa_nazwa)
                        except:
                            try:
                                bb_nazwa = os.path.join(
                                    subdir,
                                    operat + str(kolejny) + "bbb" + dokument,
                                )
                                os.rename(plik, bb_nazwa)
                                bb.add(bb_nazwa)
                            except:
                                with open(
                                    os.path.join(sciezka, "bledy.txt"), "a"
                                ) as bl:
                                    bl.write(
                                        plik
                                        + "\t"
                                        + nazwa
                                        + "\tNie udało się zmienić \
                                            nazwy pliku.\n"
                                    )
                kolejny += 1
    for i in aa:
        try:
            os.rename(i, i.split("aaa")[0] + i.split("aaa")[1])
        except:
            with open(os.path.join(sciezka, "bledy.txt"), "a") as bl:
                bl.write(
                    i
                    + "\t"
                    + i.split("aaa")[0]
                    + i.split("aaa")[1]
                    + "\tNie udało się zmienić nazwy pliku.\n"
                )

    for i in bb:
        try:
            os.rename(i, i.split("bbb")[0] + i.split("bbb")[1])
        except:
            with open(os.path.join(sciezka, "bledy.txt"), "a") as bl:
                bl.write(
                    i
                    + "\t"
                    + i.split("bbb")[0]
                    + i.split("bbb")[1]
                    + "\tNie udało się zmienić nazwy pliku.\n"
                )

    aa = set()
    bb = set()
    ponownie = {}
    for _, _, files in os.walk(subdir):
        for file in natsorted(files):
            if file.upper().endswith((".TXT", ".KCD", ".DXF", ".DWG")):
                nazwa = file.split(os.path.basename(subdir))[1]
                nr_tomu = 0
                if regex.match(r"^.T.+", nazwa):
                    nr_tomu = 1
                    tom = regex.match(r"^.(T.*?)(_[1-9]|-[1-9])", nazwa)[1]
                    nazwa = regex.match(
                        r"^.T.*?((_[1-9].+$)|-[1-9].+$)", nazwa
                    )[1]
                if nazwa.startswith("-"):
                    typ = int(nazwa.split("-")[1])
                else:
                    typ = int(nazwa.split("_")[1].split("-")[0])
                rozszerz = os.path.splitext(nazwa)[1]
                if rozszerz not in ponownie:
                    ponownie[rozszerz] = 1
                    continue
                elif rozszerz in ponownie:
                    do_tego = ponownie[rozszerz]
                    do_tego += 1
                    duze_litery = file.upper()
                    pierwotna = regex.match(
                        r"^.+-(.+)" + rozszerz.upper(), duze_litery
                    )[1].zfill(3)
                    if not str(pierwotna) == str(do_tego).zfill(3):
                        print(str(count) + "\t" + file)
                        count += 1
                        bylo = file.split(pierwotna)[0]
                        rozszerzenie = os.path.splitext(file)[1]
                        bedzie = bylo + str(do_tego).zfill(3) + rozszerzenie
                        try:
                            os.rename(
                                os.path.join(subdir, file),
                                os.path.join(subdir, bedzie),
                            )
                        except:
                            try:
                                aa_nazwa = os.path.join(
                                    subdir,
                                    bylo
                                    + "aaa"
                                    + str(do_tego).zfill(3)
                                    + rozszerzenie,
                                )
                                os.rename(plik, aa_nazwa)
                                aa.add(aa_nazwa)
                            except:
                                try:
                                    bb_nazwa = os.path.join(
                                        subdir,
                                        bylo
                                        + "bbb"
                                        + str(do_tego).zfill(3)
                                        + rozszerzenie,
                                    )
                                    os.rename(plik, bb_nazwa)
                                    bb.add(bb_nazwa)
                                except:
                                    with open(
                                        os.path.join(sciezka, "bledy.txt"), "a"
                                    ) as bl:
                                        bl.write(
                                            os.path.join(subdir, file)
                                            + "\t"
                                            + os.path.join(subdir, bedzie)
                                            + "\tNie udało się zmienić \
                                                nazwy pliku.\n"
                                        )
                    ponownie[rozszerz] = do_tego

    for i in aa:
        try:
            os.rename(i, i.split("aaa")[0] + i.split("aaa")[1])
        except:
            with open(os.path.join(sciezka, "bledy.txt"), "a") as bl:
                bl.write(
                    i
                    + "\t"
                    + i.split("aaa")[0]
                    + i.split("aaa")[1]
                    + "\tNie udało się zmienić nazwy pliku.\n"
                )

    for i in bb:
        try:
            os.rename(i, i.split("bbb")[0] + i.split("bbb")[1])
        except:
            with open(os.path.join(sciezka, "bledy.txt"), "a") as bl:
                bl.write(
                    i
                    + "\t"
                    + i.split("bbb")[0]
                    + i.split("bbb")[1]
                    + "\tNie udało się zmienić nazwy pliku.\n"
                )

input("\nKONIEC.")
