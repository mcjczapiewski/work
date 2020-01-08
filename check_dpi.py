# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# import bibliotek
from PIL import Image
import os
import datetime
import codecs
from natsort import natsort_keygen
nkey = natsort_keygen()

# root jesli chcemy wrzucac plik pythona do foleru, w ktorym jest folder
# do sprawdzenia
# rootdir = 'PARTIA 1.0'

Image.MAX_IMAGE_PIXELS = None

# zmienna-licznik przeskanowanych folderow i separator
countope = 1
separ = '\t'

# aktualna data i godzina
czasstart = datetime.datetime.now()
print("~~~~~~START~~~~~~\t" + str(czasstart).split('.')[0])

# usunac jesli stosujemy rootdir a w os.walk() wstawic 'rootdir'
print('\nPodaj dokładną ścieżkę folderu, z którego chcesz sprawdzać DPI:')
liczenie = input()
print('\nPodaj ścieżkę dla pliku wynikowego:')
sciezka = input()
wynikowy = os.path.basename(os.path.normpath(sciezka))
bledny = sciezka + '\\' + wynikowy + '_BLEDY_'\
    + czasstart.strftime('%Y-%m-%d') + '.txt'
print('\nPlik zostanie umieszczony w:\n' + bledny)
input("\nWciśnij ENTER aby kontynuować...")


# glowna petla
for subdir, dirs, files in os.walk(liczenie):
    dirs.sort(key=nkey)
    if (not any(fname.upper().endswith(('.JPG', '.JPEG')) for fname
                in os.listdir(subdir))):
        continue

    # rozbija sciezke do folderu i bierze tylko ostatni czlon
    # jako numer operatu
    nrope = os.path.basename(os.path.normpath(subdir))

    # licznik petli, wskazujacy aktualnie skanowany folder z operatem
    print(countope, separ, nrope)
    countope += 1

    # poczatek petli skanujacej pliki jpg
    for file in sorted(files):
        if file.upper().endswith(('.JPG', '.JPEG')):

            # tworzenie pelnej sciezki do skanowanego pliku na podstawie
            # sciezki folderu i nazwy pliku
            filename = os.path.join(subdir, file)

            try:

                # otwarcie zdjecia
                img = Image.open(filename)

                # czy jest informacja o DPI zdjecia
                if img.info.get('dpi'):

                    # odczytanie i spisanie wartosci pikseli i dpi
                    width, height = img.size
                    xdpi, ydpi = img.info['dpi']

                # jesli zdjecie nie ma DPI zapisz komunikat
                else:
                    with open(bledny, 'a') as bl:
                        bl.write('Zdjęcie nie ma DPI: ' + filename + '\r\n')

            except:
                with open(bledny, 'a') as bl:
                    bl.write('Nie udało się otworzyć zdjęcia: '
                             + filename + '\r\n')

            if xdpi < 300 or ydpi < 300:
                with codecs.open(bledny, 'a', 'utf-8') as bl:
                    bl.write(str(xdpi) + '\t' + str(ydpi) + '\t' + filename
                             + '\r\n')

# czas trwania calego skryptu
czaskoniec = datetime.datetime.now()
roznicaczas = czaskoniec - czasstart
czastrwania = roznicaczas.total_seconds()/60
print('\nCałość zajęła (minuty):')
print("%.2f" % czastrwania)
print("\n~~~~~~KONIEC~~~~~~\t" + str(czaskoniec).split('.')[0])

input('Wciśnij ENTER aby zamknąć.')
