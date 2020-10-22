import os
import io
import regex
import shutil
from natsort import natsorted, natsort_keygen

nkey = natsort_keygen()

count = 1

for subdir, dirs, files in os.walk(
    r"I:\INOWROCŁAW\DANE_SKAN_SERWIS\CZĘŚĆ II"  # noqa
):
    dirs.sort(key=nkey)
    if "040703_5\\syt-wys_trasy" in subdir:
        continue
    if any(fname.upper().endswith(".XML") for fname in os.listdir(subdir)):
        nrope = os.path.basename(subdir)
        operat = subdir
        for file in natsorted(files):
            if file.upper().endswith(".XML"):
                xml = os.path.join(subdir, file)
                with io.open(xml, "r", encoding="utf-8") as oxml:
                    for line in oxml:
                        if "obreb" in line:
                            try:
                                obreb = regex.match(r".+\>(.+?)\<.+", line)[1]
                            except:
                                print(xml)
                            break
                    with io.open(
                        r"I:\INOWROCŁAW\DANE_SKAN_SERWIS\CZĘŚĆ II\maciek_2020-04-22\id_nazwa_obrebu.txt",
                        "r",
                        encoding="utf-8",
                    ) as lista:
                        for line in lista:
                            porownaj, nazwa = line.strip().split("\t")
                            if porownaj == obreb:
                                for fname in os.listdir(
                                    r"I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614\ZADANIE 3\ZŁOTNIKI KUJAWSKIE"  # noqa
                                ):
                                    if fname == nazwa:
                                        folder = os.path.join(
                                            r"I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614\ZADANIE 3\ZŁOTNIKI KUJAWSKIE",  # noqa
                                            fname,
                                        )
                                        if os.path.exists(
                                            os.path.join(folder, nrope)
                                        ):
                                            with io.open(
                                                r"I:\INOWROCŁAW\DANE_SKAN_SERWIS\CZĘŚĆ II\maciek_2020-04-22\juz_istnialy.txt",  # noqa
                                                "a",
                                                encoding="utf-8",
                                            ) as przeniesione:
                                                przeniesione.write(
                                                    operat
                                                    + "\t"
                                                    + folder
                                                    + "\n"
                                                )
                                        else:
                                            shutil.move(
                                                operat,
                                                os.path.join(folder, nrope),
                                            )
                                            # print(operat)
                                            # print(os.path.join(folder, nrope))
                                            print(
                                                str(count)
                                                # + "\t"
                                                # + os.path.join(folder, nrope)
                                            )
                                            with io.open(
                                                r"I:\INOWROCŁAW\DANE_SKAN_SERWIS\CZĘŚĆ II\maciek_2020-04-22\przeniesione.txt",  # noqa
                                                "a",
                                                encoding="utf-8",
                                            ) as przeniesione:
                                                przeniesione.write(
                                                    operat
                                                    + "\t"
                                                    + folder
                                                    + "\n"
                                                )
                                            count += 1
