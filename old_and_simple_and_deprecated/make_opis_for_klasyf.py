import os
import io
import regex

path = input("PATH: ")
count = 1

for subdir, dirs, _ in os.walk(path):
    if any(
        fname.upper().endswith((".JPG", ".JPEG"))
        for fname in os.listdir(subdir)
    ):
        try:
            gmina = regex.match(
                r"[0-9][0-9][0-9][0-9]([0-9][0-9][0-9])", subdir.split("\\")[4]
            )[1]
            obreb = subdir.split("\\")[5]
            if "000" in obreb:
                obreb = regex.match(r"000(.)", obreb)[1]
            else:
                obreb = regex.match(r"00(..)", obreb)[1]
            if "KLASYF" in subdir.split("\\")[6]:
                eska = "S:OPERAT KLASYFIKACYJNY"
            elif "GLEB" in subdir.split("\\")[6]:
                eska = "S:OPERAT GLEBOWO-ROLNICZY"
            with io.open(
                os.path.join(subdir, "opis.txt"), "a", encoding="Windows-1250"
            ) as opis:
                opis.write(
                    "Z:"
                    + gmina
                    + ":"
                    + obreb
                    + "\n"
                    + eska
                    + "\n"
                    + "A:52"
                    + "\n"
                    + "C:3"
                    + "\n"
                )
                print(count)
                count += 1
        except:
            print(subdir)
            continue
