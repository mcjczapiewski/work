import os
import io
import regex
import shutil
from natsort import natsorted, natsort_keygen
nkey = natsort_keygen()

count = 1

for subdir, dirs, files in os.walk(r'I:\INOWROCŁAW\DANE PODGiK\SKANY OPERATÓW\gmina \
                                     Inowroclaw\!OPERATY_KTÓRE_ODDAJEMY'):
    dirs.sort(key=nkey)
    if 'brak_nr_obrebu_w_xml' in subdir:
        continue
    if any(fname.upper().endswith('.XML') for fname in os.listdir(subdir)):
        nrope = os.path.basename(subdir)
        operat = subdir
        for file in natsorted(files):
            if file.upper().endswith('.XML'):
                xml = os.path.join(subdir, file)
                with io.open(xml, 'r', encoding='utf-8') as oxml:
                    for line in oxml:
                        if 'obreb' in line:
                            try:
                                obreb = regex.match(r'.+\>(.+?)\<.+', line)[1]
                            except:
                                print(xml)
                            break
                    with io.open(r'D:\_MACIEK_\python_proby\p33\id_nazwa_obrebu.txt',
                                 'r', encoding='utf-8') as lista:
                        for line in lista:
                            porownaj = line.split('\t')[0]
                            nazwa = line.split('\t')[1].split('\n')[0]
                            if porownaj == obreb:
                                for fname in os.listdir(r'I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\2019\
                                                        0614\INOWROCŁAW'):
                                    if fname == nazwa:
                                        folder = os.path.join(r'I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\2019\
                                                              0614\INOWROCŁAW', fname)
                                        if os.path.exists(os.path.join(folder, nrope)):
                                            with io.open(r'D:\_MACIEK_\python_proby\p33\juz_istnialy.txt',
                                                         'a', encoding='utf-8') as przeniesione:
                                                przeniesione.write(operat + '\t' + folder + '\n')
                                        else:
                                            shutil.move(operat, os.path.join(folder, nrope))
                                            print(str(count) + '\t' + os.path.join(folder, nrope))
                                            with io.open(r'D:\_MACIEK_\python_proby\p33\przeniesione.txt',
                                                         'a', encoding='utf-8') as przeniesione:
                                                przeniesione.write(operat + '\t' + folder + '\n')
                                            count += 1
