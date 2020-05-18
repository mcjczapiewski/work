# -*- coding: utf-8 -*-

import os, shutil, io
from natsort import natsorted, natsort_keygen
nkey = natsort_keygen()

count = 1

zrodlo = input('podaj źródło: ')
desti = input('podaj dest: ')

for subdir, dirs, _ in os.walk(zrodlo):
#    if 'gotowe' not in subdir:
#        continue
    dirs.sort(key=nkey)
    opis = os.path.join(subdir, 'opis.txt')
    if os.path.exists(opis):
        print(count)
        count += 1

# with io.open(r'P:\cyfryzacja_powiat_wloclawski\ETAP_4_WR\kopiuj.txt', 'r', encoding = 'utf-8') as opisy:
#    for line in opisy:
#        print(count)
#        count += 1
#        opis = line.split('\n')[0]
#        subdir = os.path.dirname(opis)

        tutaj = os.path.join(desti, str.split(subdir, ':\\')[1])
        if os.path.exists(tutaj):
            continue
        else:
            os.makedirs(tutaj)
        try:
            shutil.copy2(opis, tutaj)
        except:
            raise
            print(opis)
