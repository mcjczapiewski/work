import os

rootdir = 'FOLDERY'  # TU WPISUJESZ NAZWE FOLDERU, TEN PLIK MUSI BYC W JEDNYM FOLDERZE Z LOKALIZACJ¥ CO TU WPISZESZ

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if file == 'opis.txt':
            path = os.path.join(subdir, file)
            with open(path, 'a') as f:
                f.write("\n{0}".format(subdir))