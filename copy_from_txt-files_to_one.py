# -*- coding: utf-8 -*-

	#import bibliotek
import os, datetime

	#zmienna-licznik przeskanowanych folderow i separator
countope = 0
separ = '\t'

	#aktualna data i godzina
czasstart = datetime.datetime.now()
print("~~~~~~START~~~~~~\t" + str(czasstart).split('.')[0])

	#usunac jesli stosujemy rootdir a w os.walk() wstawic 'rootdir'
print('\nPodaj dokładną ścieżkę folderu, z którego chcesz kopiować:')
liczenie = input()
print('\nPodaj ścieżkę dla pliku wynikowego:')
sciezka = input()
wynikowy = os.path.basename(os.path.normpath(sciezka))
plikwynik = sciezka+'\\'+wynikowy+'_opisy_'+czasstart.strftime('%Y-%m-%d')+'.txt'
print('\nPlik zostanie umieszczony w:\n' + plikwynik)
bledny = sciezka+'\\'+wynikowy+'_BLEDY_'+czasstart.strftime('%Y-%m-%d')+'.txt'
input("\nWciśnij ENTER aby kontynuować...")
print('\nTrwa liczenie folderów, poczekaj chwilkę...\n')

	#petla liczaca foldery
for _, dirnames, _ in os.walk(liczenie):
  # ^ this idiom means "we won't be using this value"
	countope += len(dirnames)

	#glowna petla
for subdir, dirs, files in os.walk(liczenie):
	dirs.sort()

		#rozbija sciezke do folderu i bierze tylko ostatni czlon jako numer operatu
	nrope = os.path.basename(os.path.normpath(subdir))

		#licznik petli, wskazujacy aktualnie skanowany folder z operatem
	print (countope,separ,nrope)
	countope -= 1
	
		#poczatek petli skanujacej pliki jpg
	for file in sorted(files):
		if file == 'opis.txt':
				
				#tworzenie pelnej sciezki do skanowanego pliku na podstawie sciezki folderu i nazwy pliku
			filename = os.path.join(subdir, file)
			
			try:
			
				with open(filename) as source:
					with open(plikwynik, 'a') as target:
						for line in source:
							target.write('\n{0}'.format(line))
			
			except:
				with open (bledny, 'a') as bl:
					bl.write('Nie udało się otworzyć pliku: '+filename+'\n')

	#czas trwania calego skryptu
czaskoniec = datetime.datetime.now()
roznicaczas = czaskoniec - czasstart
czastrwania = roznicaczas.total_seconds()/60
print ('\nCałość zajęła (minuty):')
print ("%.2f" % czastrwania)
print("\n~~~~~~KONIEC~~~~~~\t" + str(czaskoniec).split('.')[0])

input('Wciśnij ENTER aby wyjść...')
