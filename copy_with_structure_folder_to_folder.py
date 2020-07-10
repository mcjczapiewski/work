# -*- coding: utf-8 -*-

import os
import shutil
from natsort import natsort_keygen, natsorted

nkey = natsort_keygen()
count = 1

source = input("podaj źródło: ")
destination = input("podaj dest: ")

for subdir, dirs, files in os.walk(source):
    dirs.sort(key=nkey)
    if "merge" not in subdir:
        continue
    if subdir.split("\\")[6] not in (
        "040707_5.0010",
        "040707_5.0011",
        "040707_5.0002",
        "040707_5.0003",
        "040707_5.0004",
        "040707_5.0005",
    ):
        continue
    copy_here = os.path.join(destination, str.split(subdir, ":\\")[1])
    if not os.path.exists(copy_here):
        os.makedirs(copy_here)
    for file in natsorted(files):
        file_to_copy = os.path.join(subdir, file)
        try:
            shutil.copy2(file_to_copy, copy_here)
            print(count)
            count += 1
        except:
            raise
            print(file_to_copy)
