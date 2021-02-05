import os

import regex
from natsort import natsorted

names_dic = {}

for subdir, dirs, files in os.walk(
    r"D:\_MACIEK_\python_proby\zasilenie_produkcyjne\go"
):
    for file in natsorted(files):
        name = regex.search(r"^(.+)-.*\.jpg", file)[1]
        if name not in names_dic:
            names_dic[name] = 2
        else:
            names_dic[name] += 1
        old = os.path.join(subdir, file)
        new = os.path.join(
            subdir,
            name + "___" + str(names_dic[name]) + os.path.splitext(file)[1],
        )
        os.rename(old, new)
