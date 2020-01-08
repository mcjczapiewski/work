# -*- coding: utf-8 -*-

    #import bibliotek
import os, datetime, regex, io
import fnmatch as fn
from natsort import natsort_keygen

    #zmienna-licznik przeskanowanych folderow i separator
countope = 1

    #aktualna data i godzina
czasstart = datetime.datetime.now()
print("~~~~~~START~~~~~~\t" + str(czasstart).split('.')[0])

    #usunac jesli stosujemy rootdir a w os.walk() wstawic 'rootdir'
print('\nPodaj ścieżkę do sprawdzania opisów:')
sprnr = input()
print('\nPodaj ścieżkę dla ew. pliku z błędami:')
sciezka = input()
bledny = sciezka+'\\'+os.path.basename(os.path.normpath(sciezka))+'_BLEDY_'+czasstart.strftime('%Y-%m-%d')+'.txt'
print('\nPlik zostanie umieszczony w:\n' + bledny)
input("\nWciśnij ENTER aby kontynuować...")
dane = r'D:\_MACIEK_\cyfryzacja_wloclawski\G_lubanie\asor_cecha.txt'


    #glowna petla
for subdir, dirs, _ in os.walk(sprnr):
    dirs.sort(key=natsort_keygen())
    if any(fname.upper().endswith('.JPG') for fname in os.listdir(subdir)) and 'DOKUMEN' not in subdir:
        nrope = os.path.basename(subdir)
        opis = os.path.join(subdir, 'opis.txt')
        if os.path.exists(opis):
            print(str(countope)+'\t'+nrope)
            countope += 1
            try:
                with open(dane, 'r') as d:
                    for line in d:
                        if line.split('\t')[0] == nrope:
                            asor = line.split('\t')[1]
                            cecha = (line.split('\t')[2]).split('\n')[0]
                            
                            if str(asor) == 'BRAK':
                                with open(opis, 'r') as o:
                                    if not any(regex.match('^A:.+', line) for line in o):
                                        with open(bledny, 'a') as bl:
                                            bl.write(opis+'\tasortyment nieuzupełniony\n')
                            elif str(asor) == 'JEST':
                                with open(opis, 'r') as o:
                                    if any(regex.match('^A:.+', line) for line in o):
                                        with open(bledny, 'a') as bl:
                                            bl.write(opis+'\tasortyment niepotrzebnie uzupełniony\n')
                            if str(cecha) == 'BRAK':
                                with open(opis, 'r') as o:
                                    if not any(regex.match('^C:.+', line) for line in o):
                                        with open(bledny, 'a') as bl:
                                            bl.write(opis+'\tcecha nieuzupełniona\n')
                            elif cecha == 'JEST':
                                with open(opis, 'r') as o:
                                    if any(regex.match('^C:.+', line) for line in o):
                                        with open(bledny, 'a') as bl:
                                            bl.write(opis+'\tcecha niepotrzenie uzupełniona\n')
            except:
                continue
##        else:
##            with open(bledny, 'a') as bl:
##                bl.write(subdir+'\tBRAK OPISU DLA OPERATU\n')


        
    #czas trwania calego skryptu
czaskoniec = datetime.datetime.now()
roznicaczas = czaskoniec - czasstart
czastrwania = roznicaczas.total_seconds()/60
print ('\nCałość zajęła (minuty):')
print ("%.2f" % czastrwania)
print("\n~~~~~~KONIEC~~~~~~\t" + str(czaskoniec).split('.')[0])

input('Wciśnij ENTER aby wyjść...')
