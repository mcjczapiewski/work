import os
import regex
from natsort import natsort_keygen

nkey = natsort_keygen()

i = ["szkic", "proto", "okładka", "spis", "opis.txt"]
prawne = [
    "P.0418.1967.50",
    "P.0418.1967.72",
    "P.0418.1967.73",
    "P.0418.1967.52",
]

for subdir, dirs, files in os.walk(r"H:\SKANY"):
    dirs.sort(key=nkey)
    if os.path.basename(subdir) in prawne:
        for file in sorted(files):
            print(file)
        for file in sorted(files):
            if not any(p in file for p in i):
                os.remove(os.path.join(subdir, file))

for subdir, dirs, _ in os.walk(r"H:"):
    dirs.sort(key=nkey)
    if "EWID" in subdir and any(
        fname.endswith(".JPG") for fname in os.listdir(subdir)
    ):
        if not any(
            regex.match("^.+_.+_.+", fname) and not any(p in fname for p in i)
            for fname in os.listdir(subdir)
        ):
            print(subdir)
