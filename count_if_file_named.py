import os
import datetime
import msvcrt

today = datetime.datetime.now().date()

path = r"D:\WPG\inowroclawski\040701_1.0006"
# path = input("Wklej ścieżkę do folderu głównego: ")
again = "t"

while again == "t":
    count_all = count_today = 0
    current_time = datetime.datetime.now().time()
    print(f"\n{current_time.hour}:{str(current_time.minute).zfill(2)}")
    for subdir, dirs, files in os.walk(path):
        if os.path.basename(subdir) in os.listdir(subdir):
            folder_creation_time = datetime.date.fromtimestamp(
                os.path.getctime(os.path.join(subdir, os.path.basename(subdir)))
            )
            for file in files:
                count_all += 1
                if folder_creation_time == today:
                    count_today += 1

    print(f"ZROBIONE OGÓŁEM: {count_all}")
    print(f"ZROBIONE DZISIAJ: {count_today}")
    print("Powtórzyć? t/n\n> ", end="")
    again = msvcrt.getwche().lower()
    print()

input("KONIEC.")
