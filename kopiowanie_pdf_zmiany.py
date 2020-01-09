# -*- coding: utf-8 -*-

import os
import shutil
import fnmatch as fn

zrodlo = input('podaj źródło: ')
desti = input('podaj dest: ')

for subdir, dirs, files in os.walk(zrodlo):

    print(os.path.basename(subdir))
    for file in files:
        if file.endswith('.pdf') and not fn.fnmatch(file, '*SPIS*'):
            opis = os.path.join(subdir, file)
            tutaj = os.path.join(desti, str.split(os.path.basename(subdir), '_')[0])
            if not os.path.exists(tutaj):
                os.mkdir(tutaj)
            if file.split('_')[0] == str.split(os.path.basename(subdir), '_')[0]:
                try:
                    shutil.copy2(opis, tutaj)
                except:
                    print(opis)
