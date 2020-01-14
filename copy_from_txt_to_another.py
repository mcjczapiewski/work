import os

# TU WPISUJESZ NAZWE FOLDERU, TEN PLIK MUSI BYC W JEDNYM
# FOLDERZE Z LOKALIZACJĄ CO TU WPISZESZ
rootdir = "FOLDERY"

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if file == "opis.txt":
            source = "%s.txt" % subdir
            if os.path.exists(source):
                target = os.path.join(subdir, file)
                with open(source) as source_file:
                    with open(target, "a") as target_file:
                        for line in source_file:
                            if "R:" in line:
                                target_file.write("\n{0}".format(line))
