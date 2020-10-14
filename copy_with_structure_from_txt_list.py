# -*- coding: utf-8 -*-

import io
import os
import shutil

count = 1

desti = input("podaj dest: ")

with io.open(
    r"D:\_MACIEK_\cyfryzacja_inowroclawski\poprawa_2020-09-23\kopiuj.txt", "r", encoding="utf-8",
) as paths:
    for line in paths:
        print(count)
        count += 1
        path = line.strip()

        copy_here = os.path.join(desti, str.split(path, ":\\")[1])
        directory = os.path.dirname(copy_here)
        if not os.path.exists(directory):
            os.makedirs(directory)

        try:
            shutil.copy2(path, copy_here)
        except Exception as e:
            with open(
                os.path.join(desti, "errors.txt"), "a", encoding="utf-8"
            ) as errors:
                errors.write(f"{path}\n{e}\n\n")
            continue
