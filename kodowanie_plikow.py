import os
import chardet
import io
from chardet.universaldetector import UniversalDetector
from natsort import natsort_keygen

nkey = natsort_keygen()

count = 1

# sprawdzanie kodowania plikow - 1 metoda
for subdir, dirs, _ in os.walk(r"P:\cyfryzacja_powiat_wloclawski\ETAP_3"):
    dirs.sort(key=nkey)
    if os.path.exists(os.path.join(subdir, "opis.txt")):
        print(count)
        count += 1
        opis = os.path.join(subdir, "opis.txt")
        rawdata = open(opis, "rb").read()
        result = chardet.detect(rawdata)
        # print(result)
        charenc = result["encoding"]
        with open(
            r"D:\_MACIEK_\cyfryzacja_wloclawski\G_brzesc\kodowania_plikow.txt",
            "a",
        ) as kodowanie:
            kodowanie.write(opis + "\t" + charenc + "\n")


# sprawdzanie kodowania plikow - 2 metoda
detector = UniversalDetector()
for subdir, dirs, _ in os.walk(r"P:\cyfryzacja_powiat_wloclawski\ETAP_3"):
    dirs.sort(key=nkey)
    if os.path.exists(os.path.join(subdir, "opis.txt")):
        print(count)
        count += 1
        opis = os.path.join(subdir, "opis.txt")
        detector.reset()
        with open(opis, "rb") as sprawdz:
            for line in sprawdz:
                detector.feed(line)
                if detector.done:
                    break
        detector.close()
        if "utf-8" in str(detector.result):
            with open(
                r"D:\_MACIEK_\cyfryzacja_wloclawski\G_brzesc\kodowania_plikow.txt",  # noqa
                "a",
            ) as kodowanie:
                kodowanie.write(opis + "\t" + str(detector.result) + "\n")


# zapis plikow z nowym kodowaniem
for subdir, dirs, _ in os.walk(
    r"D:\_MACIEK_\cyfryzacja_wloclawski\G_brzesc\utf-8"
):
    dirs.sort(key=nkey)
    if os.path.exists(os.path.join(subdir, "opis.txt")):
        stad = os.path.join(subdir, "opis.txt")
        with io.open(stad, "r", encoding="utf-8") as pobierz:
            tresc = pobierz.read()
        with io.open(
            stad + ".new", "w", encoding="ascii", errors="ignore"
        ) as zapisz:
            zapisz.write(tresc)
