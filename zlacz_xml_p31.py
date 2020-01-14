import os
import regex
import io
from natsort import natsorted, natsort_keygen

nkey = natsort_keygen()

print(
    """\nUWAGA!
    W podanej poniżej ścieżce utworzy się plik zlaczone.txt
    Mogą także utworzyć się pliki .txt z błędami.\n\n"""
)
sciezka = input("Podaj ścieżkę: ")

poprzednia = ""
count = 1

with io.open(
    os.path.join(sciezka, "zlaczone.txt"), "a", encoding="utf-8"
) as zlacz:
    zlacz.write(
        "C1\tC2\tC3\tC4\tdataPrzyjecia\tdataWplywu\tnazwa\tpolozenieObszaru\
        \tobreb\tnazwaTworcy\tREGON\tsposobPozyskania\tpostacMaterialu\
        \trodzNoscnika\tdostep\tprzyczynyOgraniczen\ttypMaterialu\
        \tkatArchiwalna\tjezyk\topis\toznMaterialuZasobu\toMZ-Typ\toMZ-Jedn\
        \toMZ-Nr\toMZ-Rok\toMZ-Tom\toMZ-SepJednNr\toMZ-SepNrRok\tdokumentWyl\
        \tdataWyl\tdataArchLubBrak\tcel\tcelArchiwalny\tDzialkaPrzed\
        \tDzialkaPo\topis2\tidZgloszenia\tid-Jedn\tid-Nr\tid-Rok\tid-Etap\
        \tid-SepJednNr\tid-SepNrRok\tid-dataZgloszenia\tpolozenieObszaru\
        \tobreb\tnazwa\tREGON\timie\tnazwisko\tnumer_uprawnien\tcel\
        \tcelArchiwalny\trodzaj\n"
    )

for subdir, dirs, files in os.walk(sciezka):
    dirs.sort(key=nkey)
    if not any(fname.upper().endswith(".XML") for fname in os.listdir(subdir)):
        with io.open(
            os.path.join(sciezka, "brak_xml_w_folderze.txt"),
            "a",
            encoding="utf-8",
        ) as brak:
            brak.write(subdir + "\n")
        continue

    for file in natsorted(files):
        if file.upper().endswith(".XML"):
            print(count)
            count += 1
            xml = os.path.join(subdir, file)
            try:
                with io.open(xml, "r", encoding="utf-8") as oxml:
                    for line in oxml:
                        if regex.match("(^.+?>).*$", line)[1] == poprzednia:
                            continue
                        if " /" in line or regex.match(".+>.*<.+", line):
                            if "DzialkaPrzed" in line or "DzialkaPo" in line:
                                print("jest" + xml)
                                continue
                            if regex.match("^.+>.+<.+", line):
                                wartosc = regex.match("^.+>(.+)<.+", line)[1]
                            else:
                                wartosc = ""
                            with io.open(
                                os.path.join(sciezka, "zlaczone.txt"),
                                "a",
                                encoding="utf-8",
                            ) as zlacz:
                                zlacz.write(wartosc + "\t")
                        poprzednia = regex.match("(^.+?>).*$", line)[1]
                with io.open(
                    os.path.join(sciezka, "zlaczone.txt"),
                    "a",
                    encoding="utf-8",
                ) as zlacz:
                    zlacz.write(xml + "\n")

            except:
                with io.open(
                    os.path.join(
                        sciezka, "prawdopodobnie_zle_kodowanie_NIE_OTWARTO.txt"
                    ),
                    "a",
                    encoding="utf-8",
                ) as zle:
                    zle.write(xml + "\n")

input("KONIEC.")
