import os

for subdir, dirs, files in os.walk(r"D:\_MACIEK_\python_proby\seba"):
    dirs.sort()
    if "merge" in os.listdir(subdir):
        if any("M-UZ" in fname for fname in os.listdir(subdir)) and (
            any("M-PROJ" in fname for fname in os.listdir(subdir))
            or any("M-WPROJ" in fname for fname in os.listdir(subdir))
        ):
            for file in files:
                print(os.path.join(subdir, file))
