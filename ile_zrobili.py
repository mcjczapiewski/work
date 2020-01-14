import os
import datetime
import regex
from natsort import natsorted, natsort_keygen

nkey = natsort_keygen()

tego_dnia = o_data = o_nrobrebu = ile_ope = sytwys = prawne = duze = 0
count = 1
ile_dni = set()
porzadkuj = set()
tyle_zrobili = r"D:\_MACIEK_\python_proby\tyle_zrobili_wloclawek_zlecenie.txt"

if os.path.exists(tyle_zrobili):
    os.remove(tyle_zrobili)

for subdir, dirs, _ in os.walk(
    r"P:\cyfryzacja_powiat_wloclawski\ETAP_3\wloclawek_gmina\na_zewnatrz"
):
    dirs.sort(key=nkey)
    # if "na_zewnatrz" in subdir or "zlecone" not in subdir:
    #     continue
    plik = os.path.join(subdir, "opis.txt")
    if os.path.exists(plik):
        print(count)
        count += 1
        if "ponad" in subdir:
            nrobrebu = subdir.split("\\")[5] + "_ponad"
        else:
            nrobrebu = subdir.split("\\")[5]
        data = (
            str(datetime.datetime.fromtimestamp(os.path.getctime(plik)))
        ).split(" ")[0]
        if data not in ile_dni:
            ile_dni.add(data)

        if o_nrobrebu == 0:
            o_nrobrebu = nrobrebu

        if nrobrebu == o_nrobrebu:
            if o_data == 0:
                o_data = data

            if data == o_data:
                tego_dnia += 1
                if (
                    "PRAWNE" in subdir.split("\\")[6]
                    or "EWIDENCJI" in subdir.split("\\")[6]
                    or "MODERNI" in subdir.split("\\")[6]
                ):
                    prawne += 1
                elif "SYT-WYS" in subdir.split("\\")[6]:
                    sytwys += 1
                elif "ponad" in subdir.split("\\")[6]:
                    duze += 1
                continue

            else:
                with open(tyle_zrobili, "a") as tutaj:
                    tutaj.write(
                        o_nrobrebu
                        + "\t"
                        + o_data
                        + "\t"
                        + str(prawne)
                        + "\t"
                        + str(sytwys)
                        + "\t"
                        + str(duze)
                        + "\n"
                    )
                o_data = data
                ile_ope += tego_dnia
                tego_dnia = 1
                if (
                    "PRAWNE" in subdir.split("\\")[6]
                    or "EWIDENCJI" in subdir.split("\\")[6]
                    or "MODERNI" in subdir.split("\\")[6]
                ):
                    prawne = 1
                    sytwys = 0
                    duze = 0
                elif "SYT-WYS" in subdir.split("\\")[6]:
                    sytwys = 1
                    prawne = 0
                    duze = 0
                elif "ponad" in subdir.split("\\")[6]:
                    duze = 1
                    prawne = 0
                    sytwys = 0
                continue
        else:
            with open(tyle_zrobili, "a") as tutaj:
                tutaj.write(
                    o_nrobrebu
                    + "\t"
                    + o_data
                    + "\t"
                    + str(prawne)
                    + "\t"
                    + str(sytwys)
                    + "\t"
                    + str(duze)
                    + "\n"
                )
            o_nrobrebu = nrobrebu
            o_data = data
            ile_ope += tego_dnia
            if (
                "PRAWNE" in subdir.split("\\")[6]
                or "EWIDENCJI" in subdir.split("\\")[6]
                or "MODERNI" in subdir.split("\\")[6]
            ):
                prawne = 1
                sytwys = 0
                duze = 0
            elif "SYT-WYS" in subdir.split("\\")[6]:
                sytwys = 1
                prawne = 0
                duze = 0
            elif "ponad" in subdir.split("\\")[6]:
                duze = 1
                prawne = 0
                sytwys = 0
            tego_dnia = 1

ile_ope += tego_dnia
with open(tyle_zrobili, "a") as tutaj:
    tutaj.write(
        o_nrobrebu
        + "\t"
        + o_data
        + "\t"
        + str(prawne)
        + "\t"
        + str(sytwys)
        + "\t"
        + str(duze)
        + "\n"
    )

with open(tyle_zrobili, "r") as tutaj:
    for line in tutaj:
        porzadkuj.add(line)

duble = {}
for i in natsorted(porzadkuj):
    klucz = str(regex.match("^.+?\t.+?\t", i)[0])
    if klucz in duble:
        do_tego_prawne, do_tego_sytwys, do_tego_duze = duble[klucz].split("\t")
        dodaj_prawne = i.split("\t")[2].split("\n")[0]
        dodaj_sytwys = i.split("\t")[3].split("\n")[0]
        dodaj_duze = i.split("\t")[4].split("\n")[0]
        suma_prawne = int(do_tego_prawne) + int(dodaj_prawne)
        suma_sytwys = int(do_tego_sytwys) + int(dodaj_sytwys)
        suma_duze = int(do_tego_duze) + int(dodaj_duze)
        duble[klucz] = (
            str(suma_prawne) + "\t" + str(suma_sytwys) + "\t" + str(suma_duze)
        )
    else:
        wartosc = regex.search(r"^.+?\t.+?\t\K.+$", i)
        duble[klucz] = wartosc[0]

kto_ile = {}
for i in natsorted(duble):
    klucz = (
        str(regex.match(r"^00.._zlecone_.*\t(.+$)", i)[1])
        + str(regex.match(r"^00.._zlecone_(.*?)\t", i)[1])
        + "\t"
    )
    if klucz in kto_ile:
        do_tego_prawne, do_tego_sytwys, do_tego_duze = kto_ile[klucz].split(
            "\t"
        )
        dodaj_prawne, dodaj_sytwys, dodaj_duze = duble[i].split("\t")
        suma_prawne = int(do_tego_prawne) + int(dodaj_prawne)
        suma_sytwys = int(do_tego_sytwys) + int(dodaj_sytwys)
        suma_duze = int(do_tego_duze) + int(dodaj_duze)
        kto_ile[klucz] = (
            str(suma_prawne) + "\t" + str(suma_sytwys) + "\t" + str(suma_duze)
        )
    else:
        kto_ile[klucz] = duble[i]

with open(tyle_zrobili, "w") as tutaj:
    tutaj.write("OBREB\tDATA\tILE TEGO DNIA\n")
    for i in natsorted(duble):
        tutaj.write(i + str(duble[i]) + "\n" + "\n")
    for i in natsorted(kto_ile):
        tutaj.write(
            i
            + str(kto_ile[i])
            + "\n"
            + "\nW "
            + str(len(ile_dni))
            + " dni zrobionych "
            + str(ile_ope)
            + " operatów."
        )

input("\nKONIEC.")
