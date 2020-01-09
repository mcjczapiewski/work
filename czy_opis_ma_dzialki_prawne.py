import os
import io
from natsort import natsort_keygen
nkey = natsort_keygen()

for subdir, dirs, _ in os.walk(r'J:\0418102'):
    dirs.sort(key=nkey)
    if 'PRAWNE' in subdir and os.path.exists(os.path.join(subdir, 'opis.txt')):
        opis = os.path.join(subdir, 'opis.txt')
        with io.open(r'J:\0418102\zebrane.txt', 'a', encoding='utf-8') as zebrane:
            try:
                with open(opis, 'r') as ooo:
                    if not any('|' in line for line in ooo):
                        zebrane.write(subdir+'\n')
        #    except UnicodeDecodeError:
        #        with io.open(opis, 'r', encoding = 'utf-8') as ooo:
        #            if not any('|' in line for line in ooo):
        #                zebrane.write(subdir+'\n')
            except:
                print(opis)
                continue
