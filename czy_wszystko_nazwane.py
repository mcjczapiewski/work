import os, re
from natsort import natsorted, natsort_keygen
nkey = natsort_keygen()

count = 1

for subdir, dirs, files in os.walk(r'J:\0418102'):
    dirs.sort(key=nkey)
    if not any(fname.upper().endswith(('.JPG', '.JPEG')) for fname in os.listdir(subdir)):
        continue
    print(count)
    count += 1
    for file in natsorted(files):
        if file.upper().endswith(('.JPG', 'JPEG')):
            if not re.match('^.+?_.+?_.+$', file):
                with open(r'J:\0418102\bledy.txt', 'a') as bl:
                    bl.write(subdir+'\n')
            
