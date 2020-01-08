# -*- coding: utf-8 -*-

    #import bibliotek
import os, datetime, re, io
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
#print('\nLiczę foldery...')

    #liczy foldery
##for _, dirnames, _ in os.walk(sprnr):
##    countope += len(dirnames)

    #glowna petla
for subdir, dirs, _ in os.walk(sprnr):
    dirs.sort(key=natsort_keygen())
    
        #wyciaga nr operatu ze sciezki
    nrope = os.path.basename(subdir)

    opis = os.path.join(subdir, 'opis.txt')
    if os.path.exists(opis):
        print(str(countope)+'\t'+nrope)
        countope += 1
        try:
            with io.open(opis, 'r', encoding = 'utf-8') as f:
                linia = 0
                for line in f:
                    linia += 1
                    przecinek = slash = 0

                        #szuka linijki zaczynajacej sie od cyfry i z grupami podzialowymi
                        #linijka musi posiadac podzial na te same numery w liczniku
                    if re.match(r'^[0-9].+?\|(.*?)/.*?,\1', line):

                            #dzieli linijke na grupe przed i po
                        p = re.search(r'(^.+?)\|(.+$)', line)

                            #szuka znaku , i / w grupie pierwszej
                        for char in p.group(1):
                            if char == ',':
                                przecinek += 1
                            elif char == '/':
                                slash += 1

                            # jesli jest jakis / to sprawdza czy jest o 1 mniej , niz / bo inaczej jest jakis blad z dzialkami
                        if slash > 0:
                            if not przecinek == slash - 1:
                                with io.open(bledny, 'a', encoding = 'utf-8') as bl:
                                    bl.write('Błąd w działkach przed podziałem.\t'+str(linia)+'\t'+subdir+'\n')
                                    
                        przecinek = slash = 0

                            #sprawdza grupe druga
                        for char in p.group(2):
                            if char == ',':
                                przecinek += 1
                            elif char == '/':
                                slash += 1
                        if not przecinek == slash - 1:
                            with io.open (bledny, 'a', encoding = 'utf-8') as bl:
                                bl.write('Błąd w działkach PO podziale.\t'+str(linia)+'\t'+subdir+'\n')
        except UnicodeDecodeError:
            with open(opis, 'r') as f:
                linia = 0
                for line in f:
                    linia += 1
                    przecinek = slash = 0

                        #szuka linijki zaczynajacej sie od cyfry i z grupami podzialowymi
                        #linijka musi posiadac podzial na te same numery w liczniku
                    if re.match(r'^[0-9].+?\|(.*?)/.*?,\1', line):

                            #dzieli linijke na grupe przed i po
                        p = re.search(r'(^.+?)\|(.+$)', line)

                            #szuka znaku , i / w grupie pierwszej
                        for char in p.group(1):
                            if char == ',':
                                przecinek += 1
                            elif char == '/':
                                slash += 1

                            # jesli jest jakis / to sprawdza czy jest o 1 mniej , niz / bo inaczej jest jakis blad z dzialkami
                        if slash > 0:
                            if not przecinek == slash - 1:
                                with io.open(bledny, 'a', encoding = 'utf-8') as bl:
                                    bl.write('Błąd w działkach przed podziałem.\t'+str(linia)+'\t'+subdir+'\n')
                                    
                        przecinek = slash = 0

                            #sprawdza grupe druga
                        for char in p.group(2):
                            if char == ',':
                                przecinek += 1
                            elif char == '/':
                                slash += 1
                        if not przecinek == slash - 1:
                            with io.open (bledny, 'a', encoding = 'utf-8') as bl:
                                bl.write('Błąd w działkach PO podziale.\t'+str(linia)+'\t'+subdir+'\n')

        except:
            with io.open(r'D:\_MACIEK_\python_proby\bledy_otwarcia.txt', 'a', encoding = 'utf-8') as bl:
                bl.write(subdir+'\n')
                            
            
    #czas trwania calego skryptu
czaskoniec = datetime.datetime.now()
roznicaczas = czaskoniec - czasstart
czastrwania = roznicaczas.total_seconds()/60
print ('\nCałość zajęła (minuty):')
print ("%.2f" % czastrwania)
print("\n~~~~~~KONIEC~~~~~~\t" + str(czaskoniec).split('.')[0])

input('Wciśnij ENTER aby wyjść...')
