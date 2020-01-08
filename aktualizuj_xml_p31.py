import os, io, regex
from natsort import natsorted, natsort_keygen
nkey = natsort_keygen()

print('\nUWAGA!\nW folderze wskazanym jako ścieżka do danych może utworzyć się plik BLEDY_XML.txt\n\n')
sciezka = input('Ściezka do plików xml: ')
sciezka_dane = input('Ścieżka do FOLDERU, w którym znajdują się pliki dane.txt oraz rodzaje.txt: ')
count = 1

for subdir, dirs, files in os.walk(sciezka):
    dirs.sort(key=nkey)
    for file in natsorted(files):
        if file.upper().endswith('.XML'):
            linie = []
            cel = 0
            xml = os.path.join(subdir, file)
            with io.open(os.path.join(sciezka_dane, 'dane.txt'), 'r', encoding = 'utf-8') as dane:
                if not any(line.split('\t')[0] == os.path.splitext(file)[0] for line in dane):
                    with io.open(os.path.join(sciezka_dane, 'BLEDY_XML.txt'), 'a', encoding = 'utf-8') as bledy:
                        bledy.write('BRAK ODPOWIEDNIKA W DANYCH\t'+os.path.join(subdir, file))
                    break
                dane.seek(0)
                for line in dane:   
                    if line.split('\t')[0] == os.path.splitext(file)[0]:
                        nrope, przyjecie, data, opis2, opis = line.split('\t')
                        opis = opis.split('\n')[0]
                    
            try:
                with io.open(xml, 'r', encoding = 'utf-8') as oxml:
                    for line in oxml:
                        if 'dataPrzyjecia' in line and przyjecie != '':
                            line = '    <pzg_dataPrzyjecia>'+str(przyjecie)+'</pzg_dataPrzyjecia>\n'
                            linie.append(line)
                        elif 'dataWplywu' in line and data != '':
                            line = '    <pzg_dataWplywu>'+str(data)+'</pzg_dataWplywu>\n'
                            linie.append(line)
                        elif cel == 0 and regex.match('^.+<obreb>.*</obreb>.*', line):
                            try:
                                obreb = regex.match('^.+<obreb>(.*)</obreb>.*', line)[0]
                            except:
                                obreb = ''
                            linie.append(line)
                        elif cel == 0 and '<nazwa>' in line:
                            try:
                                nazwa = regex.match('^.+<nazwa>(.*)</nazwa>.*', line)[0]
                            except:
                                nazwa = ''
                            linie.append(line)
                        elif cel == 0 and regex.match('.*REGON.*', line):
                            try:
                                REGON = regex.match('^.*<REGON>(.*)</REGON>.*', line)[0]
                            except:
                                REGON = ''
                            linie.append(line)
                        elif 'pzg_opis' in line and opis != '':
                            line = '    <pzg_opis>'+str(opis)+'</pzg_opis>\n'
                            linie.append(line)
                        elif cel == 0 and 'pzg_cel' in line:
                            try:
                                pzg_cel = regex.match('^.*<pzg_cel>(.*)</pzg.*', line)[0]
                            except:
                                pzg_cel = ''
                            linie.append(line)
                        elif cel == 0 and 'celArchiwalny' in line:
                            cel = 1
                            try:
                                archiwalny = regex.match('^.*<celArchiwalny>(.*)</cel.*', line)[0]
                            except:
                                archiwalny = ''
                            linie.append(line)
                        elif 'opis2' in line and opis2 != '':
                            line = '    <opis2>'+str(opis2)+'</opis2>\n'
                            linie.append(line)
                        elif cel == 1 and 'obreb' in line and obreb != '':
                            linie.append(obreb+'\n')
                        elif cel == 1 and 'nazwa' in line and nazwa != '':
                            linie.append(nazwa+'\n')
                        elif cel == 1 and 'REGON' in line and REGON != '':
                            linie.append(REGON+'\n')
                        elif cel == 1 and 'pzg_cel' in line and pzg_cel != '':
                            linie.append(pzg_cel+'\n')
                            do_rodzaju = regex.match('^.*<pzg_cel>(.*)</pzg.*', pzg_cel)[1]
                            with io.open(os.path.join(sciezka_dane, 'rodzaje.txt'), 'r', encoding = 'utf-8') as rodzaje:
                                if not any(line.split('\t')[0] == do_rodzaju for line in rodzaje):
                                    with io.open(os.path.join(sciezka_dane, 'BLEDY_XML.txt'), 'a', encoding = 'utf-8') as bledy:
                                        bledy.write('BRAK RODZAJU DLA TEGO CELU\t'+os.path.join(subdir, file))
                                    trzy = ''
                                    continue
                                rodzaje.seek(0)
                                for line in rodzaje:
                                    if do_rodzaju == line.split('\t')[0]:
                                        jeden, dwa, trzy = line.split('\t')
                                        trzy = trzy.split('\n')[0]
                        elif cel == 1 and 'celArchiwalny' in line and archiwalny != '':
                            linie.append(archiwalny+'\n')
                            do_rodzaju = regex.match('^.*<celArchiwalny>(.*)</cel.*', archiwalny)[1]
                            with io.open(os.path.join(sciezka_dane, 'rodzaje.txt'), 'r', encoding = 'utf-8') as rodzaje:
                                if not any(line.split('\t')[1] == do_rodzaju for line in rodzaje):
                                    with io.open(os.path.join(sciezka_dane, 'BLEDY_XML.txt'), 'a', encoding = 'utf-8') as bledy:
                                        bledy.write('BRAK RODZAJU DLA TEGO CELU\t'+os.path.join(subdir, file))
                                    trzy = ''
                                    continue
                                rodzaje.seek(0)
                                for line in rodzaje:
                                    if do_rodzaju == line.split('\t')[1]:
                                        jeden, dwa, trzy = line.split('\t')
                                        trzy = trzy.split('\n')[0]
                        elif cel == 1 and 'pzg_rodzaj' in line and trzy != '':
                            line = '    <pzg_rodzaj>'+str(trzy)+'</pzg_rodzaj>\n'
                            linie.append(line)
                        else:
                            linie.append(line)

                with io.open(xml, 'w', encoding = 'utf-8') as wxml:
                    for i in linie:
                        wxml.write(i)

                print(count)
                count += 1
                        
            except UnicodeDecodeError:
                with io.open(os.path.join(sciezka_dane, 'BLEDY_XML.txt'), 'a', encoding = 'utf-8') as bledy:
                    bledy.write('BŁĘDNE KODOWANIE XMLa\t'+os.path.join(subdir, file))
                continue

            except:
                raise

input('KONIEC.')
