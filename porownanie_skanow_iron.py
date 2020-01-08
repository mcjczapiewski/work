# -*- coding: utf-8 -*-

    #import bibliotek
import os, datetime, ctypes, string, fnmatch

    #zmienna-licznik przeskanowanych folderow i separator
countope = zdjecia = porow_zdj = 0
separ = '\t'

    #aktualna data i godzina
czasstart = datetime.datetime.now()
print("~~~~~~START~~~~~~\t" + str(czasstart).split('.')[0])

    #usunac jesli stosujemy rootdir a w os.walk() wstawic 'rootdir'
print('\nSciezka do zdjęć Iron:')
liczenie = input()
print('\nScieżka do naszych:')
porownanie = input()
print('\nPodaj ścieżkę dla pliku wynikowego:')
sciezka = input()
wynikowy = os.path.basename(os.path.normpath(sciezka))
bledny = sciezka+'\\'+wynikowy+'_roznice_'+czasstart.strftime('%Y-%m-%d')+'.txt'
print('\nPlik zostanie umieszczony w:\n' + bledny)
print('\nPodaj nazwę okna skryptu:')
nazwaokna = input()
ctypes.windll.kernel32.SetConsoleTitleW(nazwaokna)
input("\nWciśnij ENTER aby kontynuować...")

print('\nLiczę foldery...')

for _, dirnames, _ in os.walk(liczenie):
    for n in dirnames:
        czy_przejsc = n.upper()
        czy_przejsc1 = fnmatch.fnmatch(czy_przejsc, '*DOKUMEN*')
        if czy_przejsc1:
            continue
        countope += 1

    #glowna petla
for subdir, dirs, files in os.walk(liczenie):
    dirs.sort()

    pierw_fold = subdir.upper()
    czy_dok = fnmatch.fnmatch(pierw_fold, '*DOKUMEN*')
    if czy_dok:
        continue

        #rozbija sciezke do folderu i bierze tylko ostatni czlon jako numer operatu
    nrope = os.path.basename(os.path.normpath(subdir))
    folder_name = subdir
        
        #licznik petli, wskazujacy aktualnie skanowany folder z operatem
    print (countope,separ,nrope)
    countope -= 1
    
        #poczatek petli skanujacej pliki jpg
    for file in files:
        nowego = file.upper()
        if nowego.endswith('.JPG' or '.JPEG'):
            zdjecia += 1

    for subdir, dirs, files in os.walk(porownanie):
        dirs.sort()
        drug_fold = subdir.upper()
        czy_dok1 = fnmatch.fnmatch(drug_fold, '*DOKUMEN*')
        if czy_dok1:
            continue
        
        nrope2 = os.path.basename(os.path.normpath(subdir))
        if nrope2 == nrope:
            for file in files:
                wielkie = file.upper()
                if wielkie.endswith('.JPG' or '.JPEG'):
                    porow_zdj += 1
            if zdjecia != porow_zdj:
                with open(bledny, 'a') as bl:
                    bl.write(('ich\t'+folder_name+'\t'+str(zdjecia)+'\tnasze\t'+subdir+'\t'+str(porow_zdj)+'\n'))
                dk_przej_gl = folder_name+'_DOKUMENTACJA_PRZEJSCIOWA'
                if os.path.exists(dk_przej_gl):
                    for _, _, files in os.walk(dk_przej_gl):
                        for file in files:
                            wielkie1 = file.upper()
                            if wielkie1.endswith('.JPG' or '.JPEG'):
                                zdjecia += 1
                dk_przej_por = subdir+'_DOKUMENTACJA_PRZEJSCIOWA'
                if os.path.exists(dk_przej_por):
                    for _, _, files in os.walk(dk_przej_por):
                        for file in files:
                            wielkie2 = file.upper()
                            if wielkie2.endswith('.JPG' or '.JPEG'):
                                porow_zdj += 1
                with open(bledny, 'a') as bl1:
                    bl1.write(('ich z przejściową\t'+folder_name+'\t'+str(zdjecia)+'\tnasze z przejściową\t'+subdir+'\t'+str(porow_zdj)+'\n'))

                            
            porow_zdj = 0
        
    zdjecia = 0
            
    #czas trwania calego skryptu
czaskoniec = datetime.datetime.now()
roznicaczas = czaskoniec - czasstart
czastrwania = roznicaczas.total_seconds()/60
print ('\nCałość zajęła (minuty):')
print ("%.2f" % czastrwania)
print("\n~~~~~~KONIEC~~~~~~\t" + str(czaskoniec).split('.')[0])

input('Wciśnij ENTER aby wyjść...')
