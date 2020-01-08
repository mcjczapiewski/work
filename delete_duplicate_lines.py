# jesli zduplikowana linijka moze wystapic na koncu pliku, to musi miec "enter" np.
# "jezeli\r\n
#  jezeli"	to nie to samo, ale
# "jezeli\r\n
#  jezeli\r\n" jest duplikatem; uzyc regexu do dodania \r\n
# PLIK MUSI BYC W LOKALIZACJI GDZIE FOLDER GLOWNY Z FOLDERAMI Z OPERATAMI
# jezeli operaty sa w \foldery\foldery_z_operatami
# to plik musi byc w \foldery i ustawić rootdir na foldery_z_operatami

import os

rootdir = 'kopia'

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if file == 'opis.txt':
            lines_seen = set() # holds lines already seen
            path = os.path.join (subdir, file)
            target = 'opis2.txt'
            new_file = os.path.join (subdir, target)
            with open(path, 'r') as f:
                with open(new_file, "w") as outfile:
                    for line in f:
                        if line not in lines_seen: # not a duplicate
                            outfile.write(line)
                            lines_seen.add(line)
                    outfile.close()
                    lines_seen = None
