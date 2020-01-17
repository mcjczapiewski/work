import os
import regex

path = input("Enter the path: ")
count = 1

for subdir, dirs, files in os.walk(path):
    for file in files:
        if file.upper().endswith((".JPG", ".JPEG")) and not regex.match(
            "^.+_.+_.+", file
        ):
            print(str(count) + "\t" + subdir)
            count += 1
            break
