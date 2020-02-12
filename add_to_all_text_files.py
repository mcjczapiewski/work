# it has to be in directory which contains subfolders, folder
# cannot be named 'test' neither be just a number

import os

for root, dirs, files in os.walk(r"D:\GESUT_BDOT_Otwock\TESTY\FOLDERY"):
    for file in files:
        if file.endswith(".txt"):
            # print file
            path = os.path.join(root, file)
            with open(path, "a") as f:
                f.write("R:")
