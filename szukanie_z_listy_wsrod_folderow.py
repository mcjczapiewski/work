# -*- coding: utf-8 -*-

import os
import re
from natsort import natsorted

zrodlo = input('podaj źródło: ')
nazwy = set()
count = 1

with open(r'D:\python_proby\tu\lili.txt', 'r') as lili:
    for line in lili:
        nazwy.add(str.split(line, '\n')[0])

for _, dirnames, _ in os.walk(zrodlo):
    for dirname in natsorted(dirnames):
        if re.match('^P((?![a-zA-Z]).)*$', dirname):
            print(str(count) + '\t' + dirname)
            count += 1
            if dirname in nazwy:
                with open(r'D:\python_proby\tu\znalezione_nie_kradzione.txt', 'a') as znk:
                    znk.write(dirname + '\n')
