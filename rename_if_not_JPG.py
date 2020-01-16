import os
from natsort import natsorted

sciezka = input("Podaj ścieżkę: ")

count = 1

for subdir, dirs, files in os.walk(sciezka):
    for file in natsorted(files):
        if file.endswith((".jpg", ".jpeg", ".JPEG")):
            print(count)
            count += 1
            os.rename(
                os.path.join(subdir, file),
                os.path.join(subdir, os.path.splitext(file)[0] + ".JPG"),
            )
