import os
import regex
import shutil

_path = input("Enther the path to main directory with images: ")
desti = input(
    "Enter the path to destination directory to copy files \
with changed names: "
)

_copy = []
count = 1

for subdir, dirs, files in os.walk(_path):
    dirs.sort()
    if any(fname.upper().startswith("T") for fname in os.listdir(subdir)):
        print("NAMES CHANGING: " + str(count))
        count += 1
        for file in sorted(files):
            if file.upper().endswith((".JPG", "JPEG")) and file.startswith(
                "T"
            ):
                _old = file
                try:
                    _new = regex.sub(
                        r"^(T.*?\.)(.+?_)(.+$)", r"\g<2>\g<1>\g<3>", file
                    )
                    os.rename(
                        os.path.join(subdir, _old), os.path.join(subdir, _new)
                    )
                except:
                    print(subdir)
                    break

        _copy.append(subdir)

count = 1
for i in _copy:
    _here = os.path.join(desti, str.split(i, ":\\")[1])
    print("COPYING: " + str(count))
    count += 1
    try:
        shutil.copytree(i, _here)
    except:
        if not os.path.exists(_here):
            os.makedirs(_here)
        shutil.copy2(i, _here)

input("THE END. Press something...")
