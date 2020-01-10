import os
import io
import regex
from natsort import natsort_keygen
nkey = natsort_keygen()

for subdir, dirs, _ in os.walk(r'H:\0418102'):
    dirs.sort(key=nkey)
    opis = os.path.join(subdir, 'opis.txt')
    if os.path.exists(opis):
        linie = []
        try:
            with io.open(opis, 'r', encoding='utf-8') as oopis:
                if any(line.startswith(os.path.basename(subdir)) for line in oopis):
                    oopis.seek(0)
                    for line in oopis:
                        if line.startswith(os.path.basename(subdir)):
                            line = regex.match('(^.+?_)(.+$)', line)[2]
                            linie.append(line + '\n')
                        else:
                            linie.append(line)
            if not linie:
                continue
            with io.open(opis, 'w', encoding='utf-8') as wopis:
                for i in linie:
                    wopis.write(i)

        except UnicodeDecodeError:
            with open(opis, 'r') as oopis:
                if any(line.startswith(os.path.basename(subdir)) for line in oopis):
                    oopis.seek(0)
                    for line in oopis:
                        if line.startswith(os.path.basename(subdir)):
                            line = regex.match('(^.+?_)(.+$)', line)[2]
                            linie.append(line + '\n')
                        else:
                            linie.append(line)
            if not linie:
                continue
            with open(opis, 'w') as wopis:
                for i in linie:
                    wopis.write(i)

        except:
            print(opis)
