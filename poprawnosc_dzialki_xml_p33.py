import os, io, regex
from natsort import natsorted, natsort_keygen
nkey = natsort_keygen()

count = 1

xmle = input('Scieżka: ')

for subdir, dirs, files in os.walk(xmle):
    dirs.sort(key=nkey)
    if not any(fname.upper().endswith('.XML') for fname in os.listdir(subdir)):
        continue

    for file in natsorted(files):
        if file.upper().endswith('.XML'):
            print(str(count)+'\t'+subdir.split('\\')[5]+'___'+subdir.split('\\')[6])
            count += 1
            xml = os.path.join(subdir, file)
            with io.open(xml, 'r', encoding = 'utf-8') as plik:
                stop = 1
                linia = 0
                for line in plik:
                    if 'celArchiwalny' in line:
                        stop = 0
                        continue
                    elif stop == 1:
                        continue
                    if 'opis' in line:
                        break
                    if not regex.match('^    <dzialkaPrzed>.*</dzialkaPrzed>\n', line) and 'Po' not in line:
                        with io.open(r'D:\_MACIEK_\python_proby\p33\dzialki_xml.txt', 'a', encoding = 'utf-8') as dz:
                            dz.write(xml+'\n')
                    elif not regex.match('^    <dzialkaPo>.*</dzialkaPo>\n', line) and 'Przed' not in line:
                        with io.open(r'D:\_MACIEK_\python_proby\p33\dzialki_xml.txt', 'a', encoding = 'utf-8') as dz:
                            dz.write(xml+'\n')
