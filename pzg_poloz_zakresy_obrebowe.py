wsp = []
zbior = {}
kolejna = 1
do_zbioru = ''

with open(r'D:\_MACIEK_\python_proby\proba\pzg_poloz.txt', 'r') as pzg_poloz:
    for line in pzg_poloz:
        uid, typ, rodzic, nrporz, status, x, y = line.split(' ')
        y = y.split('\n')[0]
        if not int(nrporz) == kolejna:
            n = len(wsp)
            area = 0.0
            for i in range(n):
                j = (i + 1) % n
                area += float(wsp[i].split(',')[0]) * float(wsp[j].split(',')[1])
                area -= float(wsp[j].split(',')[0]) * float(wsp[i].split(',')[1])
            area = abs(area) / 2.0
            zbior[do_zbioru] = area
        if int(nrporz) == 1:
            do_zbioru = rodzic + ' ' + typ
            wsp = []
            wsp.append(x + ',' + y)
            kolejna = 1
        else:
            wsp.append(x + ',' + y)
        kolejna += 1

with open(r'D:\_MACIEK_\python_proby\proba\zbior_zakresow.txt', 'a') as zakresy:
    zakresy.write(str(zbior))
