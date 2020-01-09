# -*- coding: utf-8 -*-

# import bibliotek
import os
import datetime
import ctypes

# zmienna-licznik przeskanowanych folderow i separator
countope = zdjecia = 0
separ = '\t'

# aktualna data i godzina
czasstart = datetime.datetime.now()
print("~~~~~~START~~~~~~\t" + str(czasstart).split('.')[0])

# usunac jesli stosujemy rootdir a w os.walk() wstawic 'rootdir'
print('\nPodaj dokładną ścieżkę folderu, z którego chcesz liczyć zdjęcia:')
liczenie = input()
print('\nPodaj ścieżkę dla pliku wynikowego:')
sciezka = input()
wynikowy = os.path.basename(os.path.normpath(sciezka))
bledny = sciezka + '\\' + wynikowy + '_PONAD_5_' + czasstart.strftime('%Y-%m-%d') + '.txt'
print('\nPlik zostanie umieszczony w:\n' + bledny)
print('\nPodaj nazwę okna skryptu:')
nazwaokna = input()
ctypes.windll.kernel32.SetConsoleTitleW(nazwaokna)
input("\nWciśnij ENTER aby kontynuować...")

# glowna petla
for subdir, dirs, files in os.walk(liczenie):
    dirs.sort()
    if not any(fname.upper().endswith(('.JPG', '.JPEG')) for fname
               in os.listdir(subdir)) or 'DOKUMENTACJA' in subdir or 'ZAŁOŻE'\
            in subdir or 'MODERNIZACJA' in subdir or 'ponad' in subdir:
        continue
    # rozbija sciezke do folderu i bierze tylko ostatni czlon jako numer operatu
    nrope = os.path.basename(os.path.normpath(subdir))

    # licznik petli, wskazujacy aktualnie skanowany folder z operatem
    countope += 1
    print(countope, separ, nrope)

    # poczatek petli skanujacej pliki jpg
    for file in sorted(files):
        if file.upper().endswith('SZKIC.JPG' or 'SZKIC.JPEG'):
            zdjecia += 1

    if zdjecia >= 6:
        with open(bledny, 'a') as bl:
            bl.write(subdir + '\n')

    zdjecia = 0

# czas trwania calego skryptu
czaskoniec = datetime.datetime.now()
roznicaczas = czaskoniec - czasstart
czastrwania = roznicaczas.total_seconds() / 60
print('\nCałość zajęła (minuty):')
print("%.2f" % czastrwania)
print("\n~~~~~~KONIEC~~~~~~\t" + str(czaskoniec).split('.')[0])

input('Wciśnij ENTER aby wyjść...')
