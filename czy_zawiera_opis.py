import os, re
from natsort import natsorted, natsort_keygen
nkey = natsort_keygen()

count = 1
sciezka = r'J:\0418052'

for subdir, dirs, files in os.walk(sciezka):
    dirs.sort(key=nkey)
    if not any(fname.upper().endswith('.JPG') for fname in os.listdir(subdir)) or 'DOKUMENTACJA' in subdir:
        continue
    print(count)
    count += 1
    if not os.path.exists(os.path.join(subdir, 'opis.txt')):
##        print(subdir)
        with open(os.path.join(sciezka, 'brak_opisu.txt'), 'a') as bl:
            bl.write(subdir+'\n')
