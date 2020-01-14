import os

# TU WPISUJESZ NAZWE FOLDERU, TEN PLIK MUSI BYC W
# JEDNYM FOLDERZE Z LOKALIZACJĄ CO TU WPISZESZ
rootdir = "folder"

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if file == "opis.txt":
            path = os.path.join(subdir, file)
            newfile = "opis2.txt"
            newpath = os.path.join(subdir, newfile)
            with open(path, "r") as f1:
                file_lines = [
                    "".join([x.strip(), format(subdir), "\n"])
                    for x in f1.readlines()
                ]
            with open(newpath, "a") as f:
                f.writelines(file_lines)
