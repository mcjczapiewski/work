import os
import io
import shutil
from natsort import natsort_keygen

nkey = natsort_keygen()
count = 1

path = input("PATH: ")

for subdir, dirs, files in os.walk(path):
    dirs.sort(key=nkey)
    if 'DOKUM' not in subdir:
        for file in files:
            if "dokumenta" in file:
                from_here = os.path.join(subdir, file)
                there = subdir + "_DOKUMENTACJA_PRZEJSCIOWA"
                if not os.path.exists(there):
                    os.makedirs(there)
                try:
                    shutil.move(from_here, there)
                    print(count)
                    count += 1
                except:
                    with io.open(
                        os.path.join(path, "bledy_przenoszenia.txt"),
                        "a",
                        encoding="utf-8",
                    ) as bledy:
                        bledy.write(from_here + "\n")
