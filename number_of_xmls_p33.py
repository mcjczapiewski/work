import os
import io
from natsort import natsort_keygen

nkey = natsort_keygen()

xmls = r"\\Waw-dt1409\h\Inowrocław"  # noqa
count = how_much = 1
previous = ""

for subdir, dirs, files in os.walk(xmls):
    dirs.sort(key=nkey)
    if how_much > 1:
        with io.open(
            r"\\waw-dt1409\h\Inowrocław\!! KONTROLE\ponad_1_xml.txt",
            "a",
            encoding="utf-8",
        ) as nowy:
            nowy.write(str(how_much) + "\t" + previous + "\n")
    if any(
        fname.upper().endswith(".PDF") for fname in os.listdir(subdir)
    ) and not any(
        fname.upper().endswith(".XML") for fname in os.listdir(subdir)
    ):
        with io.open(
            r"\\waw-dt1409\h\Inowrocław\!! KONTROLE\brak_xml.txt",
            "a",
            encoding="utf-8",
        ) as bx:
            bx.write(subdir + "\n")
    how_much = 0
    for file in files:
        if file.upper().endswith(".XML"):
            print(count)
            count += 1
            how_much += 1
    previous = subdir
