import os
import regex
from natsort import natsorted, natsort_keygen

nkey = natsort_keygen()

nazwy = (
    "decyzja",
    "dokumentacja przejściowa",
    "dziennik pomiarowy",
    "inny",
    "mapa",
    "okładka",
    "opis topograficzny",
    "protokół",
    "spis treści",
    "sprawozdanie techniczne",
    "szkic",
    "wykaz współrzędnych",
    "wykaz współrzędnych",
)
sciezka = input("Enter the path: ")

count = 1

for subdir, dirs, files in os.walk(sciezka):
    dirs.sort(key=nkey)

    if not any(fname.upper().endswith(".JPG") for fname in os.listdir(subdir)):
        if os.path.basename(subdir).startswith("P."):
            with open(
                os.path.join(sciezka, "directories_w-o_JPGs.txt"), "a"
            ) as np:
                np.write(os.path.join(subdir) + "\n")
        continue

    print(
        str(count)
        + "\t"
        + os.path.basename(os.path.dirname(subdir))
        + "\\"
        + os.path.basename(subdir)
    )
    count += 1

    for file in natsorted(files):
        if file.upper().endswith(".JPG"):
            try:
                nazwa = regex.match(r"^.+_(.+)\.jpg", file.lower())[1]
                if nazwa not in nazwy:
                    with open(
                        os.path.join(sciezka, "mixed_names.txt"), "a"
                    ) as np:
                        np.write(os.path.join(subdir, file) + "\n")
            except:
                continue
