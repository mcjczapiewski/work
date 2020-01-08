# -*- coding: cp1250 -*-

    #import bibliotek
import os, datetime, ctypes
from natsort import natsorted, natsort_keygen
nkey = natsort_keygen()

    #zmienna-licznik przeskanowanych folderow i separator
countope = zdjecia = 0
separ = '\t'

    #aktualna data i godzina
czasstart = datetime.datetime.now()
print("~~~~~~START~~~~~~\t" + str(czasstart).split('.')[0])

    #usunac jesli stosujemy rootdir a w os.walk() wstawic 'rootdir'
print('\nPodaj dokładną ścieżkę folderu, z którego chcesz liczyć zdjęcia:')
liczenie = input()
print('\nPodaj ścieżkę dla pliku wynikowego:')
sciezka = input()
wynikowy = os.path.basename(os.path.normpath(sciezka))
bledny = sciezka+'\\'+wynikowy+'_PONAD_1000_'+czasstart.strftime('%Y-%m-%d')+'.txt'
print('\nPlik zostanie umieszczony w:\n' + bledny)
print('\nPodaj nazwę okna skryptu:')
nazwaokna = input()
ctypes.windll.kernel32.SetConsoleTitleW(nazwaokna)
input("\nWciśnij ENTER aby kontynuować...")

    #glowna petla
for subdir, dirs, files in os.walk(liczenie):
    dirs.sort(key=nkey)
    if not any(fname.upper().endswith(('.JPG', '.JPEG')) for fname in os.listdir(subdir)):
        continue
        #rozbija sciezke do folderu i bierze tylko ostatni czlon jako numer operatu
    nrope = os.path.basename(os.path.normpath(subdir))
        
        #licznik petli, wskazujacy aktualnie skanowany folder z operatem
    countope += 1
    print (countope,separ,nrope)
    
        #poczatek petli skanujacej pliki jpg
    for file in natsorted(files):
        if file.upper().endswith(('.JPG', '.JPEG')):
            zdjecia += 1    
    
    if zdjecia >= 1000:
        with open(bledny, 'a') as bl:
            bl.write(subdir+'\n')
            
    zdjecia = 0
            
    #czas trwania calego skryptu
czaskoniec = datetime.datetime.now()
roznicaczas = czaskoniec - czasstart
czastrwania = roznicaczas.total_seconds()/60
print ('\nCałość zajęła (minuty):')
print ("%.2f" % czastrwania)
print("\n~~~~~~KONIEC~~~~~~\t" + str(czaskoniec).split('.')[0])

input('Wciśnij ENTER aby wyjść...')
