import os, fnmatch, re
from natsort import natsort_keygen
nkey = natsort_keygen()

tutaj = r'I:\DANE_i_BAZY_2019-06-13\skany'
print('Ścieżka to: '+tutaj)
input('Wciśnij ENTER aby kontynuować...')
count = 0
lista = set()

for subdir, dirs, _ in os.walk(tutaj):
    dirs.sort(key=nkey)
    count += 1
    if fnmatch.fnmatch(subdir, '*;*'):
        print(str(count)+'\t'+os.path.basename(subdir))
        oryginal = str.split(subdir, ';')[0]
        d = subdir
        num = str.split(os.path.basename(subdir), ';')[0]
        if os.path.exists(os.path.join(subdir, 'opis.txt')):
            with open(os.path.join(subdir, 'opis.txt'), 'r') as glowny:
                glowny = glowny.read()
            if os.path.exists(os.path.join(oryginal, 'opis.txt')):
                print('\t\t\t'+os.path.basename(oryginal))
                with open(os.path.join(oryginal, 'opis.txt'), 'r') as file:
                    file = file.read()
                if file == glowny:
                    with open(r'D:\python_proby\powtarzajace_identyczne_opisy.txt', 'a') as po:
                        po.write('\t'+oryginal+'\n'+file+'\t'+subdir+'\n'+glowny+'\n\n')
                else:
                    with open(r'D:\python_proby\powtarzajace_nie_te_same_opisy.txt', 'a') as po:
                        po.write(oryginal+'\n'+subdir+'\n\n')
            for subdir, dirs, _ in os.walk(tutaj):
                dirs.sort(key=nkey)
                if subdir.startswith(oryginal+';'):
                    if re.match('^.+'+num+';.+', subdir):
                        if not subdir == d:
                            czy_bylo = subdir+d
                            if not czy_bylo in lista:
                                print('\t\t\t'+os.path.basename(subdir))
                                if os.path.exists(os.path.join(subdir, 'opis.txt')):
                                    lista.add(d+subdir)
                                    with open(os.path.join(subdir, 'opis.txt'), 'r') as file:
                                        file = file.read()
                                    if file == glowny:
                                        with open(r'D:\python_proby\powtarzajace_identyczne_opisy.txt', 'a') as po:
                                            po.write('\t'+d+'\n'+file+'\t'+subdir+'\n'+glowny+'\n\n')
                                    else:
                                        with open(r'D:\python_proby\powtarzajace_nie_te_same_opisy.txt', 'a') as po:
                                            po.write(d+'\n'+subdir+'\n\n')
