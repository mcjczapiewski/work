import os
import regex
import io
from natsort import natsorted, natsort_keygen

nkey = natsort_keygen()

count = 1

print(
    "\nUWAGA!\nPLIK Z EWENTUALNYMI BŁĘDAMI ZOSTANIE ZAPISANY \
    W PODANEJ PONIŻEJ LOKALIZACJI!\n\n"
)
sciezka = input("Enter the path: ")

for subdir, dirs, files in os.walk(sciezka):
    dirs.sort(key=nkey)
    if not any(
        fname.upper().endswith((".PDF", ".JPG"))
        for fname in os.listdir(subdir)
    ):
        continue
    print(count)
    count += 1
    nrope = os.path.basename(subdir)

    if not os.path.exists(os.path.join(subdir, nrope + ".wkt")):
        with io.open(
            os.path.join(sciezka, "brak_wkt_glownej.txt"),
            "a",
            encoding="utf-8",
        ) as bl:
            bl.write(subdir + "\n")

    for file in natsorted(files):
        if file.upper().endswith((".PDF", ".JPG")) and regex.match(
            "^.+((M-WYN)|(M-WYW)|(SZK-POL)).+$", file
        ):
            if not os.path.exists(
                os.path.join(subdir, os.path.splitext(file)[0] + ".wkt")
            ):
                with io.open(
                    os.path.join(sciezka, "brak_wkt_pliku.txt"),
                    "a",
                    encoding="utf-8",
                ) as bl:
                    bl.write(os.path.join(subdir, file) + "\n")

    if not any(
        regex.match("^.+((M-WYN)|(M-WYW)|(SZK-POL)).+$", fname.upper())
        for fname in os.listdir(subdir)
    ):
        for file in natsorted(files):
            if file.upper().endswith((".PDF", ".JPG")) and "M-UZ" in file:
                if not os.path.exists(
                    os.path.join(subdir, os.path.splitext(file)[0] + ".wkt")
                ):
                    with io.open(
                        os.path.join(sciezka, "brak_wkt_pliku.txt"),
                        "a",
                        encoding="utf-8",
                    ) as bl:
                        bl.write(os.path.join(subdir, file) + "\n")

input("THE END. Press something...")
