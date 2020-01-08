import os, regex, shutil
from natsort import natsorted as nts

def operaty():
    nrope = 1
    braki = set()
    brak_zakresu = 0
    with open(zbiorczy_wkt, 'r') as zbiorczy:
        for line in zbiorczy:
            print(nrope)
            if not regex.search('\(\(\(.+\(', line):
                line = regex.sub('MULTI', '', line)
            if 'EMPTY' in line:
                braki.add(str(nrope))
                brak_zakresu += 1
                nrope += 1
                continue
            nrnr = (regex.split('\_\_\_', line)[2]).split('\n')[0]+'__'+regex.split('\_\_\_', line)[1]
            line = regex.sub('\"(.+?)\".*$', '\g<1>', line)
            plik_wkt = os.path.join(tusawkt, nrnr+'.wkt')
            nrope += 1
            with open(plik_wkt, 'a') as wkt:
                wkt.write(line)
    print('\n~~~~~~~~~~~~~~\nBrak zakresów dla '+str(brak_zakresu)+' operatów w liniach:')
    print(nts(braki))


def pliki():
    nrope = 1
    braki = set()
    brak_zakresu = 0
    with open(zbiorczy_wkt, 'r') as zbiorczy:
        for line in zbiorczy:
            print(nrope)
            if not regex.search('\(\(\(.+\(', line):
                line = regex.sub('MULTI', '', line)
            if 'EMPTY' in line:
                braki.add(str(nrope))
                brak_zakresu += 1
                nrope += 1
                continue
            nrnr = regex.search('^.+\)\)\).*?,\K.+?(?=,)', line)[0]
            if '\"' in nrnr:
                nrnr = (regex.split('\_\_\_', line)[2]).split('\n')[0]+'__'+regex.search('(")(.*?)(")', nrnr)[2]
            else:
                nrnr = (regex.split('\_\_\_', line)[2]).split('\n')[0]+'__'+nrnr
            nrope += 1
            line = regex.sub('\"(.+?)\".*$', '\g<1>', line)
            plik_wkt = os.path.join(tusawkt, nrnr+'.wkt')
            with open(plik_wkt, 'a') as wkt:
                wkt.write(line)
    print('\n~~~~~~~~~~~~~~\nBrak zakresów dla '+str(brak_zakresu)+' dokumentów w liniach:')
    print(nts(braki))


def teraz_kopiuj():
    def kopiuj():
        for subdir, dirs, _ in os.walk(operaty):
            if os.path.basename(subdir) == czy_pasi:
                if not os.path.exists(os.path.join(subdir, file)):
                    try:
                        shutil.copy2(os.path.join(tusawkt, file), subdir)
                    except:
                        with open(os.path.join(os.path.dirname(zbiorczy_wkt), 'BLEDY.txt'), 'a') as bledy:
                            bledy.write(os.path.join(tusawkt, file)+'\tNie udało się skopiować...\n')
                else:
                    with open(os.path.join(os.path.dirname(zbiorczy_wkt), 'BLEDY.txt'), 'a') as bledy:
                        bledy.write(os.path.join(tusawkt, file)+'\tTaki plik już istnieje...\n')
                    
    operaty = input('Podaj ścieżkę do folderu z operatami: ')
    while not os.path.exists(operaty):
        operaty = input('Podaj ścieżkę do folderu z operatami: ')
    
    for _, _, files in os.walk(tusawkt):
        for file in files:
            if '-' in file:
                czy_pasi = regex.search('__.+_', file)[0]
                czy_pasi = regex.sub('__|_$', '', czy_pasi)
                kopiuj()
            else:
                czy_pasi = regex.search('__.+\.wkt', file)[0]
                czy_pasi = regex.sub('__|\.wkt', '', czy_pasi)
                kopiuj()
    input('\nWciśnij ENTER aby zamknąć...')


def czy_kopiuj():
    czy_kopia = input('\n~~~~~~~~~~~~~~\nCzy chcesz teraz także skopiowac WKT do odpowiednich folderów? t/n:  ')
    if czy_kopia == 't':
        teraz_kopiuj()
    elif czy_kopia == 'n':
        input('Wciśnij ENTER, aby zamknąć program...')


def rozkopiowanie():
    for subdir, dirs, files in os.walk(operaty):
        for file in files:
            if regex.match('.+((-M-)|(-SZK-)).+\.PDF', file):
                wkt_operatu = os.path.join(subdir, os.path.basename(subdir)+'.wkt')
                if os.path.exists(wkt_operatu):
                    new_wkt = os.path.join(subdir, os.path.splitext(file)[0]+'.wkt')
                    if os.path.exists(new_wkt):
                        continue
                    else:
                        try:
                            shutil.copy2(wkt_operatu, new_wkt)
                        except:
                            with open(os.path.join(os.path.dirname(operaty), 'BLEDY.txt'), 'a') as bledy:
                                bledy.write(new_wkt+'\tNie udało się utworzyć.\n')
                else:
                    with open(os.path.join(os.path.dirname(operaty), 'BLEDY.txt'), 'a') as bledy:
                        bledy.write(subdir+'\tBrak wkt dla operatu.\n')
                    break


co_robimy = input('Co chcesz robić?:\n1 - utworzenie wkt dla operatów z csv\n2 - utworzenie dla wkt dla plików z csv\n3 - kopiowanie wkt do folderów operatów\n4 - rozkopiowanie istniejących wkt dla operatów do szkiców i map, które ich jeszcze nie mają\nPodaj cyfrę: ')
if co_robimy == '1':
    tusawkt = input('Podaj ścieżkę do zapisania plików wkt: ')
    zbiorczy_wkt = os.path.join(input('Podaj ścieżkę folderu, w którym znajduje się plik dla_operatow.csv: '), 'dla_operatow.csv')
    operaty()
    czy_kopiuj()
elif co_robimy == '2':
    tusawkt = input('Podaj ścieżkę do zapisania plików wkt: ')
    zbiorczy_wkt = os.path.join(input('Podaj ścieżkę folderu, w którym znajduje się plik dla_plikow.csv: '), 'dla_plikow.csv')
    pliki()
    czy_kopiuj()
elif co_robimy == '3':
    tusawkt = input('Podaj ścieżkę do folderu z plikami wkt: ')
    teraz_kopiuj()
elif co_robimy == '4':
    operaty = input('Podaj ścieżkę do folderu z operatami: ')
    rozkopiowanie()
