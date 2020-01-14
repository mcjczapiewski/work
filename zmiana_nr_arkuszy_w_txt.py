# -*- coding: utf-8 -*-

# import bibliotek
import datetime

# zmienna-licznik przeskanowanych folderow i separator
countope = 0

# aktualna data i godzina
czasstart = datetime.datetime.now()
print("~~~~~~START~~~~~~\t" + str(czasstart).split(".")[0])

# usunac jesli stosujemy rootdir a w os.walk() wstawic 'rootdir'
input("\nWciśnij ENTER aby kontynuować...")


with open(r"D:\python_proby\arkusze.txt", "r+") as a:
    for line in a:
        nr = str.split(line, "-")
        tu = line
        with open(r"D:\python_proby\odpowiedniki.txt", "r") as o:
            for line in o:
                t = str.split(line, "\t")
                w = str.split(t[1], "\n")
                if nr[0] == t[0]:
                    nr[0] = str.replace(nr[0], nr[0], w[0])
                    with open(r"D:\python_proby\zmiana.txt", "a") as z:
                        z.write(nr[0] + "-" + nr[1])

# czas trwania calego skryptu
czaskoniec = datetime.datetime.now()
roznicaczas = czaskoniec - czasstart
czastrwania = roznicaczas.total_seconds() / 60
print("\nCałość zajęła (minuty):")
print("%.2f" % czastrwania)
print("\n~~~~~~KONIEC~~~~~~\t" + str(czaskoniec).split(".")[0])

input("Wciśnij ENTER aby wyjść...")
