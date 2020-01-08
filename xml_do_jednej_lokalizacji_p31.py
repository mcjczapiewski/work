import os, shutil
from natsort import natsorted, natsort_keygen
nkey = natsort_keygen()

stad = input('Skąd brać xmle?: ')
tutaj = input('Katalog docelowy: ')
count = 1

for subdir, dirs, files in os.walk(stad):
    dirs.sort(key=nkey)
    if not any(fname.upper().endswith('.XML') for fname in os.listdir(subdir)):
        continue
    for file in natsorted(files):
        if file.upper().endswith('.XML'):
            xml = os.path.join(subdir, file)
            doc = os.path.join(tutaj, file)
            if os.path.exists(doc):
                print(str(count)+'\tNR JUŻ ISTNIEJE!\t'+xml)
            else:
                shutil.copy(xml, doc)
                print(count)
            count += 1

input('KONIEC.')
