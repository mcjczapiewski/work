s_rodzic = s_grupa = idmz = typ = rodzic = id_dzialki = ""
przed_po = grupa = nic = ""
nowy = "0"
przed = {}
po = {}
usun = []
pierwsze = ""
obdg = r"D:\_MACIEK_\python_proby\proba\obdg.txt"

with open(obdg, "r") as obdg:
    for line in obdg:
        uid, typ, rodzic, id_dzialki, przed_po, grupa, nic = line.split("\t")
        s_grupa = str(int(grupa) - 1)
        if pierwsze == "":
            s_rodzic = rodzic
            pierwsze = "a"

        if s_rodzic != rodzic:
            nowy = "1"

        if przed_po == "0" and nowy == "0":
            if grupa not in przed:
                przed[grupa] = rodzic + "_" + id_dzialki
            else:
                przed[grupa] = przed[grupa] + "," + rodzic + "_" + id_dzialki
        elif przed_po == "1" and nowy == "0":
            if grupa not in po:
                po[grupa] = rodzic + "_" + id_dzialki
            else:
                po[grupa] = po[grupa] + "," + rodzic + "_" + id_dzialki

        if nowy == "1":
            with open(
                r"D:\_MACIEK_\python_proby\proba\zapis.txt", "a"
            ) as zapis:
                zapis.write(
                    str(rodzic)
                    + "\tprzed\t"
                    + str(przed)
                    + "\n"
                    + str(rodzic)
                    + "\tpo\t"
                    + str(po)
                    + "\n"
                )
            przed = {}
            po = {}
            if przed_po == "0":
                if grupa not in przed:
                    przed[grupa] = rodzic + "_" + id_dzialki
            elif przed_po == "1":
                if grupa not in po:
                    po[grupa] = rodzic + "_" + id_dzialki
            nowy = "0"

        s_rodzic = rodzic
