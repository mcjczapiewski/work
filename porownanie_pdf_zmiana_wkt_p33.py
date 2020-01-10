# -*- coding: utf-8 -*-
import cv2
import os
import datetime
import fitz
import io
import numpy as np
from natsort import natsorted, natsort_keygen
nkey = natsort_keygen()


###########################################################
def pix2np(pix):
    im = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
    im = np.ascontiguousarray(im[..., [2, 1, 0]])  # rgb to bgr
    return im


###########################################################
def porownajpdf():
    # countope = 0
    folder_drugi = ''
    print('\nPodaj ścieżkę do folderu z PIERWOTNYMI plikami PDF:')
    sprawdzanie = input()
    print('\nPodaj ścieżkę do folderu z plikami PDF do porównania:')
    do_porownania = input()
    print('\nTrwa liczenie folderów, poczekaj chwilkę...\n')
    # for _, dirnames, _ in os.walk(sprawdzanie):
    #   ^ this idiom means "we won't be using this value"
        # countope += len(dirnames)
    wszystkie = 1
    with open(r'D:\_MACIEK_\python_proby\p33\sciezki.txt', 'r') as sciezki:
        for line in sciezki:
            sprawdzanie = line.split('\n')[0]
            for subdir, dirs, files in os.walk(sprawdzanie):
                dirs.sort(key=nkey)
                if not any(fname.endswith('.PDF') for fname in os.listdir(subdir)):
                    continue
                folder_glowny = subdir
                dopasuj = os.path.basename(os.path.dirname(folder_glowny)) + os.path.basename(folder_glowny)
                czy_znalazl = 0
                szybciej = 'a'
                byly_juz = set()
                nrope = os.path.basename(subdir)
                print(str(wszystkie) + ' z ok. 10 000\t' + nrope)
                wszystkie += 1
                for file in natsorted(files):
                    if file.endswith('.pdf') or file.endswith('.PDF'):
                        pierwotne = file
                        pierwsze = os.path.join(folder_glowny, pierwotne)
                        przerwij = 0
                        try:
                            doc = fitz.open(pierwsze)
                            strony_s = doc.pageCount
                            pix = doc.getPagePixmap(0, alpha=False)
                            original = pix2np(pix)
                        except:
                            with io.open(bledny, 'a', encoding='utf-8') as bl:
                                bl.write('Nie udało się otworzyć PIERWOTNEGO:\t' + pierwsze + '\n')
                            continue
                        if szybciej == 'a':
                            idz_tu = do_porownania
                        else:
                            idz_tu = folder_drugi
                        for subdir, dirs, files in os.walk(idz_tu):
                            dirs.sort(key=nkey)
                            folder_drugi = subdir
                            if (os.path.basename(os.path.dirname(subdir))
                                    + os.path.basename(subdir) == dopasuj):
                                czy_znalazl = 1
                                for file in natsorted(files):
                                    if file.endswith('.pdf') or file.endswith('.PDF'):
                                        porownane = file
                                        drugie = os.path.join(subdir, porownane)
                                        if drugie in byly_juz:
                                            continue
                                        try:
                                            doc = fitz.open(drugie)
                                            strony_n = doc.pageCount
                                            if not strony_s == strony_n:
                                                continue
                                            pix = doc.getPagePixmap(0, alpha=False)
                                            image_to_compare = pix2np(pix)
                                        except:
                                            with io.open(bledny, 'a', encoding='utf-8') as bl:
                                                bl.write('Nie udało się otworzyć PORÓWNYWANEGO:\t')
                                                bl.write(drugie + '\n')
                                            continue
                                        # try:
                                        if original.shape == image_to_compare.shape:
                                            difference = cv2.subtract(original, image_to_compare)
                                            b, g, r = cv2.split(difference)
                                            if (cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0
                                                    and cv2.countNonZero(r) == 0):
                                                if pierwotne == porownane:
                                                    przerwij = 1
                                                    byly_juz.add(drugie)
                                                    break
                                                else:
                                                    with io.open(plikwynik, 'a', encoding='utf-8') as w:
                                                        w.write(pierwsze + '\t' + drugie + '\n')
                                                    przerwij = 1
                                                    byly_juz.add(drugie)
                                                    break
                                        # except:
                                        #     raise
                                        #     with io.open(bledny, 'a', encoding='utf-8') as bl:
                                        #         bl.write('Nie udało się porównać:\t' + drugie + '\n')
                                        #     continue
                                if przerwij == 1:
                                    break
                if czy_znalazl == 0:
                    with io.open(bledny, 'a', encoding='utf-8') as bl:
                        bl.write('NIE ZNALEZIONO FOLDERU O TAKIEJ SAMEJ NAZWIE!:\t' + folder_glowny + '\n')
    czaskoniec = datetime.datetime.now()
    roznicaczas = czaskoniec - czasstart
    czastrwania = roznicaczas.total_seconds() / 60
    print('\nSkończyłem porównywać PDFy. Mam listę zmian w pliku. Ta część zajęła (minuty):')
    print("%.2f" % czastrwania)
    taknie = 0
    while taknie == 0:
        czy_koniec = input('Czy mam zmienić też nazwy plików WKT? Y/N: ')
        if czy_koniec == 'Y' or czy_koniec == 'y':
            taknie = 1
            zmienwkt()
        elif czy_koniec == 'N' or czy_koniec == 'n':
            taknie = 1
            input('\nDobrze. W takim razie wciśnij ENTER aby wyjść...')
        else:
            print('\n\nNie mam takiej opcji...')


###########################################################
def zmienwkt():
    print('\nPodaj ścieżkę do folderu z plikami WKT:')
    wukaty = input()
    usun_a = set()
    do_konca = 0
    with io.open(plikwynik, 'r', encoding='utf-8') as pw:
        for line in pw:
            do_konca += 1
    with io.open(plikwynik, 'r', encoding='utf-8') as pw:
        for line in pw:
            print(do_konca)
            do_konca -= 1
            starawkt = os.path.splitext(str.split(line, '\t')[2])[0] + '.wkt'
            nowawkt = os.path.splitext(str.split(line, '\t')[3])[0] + '.wkt'
            przerwij = 0
            for subdir, dirs, files in os.walk(wukaty):
                dirs.sort(key=nkey)
                if str.split(line, '\t')[1] == os.path.basename(subdir):
                    for file in natsorted(files):
                        if file == starawkt:
                            do_zmiany = os.path.join(subdir, file)
                            po_zmianie = os.path.join(subdir, nowawkt)
                            try:
                                os.rename(do_zmiany, po_zmianie)
                                przerwij = 1
                                break
                            except FileExistsError:
                                subnewname = os.path.splitext(nowawkt)[0] + 'a.wkt'
                                try:
                                    os.rename(do_zmiany, os.path.join(subdir, subnewname))
                                    usun_a.add(os.path.join(subdir, subnewname))
                                    przerwij = 1
                                    break
                                except:
                                    with io.open(blednywkt, 'a', encoding='utf-8') as bwkt:
                                        bwkt.write('Nie udało się zmienić nazwy pliku:\t' + do_zmiany + '\n')
                                    przerwij = 1
                                    break
                            except:
                                with io.open(blednywkt, 'a', encoding='utf-8') as bwkt:
                                    bwkt.write('Nie udało się zmienić nazwy pliku:\t' + do_zmiany + '\n')
                                przerwij = 1
                                break
                if przerwij == 1:
                    break
    if usun_a:
        for line in natsorted(usun_a):
            czysty = str.split(os.path.basename(line), 'a.wkt')[0] + '.wkt'
            try:
                os.rename(line, os.path.join(os.path.dirname(line), czysty))
            except:
                with io.open(blednywkt, 'a', encoding='utf-8') as bl:
                    bl.write('Nie mogłem zmienić nazwy, plik o takiej samej nazwie chyba wciąż istnieje:\t')
                    bl.write(line)
    czaskoniec = datetime.datetime.now()
    roznicaczas = czaskoniec - czasstart
    czastrwania = roznicaczas.total_seconds() / 60
    print('\nSkończone!\nCałość zajęła (minuty):')
    print("%.2f" % czastrwania)
    print("\n~~~~~~KONIEC~~~~~~\t" + str(czaskoniec).split('.')[0])
    input('Wciśnij ENTER aby wyjść...')


###########################################################
czasstart = datetime.datetime.now()
print("~~~~~~START~~~~~~\t" + str(czasstart).split('.')[0])
print('\nPodaj ścieżkę do folderu od pliku wynikowego:')
sciezka = input()
wynikowy = os.path.basename(os.path.normpath(sciezka))
plikwynik = sciezka + '\\' + wynikowy + '_identyczne_' + czasstart.strftime('%Y-%m-%d') + '.txt'
plikwynik = r'D:\_MACIEK_\python_proby\p33\p33_identyczne_2019-08-13.txt'
print('\nPlik zostanie umieszczony w (bądź jeśli już istnieje to pobrany z):\n' + plikwynik)
bledny = sciezka + '\\' + wynikowy + '_BLEDY_' + czasstart.strftime('%Y-%m-%d') + '.txt'
bledny = r'D:\_MACIEK_\python_proby\p33\p33_BLEDY_2019-08-13.txt'
blednywkt = sciezka + '\\' + wynikowy + '_BLEDYwkt_' + czasstart.strftime('%Y-%m-%d') + '.txt'
corobimy = 0
while corobimy == 0:
    print('\nCzy chcesz:\n1.\tPorównywać PDFy?\n2.\tPDFy są już porównane i jest plik tekstowy \
          ze zmianami w nazwach, więc idziemy od razu do WKT.')
    tak_wiec = input('\nWpisz 1 lub 2: ')
    if tak_wiec == '1':
        corobimy = 1
        porownajpdf()
    elif tak_wiec == '2':
        corobimy = 1
        zmienwkt()
    else:
        print('\n\nNie ma takiej opcji...')
