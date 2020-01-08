# -*- coding: utf-8 -*-

# import bibliotek
import os
import datetime

# zmienna-licznik przeskanowanych folderow i separator
czysazdjecia = 0

# aktualna data i godzina
czasstart = datetime.datetime.now()
print("~~~~~~START~~~~~~\t" + str(czasstart).split('.')[0])

# usunac jesli stosujemy rootdir a w os.walk() wstawic 'rootdir'
print('\nScieżka do folderu z plikiem brak_opisow.txt:')
braki = input()
brakopisow = braki+'\\brak_opisu.txt'
print('\nPodaj ścieżkę dla ew. pliku z błędami:')
sciezka = input()
bledny = sciezka+'\\'+os.path.basename(os.path.normpath(sciezka))+'_'+czasstart.strftime('%Y-%m-%d')+'.txt'
print('\nPlik zostanie umieszczony w:\n' + bledny)
input("\nWciśnij ENTER aby kontynuować...")

with open(brakopisow, 'r') as bo:
    for line in bo:
        sprawdzfolder = line.rstrip('\n')
        for _, _, files in os.walk(sprawdzfolder):
            for file in files:
                if file.startswith('Thumb*'):
                    continue
                else:
                    czysazdjecia += 1

        with open(bledny, 'a') as bl:
            bl.write(str(czysazdjecia)+'\t'+sprawdzfolder+'\n')

        czysazdjecia = 0

# czas trwania calego skryptu
czaskoniec = datetime.datetime.now()
roznicaczas = czaskoniec - czasstart
czastrwania = roznicaczas.total_seconds()/60
print('\nCałość zajęła (minuty):')
print("%.2f" % czastrwania)
print("\n~~~~~~KONIEC~~~~~~\t" + str(czaskoniec).split('.')[0])

input('Wciśnij ENTER aby wyjść...')
