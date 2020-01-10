# -*- coding: utf-8 -*-

# import bibliotek
import os
import datetime
import ctypes
from pdf2image import convert_from_path
from PIL import Image
from pathlib import Path

Image.MAX_IMAGE_PIXELS = None

# zmienna-licznik folderow i separator
nrstr = 1
countope = 0
separ = '\t'

# aktualna data i godzina
czasstart = datetime.datetime.now()
print("~~~~~~START~~~~~~\t" + str(czasstart).split('.')[0])

# deklaracja sciezki
print('\nPodaj ścieżkę głównego folderu, z którego chcesz konwertować PDFy:')
rozdziel = input()
print('\nPodaj lokalizację dla plików z błędami:')
sciezka = input()
wynikowy = os.path.basename(os.path.normpath(sciezka))
bledy_druku = sciezka + '\\' + wynikowy + '_bledy_druku_' + czasstart.strftime('%Y-%m-%d') + '.txt'
nie_utworzone = sciezka + '\\' + wynikowy + '_nie_utworzone_' + czasstart.strftime('%Y-%m-%d') + '.txt'
print('\nPodaj nazwę okna skryptu:')
nazwaokna = input()
ctypes.windll.kernel32.SetConsoleTitleW(nazwaokna)
input('\nWciśnij ENTER aby kontynuować...\n')
print('\nTrwa liczenie PDFów, poczekaj chwilkę...\n')

# petla liczaca pdfy
for _, _, filenames in os.walk(rozdziel):
  # ^ this idiom means "we won't be using this value"
    for filename in filenames:
        if filename.endswith('.pdf') or filename.endswith('.PDF'):
            countope += 1

# glowna petla
for subdir, dirs, files in os.walk(rozdziel):
    dirs.sort()

    # rozbija sciezke do folderu i bierze tylko ostatni czlon jako numer operatu
    nrope = os.path.basename(os.path.normpath(subdir))

    # poczatek petli skanujacej pliki pdf
    for file in sorted(files):
        if file.endswith('.pdf') or file.endswith('.PDF'):

            # oddziela .pdf od nazwy pliku
            nazwa_pdf, rozszerzenie = os.path.splitext(file)

            # licznik petli, wskazujacy aktualny folder z PDFem
            print(countope, separ, nrope)
            countope -= 1

            # tworzenie pelnej sciezki do rodzielanego pliku na podstawie sciezki folderu i nazwy pliku
            filename = os.path.join(subdir, file)

            # konwertowanie PDF na pliki ppm
            try:
                images_from_path = convert_from_path(filename, output_folder=subdir, dpi=300)
            except:
                with open(bledy_druku, 'a') as bd:
                    bd.write('Otwarcie pliku się nie powiodło!:\t' + filename + '\n')

            # konwertowanie ppm na jpg
            for page in images_from_path:

                # zfill dodaje zera wiodace
                strona = str(nrstr).zfill(3)
                nazwa = subdir + '\\' + nazwa_pdf + '_wpg_' + strona + '.jpg'
                page.save(nazwa, 'JPEG', dpi=[300, 300])
                nrstr += 1
                # sprawdza czy na pewno plik sie utworzyl
                if Path(subdir + '\\' + nazwa_pdf + '_wpg_' + strona + '.jpg').exists():
                    continue
                else:
                    with open(bledy_druku, 'a') as bd:
                        bd.write('Strona się nie wydrukowała!:\t' + strona + '\t' + nazwa + '\n')
            nrstr = 1

            for entry in os.scandir(subdir):
                if entry.name.endswith('.ppm'):
                    os.remove(entry)

            if Path(subdir + '\\' + nazwa_pdf + '_wpg_001.jpg').exists():
                continue
            else:
                with open(nie_utworzone, 'a') as nu:
                    nu.write(filename + '\n')

# czas trwania calego skryptu
czaskoniec = datetime.datetime.now()
roznicaczas = czaskoniec - czasstart
czastrwania = roznicaczas.total_seconds() / 60
print('\nCałość zajęła (minuty):')
print("%.2f" % czastrwania)
print("\n~~~~~~KONIEC~~~~~~\t" + str(czaskoniec).split('.')[0])

input('Wciśnij ENTER aby wyjść...')
