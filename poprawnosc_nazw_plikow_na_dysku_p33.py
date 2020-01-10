import os
import regex
import io
from natsort import natsorted, natsort_keygen
nkey = natsort_keygen()

nazwy = ('AKN', 'AWZ', 'AMZ', 'ADEB', 'ADEL', 'MATR', 'DEC', 'DOK-IN',
         'DOK-WYJ', 'DOK-OBL', 'DZ-P', 'DZ-R', 'K-BUD', 'K-PAR', 'M-KL', 'M-IN',
         'M-KAT', 'M-WYN', 'M-UZ', 'M-WYW', 'M-PROJ', 'M-WPROJ', 'MPZP', 'ZGL-ODP',
         'OPIN', 'OIM', 'OTOP', 'ORZ', 'OSW', 'POST', 'P-KW', 'P-G', 'P-IN', 'P-KAT',
         'R-IN', 'R-GPS', 'REJ-ARCH', 'REJ-IN', 'REJ-SCAL', 'SK-D', 'SK-W', 'SPIS',
         'S-TECH', 'STR-TYT', 'SZK-INN', 'SZK-KAT', 'SZK-OSN', 'SZK-POL', 'SZK-PRZ',
         'TR-PKT', 'UGO', 'UPOW', 'WNI-IN', 'WNI-PRZ', 'W-S', 'W-WSP', 'W-WYW', 'W-ZDE',
         'Z-KAT', 'Z-POM', 'ZASW', 'ZAW-ZGL', 'ZAW-IN', 'ZAW-KW', 'ZGL-PRAC', 'ZW')
sciezka = input('Podaj ścieżkę: ')

count = 1

for subdir, dirs, files in os.walk(sciezka):
    dirs.sort(key=nkey)

    if (not any(fname.upper().endswith('.PDF') for fname in os.listdir(subdir)) or not
            os.path.basename(subdir).startswith('P')):
        continue

    print(str(count) + '\t' + os.path.basename(os.path.dirname(subdir)) + '\\' + os.path.basename(subdir))
    count += 1

    for file in natsorted(files):
        if file.upper().endswith('.PDF'):
            if not regex.match(r'^P.+[0-9]\.PDF', file.upper()):
                with io.open(r'I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614\DĄBROWA BISKUPIA\
                             BRAKUJĄCE_OPEARTY_19.11.2019\brakujące_operaty_Dąbrowa_Biskupia\
                             GMINA DABROWA BISKUPIA\niepoprawne_nazwy.txt',
                             'a', encoding='utf-8') as np:
                    np.write(os.path.join(subdir, file) + '\n')
            else:
                try:
                    nazwa = regex.match(r'^.+?-(.+[A-Z])-[0-9].+PDF', file.upper())[1]
                except:
                    print('\t\t\t' + os.path.join(subdir, file))
                if nazwa not in nazwy:
                    with io.open(r'I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614\DĄBROWA BISKUPIA\
                                 BRAKUJĄCE_OPEARTY_19.11.2019\brakujące_operaty_Dąbrowa_Biskupia\
                                 GMINA DABROWA BISKUPIA\niepoprawne_nazwy.txt',
                                 'a', encoding='utf-8') as np:
                        np.write(os.path.join(subdir, file) + '\n')
