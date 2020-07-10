import os
import datetime

today = datetime.datetime.now().date()

path = (
    r"P:\cyfryzacja_powiat_inowroclawski\SKANY\040701_1\prawne\040701_1.0001"
)
# path = input("Wklej ścieżkę do folderu głównego: ")
count_all = count_today = 0

for subdir, dirs, files in os.walk(path):
    if os.path.basename(subdir) in os.listdir(subdir):
        folder_creation_time = datetime.date.fromtimestamp(
            os.path.getctime(os.path.join(subdir, os.path.basename(subdir)))
        )
        for file in files:
            count_all += 1
            if folder_creation_time == today:
                count_today += 1

print("ZROBIONE OGÓŁEM: " + str(count_all))
print("ZROBIONE DZISIAJ: " + str(count_today))
input("KONIEC.")
