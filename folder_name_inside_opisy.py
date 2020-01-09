import os

# TU WPISUJESZ NAZWE FOLDERU, TEN PLIK MUSI BYC
# W JEDNYM FOLDERZE Z LOKALIZACJĄ CO TU WPISZESZ
rootdir = 'FOLDERY'

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if file == 'opis.txt':
            path = os.path.join(subdir, file)
            with open(path, 'a') as f:
                f.write("\n{0}".format(subdir))
