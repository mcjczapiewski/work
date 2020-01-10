import os
import shutil
from natsort import natsorted, natsort_keygen
nkey = natsort_keygen()

tutaj = input('sciezka do folderu: ')
usun = input('sciezka na smieci: ')
du = 1

for subdir, dirs, files in os.walk(tutaj):
    dirs.sort(key=nkey)
    for file in natsorted(files):
        if file.endswith('.txt'):
            pedeef = os.path.join(subdir, os.path.splitext(file)[0] + '.pdf')
            if os.path.exists(pedeef):
                print('Do usunięcia: ' + str(du))
                du += 1
                shutil.move(pedeef, os.path.join(usun, os.path.splitext(file)[0] + '.pdf'))

input('Enter aby zamknąć...')
