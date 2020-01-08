import os, shutil, regex, io
from natsort import natsort_keygen, natsorted
nkey = natsort_keygen()

for subdir, dirs, files in os.walk(r'I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614\DĄBROWA BISKUPIA'):
    dirs.sort(key=nkey)
    if not any(fname.upper().endswith('.XML') for fname in os.listdir(subdir)):
        continue
    for file in natsorted(files):
        if file.upper().endswith('.XML'):
            xml = os.path.join(subdir, file)
            with io.open(xml, 'r', encoding = 'utf-8') as xxml:
                for line in xxml:
                    if regex.match('^    <pzg_dataZgloszenia></pzg', line):
                        with open(r'D:\_MACIEK_\python_proby\xml_bez_daty.txt', 'a') as bezdaty:
                            bezdaty.write(xml+'\n')
                    elif regex.match('^    <celArchiwalny></cel', line) and regex.match('^    <pzg_cel></pzg', line):
                        with open(r'D:\_MACIEK_\python_proby\xml_bez_celu.txt', 'a') as bezcelu:
                            bezcelu.write(xml+'\n')
