import os
import regex

_path = input("Enter the path to files: ")
_cechy = _asor = []
count = 1

with open(r"D:\_MACIEK_\python_proby\op_cechy.txt", "r") as cechy:
    for line in cechy:
        _cechy.append(line.split("\n")[0])
with open(r"D:\_MACIEK_\python_proby\op_asor.txt", "r") as asort:
    for line in asort:
        _asor.append(line.split("\n")[0])

for subdir, dirs, _ in os.walk(_path):
    if (
        not any(fname.upper().endswith(".JPG") for fname in os.listdir(subdir))
        or "BDOT500" in subdir
        or "Fabianki" in subdir
        or "NIE_RUSZAC" in subdir
        or "DOKUMENT" in subdir
    ):
        continue
    nrope = os.path.basename(subdir)
    if regex.match(r"^.+\..+\..+\..+", nrope):
        if "_" in nrope:
            nrope = nrope.split("_")[0]
        elif ";" in nrope:
            nrope = nrope.split(";")[0]
        print(count)
        count += 1
        _ma_ceche = _ma_asor = "BRAK"
        if nrope in _cechy:
            _ma_ceche = "JEST"
        if nrope in _asor:
            _ma_asor = "JEST"

        with open(r"D:\_MACIEK_\python_proby\jest_brak.txt", "a") as zapisz:
            zapisz.write(nrope + "\t" + _ma_asor + "\t" + _ma_ceche + "\n")
