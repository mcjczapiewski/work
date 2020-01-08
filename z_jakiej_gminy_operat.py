# -*- coding: utf-8 -*-

import os, re

braki = r'D:\python_proby\braki.txt'
nr_ope = r'D:\python_proby\nr_ope.txt'

if os.path.exists(r'D:\python_proby\jaka_gmina.txt'):
    yn = input('Czy chcesz usunąć stary plik z wynikiem? Y/N: ')
    if yn == 'Y' or yn == 'y':
        usun = r'D:\python_proby\jaka_gmina.txt'
        os.remove(usun)
        print('Usunięty!')
    else:
        print('Nowe dane zostaną dopisane.')

with open(braki, 'r') as b:
    for line in b:
        znaleziona = 0
        czy = str.split(line, '\n')[0]
        print(czy)
        with open(nr_ope, 'r') as no:
            for line in no:
                if re.match('^.+?(?=\t)', line)[0] == czy:
                    with open(r'D:\python_proby\jaka_gmina.txt', 'a') as wynik:
                        wynik.write(line)
                        znaleziona = 1
        if not znaleziona == 1:
            with open(r'D:\python_proby\jaka_gmina.txt', 'a') as wynik:
                wynik.write(czy+'\tNie znaleziono odpowiednika.\n')
