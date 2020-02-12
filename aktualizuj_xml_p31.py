import os
import io
import regex
from natsort import natsorted, natsort_keygen

nkey = natsort_keygen()

print(
    "\nUWAGA!\nW folderze wskazanym jako ścieżka do danych \
    może utworzyć się plik errors_XML.txt\n\n"
)
path = input("Ściezka do plików xml: ")
path_to_data = input(
    "Ścieżka do FOLDERU, w którym znajdują się \
    pliki dane.txt oraz rodzaje.txt: "
)
count = 1

for subdir, dirs, files in os.walk(path):
    dirs.sort(key=nkey)
    for file in natsorted(files):
        if file.upper().endswith(".XML"):
            my_lines = []
            target = 0
            xml = os.path.join(subdir, file)
            with io.open(
                os.path.join(path_to_data, "dane.txt"), "r", encoding="utf-8"
            ) as my_data:
                if not any(
                    line.split("\t")[0] == os.path.splitext(file)[0]
                    for line in my_data
                ):
                    with io.open(
                        os.path.join(path_to_data, "errors_XML.txt"),
                        "a",
                        encoding="utf-8",
                    ) as errors:
                        errors.write(
                            "BRAK ODPOWIEDNIKA W DANYCH\t"
                            + os.path.join(subdir, file)
                        )
                    break
                my_data.seek(0)
                for line in my_data:
                    if line.split("\t")[0] == os.path.splitext(file)[0]:
                        nrope, przyjecie, data, opis2, opis = line.split("\t")
                        opis = opis.split("\n")[0]

            try:
                with io.open(xml, "r", encoding="utf-8") as oxml:
                    for line in oxml:
                        if "dataPrzyjecia" in line and przyjecie != "":
                            line = (
                                "    <pzg_dataPrzyjecia>"
                                + str(przyjecie)
                                + "</pzg_dataPrzyjecia>\n"
                            )
                            my_lines.append(line)
                        elif "dataWplywu" in line and data != "":
                            line = (
                                "    <pzg_dataWplywu>"
                                + str(data)
                                + "</pzg_dataWplywu>\n"
                            )
                            my_lines.append(line)
                        elif target == 0 and regex.match(
                            "^.+<obreb>.*</obreb>.*", line
                        ):
                            try:
                                obreb = regex.match(
                                    "^.+<obreb>(.*)</obreb>.*", line
                                )[0]
                            except:
                                obreb = ""
                            my_lines.append(line)
                        elif target == 0 and "<nazwa>" in line:
                            try:
                                nazwa = regex.match(
                                    "^.+<nazwa>(.*)</nazwa>.*", line
                                )[0]
                            except:
                                nazwa = ""
                            my_lines.append(line)
                        elif target == 0 and regex.match(".*REGON.*", line):
                            try:
                                REGON = regex.match(
                                    "^.*<REGON>(.*)</REGON>.*", line
                                )[0]
                            except:
                                REGON = ""
                            my_lines.append(line)
                        elif "pzg_opis" in line and opis != "":
                            line = (
                                "    <pzg_opis>" + str(opis) + "</pzg_opis>\n"
                            )
                            my_lines.append(line)
                        elif target == 0 and "pzg_cel" in line:
                            try:
                                pzg_cel = regex.match(
                                    "^.*<pzg_cel>(.*)</pzg.*", line
                                )[0]
                            except:
                                pzg_cel = ""
                            my_lines.append(line)
                        elif target == 0 and "celArchiwalny" in line:
                            target = 1
                            try:
                                archiwalny = regex.match(
                                    "^.*<celArchiwalny>(.*)</cel.*", line
                                )[0]
                            except:
                                archiwalny = ""
                            my_lines.append(line)
                        elif "opis2" in line and opis2 != "":
                            line = "    <opis2>" + str(opis2) + "</opis2>\n"
                            my_lines.append(line)
                        elif target == 1 and "obreb" in line and obreb != "":
                            my_lines.append(obreb + "\n")
                        elif target == 1 and "nazwa" in line and nazwa != "":
                            my_lines.append(nazwa + "\n")
                        elif target == 1 and "REGON" in line and REGON != "":
                            my_lines.append(REGON + "\n")
                        elif (
                            target == 1 and "pzg_cel" in line and pzg_cel != ""
                        ):
                            my_lines.append(pzg_cel + "\n")
                            do_rodzaju = regex.match(
                                "^.*<pzg_cel>(.*)</pzg.*", pzg_cel
                            )[1]
                            with io.open(
                                os.path.join(path_to_data, "rodzaje.txt"),
                                "r",
                                encoding="utf-8",
                            ) as rodzaje:
                                if not any(
                                    line.split("\t")[0] == do_rodzaju
                                    for line in rodzaje
                                ):
                                    with io.open(
                                        os.path.join(
                                            path_to_data, "errors_XML.txt"
                                        ),
                                        "a",
                                        encoding="utf-8",
                                    ) as errors:
                                        errors.write(
                                            "BRAK RODZAJU DLA TEGO CELU\t"
                                            + os.path.join(subdir, file)
                                        )
                                    trzy = ""
                                    continue
                                rodzaje.seek(0)
                                for line in rodzaje:
                                    if do_rodzaju == line.split("\t")[0]:
                                        jeden, dwa, trzy = line.split("\t")
                                        trzy = trzy.split("\n")[0]
                        elif (
                            target == 1
                            and "celArchiwalny" in line
                            and archiwalny != ""
                        ):
                            my_lines.append(archiwalny + "\n")
                            do_rodzaju = regex.match(
                                "^.*<celArchiwalny>(.*)</cel.*", archiwalny
                            )[1]
                            with io.open(
                                os.path.join(path_to_data, "rodzaje.txt"),
                                "r",
                                encoding="utf-8",
                            ) as rodzaje:
                                if not any(
                                    line.split("\t")[1] == do_rodzaju
                                    for line in rodzaje
                                ):
                                    with io.open(
                                        os.path.join(
                                            path_to_data, "errors_XML.txt"
                                        ),
                                        "a",
                                        encoding="utf-8",
                                    ) as errors:
                                        errors.write(
                                            "BRAK RODZAJU DLA TEGO CELU\t"
                                            + os.path.join(subdir, file)
                                        )
                                    trzy = ""
                                    continue
                                rodzaje.seek(0)
                                for line in rodzaje:
                                    if do_rodzaju == line.split("\t")[1]:
                                        jeden, dwa, trzy = line.split("\t")
                                        trzy = trzy.split("\n")[0]
                        elif (
                            target == 1 and "pzg_rodzaj" in line and trzy != ""
                        ):
                            line = (
                                "    <pzg_rodzaj>"
                                + str(trzy)
                                + "</pzg_rodzaj>\n"
                            )
                            my_lines.append(line)
                        else:
                            my_lines.append(line)

                with io.open(xml, "w", encoding="utf-8") as wxml:
                    for i in my_lines:
                        wxml.write(i)

                print(count)
                count += 1

            except UnicodeDecodeError:
                with io.open(
                    os.path.join(path_to_data, "errors_XML.txt"),
                    "a",
                    encoding="utf-8",
                ) as errors:
                    errors.write(
                        "BŁĘDNE KODOWANIE XMLa\t" + os.path.join(subdir, file)
                    )
                continue

            except:
                raise

input("THE END. Press something...")
