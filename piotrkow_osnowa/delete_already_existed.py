import shutil
import os
import regex

existed = []

for subdir, dirs, files in os.walk(
    r"D:\_MACIEK_\python_proby\zasilenie_produkcyjne",
    topdown=True,
    onerror=None,
    followlinks=False,
):
    if "main" in subdir:
        continue
    for file in files:
        if file.endswith(".jpg"):
            name = regex.search(r"(^.+-)(.|..)\.jpg", file.lower())[1]
            if name not in existed:
                existed.append(name)


for subdir, dirs, files in os.walk(
    r"D:\_MACIEK_\python_proby\zasilenie_produkcyjne\main",
    topdown=True,
    onerror=None,
    followlinks=False,
):
    for file in files:
        if file.endswith(".jpg"):
            name = regex.search(r"(^.+-)(.|..)\.jpg", file.lower())[1]
            if name not in existed:
                shutil.move(
                    os.path.join(subdir, file),
                    r"D:\_MACIEK_\python_proby\zasilenie_produkcyjne",
                )
