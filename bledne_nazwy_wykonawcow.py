# -*- coding: utf-8 -*-

# import bibliotek
import os
import datetime

# zmienna-licznik przeskanowanych folderow i separator
czysazdjecia = countope = 0
lines_seen = set()

# aktualna data i godzina
czasstart = datetime.datetime.now()
print("~~~~~~START~~~~~~\t" + str(czasstart).split('.')[0])

# usunac jesli stosujemy rootdir a w os.walk() wstawic 'rootdir'
print('\nPodaj ścieżkę ddo sprawdzania wykonawców:')
sprwyk = input()
print('\nPodaj ścieżkę dla ew. pliku z błędami:')
sciezka = input()
bledny = sciezka+'\\'+os.path.basename(os.path.normpath(sciezka))+'_'+czasstart.strftime('%Y-%m-%d')+'.txt'
print('\nPlik zostanie umieszczony w:\n' + bledny)
input("\nWciśnij ENTER aby kontynuować...")

with open(r'V:\Dane robocze\maciej\regexy_formuly_skrypty_polecenia\spis_wykonawcow_zambrowski.txt', 'r') as spiswyk:
    for line in spiswyk:
        lines_seen.add(line.rstrip('\n'))

# for _, dirnames, _ in os.walk(sprwyk):
#     countope += len(dirnames)

for subdir, dirs, files in os.walk(sprwyk):
    print(countope)
    countope += 1
    for file in files:
        if file == 'opis.txt':
            opisek = os.path.join(subdir, file)
            with open(opisek, 'r') as opis:
                for line in opis:
                    if line.startswith('X:'):
                        if line.rstrip('\n') not in lines_seen:
                            with open(bledny, 'a') as bl:
                                bl.write(line)

# czas trwania calego skryptu
czaskoniec = datetime.datetime.now()
roznicaczas = czaskoniec - czasstart
czastrwania = roznicaczas.total_seconds()/60
print('\nCałość zajęła (minuty):')
print("%.2f" % czastrwania)
print("\n~~~~~~KONIEC~~~~~~\t" + str(czaskoniec).split('.')[0])

input('Wciśnij ENTER aby wyjść...')
