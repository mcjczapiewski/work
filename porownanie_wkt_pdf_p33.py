# -*- coding: utf-8 -*-

    #import bibliotek
import os, datetime, fnmatch, shutil

    #zmienna-licznik przeskanowanych folderow i separator
countope = 0
separ = '\t'

    #aktualna data i godzina
czasstart = datetime.datetime.now()
print("~~~~~~START~~~~~~\t" + str(czasstart).split('.')[0])

    #usunac jesli stosujemy rootdir a w os.walk() wstawic 'rootdir'
print('\nScieżka do plików PDF:')
tusapdfy = input()
print('\nScieżka do plików WKT:')
tusawkt = input()
print('\nPodaj ścieżkę dla ew. pliku z błędami:')
sciezka = input()
bledny = sciezka+'\\'+os.path.basename(os.path.normpath(sciezka))+'_'+czasstart.strftime('%Y-%m-%d')+'.txt'
print('\nPlik zostanie umieszczony w:\n' + bledny)
input("\nWciśnij ENTER aby kontynuować...")
print('\nLiczę foldery...')

for _, dirnames, _ in os.walk(tusapdfy):
    countope += len(dirnames)

    #glowna petla
for subdir, dirs, files in os.walk(tusapdfy):
    dirs.sort()
    przerwij = 0
    
        #rozbija sciezke do folderu i bierze tylko ostatni czlon jako numer operatu
    nrope = os.path.basename(os.path.normpath(subdir))
    folderpdf = subdir
        
        #licznik petli, wskazujacy aktualnie skanowany folder z operatem
    print (countope,separ,nrope)
    countope -= 1
    
        #poczatek petli skanujacej pliki pdf
    for file in files:

            #wszystkie nazwy plikow do wielkiej litery w celu ujednolicenia - tylko w skrypcie, nie zmienia nazw plikow
        nowy = file.upper()
        if nowy.endswith('.PDF'):

                #nazwa pliku bez rozszerzenia - zeby zrobic wkt z ta sama nazwa
            nazwapdf = os.path.splitext(file)[0]

                #szuka odpowiadajacego folderu z operatem o tym samym nr w WKT
            for subdir, dirs, _ in os.walk(tusawkt):
                dirs.sort()

                nrope2 = os.path.basename(os.path.normpath(subdir))

                    #jesli znalazl odpowiedni operat to:
                if nrope2 == nrope:
                    folderwkt = subdir
                    plikwkt = nrope2+'.wkt'
                    wktpath = os.path.join(folderwkt, plikwkt)

                        #sprawdza czy .WKT dla tego operatu istnieje, jesli tak, to probuje go kopiowac
                    if os.path.exists(wktpath):

                            #nazwa i sciezka dla nowo tworzonego pliku wkt
                        nowywkt = nazwapdf+'.wkt'
                        nowywktpath = os.path.join(folderwkt, nowywkt)

                            #jesli plik w tej lokalizacji o takiej nazwie juz istnieje, to idzie do kolejnego pliku PDF
                        if os.path.exists(nowywktpath):
                            continue

                            #jesli nie, to probuje utworzyc dany plik
                        else:
                            try:
                                shutil.copy(wktpath, nowywktpath)

                                #w razie bledu, wypisze sciezke pliku, ktory sie nie utworzyl
                            except:
                                with open(bledny, 'a') as bl:
                                    bl.write('Nie udało się utworzyć pliku:\t'+nowywktpath+'\n')

                        #jesli [nr_ope].WKT nie istnieje
                    else:
                        with open(bledny, 'a') as bl:
                            bl.write('Dla danego operatu nie istnieje plik .wkt:\t'+folderpdf+'\n')
                        przerwij = 1
                        break

        if przerwij == 1:
            break
                
            
    #czas trwania calego skryptu
czaskoniec = datetime.datetime.now()
roznicaczas = czaskoniec - czasstart
czastrwania = roznicaczas.total_seconds()/60
print ('\nCałość zajęła (minuty):')
print ("%.2f" % czastrwania)
print("\n~~~~~~KONIEC~~~~~~\t" + str(czaskoniec).split('.')[0])

input('Wciśnij ENTER aby wyjść...')
