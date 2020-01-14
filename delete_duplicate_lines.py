# jesli zduplikowana linijka moze wystapic na koncu pliku, to musi miec "enter" np.  # noqa
# "jezeli\r\n
#  jezeli"	to nie to samo, ale
# "jezeli\r\n
#  jezeli\r\n" jest duplikatem; uzyc regexu do dodania \r\n

import os

sciezka = input("Podaj ścieżkę: ")

for subdir, dirs, files in os.walk(sciezka):
    for file in files:
        if file == "opis.txt":
            lines_seen = set()  # holds lines already seen
            path = os.path.join(subdir, file)
            target = "opis2.txt"
            new_file = os.path.join(subdir, target)
            with open(path, "r") as f:
                with open(new_file, "w") as outfile:
                    for line in f:
                        if line not in lines_seen:  # not a duplicate
                            outfile.write(line)
                            lines_seen.add(line)
                    outfile.close()
                    lines_seen = None
