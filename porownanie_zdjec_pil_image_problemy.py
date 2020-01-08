# -*- coding: utf-8 -*-

import os, datetime, fnmatch
from PIL import Image
 
lines_seen = set()
nie_powtarzaj = set()
countope = 0
separ = '\t'

Image.MAX_IMAGE_PIXELS = None

    #aktualna data i godzina
czasstart = datetime.datetime.now()
print("~~~~~~START~~~~~~\t" + str(czasstart).split('.')[0])
uplynelo = datetime.datetime.now()

    #sciezki do plikow
print('\nPodaj dokładną ścieżkę folderu, w którym chcesz porównywać:')
sprawdzanie = input()
print('\nPodaj ścieżkę dla pliku wynikowego:')
sciezka = input()
wynikowy = os.path.basename(os.path.normpath(sciezka))
plikwynik = sciezka+'\\'+wynikowy+'_identyczne_'+czasstart.strftime('%Y-%m-%d')+'.txt'
plikrozne = sciezka+'\\'+wynikowy+'_rozne_'+czasstart.strftime('%Y-%m-%d')+'.txt'
print('\nPlik zostanie umieszczony w:\n' + plikwynik)
bledny = sciezka+'\\'+wynikowy+'_BLEDY_'+czasstart.strftime('%Y-%m-%d')+'.txt'
input("\nWciśnij ENTER aby kontynuować...")
print('\nTrwa liczenie folderów, poczekaj chwilkę...\n')

    #petla liczaca foldery
for _, dirnames, _ in os.walk(sprawdzanie):
  # ^ this idiom means "we won't be using this value"
	countope += len(dirnames)
	
for subdir, dirs, files in os.walk(sprawdzanie):
    dirs.sort()
    folder_glowny = subdir
    plik_z_kolei = 1
    countpliki = 0

        #rozbija sciezke do folderu i bierze tylko ostatni czlon jako numer operatu
    nrope = os.path.basename(os.path.normpath(folder_glowny))

        #ile minelo czasu od poczatku
    czastrwania = (datetime.datetime.now() - czasstart).total_seconds()/60
    print ('\nOd początku minęło: '+"%.2f" % czastrwania+'min')
    ten_folder_czas = datetime.datetime.now()

    countpliki = len(fnmatch.filter(next(os.walk(folder_glowny))[2], '*.jpg' or '*.jepg' or '*.JPG' or '*.JPEG'))
    
        #licznik petli, wskazujacy aktualnie skanowany folder z operatem
    print (countope,separ,nrope)
    countope -= 1

    for file in sorted(files):
        if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.JPG') or file.endswith('.JPEG'):
            pierwotne = file
            pierwsze = os.path.join(folder_glowny, pierwotne)
            countfiles = 0
            
            try:
                original = Image.open(os.path.join(folder_glowny, file))

                for subdir, dirs, files in os.walk(sprawdzanie):
                    dirs.sort()
                    for file in sorted(files):
                    
                        #czas od rozpoczecia tego folderu glownego
                        minelo = (datetime.datetime.now() - uplynelo).total_seconds()/60
                        countfiles += 1
                        if minelo >= 1:
                            czastrwania = (datetime.datetime.now() - ten_folder_czas).total_seconds()/60
                            print ('Na tym folderze upłynęło: '+"%.2f" % czastrwania+'min\nAktualnie sprawdzany plik ('+str(plik_z_kolei)+' z '+str(countpliki)+' w tym folderze) porównano z '+str(countfiles)+' zdjęciami.\n')
                            uplynelo = datetime.datetime.now()

                            #kontynuacja petli
                        if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.JPG') or file.endswith('.JPEG'):
                            porownane = file
                            drugie = os.path.join(subdir, porownane)

                            #sprawdza czy plik oryginalny nie byl juz sprawdzany z drugim w odwrotnej kolejnosci (a,b = b,a)
                            czy_bylo = str(drugie+'\t'+pierwsze)
                            if czy_bylo in lines_seen:
                                continue

                            #jesli jeszcze nie byly to dodaje ta kombinacje do pamieci, zeby przy kolejnych plikach znow sprawdzic
                            else:
                                line = str(pierwsze+'\t'+drugie)
                                lines_seen.add(line)

                                #jesli sciezka pierwszego pliku zgadza sie ze sciezka drugiego to ich nie powrownuje (ten sam plik)
                                if pierwsze == drugie:
                                    continue

                                #jesli pierwsze i drugie byly juz identyczne do innego pliku tzn. ze wzgledem siebie tez sa identyczne wiec nie porownuje ich ponownie
                                elif pierwsze in nie_powtarzaj and drugie in nie_powtarzaj:
                                    continue                                
                           
                                else:
                                    try:
                                        image_to_compare = Image.open(drugie)
 
                                    # 1) Check if 2 images are equals
                                        try:
                                            if original == image_to_compare:
                                                with open (plikwynik, 'a') as wynik:
                                                    wynik.write('IDENTYCZNE\t'+pierwsze+'\t'+drugie+'\n')
                                                nie_powtarzaj.add(drugie)

                                        #jesli nie to nie
                                            else:
                                                with open (plikrozne, 'a') as wynik:
                                                    wynik.write('\tróżnią się\t'+pierwsze+'\t'+drugie+'\n')

                                        except:
                                            with open (bledny, 'a') as bl:
                                               bl.write(pierwsze+'\t'+drugie+'\tnie zostały porównane\n')
                                               
                                    except:
                                        with open (bledny, 'a') as bl:
                                            bl.write(drugie+'\tnie otwiera się\n')
                                        continue

            except:
                with open (bledny, 'a') as bl:
                    bl.write(pierwsze+'\tnie otwiera się\n')
                continue
        plik_z_kolei += 1

        #czas trwania calego skryptu
czaskoniec = datetime.datetime.now()
roznicaczas = czaskoniec - czasstart
czastrwania = roznicaczas.total_seconds()/60
print ('\nCałość zajęła (minuty):')
print ("%.2f" % czastrwania)
print("\n~~~~~~KONIEC~~~~~~\t" + str(czaskoniec).split('.')[0])

input('Wciśnij ENTER aby wyjść...')
