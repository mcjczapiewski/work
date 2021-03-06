import os
import regex
import io
from natsort import natsort_keygen

nkey = natsort_keygen()

count = 1
asor = cechy = set()

with io.open(
    r"D:\_MACIEK_\cyfryzacja_wloclawski\asortym.txt", "r", encoding="utf-8"
) as asort:
    for line in asort:
        bb = regex.split(",|;", line)
        for i in bb:
            asor.add(i)

with io.open(
    r"D:\_MACIEK_\cyfryzacja_wloclawski\cechy.txt", "r", encoding="utf-8"
) as cech:
    for line in cech:
        bb = regex.split(",|;", line)
        for i in bb:
            cechy.add(i)

opisy = r"P:\cyfryzacja_powiat_wloclawski"

for subdir, dirs, _ in os.walk(opisy):
    dirs.sort(key=nkey)
    if (
        not any(fname.endswith(".txt") for fname in os.listdir(subdir))
        or "Fabianki" in subdir
        or "BDOT500" in subdir
    ):
        continue
    opis = os.path.join(subdir, "opis.txt")
    if os.path.exists(opis):
        print(str(count) + "\t" + opis)
        count += 1
        try:
            with io.open(opis, "r", encoding="utf-8") as op:
                for line in op:
                    if line.startswith("C:"):
                        bb = regex.sub(r"^C:(.+?)(\n|$)", r"\g<1>", line)
                        bb = regex.split(",", bb)
                        for i in bb:
                            if i not in cechy:
                                with io.open(
                                    r"D:\_MACIEK_\python_proby\bledy_cechy.txt",  # noqa
                                    "a",
                                    encoding="utf-8",
                                ) as bl:
                                    bl.write(subdir + "\n")
                    elif line.startswith("A:"):
                        bb = regex.sub(r"^A:(.+?)(\n|$)", r"\g<1>", line)
                        bb = regex.split(",", bb)
                        for i in bb:
                            if i not in asor:
                                with io.open(
                                    r"D:\_MACIEK_\python_proby\bledy_asort.txt",  # noqa
                                    "a",
                                    encoding="utf-8",
                                ) as bl:
                                    bl.write(subdir + "\n")
        except UnicodeDecodeError:
            with open(opis, "r") as op:
                for line in op:
                    if line.startswith("C:"):
                        bb = regex.sub(r"^C:(.+?)(\n|$)", r"\g<1>", line)
                        bb = regex.split(",", bb)
                        for i in bb:
                            if i not in cechy:
                                with io.open(
                                    r"D:\_MACIEK_\python_proby\bledy_cechy.txt",  # noqa
                                    "a",
                                    encoding="utf-8",
                                ) as bl:
                                    bl.write(subdir + "\n")
                    elif line.startswith("A:"):
                        bb = regex.sub(r"^A:(.+?)(\n|$)", r"\g<1>", line)
                        bb = regex.split(",", bb)
                        for i in bb:
                            if i not in asor:
                                with io.open(
                                    r"D:\_MACIEK_\python_proby\bledy_asort.txt",  # noqa
                                    "a",
                                    encoding="utf-8",
                                ) as bl:
                                    bl.write(subdir + "\n")
        except:
            with io.open(
                r"D:\_MACIEK_\python_proby\bledy_otwarcia.txt",
                "a",
                encoding="utf-8",
            ) as bl:
                bl.write(subdir + "\n")
print("KONIEC")
