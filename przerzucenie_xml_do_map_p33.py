import os
import shutil
from natsort import natsorted, natsort_keygen
nkey = natsort_keygen()

count = 1
hamuj = 0

mapy = input('Podaj ścieżkę do map: ')
xmle = input('Podaj ścieżkę do xmli: ')

for subdir, dirs, files in os.walk(mapy):
    dirs.sort(key=nkey)
    mapa = subdir
    for file in natsorted(files):
        if (file.lower()).endswith('.tif'):
            dopasuj = os.path.splitext(file)[0]
            for subdir, dirs, files in os.walk(xmle):
                dirs.sort(key=nkey)
                for file in natsorted(files):
                    if file == dopasuj + '.xml':
                        stad = os.path.join(subdir, file)
                        tutaj = os.path.join(mapa, file)
                        if not os.path.exists(tutaj):
                            try:
                                shutil.move(stad, tutaj)
                                print(str(count) + '\t' + tutaj)
                                count += 1
                                hamuj = 1
                                break
                            except:
                                with open(os.path.join(xmle, 'NIE_UDALO_SIE_PRZENIESC.txt'), 'a') as bledy:
                                    bledy.write(stad + '\n')
                        else:
                            with open(os.path.join(xmle, 'XML_JUZ_ISTNIEJE.txt'), 'a') as bledy:
                                bledy.write(tutaj + '\n')
                if hamuj == 1:
                    hamuj = 0
                    break


input('Wciśnij ENTER żeby zamknąć...')
