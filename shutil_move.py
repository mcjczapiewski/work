import os, shutil, io

i = 1
plik = r'P:\cyfryzacja_powiat_wloclawski\ETAP_3\__DODAC_DO_ZASILENIA\UZUPELNIENIE_2020-01-07\Operaty z poprawionym DPI\przenies.txt'

with io.open(plik, 'r', encoding = 'utf-8') as sciezki:
    for line in sciezki:
        stad = line.split('\t')[0]
        tutaj = (line.split('\t')[1]).split('\n')[0]
        print(i)
        try:
            if not os.path.exists(os.path.dirname(tutaj)):
                os.makedirs(os.path.dirname(tutaj))
            shutil.move(stad, tutaj)
        except:
            print(str(i)+'\t~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'+line)
        i += 1
 
