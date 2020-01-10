import os
from natsort import natsort_keygen
nkey = natsort_keygen()

count = 1
sciezka = r'P:\cyfryzacja_powiat_wloclawski\ETAP_3\wloclawek_gmina_2'

for subdir, dirs, files in os.walk(sciezka):
    dirs.sort(key=nkey)
    if not any(fname.upper().endswith('.JPG') for fname in os.listdir(subdir)) or 'DOKUMENTACJA' in subdir:
        continue
    print(count)
    count += 1
    if not os.path.exists(os.path.join(subdir, 'opis.txt')):
        # print(subdir)
        with open(os.path.join(sciezka, 'brak_opisu.txt'), 'a') as bl:
            bl.write(subdir + '\n')
