import os
import io
import regex
from natsort import natsort_keygen, natsorted

nkey = natsort_keygen()

path = r"I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614\ZADANIE 3\ZŁOTNIKI KUJAWSKIE"  # noqa
count = 1
characters = r"[A-Z0-9]|!| |:|\.|-|_|\\|Ą|Ę|Ó|Ś|Ł|Ż|Ź|Ć|Ń"

for subdir, dirs, files in os.walk(path):
    dirs.sort(key=nkey)
    print(count)
    count += 1
    for char in subdir:
        if not regex.match(characters, char.upper()):
            with io.open(
                fr"{path}\kontrole\kontrola dziwne nazwy\dziwne_znaki_w_folderach.txt",  # noqa
                "a",
                encoding="utf-8",
            ) as bx:
                bx.write(subdir + "\n")
    for file in natsorted(files):
        for char in file:
            if not regex.match(characters, char.upper()):
                with io.open(
                    fr"{path}\kontrole\kontrola dziwne nazwy\dziwne_znaki_w_plikach.txt",  # noqa
                    "a",
                    encoding="utf-8",
                ) as bx:
                    bx.write(os.path.join(subdir, file) + "\n")
