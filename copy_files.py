# -*- coding: utf-8 -*-

import os
import re
import shutil
import datetime
import ctypes
from pathlib import Path

# aktualna data i godzina
czasstart = datetime.datetime.now()
print("~~~~~~START~~~~~~\t" + str(czasstart).split('.')[0])

print('\nPodaj ścieżkę, w której znajduje się plik lista.txt (plik_zrodlowy \
TABULATOR folder_docelowy; kodowanie pliku txt w ANSI):')
plik_lista = input()
textfile = plik_lista+'\\lista.txt'
print('\nPodaj lokalizację dla pliku z błędami:')
sciezka = input()
wynikowy = os.path.basename(os.path.normpath(sciezka))
bledny = sciezka+'\\'+wynikowy+'_BLEDY_'+czasstart.strftime('%Y-%m-%d')+'.txt'
print('\nPodaj nazwę okna skryptu:')
nazwaokna = input()
ctypes.windll.kernel32.SetConsoleTitleW(nazwaokna)

alllines = 0
line_nb = 1

# liczy ilosc plikow do skopiowania na podstawie ilosci wierszy w pliku tekstowym
with open(textfile, 'r') as otxtl:
    for line in otxtl:
        alllines += 1

input('\nPlików do przeniesienia: '+str(alllines)+'\n\nWciśnij ENTER aby kontynuować...')

# glowna petla
with open(textfile, 'r') as otxt:
    for line in otxt:

        # odlicza do konca
        print(str(alllines))
        alllines -= 1

        # regex rozdzielajacy sciezke z ktorej kopiowac od sciezki DO ktorej kopiowac
        file2copy = re.findall(r'(^.+?(?=\t))\t(.+)', line)

        # pierwsza czesc wyniku to zrodlo, druga to docelowy folder
        for tuple in file2copy:
            sourcefile = (tuple[0])
            destpath = (tuple[1])

        # wykona tylko, jesli plik do skopiowania wciaz istnieje
        if Path(sourcefile).exists():
            try:
                shutil.copy2(sourcefile, destpath)
            except:
                with open(bledny, 'a') as bl:
                    bl.write('Wystąpił nieokreślony błąd w linii:\t'+str(line_nb)+'\r\n')
                    continue
        else:
            with open(bledny, 'a') as bl:
                bl.write('Plik z linii nr ~~'+str(line_nb)+'~~ już nie istnieje!\r\n')
        line_nb += 1

# czas trwania calego skryptu
czaskoniec = datetime.datetime.now()
roznicaczas = czaskoniec - czasstart
czastrwania = roznicaczas.total_seconds()/60
print('\nCałość zajęła (minuty):')
print("%.2f" % czastrwania)
print("\n~~~~~~KONIEC~~~~~~\t" + str(czaskoniec).split('.')[0])

if Path(bledny).exists():
    print('\n!PRZEANALIZUJ PLIK Z BŁĘDAMI!')

input('Wciśnij ENTER aby wyjść...')
