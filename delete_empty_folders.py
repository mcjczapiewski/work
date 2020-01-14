import os

sciezka = input("Podaj ścieżkę: ")
usun = []

for subdir, dirs, _ in os.walk(sciezka):
    if not os.listdir(subdir):
        usun.append(subdir)
        print(subdir)
