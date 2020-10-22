duble = {}
ciag = stary_rodzic = ""

with open(
    r"D:\_MACIEK_\python_proby\takie_same_zakresy\baza.txt", "r"
) as baza:
    for line in baza:
        rodzic = line.split("\t")[1] + "__" + line.split("\t")[2]
        wsp = line.split("\t")[4]
        numer = line.split("\t")[3]
        if int(numer) == 1:
            duble[stary_rodzic] = ciag
            ciag = wsp
            stary_rodzic = rodzic
        else:
            ciag = ciag + "__" + wsp

with open(
    r"D:\_MACIEK_\python_proby\takie_same_zakresy\duble.txt", "a"
) as ddd:
    for i in duble:
        ddd.write(i + "\t" + duble[i] + "\n")

with open(
    r"D:\_MACIEK_\python_proby\takie_same_zakresy\duble.txt", "r"
) as plik:
    for line in plik:
        rodzic, wsp = line.split("\t")
        wsp = str(wsp.split("\n")[0])
        if wsp in duble:
            wartosc = duble[wsp]
            wartosc = wartosc + "__" + str(rodzic)
            duble[wsp] = wartosc
        else:
            duble[wsp] = rodzic

with open(
    r"D:\_MACIEK_\python_proby\takie_same_zakresy\wynik.txt", "a"
) as ddd:
    for i in duble:
        ddd.write(duble[i] + "\n")
