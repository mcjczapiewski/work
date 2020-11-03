import os
import regex
import msvcrt
from natsort import natsort_keygen

path = input("Wklej ścieżkę: ")
possible_maps = ["'-M-PROJ-'", "'-M-WPROJ-'", "'-M-UZ-'", "'-M-WYN-'"]
sketch_coords = ["'-SZK-POL-'", "'-W-WSP-'"]
again = "t"

while again == "t":
    for subdir, dirs, _ in os.walk(path):
        dirs.sort(key=natsort_keygen())
        if "merge" in subdir:
            continue
        if any(regex.search("-.+-", fname) for fname in os.listdir(subdir)):
            operat = os.path.basename(subdir)
            for item in sketch_coords:
                if not any(
                    item.strip("'") in fname.upper()
                    for fname in os.listdir(subdir)
                ):
                    print(f"{operat} nie zawiera {item}.")
            if not any(
                possibility.strip("'") in fname
                for possibility in possible_maps
                for fname in os.listdir(subdir)
            ):
                missing_map = ", ".join(maps for maps in possible_maps)
                print(f"{operat} nie zawiera żadnej z map: {missing_map}.")
    print("Powtórzyć? t/n\n> ", end="")
    again = msvcrt.getwche().lower()
    print("\n")

input("KONIEC.")
