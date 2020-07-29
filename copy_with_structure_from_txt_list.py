# -*- coding: utf-8 -*-

import io
import os
import shutil

count = 1

desti = input("podaj dest: ")

with io.open(
    r"P:\cyfryzacja_powiat_inowroclawski\SKANY_III\zmiany.txt",
    "r",
    encoding="utf-8",
) as paths:
    for line in paths:
        print(count)
        count += 1
        path = line.strip()

        copy_here = os.path.join(desti, str.split(path, ":\\")[1])

        try:
            shutil.copytree(path, copy_here)
        except:
            raise
            print(path)
