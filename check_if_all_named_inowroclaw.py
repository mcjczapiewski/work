import os
import msvcrt
from natsort import natsort_keygen

path = r"D:\WPG\inowroclawski\040701_1.0006"
# path = input("Podaj ścieżkę: ")
again = "t"

while again == "t":
    count = 1
    pdfs_to_name = 0
    for subdir, dirs, _ in os.walk(path):
        dirs.sort(key=natsort_keygen())
        steps_inside_path = len(subdir.split("\\"))
        if steps_inside_path == 5:
            up_to_merge = os.path.join(
                subdir, os.path.basename(subdir), "merge"
            )
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
                        pdfs_to_name += len(os.listdir(subdir))
                        print(f"{subdir}")
                        count += 1
            elif os.path.exists(is_there_basename):
                if not any(
                    fname.upper().endswith(".PDF")
                    for fname in os.listdir(is_there_basename)
                ):
                    pdfs_to_name += len(os.listdir(subdir))
                    print(f"{subdir}")
                    count += 1
            else:
                pdfs_to_name += len(os.listdir(subdir))
                print(f"{subdir}")
                count += 1

    print(f"\nPozostało {count} operatów, {pdfs_to_name} pdfów do nazwania.")
    print("Powtórzyć? t/n\n> ", end="")
    again = msvcrt.getwche().lower()
    print()

input("KONIEC.")
