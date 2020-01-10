import os
import regex
import io
from natsort import natsorted, natsort_keygen
nkey = natsort_keygen()

nowe = []
count = 1

with io.open(r'D:\_MACIEK_\python_proby\p33\zapis.txt', 'r', encoding='utf-8') as sciezki:
    for line in sciezki:
        sciezka = line
        zmien = regex.match('.+\t.+(040706_5.....).*', sciezka)[1]
        with io.open(r'D:\_MACIEK_\python_proby\p33\obreby.txt', 'r', encoding='utf-8') as obreby:
            for line in obreby:
                if zmien == regex.match('(^.+)\t.+', line)[1]:
                    nato = regex.match('.+\t(.+)', line)[1]
        sciezka = regex.sub(r'(^.+\t.+)(040706_5.....)(.*)', r'\g<1>' + nato + r'\g<3>', sciezka)
        nowe.append(sciezka)

with io.open(r'D:\_MACIEK_\python_proby\p33\zapis.txt', 'w', encoding='utf-8') as sciezki:
    for i in natsorted(nowe):
        sciezki.write(i)


with io.open(r'D:\_MACIEK_\python_proby\p33\obreby.txt', 'r', encoding='utf-8') as obreby:
    for line in obreby:
        obreb = line.split('\t')[1].split('\n')[0]
        if not any(fname == obreb for fname
                   in os.listdir(r'I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614\ZADANIE 2\KRUSZWICA')):
            print(obreb)

for subdir, dirs, _ in os.walk(r'I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614\ZADANIE 2\KRUSZWICA'):
    dirs.sort(key=nkey)
    print(count)
    count += 1
    with io.open(r'D:\_MACIEK_\python_proby\p33\sciezki.txt', 'r', encoding='utf-8') as sciezki:
        for line in sciezki:
            nazwa = line.split('\t')[1].split('\n')[0]
            if subdir == nazwa:
                print(line)
