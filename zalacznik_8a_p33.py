# -*- coding: utf-8 -*-

import os
import io
from natsort import natsorted, natsort_keygen
nkey = natsort_keygen()

count = 1
sciezka = input('Podaj ścieżkę do folderu: ')

for subdir, dirs, files in os.walk(sciezka):
    dirs.sort(key=nkey)
    if not any(fname.upper().endswith('.PDF') for fname in os.listdir(subdir)):
        continue
    cyfrowe = wkt = 0
    numer = os.path.basename(subdir)
    if numer.upper().startswith('P.'):
        id_ope = numer
        nr_ope = ''
    else:
        id_ope = ''
        nr_ope = numer
    for file in natsorted(files):
        if file.upper().endswith('.PDF'):
            cyfrowe += 1
        elif file.upper().endswith('.WKT'):
            wkt += 1
    if wkt > 1:
        wkt -= 1
    with io.open(os.path.join(sciezka, 'zalacznik8a.txt'), 'a', encoding='utf-8') as wynik:
        wynik.write(str(count) + '\t' + str(id_ope) + '\t' + str(nr_ope) + '\t')
        wynik.write(str(cyfrowe) + '\t' + str(wkt) + '\n')
    print(count)
    count += 1
