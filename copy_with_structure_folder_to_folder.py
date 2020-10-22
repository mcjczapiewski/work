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
    if "merge" in subdir:
        continue
    copy_here = os.path.join(destination, str.split(subdir, ":\\")[1])
    if not os.path.exists(copy_here):
        os.makedirs(copy_here)
    for file in natsorted(files):
        if not file.upper().endswith(".PDF"):
            continue
        file_to_copy = os.path.join(subdir, file)
        try:
            shutil.copy2(file_to_copy, copy_here)
            print(count)
            count += 1
        except:
            raise
            print(file_to_copy)
