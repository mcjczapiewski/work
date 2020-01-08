# -*- coding: utf-8 -*-

    #import bibliotek
import os, datetime, shutil
from natsort import natsorted
from natsort import natsort_keygen
nkey = natsort_keygen()

    #zmienna-licznik przeskanowanych folderow i separator
countope = 0
separ = '\t'

    #aktualna data i godzina
czasstart = datetime.datetime.now()
print("~~~~~~START~~~~~~\t" + str(czasstart).split('.')[0])

    #usunac jesli stosujemy rootdir a w os.walk() wstawic 'rootdir'
print('\nPodaj ścieżkę folderu, z którego chcesz rozrzucić pliki:')
tutaj = input()
print('\nPodaj ścieżkę docelowych folderów:')
nowe = input()
input("\nWciśnij ENTER aby kontynuować...")

    #glowna petla
for _, _, files in os.walk(tutaj):
    for file in files:
        stad = os.path.join(tutaj, file)
        for subdir, dirs, _ in os.walk(nowe):
            shutil.copy2(stad, subdir)
        
    
    

            
    #czas trwania calego skryptu
czaskoniec = datetime.datetime.now()
roznicaczas = czaskoniec - czasstart
czastrwania = roznicaczas.total_seconds()/60
print ('\nCałość zajęła (minuty):')
print ("%.2f" % czastrwania)
print("\n~~~~~~KONIEC~~~~~~\t" + str(czaskoniec).split('.')[0])

input('Wciśnij ENTER aby wyjść...')
