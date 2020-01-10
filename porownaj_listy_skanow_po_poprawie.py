dysk = set()

with open(r'D:\_MACIEK_\python_proby\skany_fabianki\lista_P.txt', 'r') as listadysk:
    for line in listadysk:
        dysk.add(line)

with open(r'D:\_MACIEK_\python_proby\skany_fabianki\lista_dysk.txt', 'r') as listaP:
    for line in listaP:
        if line not in dysk:
            with open(r'D:\_MACIEK_\python_proby\skany_fabianki\jest_a_nie_bylo.txt', 'a') as brak:
                brak.write(line)
