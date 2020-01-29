import os
import io
from natsort import natsort_keygen

nkey = natsort_keygen()

count = notdoneyet = 1
path = r"P:\cyfryzacja_powiat_wloclawski"
_file = r"P:\cyfryzacja_powiat_wloclawski\brak_opisu.txt"

with io.open(_file, "r", encoding="utf-8") as missing:
    for line in missing:
        for subdir, dirs, files in os.walk(line.split("\n")[0]):
            dirs.sort(key=nkey)
            if (
                not any(
                    fname.upper().endswith(".JPG")
                    for fname in os.listdir(subdir)
                )
                or "DOKUMENTACJA" in subdir
                or "NIE_RUSZAC" in subdir
                or "ZARYSY" in subdir
                or "BDOT500" in subdir
                or "wielkie" in subdir
            ):
                continue
            # print(count)
            # count += 1
            if not os.path.exists(os.path.join(subdir, "opis.txt")):
                print(str(notdoneyet) + "\t" + subdir)
                notdoneyet += 1
                with io.open(
                    os.path.join(path, "brak_opisu_2.txt"),
                    "a",
                    encoding="utf-8",
                ) as bl:
                    bl.write(subdir + "\n")

print("THE END.")
