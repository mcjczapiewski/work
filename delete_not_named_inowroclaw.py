import os

count = 1

for subdir, dirs, files in os.walk(r"D:\_MACIEK_\python_proby\seba"):
    dirs.sort()
    if (
        os.path.basename(subdir) in os.listdir(subdir)
        and "merge" not in subdir
    ):
        for file in files:
            if "wpg" not in file:
                os.remove(os.path.join(subdir, file))
    print(count)
    count += 1
