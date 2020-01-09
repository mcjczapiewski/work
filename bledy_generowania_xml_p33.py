import os
import io
import regex
from natsort import natsorted, natsort_keygen

count = 1

bylo = set()
with io.open(r'D:\_MACIEK_\python_proby\p33\bledy_xml_bylo.txt', 'r', encoding='utf-8') as aaa:
    for line in aaa:
        bylo.add(line.split('\n')[0])

for subdir, dirs, files in os.walk(r'I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614\INOWROCŁAW'):
    dirs.sort(key=natsort_keygen())
    if not any(fname.upper().endswith('.XML') for fname in os.listdir(subdir)):
        continue
    for file in natsorted(files):
        if file.upper().endswith('.XML'):
            xml = os.path.join(subdir, file)
            print(count)
            count += 1
            if xml in bylo:
                continue
            try:
                with io.open(xml, 'r', encoding='utf-8') as oxml:
                    czytaj = 0
                    for line in oxml:
                        if regex.match('^.+celArchiwalny.+', line):
                            czytaj = 1
                            continue
                        if 'opis2' in line:
                            break
                        if czytaj == 1:
                            if not regex.match(r'^.+(<dzialkaPrzed></dzialkaPrzed>|\
                                                <dzialkaPrzed>0407[0-9][0-9]_[0-9]\.[0-9][0-9][0-9][0-9]\..+\
                                                </dzialkaPrzed>|<dzialkaPo></dzialkaPo>|\
                                                <dzialkaPo>0407[0-9][0-9]_[0-9]\.[0-9][0-9][0-9][0-9]\..+\
                                                </dzialkaPo>).*', line):
                                with io.open(r'D:\_MACIEK_\python_proby\p33\BLEDY_XML_PRZED-PO.txt',
                                             'a', encoding='utf-8') as bl:
                                    bl.write(xml + '\n')
                                with io.open(r'D:\_MACIEK_\python_proby\p33\BLEDY_XML_PRZED-PO-linijki.txt',
                                             'a', encoding='utf-8') as bl:
                                    bl.write(xml + '\n' + line + '\n\n')

            except:
                with io.open(r'D:\_MACIEK_\python_proby\p33\inne_kodowanie.txt', 'a', encoding='utf-8') as bl:
                    bl.write(xml + '\n')
