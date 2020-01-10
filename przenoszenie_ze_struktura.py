# -*- coding: utf-8 -*-

import os
import shutil
# from distutils.dir_util import copy_tree

desti = input('podaj dest: ')

with open(r'P:\cyfryzacja_powiat_wloclawski\ETAP_3\Izbica_skany\sciezki.txt', 'r') as pliki:
    for line in pliki:
        opis = line.split('\n')[0]
        # if not os.path.exists(opis):
        #     print(opis + '\tsciezka nie istnieje')
        #     continue
        # if not any(fname.endswith('.wkt') for fname in os.listdir(opis)):
        #     print(opis + '\tbrak wkt')
        #     continue
        # for _, _, files in os.walk(opis):
        #     for file in files:
        #         if file.endswith('.wkt'):
        #             wkt = os.path.join(opis, file)
        tutaj = os.path.join(desti, os.path.dirname(opis.split(':\\')[1]))
        # print(tutaj)
        if not os.path.exists(tutaj):
            os.makedirs(tutaj)
        try:
            shutil.move(opis, tutaj)
        except:
            print(opis)
