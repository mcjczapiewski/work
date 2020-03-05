import os
import regex
from natsort import natsort_keygen

nkey = natsort_keygen()

i = ["szkic", "proto", "okładka", "spis", "opis.txt"]
prawne = [
    "P.0418.1966.5",
    "P.0418.1967.38",
    "P.0418.1967.105",
    "P.0418.1968.30",
    "P.0418.2008.16",
    "P.0418.2009.23",
    "P.0418.2012.966",
]

for subdir, dirs, files in os.walk(r"D:\_MACIEK_\cyfryzacja_wloclawski\kontrola_etap_2.2\do_bazy"):
    dirs.sort(key=nkey)
    if os.path.basename(subdir) in prawne:
        for file in sorted(files):
            if not any(p in file for p in i):
                os.remove(os.path.join(subdir, file))
                # print(file)

# for subdir, dirs, _ in os.walk(r"H:"):
#     dirs.sort(key=nkey)
#     if "EWID" in subdir and any(
#         fname.endswith(".JPG") for fname in os.listdir(subdir)
#     ):
#         if not any(
#             regex.match("^.+_.+_.+", fname) and not any(p in fname for p in i)
#             for fname in os.listdir(subdir)
#         ):
#             print(subdir)
