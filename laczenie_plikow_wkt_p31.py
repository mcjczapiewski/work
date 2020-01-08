import os, io, regex
from natsort import natsorted, natsort_keygen
nkey = natsort_keygen()
from chardet.universaldetector import UniversalDetector
detector = UniversalDetector()

wkt = input('Scieżka do folderu z wkt: ')
wynik = input('Scieżka dla pliku wynikowego: ')
plikwynik = os.path.join(wynik, 'polaczone_wkt.txt')

count = 1

with io.open(plikwynik, 'a', encoding = 'utf-8') as pw:
    for subdir, dirs, files in os.walk(wkt):
        dirs.sort(key=nkey)
        if not any(fname.upper().endswith('.WKT') for fname in os.listdir(subdir)):
            continue
        for file in natsorted(files):
            if file.upper().endswith('.WKT'):
                zapisane = 0
                print(count)
                count += 1
                stad = os.path.join(subdir, file)
                detector.reset()
                with open(stad, 'rb') as sprawdz:
                    for line in sprawdz:
                        detector.feed(line)
                        if detector.done:
                            break
                detector.close()
                kodek = str(detector.result['encoding'])
                if not kodek == 'ascii':
                    with io.open(stad, 'r', encoding = str(kodek)) as kopiuj:
                        for line in kopiuj:
                            if regex.match('^.+\)\n', line):
                                zlacz = line.split('\n')[0]+';'+os.path.splitext(file)[0]+'\n'
                            else:
                                zlacz = line+';'+os.path.splitext(file)[0]+'\n'
                            pw.write(zlacz)
                            zapisane = 1


                else:
                    with io.open(stad, 'r', encoding = 'utf-8') as kopiuj:
                        for line in kopiuj:
                            if regex.match('^.+\)\n', line):
                                zlacz = line.split('\n')[0]+';'+os.path.splitext(file)[0]+'\n'
                            else:
                                zlacz = line+';'+os.path.splitext(file)[0]+'\n'
                            pw.write(zlacz)
                            zapisane = 1

                if zapisane == 0:
                    pw.write(';'+os.path.splitext(file)[0]+'\n')
                        
input('KONIEC.')
