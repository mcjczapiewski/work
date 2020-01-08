# -*- coding: cp1250 -*-

	#import bibliotek
from shutil import copy2
import os
import datetime

	#zmienna-licznik przeskanowanych folderow i separator
countope = 1
separ = '\t'

	#aktualna data i godzina
czasstart = datetime.datetime.now()
print("~~~~~~START~~~~~~\t" + str(czasstart).split('.')[0])

	#deklaracja sciezek
print('\nPodaj �cie�k� g��wnego folderu, z kt�rego chcesz kopiowa� ok�adki:')
kopiaokl = input()
print('\nPodaj �cie�k�, do kt�rej chcesz kopiowa�:')
sciezka = input()
print('\nPodaj �cie�k� dla pliku z ewentualnymi b��dami:')
tekstowy = input()
wynikowy = os.path.basename(os.path.normpath(tekstowy))
plikwynik = tekstowy+'\\'+wynikowy+'_bledy_kopiowania_'+czasstart.strftime('%Y-%m-%d')+'.txt'
print('\nPlik z b��dami zostanie umieszczony w:\n' + plikwynik)
input("\nWci�nij ENTER aby kontynuowa�...\n")

	#utworzenie wynikowego pliku tekstowego z pierwsza linijka zawierajaca opisy kolumn
with open (plikwynik, 'a') as wynik:
	wynik.write('UPS! Co� posz�o nie tak...\nNumer operatu g��wnego\tNumer operatu wynikowego\n')
	
	#glowna petla
for subdir, dirs, files in os.walk(kopiaokl):
	dirs.sort()

		#rozbija sciezke do folderu i bierze tylko ostatni czlon jako numer operatu
	nrope = os.path.basename(os.path.normpath(subdir))
		
		#poczatek petli skanujacej pliki jpg
	for file in sorted(files):
		if (file == '00_000_ok�adka.jpg'):
				
				#licznik petli, wskazujacy aktualnie skanowany folder z operatem
			print (countope,separ,nrope)
			countope += 1
			
				#tworzenie pelnej sciezki do skanowanego pliku na podstawie sciezki folderu i nazwy pliku
			filename = os.path.join(subdir, file)
			
				#szukanie odpowiadajacego folderu z operatem w zrzuconych z plyt
			for subdir, dirs, _ in os.walk(sciezka):
				dirs.sort()
				
					#rozbija sciezke do folderu i bierze tylko ostatni czlon jako numer operatu
				nropecopy = os.path.basename(os.path.normpath(subdir))
				
					#porownanie czy nr operatu z folderu z okladka zgadza sie z nr operatu z folderu zrzuconego z plyty
				if nrope == nropecopy:
				
						#jesli tak, kopiuje okladke
					try:
						copy2(filename, subdir)
					
					#jesli nie, wpisuje numery folderow do pliku tekstowego
					except:
						with open (plikwynik, 'a') as wynik:
							wynik.write(nrope+'\t'+nropecopy+'\n')
						
	#czas trwania calego skryptu
czaskoniec = datetime.datetime.now()
roznicaczas = czaskoniec - czasstart
czastrwania = roznicaczas.total_seconds()/60
print ('\nCa�o�� zaj�a (minuty):')
print ("%.2f" % czastrwania)
print("\n~~~~~~KONIEC~~~~~~\t" + str(czaskoniec).split('.')[0])
