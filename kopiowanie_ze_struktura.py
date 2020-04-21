# -*- coding: utf-8 -*-

import os
import shutil

import io
from natsort import natsort_keygen

nkey = natsort_keygen()

count = 1

# numery = [
#     "P.0418.2012.257",
#     "P.0418.1961.14",
#     "P.0418.1962.11",
#     "P.0418.1961.12",
# ]

# zrodlo = input("podaj źródło: ")
desti = input("podaj dest: ")

# for subdir, dirs, _ in os.walk(zrodlo):
#     # if 'gotowe' not in subdir:
#     #     continue
#     dirs.sort(key=nkey)
#     # if any(i == os.path.basename(subdir) for i in numery):
#     opis = os.path.join(subdir, 'opis.txt')
#     if os.path.exists(opis):
#         print(count)
#         count += 1

with io.open(
    r"\\waw-dt1407\g\20200401\kopiowanie22.txt",  # noqa
    "r",
    encoding="utf-8",
) as opisy:
    for line in opisy:
        print(count)
        count += 1
        opis = line.split("\n")[0]
        # subdir = os.path.dirname(opis)

        tutaj = os.path.join(desti, str.split(opis, "\\\\")[1])
        # if os.path.exists(tutaj):
        #     pass
        # else:
        #     os.makedirs(tutaj)
        try:
            shutil.copytree(opis, tutaj)
        except FileNotFoundError:
            print(opis)
            continue
        except:
            raise
            print(opis)
