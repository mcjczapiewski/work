import os
from natsort import natsort_keygen

nkey = natsort_keygen()

sciezka = r"P:\cyfryzacja_powiat_wloclawski\ETAP_3\do_nazwania\I_PARTIA_88298_plikow\nazwane_dysk\0418115"  # noqa
zrobione = zlecone = ilosc = 0

for subdir, dirs, _ in os.walk(sciezka):
    dirs.sort(key=nkey)
    if (
        not any(fname.upper().endswith(".JPG") for fname in os.listdir(subdir))
        or "DOKUMENTACJA" in subdir
        and "na_zewnatrz" in subdir
    ):
        continue
    ilosc += 1
    if "zlecone" in subdir.lower():
        zlecone += 1
    if "zrobione" in subdir.lower():
        zrobione += 1

    print(str(zrobione) + "\t" + str(zlecone) + "\t" + str(ilosc))
