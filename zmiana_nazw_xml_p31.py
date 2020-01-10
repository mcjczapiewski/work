# -*- coding: utf-8 -*-

# import bibliotek
import os
import datetime
import regex
import io
from natsort import natsorted, natsort_keygen
nkey = natsort_keygen()

# aktualna data i godzina
czasstart = datetime.datetime.now()
print("~~~~~~START~~~~~~\t" + str(czasstart).split('.')[0])

sciezka = input('Podaj ścieżkę do folderu z plikami xml: ')

for subdir, dirs, files in os.walk(sciezka):
    dirs.sort(key=nkey)
    for file in natsorted(files):
        if file.endswith(('.xml', '.XML')):
            path2file = os.path.join(subdir, file)
            with io.open(path2file, 'r', encoding='utf-8') as xml:
                for line in xml:
                    if regex.match(r'.*pierwszyCzlon.*', line):
                        c1 = (regex.sub(r'.*\>(.*)\<.*', r'\g<1>', line)).split('\n')[0]
                    elif regex.match(r'.*drugiCzlon.*', line):
                        c2 = (regex.sub(r'.*\>(.*)\<.*', r'\g<1>', line)).split('\n')[0]
                    elif regex.match(r'.*trzeciCzlon.*', line):
                        c3 = (regex.sub(r'.*\>(.*)\<.*', r'\g<1>', line)).split('\n')[0]
                    elif regex.match(r'.*czwartyCzlon.*', line):
                        c4 = (regex.sub(r'.*\>(.*)\<.*', r'\g<1>', line)).split('\n')[0]
            new_name = os.path.join(subdir, c1 + '.' + c2 + '.' + c3 + '.' + c4 + '.xml')
            if not os.path.exists(new_name):
                try:
                    os.rename(path2file, new_name)
                except:
                    with open(os.path.join(sciezka, 'bledy.txt'), 'a') as bledy:
                        bledy.write(path2file + '\tNie udało się zmienić nazwy.\n')
            else:
                with open(os.path.join(sciezka, 'bledy.txt'), 'a') as bledy:
                    bledy.write(path2file + '\tTaka ścieżka już istnieje.\n')

# czas trwania calego skryptu
czaskoniec = datetime.datetime.now()
roznicaczas = czaskoniec - czasstart
czastrwania = roznicaczas.total_seconds() / 60
print('\nCałość zajęła (minuty):')
print("%.2f" % czastrwania)
print("\n~~~~~~KONIEC~~~~~~\t" + str(czaskoniec).split('.')[0])

input('Wciśnij ENTER aby wyjść...')
