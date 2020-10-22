import os
import io
from natsort import natsorted, natsort_keygen

nkey = natsort_keygen()

origin = r"I:\INOWROCŁAW\DANE PODGiK\SKANY OPERATÓW\miasto i gmina Kruszwica"
przenazwanie = os.path.join(origin, "zmiana_podgik.txt")
zmienione = os.path.join(origin, "zmienione.txt")
bledy_zmian = os.path.join(origin, "nie_udalo_sie_zmienic.txt")
niezmienione = os.path.join(origin, "niezmienione.txt")

count = ncount = 1

for subdir, dirs, files in os.walk(origin):
    dirs.sort(key=nkey)
    if "NIE ODDAJEMY" in subdir:
        continue
    dok = 1
    zwieksz = []
    for file in natsorted(files):
        strona = 1
        with io.open(przenazwanie, "r", encoding="utf-8") as zmiany:
            for line in zmiany:
                jeden, dwa, bylo, bedzie = line.split("\t")
                bedzie = bedzie.split("\n")[0]
                if dwa in subdir and file == bylo:
                    if bedzie in zwieksz:
                        for i in zwieksz:
                            if i == bedzie:
                                strona = strona + 1
                    zwieksz.append(bedzie)
                    stare = os.path.join(subdir, file)
                    nowe = os.path.join(
                        subdir,
                        dwa
                        + "_"
                        + str(dok)
                        + "-"
                        + bedzie
                        + "-"
                        + str(strona).zfill(3)
                        + os.path.splitext(file)[1],
                    )

                    if os.path.exists(
                        os.path.join(
                            subdir, os.path.splitext(file)[0] + ".wkt"
                        )
                    ):
                        wkt = os.path.join(
                            subdir, os.path.splitext(file)[0] + ".wkt"
                        )
                        wkt_nowe = os.path.join(
                            subdir,
                            dwa
                            + "_"
                            + str(dok)
                            + "-"
                            + bedzie
                            + "-"
                            + str(strona).zfill(3)
                            + os.path.splitext(wkt)[1],
                        )
                        try:
                            os.rename(wkt, wkt_nowe)
                            with io.open(
                                zmienione, "a", encoding="utf-8"
                            ) as zmiany:
                                zmiany.write(wkt + "\t" + wkt_nowe + "\n")
                        except:
                            with io.open(
                                bledy_zmian, "a", encoding="utf-8"
                            ) as bl:
                                bl.write(wkt + "\n")
                    try:
                        os.rename(stare, nowe)
                        with io.open(
                            zmienione, "a", encoding="utf-8"
                        ) as zmiany:
                            zmiany.write(stare + "\t" + nowe + "\n")
                    except:
                        with io.open(bledy_zmian, "a", encoding="utf-8") as bl:
                            bl.write(stare + "\n")
                    dok += 1
                    print(count)
                    count += 1

lista = set()
with io.open(zmienione, "r", encoding="utf-8") as zmiany:
    for line in zmiany:
        lista.add(line.split("\t")[1].split("\n")[0])

for subdir, dirs, files in os.walk(origin):
    dirs.sort(key=nkey)
    if "NIE ODDAJEMY" in subdir:
        continue
    for file in natsorted(files):
        if (
            "Thumbs" in file
            or file == os.path.basename(subdir) + ".wkt"
            or file.endswith(".htm")
        ):
            continue
        if os.path.join(subdir, file) not in lista:
            with io.open(niezmienione, "a", encoding="utf-8") as bl:
                bl.write(os.path.join(subdir, file) + "\n")
            print("NIEZMIENIONE\t" + str(ncount))
            ncount += 1
