import os
import io
import regex
from natsort import natsorted, natsort_keygen
nkey = natsort_keygen()

count = 1
juz_byly = set()

nowe = input('Podaj ścieżkę do nowych danych: ')
oryginal = input('Podaj ściezkę do starych danych: ')
sciezka = input('Wskaż folder do zapisu plików z błędami: ')

for subdir, dirs, _ in os.walk(nowe):
    dirs.sort(key=nkey)
    if not any(fname.endswith('.PDF') for fname in os.listdir(subdir)):
        continue
    n_folder = subdir
    dopasuj = os.path.basename(os.path.dirname(n_folder)) + os.path.basename(n_folder)
    zbior_pdf = set()
    print(str(count) + '\t' + dopasuj)
    count += 1
    znaleziono = 0
    for fname in os.listdir(oryginal):
        if fname == os.path.basename(os.path.dirname(n_folder)):
            tosamo = os.path.join(oryginal, fname)
    for subdir, dirs, _ in os.walk(tosamo):
        dirs.sort(key=nkey)
        if not any(fname.endswith('.PDF') for fname in os.listdir(subdir)):
            continue
        if subdir not in juz_byly:
            if os.path.basename(os.path.dirname(subdir)) + os.path.basename(subdir) == dopasuj:
                o_folder = subdir
                juz_byly.add(o_folder)
                znaleziono = 1
                break
    if znaleziono == 0:
        with io.open(os.path.join(sciezka, 'nie_bylo_takiego_folderu.txt'), 'a', encoding='utf-8') as heh:
            heh.write(n_folder + '\n')
        continue

    for _, _, files in os.walk(n_folder):
        for file in natsorted(files):
            if (file.upper()).endswith('.PDF'):
                n_nazwa = file
                n_pdf = os.path.join(n_folder, n_nazwa)
                n_rozmiar = os.path.getsize(n_pdf)
                zbior_pdf.add(n_nazwa)

                o_pdf = os.path.join(o_folder, n_nazwa)
                if os.path.exists(o_pdf):
                    o_rozmiar = os.path.getsize(o_pdf)
                    if not o_rozmiar - 5000 <= n_rozmiar <= o_rozmiar + 5000:
                        with io.open(os.path.join(sciezka, 'rozne_wagi_plikow.txt'),
                                     'a', encoding='utf-8') as wagi:
                            wagi.write(n_pdf + '\t' + o_pdf + '\n')
                        continue
                    else:
                        with io.open(os.path.join(sciezka, 'wagi_plikow_sa_takie_same.txt'),
                                     'a', encoding='utf-8') as same:
                            same.write(n_pdf + '\t' + o_pdf + '\n')
                else:
                    with io.open(os.path.join(sciezka, 'takie_pdf_nie_istnialy.txt'),
                                 'a', encoding='utf-8') as new:
                        new.write(n_pdf + '\n')
    for _, _, files in os.walk(o_folder):
        for file in natsorted(files):
            if (file.upper()).endswith('.PDF'):
                if file not in zbior_pdf:
                    o_pdf = os.path.join(o_folder, file)
                    with io.open(os.path.join(sciezka, 'kiedys_byly_teraz_nie_ma.txt'),
                                 'a', encoding='utf-8') as brak:
                        brak.write(o_pdf + '\n')

count = 1
for subdir, dirs, _ in os.walk(oryginal):
    dirs.sort(key=nkey)
    if not any(fname.endswith('.PDF') for fname in os.listdir(subdir)):
        continue
    if subdir not in juz_byly:
        print(str(count) + '\tNIE MA W NOWYCH')
        count += 1
        with io.open(os.path.join(sciezka, 'foldery_ktorych_nie_ma_w_nowych.txt'),
                     'a', encoding='utf-8') as braki:
            braki.write(subdir + '\n')


count = 1
with io.open(os.path.join(sciezka, 'kiedys_byly_teraz_nie_ma.txt'), 'r', encoding='utf-8') as sprawdz:
    for line in sprawdz:
        pdf = line.split('\n')[0]
        wkt = (line.split('\n')[0]).split('.PDF')[0] + '.wkt'
        if os.path.exists(wkt):
            print(str(count) + '\tA MIAŁ WKT')
            count += 1
            with io.open(os.path.join(sciezka, 'teraz_nie_ma_mial_wkt.txt'), 'a', encoding='utf-8') as oj:
                oj.write(pdf + '\t' + wkt + '\n')

count = 1
with io.open(os.path.join(sciezka, 'kiedys_byly_teraz_nie_ma.txt'), 'r', encoding='utf-8') as sprawdz:
    for line in sprawdz:
        line = (line.split('\n')[0]).replace(r'I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614', 'H:')
        tutaj = os.path.dirname(line)
        moze_jednak = regex.sub('^.+?(-.+$)', '\\1', line)
        for subdir, dirs, files in os.walk(tutaj):
            for file in natsorted(files):
                if regex.match('^.*' + moze_jednak, file):
                    print(count)
                    count += 1
                    with io.open(os.path.join(sciezka, 'ale_sa_z_innym_nr_dok.txt'),
                                 'a', encoding='utf-8') as inne:
                        inne.write(os.path.join(subdir, file) + '\n')
