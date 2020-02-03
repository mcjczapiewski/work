import os
import io
import regex
from natsort import natsorted, natsort_keygen

nkey = natsort_keygen()

xmle = r"I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614\ZADANIE 2\XML_GNIEWKOWO\xmle\pliki xml całość"  # noqa
numery_p = r"D:\_MACIEK_\python_proby\p33\p_do_xml.txt"
count = 1

# with io.open(sciezki, "r", encoding="utf-8") as idz:
#     for line in idz:
#         sciezka = line.split("\n")[0]
#         print(sciezka)
#         for subdir, dirs, files in os.walk(sciezka):
#             dirs.sort(key=nkey)
#             if not any(
#                 fname.upper().endswith(".XML") for fname in os.listdir(subdir)
#             ):
#                 with io.open(
#                     os.path.join(os.path.dirname(sciezki), "bez_xml.txt"),
#                     "a",
#                     encoding="utf-8",
#                 ) as bx:
#                     bx.write(subdir + "\n")
#             for file in natsorted(files):
#                 if file.upper().endswith(".XML") and file.upper().startswith(
#                     "P."
#                 ):
#                     tresc = []
#                     print(str(count) + "\t" + subdir)
#                     count += 1
#                     zasob, powiat, rok, numer, rozszerz = file.split(".")
#                     if "_T" in numer:
#                         numer = numer.split("_")[0]
#                     xml = os.path.join(subdir, file)
#                     try:
#                         with io.open(xml, "r", encoding="utf-8") as r_xml:
#                             for line in r_xml:
#                                 if regex.match(r"^.*pierwszyCzlon><", line):
#                                     zapis = regex.sub(
#                                         r"(^.*<pierwszyCzlon>)(.+$)",
#                                         r"\g<1>" + zasob + r"\g<2>",
#                                         line,
#                                     )
#                                 elif regex.match(r"^.*drugiCzlon><", line):
#                                     zapis = regex.sub(
#                                         r"(^.*<drugiCzlon>)(.+$)",
#                                         r"\g<1>" + powiat + r"\g<2>",
#                                         line,
#                                     )
#                                 elif regex.match(r"^.*trzeciCzlon><", line):
#                                     zapis = regex.sub(
#                                         r"(^.*<trzeciCzlon>)(.+$)",
#                                         r"\g<1>" + rok + r"\g<2>",
#                                         line,
#                                     )
#                                 elif regex.match(r"^.*czwartyCzlon><", line):
#                                     zapis = regex.sub(
#                                         r"(^.*<czwartyCzlon>)(.+$)",
#                                         r"\g<1>" + numer + r"\g<2>",
#                                         line,
#                                     )
#                                 else:
#                                     zapis = line
#                                 tresc.append(zapis)
#                         with io.open(xml, "w", encoding="utf-8") as nowy:
#                             for i in tresc:
#                                 nowy.write(i)
#                     except PermissionError:
#                         with io.open(
#                             r"D:\_MACIEK_\python_proby\p33\numer_p_do_xml\bledy_otwarcia.txt",  # noqa
#                             "a",
#                             encoding="utf-8",
#                         ) as bl:
#                             bl.write(xml + "\n")
#                     except:
#                         with io.open(
#                             r"D:\_MACIEK_\python_proby\p33\numer_p_do_xml\bledy_nieznane.txt",  # noqa
#                             "a",
#                             encoding="utf-8",
#                         ) as bl:
#                             bl.write(xml + "\n")

for subdir, dirs, files in os.walk(xmle):
    dirs.sort(key=nkey)
    for file in natsorted(files):
        if file.upper().endswith(".XML"):
            tresc = []
            print(str(count) + "\t" + file)
            count += 1
            with io.open(numery_p, "r", encoding="utf-8") as numery:
                for line in numery:
                    idmz, c1, c2, c3, c4 = line.split("\t")
                    c4 = c4.split("\n")[0]
                    if os.path.splitext(file)[0] == idmz:
                        xml = os.path.join(subdir, file)
                        try:
                            with io.open(xml, "r", encoding="utf-8") as r_xml:
                                for line in r_xml:
                                    if regex.match(
                                        r"^.*pierwszyCzlon><", line
                                    ):
                                        zapis = regex.sub(
                                            r"(^.*<pierwszyCzlon>)(.+$)",
                                            r"\g<1>" + c1 + r"\g<2>",
                                            line,
                                        )
                                    elif regex.match(r"^.*drugiCzlon><", line):
                                        zapis = regex.sub(
                                            r"(^.*<drugiCzlon>)(.+$)",
                                            r"\g<1>" + c2 + r"\g<2>",
                                            line,
                                        )
                                    elif regex.match(
                                        r"^.*trzeciCzlon><", line
                                    ):
                                        zapis = regex.sub(
                                            r"(^.*<trzeciCzlon>)(.+$)",
                                            r"\g<1>" + c3 + r"\g<2>",
                                            line,
                                        )
                                    elif regex.match(
                                        r"^.*czwartyCzlon><", line
                                    ):
                                        zapis = regex.sub(
                                            r"(^.*<czwartyCzlon>)(.+$)",
                                            r"\g<1>" + c4 + r"\g<2>",
                                            line,
                                        )
                                    else:
                                        zapis = line
                                    tresc.append(zapis)
                            with io.open(xml, "w", encoding="utf-8") as nowy:
                                for i in tresc:
                                    nowy.write(i)
                        except PermissionError:
                            with io.open(
                                r"D:\_MACIEK_\python_proby\p33\bledy_otwarcia.txt",  # noqa
                                "a",
                                encoding="utf-8",
                            ) as bl:
                                bl.write(xml + "\n")
                        except:
                            with io.open(
                                r"D:\_MACIEK_\python_proby\p33\numer_p_do_xml\bledy_nieznane.txt",  # noqa
                                "a",
                                encoding="utf-8",
                            ) as bl:
                                bl.write(xml + "\n")
