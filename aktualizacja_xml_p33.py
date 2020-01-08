import os
import regex
import io
from natsort import natsorted, natsort_keygen
nkey = natsort_keygen()

sciezka = r'I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614\DĄBROWA BISKUPIA'
# sciezka = r'D:\_MACIEK_\python_proby\p33\aktualizacja_xml\xml'
wykaz = r'D:\_MACIEK_\python_proby\p33\aktualizacja_xml\wykaz.txt'
count = 1

for subdir, dirs, files in os.walk(sciezka):
    dirs.sort(key=nkey)
    if not any(fname.upper().endswith('.XML') for fname in os.listdir(subdir)):
        continue
    for file in natsorted(files):
        if file.upper().endswith('.XML'):
            linie = []
            xml = os.path.join(subdir, file)
            # with io.open(wykaz, 'r', encoding = 'utf-8') as owykaz:
            #     for line in owykaz:
            #         operat, pzg, jedn, nr, rok, sepnr, seprok = line.split('\t')
            #         seprok = seprok.split('\n')[0]
            #         if os.path.splitext(file)[0] == operat:
            #             print(count)
            #             count += 1
            #             with io.open(xml, 'r', encoding = 'utf-8') as oxml:
            #                 for line in oxml:
            #                     if 'pzg_idZgloszenia' in line:
            #                         line = regex.sub('(^.+?\>)(.*?)(\<.+$)', '\g<1>'+pzg+'\g<3>', line)
            #                         linie.append(line)
            #                     elif 'idZgloszeniaJedn' in line:
            #                         line = regex.sub('(^.+?\>)(.*?)(\<.+$)', '\g<1>'+jedn+'\g<3>', line)
            #                         linie.append(line)
            #                     elif 'idZgloszeniaNr' in line:
            #                         line = regex.sub('(^.+?\>)(.*?)(\<.+$)', '\g<1>'+nr+'\g<3>', line)
            #                         linie.append(line)
            #                     elif 'idZgloszeniaRok' in line:
            #                         line = regex.sub('(^.+?\>)(.*?)(\<.+$)', '\g<1>'+rok+'\g<3>', line)
            #                         linie.append(line)
            #                     elif 'idZgloszeniaSepJednNr' in line:
            #                         line = regex.sub('(^.+?\>)(.*?)(\<.+$)', '\g<1>'+sepnr+'\g<3>', line)
            #                         linie.append(line)
            #                     elif 'idZgloszeniaSepNrRok' in line:
            #                         line = regex.sub('(^.+?\>)(.*?)(\<.+$)', '\g<1>'+seprok+'\g<3>', line)
            #                         linie.append(line)
            #                     else:
            #                         linie.append(line)
            #             with io.open(xml, 'w', encoding = 'utf-8') as wxml:
            #                 for i in linie:
            #                     wxml.write(i)

            with io.open(xml, 'r', encoding='utf-8') as oxml:
                if not any(regex.match('^.*<nazwa></nazwa>.*$', line)
                           for line in oxml):
                    continue
                print(count)
                count += 1
                oxml.seek(0)
                for line in oxml:
                    if '<nazwa></nazwa>' in line:
                        line = regex.sub('(^.+?[>])(.*?)([<].+$)',
                                         '\g<1>TWÓRCA NIEZNANY\g<3>', line)
                        linie.append(line)
                    else:
                        linie.append(line)
            with io.open(xml, 'w', encoding='utf-8') as wxml:
                for i in linie:
                    wxml.write(i)
