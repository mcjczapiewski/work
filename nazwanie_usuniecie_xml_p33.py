import os
import regex
import io
from natsort import natsorted, natsort_keygen

nkey = natsort_keygen()

sciezka = input("Podaj scieżkę do folderu z plikami xml: ")
count = 1

for subdir, dirs, files in os.walk(sciezka):
    dirs.sort(key=nkey)
    if not any(fname.upper().endswith(".XML") for fname in os.listdir(subdir)):
        continue
    for file in natsorted(files):
        if file.upper().endswith(".XML"):
            linie = []
            print(count)
            count += 1
            xml = os.path.join(subdir, file)
            with io.open(xml, "r", encoding="utf-8") as oxml:
                for line in oxml:
                    if "nazwa_xml" in line:
                        try:
                            nazwa = regex.match("^.+?>(.+)<.+", line)[1]
                        except:
                            print("BRAK NAZWY W XML\t" + xml)
                    else:
                        linie.append(line)
            with io.open(xml, "w", encoding="utf-8") as wxml:
                for i in linie:
                    wxml.write(i)
            try:
                os.rename(
                    xml,
                    os.path.join(subdir, nazwa + os.path.splitext(file)[1]),
                )
            except:
                print("NAZWA NIE ZMIENIONA\t" + xml)

input("KONIEC.")
