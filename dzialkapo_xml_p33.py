import os
import regex
import io
from natsort import natsorted, natsort_keygen

nkey = natsort_keygen()

count = 1

sciezka = input("Podaj ścieżkę: ")

for subdir, dirs, files in os.walk(sciezka):
    dirs.sort(key=nkey)
    if not any(fname.upper().endswith(".XML") for fname in os.listdir(subdir)):
        continue

    for file in natsorted(files):
        if file.upper().endswith(".XML"):
            xml = os.path.join(subdir, file)
            print(str(count) + "\t" + subdir)
            count += 1
            dzialki = set()
            with io.open(xml, "r", encoding="utf-8") as oxml:
                if any(
                    regex.match(r"^.+dzialkaPrzed.+04.+", line)
                    for line in oxml
                ) and not any(
                    regex.match(r"^.+dzialkaPo.+04.+", line) for line in oxml
                ):
                    nowyxml = os.path.join(
                        subdir, os.path.splitext(file)[0] + "_nowy.xml"
                    )
                    with io.open(xml, "r", encoding="utf-8") as oxml:
                        with io.open(nowyxml, "a", encoding="utf-8") as nxml:
                            for line in oxml:
                                if "dzialkaPrzed" in line:
                                    przed = regex.match(
                                        r"^.+(04.+)\<.+", line
                                    )[1]
                                    nxml.write(line)
                                    dzialki.add(przed)
                                elif "dzialkaPo" in line:
                                    for i in dzialki:
                                        nxml.write(
                                            "    <dzialkaPo>"
                                            + str(i)
                                            + "</dzialkaPo>\n"
                                        )
                                else:
                                    nxml.write(line)
                    with io.open(
                        r"D:\_MACIEK_\python_proby\p33\dzialka_po_xml\zmienionexml.txt",  # noqa
                        "a",
                        encoding="utf-8",
                    ) as zmienione:
                        zmienione.write(xml + "\n")

with io.open(
    r"D:\_MACIEK_\python_proby\p33\dzialka_po_xml\zmienionexml.txt",
    "r",
    encoding="utf-8",
) as usun:
    for line in usun:
        plik = line.split("\n")[0]
        print(count)
        count += 1
        os.remove(plik)
