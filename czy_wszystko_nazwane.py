import os
import io
import regex
from natsort import natsorted, natsort_keygen

nkey = natsort_keygen()

count = 1
sciezka = input("Enter the path: ")

for subdir, dirs, files in os.walk(sciezka):
    dirs.sort(key=nkey)
    if not any(
        fname.upper().endswith((".JPG", ".JPEG"))
        for fname in os.listdir(subdir)
    ):
        continue
    print(count)
    count += 1
    for file in natsorted(files):
        if file.upper().endswith((".JPG", "JPEG")):
            if not regex.match(r"^.+?_.+?_.+$", file):
                with io.open(
                    os.path.join(sciezka, "nienazwane.txt"),
                    "a",
                    encoding="utf-8",
                ) as bl:
                    bl.write(subdir + "\n")
