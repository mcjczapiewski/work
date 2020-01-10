import os
import shutil
from natsort import natsorted, natsort_keygen
nkey = natsort_keygen()

count = 1

mety = input('Sciezka MET: ')
mapy = input('Sciezka mapy: ')

for subdir, dirs, files in os.walk(mapy):
    dirs.sort(key=nkey)
    if not any(fname.upper().endswith('.TIF') for fname in os.listdir(subdir)):
        continue
    if 'MAPA' in subdir:
        for file in natsorted(files):
            if file.upper().endswith('.TIF'):
                mapa = file
                odpowiada = os.path.splitext(file)[0] + '.MET'
                for _, _, files in os.walk(mety):
                    for file in natsorted(files):
                        if file.upper().endswith('.MET'):
                            if file == odpowiada:
                                try:
                                    shutil.copy(os.path.join(mety, file), subdir)
                                    print(str(count) + '\t' + os.path.basename(subdir) + '_' + mapa)
                                    count += 1
                                except:
                                    raise
