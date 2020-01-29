import os
import io
import datetime
import regex
from natsort import natsorted, natsort_keygen

nkey = natsort_keygen()

tego_dnia = o_data = o_nrobrebu = ile_ope = sytwys = prawne = duze = 0
count = 1
ile_dni = set()
porzadkuj = set()
tyle_zrobili = r"D:\_MACIEK_\python_proby\tyle_zrobili_wloclawek_2.txt"

if os.path.exists(tyle_zrobili):
    os.remove(tyle_zrobili)

for subdir, dirs, _ in os.walk(
    r"P:\cyfryzacja_powiat_wloclawski\ETAP_3\wloclawek_gmina_2"
):
    dirs.sort(key=nkey)
    # if "na_zewnatrz" in subdir or "zlecone" not in subdir:
    #     continue
    plik = os.path.join(subdir, "opis.txt")
    if os.path.exists(plik):
        print(count)
        count += 1
        nrobrebu = subdir.split("\\")[4]
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
                    "PRAWNE" in subdir.split("\\")[5]
                    or "EWIDENCJI" in subdir.split("\\")[5]
                    or "MODERNI" in subdir.split("\\")[5]
                ):
                    prawne += 1
                elif "SYT-WYS" in subdir.split("\\")[5]:
                    sytwys += 1
                elif "ponad" in subdir.split("\\")[5]:
                    duze += 1
                continue

            else:
                with io.open(tyle_zrobili, "a", encoding="utf-8") as tutaj:
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
                    "PRAWNE" in subdir.split("\\")[5]
                    or "EWIDENCJI" in subdir.split("\\")[5]
                    or "MODERNI" in subdir.split("\\")[5]
                ):
                    prawne = 1
                    sytwys = 0
                    duze = 0
                elif "SYT-WYS" in subdir.split("\\")[5]:
                    sytwys = 1
                    prawne = 0
                    duze = 0
                elif "ponad" in subdir.split("\\")[5]:
                    duze = 1
                    prawne = 0
                    sytwys = 0
                continue
        else:
            with io.open(tyle_zrobili, "a", encoding="utf-8") as tutaj:
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
                "PRAWNE" in subdir.split("\\")[5]
                or "EWIDENCJI" in subdir.split("\\")[5]
                or "MODERNI" in subdir.split("\\")[5]
            ):
                prawne = 1
                sytwys = 0
                duze = 0
            elif "SYT-WYS" in subdir.split("\\")[5]:
                sytwys = 1
                prawne = 0
                duze = 0
            elif "ponad" in subdir.split("\\")[5]:
                duze = 1
                prawne = 0
                sytwys = 0
            tego_dnia = 1

ile_ope += tego_dnia
with io.open(tyle_zrobili, "a", encoding="utf-8") as tutaj:
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

with io.open(tyle_zrobili, "r", encoding="utf-8") as tutaj:
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
        str(regex.match(r"^00[0-9][0-9].*[A-Z].*\t(.+$)", i)[1])
        + str(regex.match(r"^00[0-9][0-9].*?([A-Z].*?)\t", i)[1])
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

with io.open(tyle_zrobili, "w", encoding="utf-8") as tutaj:
    tutaj.write("OBREB\tDATA\tILE TEGO DNIA\n")
    for i in natsorted(duble):
        tutaj.write(i + str(duble[i]) + "\n")
    tutaj.write("\n")
    for i in natsorted(kto_ile):
        tutaj.write(i + str(kto_ile[i]) + "\n")
    tutaj.write(
        "\nW "
        + str(len(ile_dni))
        + " dni zrobionych "
        + str(ile_ope)
        + " operatów."
    )

input("\nTHE END. Press something...")
