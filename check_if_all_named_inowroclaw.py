import os
from natsort import natsort_keygen

path = r"P:\cyfryzacja_powiat_inowroclawski\SKANY\040701_1\prawne\040701_1.0001"
# path = input("Podaj ścieżkę: ")

for subdir, dirs, _ in os.walk(path):
    dirs.sort(key=natsort_keygen())
    steps_inside_path = len(subdir.split("\\"))
    if steps_inside_path == 7:
        up_to_merge = os.path.join(subdir, os.path.basename(subdir), "merge")
        is_there_basename = os.path.join(subdir, os.path.basename(subdir))
        if os.path.exists(up_to_merge):
            if not any(
                fname.upper().endswith(".PDF")
                for fname in os.listdir(up_to_merge)
            ):
                if not any(
                    fname.upper().endswith(".PDF")
                    for fname in os.listdir(is_there_basename)
                ):
                    print(subdir)
        elif os.path.exists(is_there_basename):
            print(os.listdir(is_there_basename))
            if not any(
                fname.upper().endswith(".PDF")
                for fname in os.listdir(is_there_basename)
            ):
                print(subdir)
        else:
            print(subdir)
