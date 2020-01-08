# -*- coding: utf-8 -*-

import os, re, datetime, ctypes
from pathlib import Path

    #aktualna data i godzina
czasstart = datetime.datetime.now()
print("~~~~~~START~~~~~~\t" + str(czasstart).split('.')[0])

print('\nPodaj ścieżkę, w której znajduje się plik sprawdzaj.txt (format ANSI) :')
plik_lista = input()
textfile = plik_lista+'\\sprawdzaj.txt'
print('\nPodaj lokalizację dla pliku z błędami:')
sciezka = input()
wynikowy = os.path.basename(os.path.normpath(sciezka))
bledny = sciezka+'\\'+wynikowy+'_NIEISTNIEJACE_'+czasstart.strftime('%Y-%m-%d')+'.txt'
print('\nPodaj nazwę okna skryptu:')
nazwaokna = input()
ctypes.windll.kernel32.SetConsoleTitleW(nazwaokna)

alllines = 0

with open (textfile, 'r') as otxtl:
    for line in otxtl:
        alllines += 1

input('\nPlików do sprawdzenia: '+str(alllines)+'\n\nWciśnij ENTER aby kontynuować...')

with open (textfile, 'r') as otxt:
    for line in otxt:
        print(str(alllines))
        alllines -= 1
        sprawdz = line.rstrip('\n')

        if not Path(sprawdz).exists():
            with open(bledny, 'a') as bl:
                bl.write(sprawdz+'\n')

    #czas trwania calego skryptu
czaskoniec = datetime.datetime.now()
roznicaczas = czaskoniec - czasstart
czastrwania = roznicaczas.total_seconds()/60
print ('\nCałość zajęła (minuty):')
print ("%.2f" % czastrwania)
print("\n~~~~~~KONIEC~~~~~~\t" + str(czaskoniec).split('.')[0])

if Path(bledny).exists():
    print('\n!PRZEANALIZUJ PLIK Z BŁĘDAMI!')

input('Wciśnij ENTER aby wyjść...')
        
