import io
from natsort import natsort_keygen

nkey = natsort_keygen()

nazwy = (
    "decyzja",
    "dokumentacja przejściowa",
    "dziennik pomiarowy",
    "inny",
    "mapa",
    "okładka",
    "opis topograficzny",
    "protokół",
    "spis treści",
    "sprawozdanie techniczne",
    "szkic",
    "wykaz współrzędnych",
)

count = 1

with io.open(
    r"D:\_MACIEK_\python_proby\operdok\baza.txt", "r", encoding="utf-8"
) as baza:
    for line in baza:
        uid = line.split("\t")[0]
        nazwa = line.split("_")[1].split("\n")[0]
        if nazwa.lower() not in nazwy:
            with io.open(
                r"D:\_MACIEK_\python_proby\operdok\bledy.txt",
                "a",
                encoding="utf-8",
            ) as bl:
                bl.write(line)
