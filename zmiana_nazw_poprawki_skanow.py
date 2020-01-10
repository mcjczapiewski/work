from natsort import natsorted
import regex
import os

jeden = r'P:\cyfryzacja_powiat_wloclawski\ETAP_3\wloclawek_gmina\na_zewnatrz\0028_\
    zlecone_M\ponad_10\JEDNOSTKOWE OPERATY SYT-WYS\P.0418.1993.552'
dwa = r'P:\cyfryzacja_powiat_wloclawski\ETAP_3\do_nazwania\I_PARTIA_88298_plikow\POPRAWKI\0418\
    132\0028\JEDNOSTKOWE OPERATY SYT-WYS\P.0418.1993.552'
for subdir, dirs, files in os.walk(jeden):
    for file in natsorted(files):
        if file.upper().endswith('.JPG'):
            ori = file
            for subdir, dirs, files in os.walk(dwa):
                for file in natsorted(files):
                    if not regex.match('^.+_.+_.+', file) and file.upper().endswith('.JPG'):
                        os.rename(os.path.join(subdir, file), os.path.join(subdir, ori))
                        break
                break
