import os
import shutil
import io
from natsort import natsorted, natsort_keygen
nkey = natsort_keygen()

count = 1

print('\nUWAGA!\nW lokalizacji podanej jako pierwsza może utworzyć się plik z błędami.')
print('Program kopiuje pliki z rozszerzeniami: .TXT, .WKT, .XML, .KCD, .DXF, .DWG, .DGN, .TFW, .DAT\n\n')
stad = input('Podaj skąd pobierać: ')
tutaj = input('Podaj dokąd kopiować: ')

for subdir, dirs, files in os.walk(stad):
    dirs.sort(key=nkey)
    glowny = subdir
    ope_glowny = os.path.basename(glowny)

    for subdir, dirs, _ in os.walk(tutaj):
        dirs.sort(key=nkey)
        doc = subdir
        ope_doc = os.path.basename(doc)

        if ope_doc == ope_glowny:
            for file in natsorted(files):
                if file.upper().endswith(('.TXT', '.WKT', '.XML', '.KCD', '.DXF', '.DWG', '.DGN',
                                          '.TFW', '.DAT')):
                    plik = os.path.join(glowny, file)
                    doc_plik = os.path.join(doc, file)

                    try:
                        shutil.copy(plik, doc_plik)
                        print(count)
                        count += 1

                    except:
                        with io.open(os.path.join(stad, 'nie_skopiowano.txt'), 'a',
                                     encoding='utf-8') as bledy:
                            bledy.write(plik + '\n')

input('\nKONIEC.')
