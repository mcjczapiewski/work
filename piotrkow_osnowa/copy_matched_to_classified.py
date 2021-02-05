import os
import shutil

with open(r"D:\_MACIEK_\python_proby\zasilenie_mockup\stat.txt", "r", encoding="utf-8") as o:
    stat = []
    for line in o:
        stat.append(line.strip())

byly = {}
exists = []
for subdir, dirs, files in os.walk(r"Y:\PIOTRKÓW_TRYB_OSNOWA\DANE_TEREN"):
    for file in files:
        if not file.lower().endswith((".jpg", ".jpeg")):
            continue
        for i in stat:
            if i.split("\t")[0] in file:
                # if i not in byly:
                #     byly[i] = 1
                # else:
                #     byly[i] += 1
                # old_file = os.path.join(subdir, file)
                # new_file = os.path.join(
                #     r"D:\_MACIEK_\python_proby\zasilenie_mockup\osn",
                #     i.split("\t")[1],
                #     i.split("\t")[0] + str(byly[i]) + os.path.splitext(file)[1],
                # )
                old_file = os.path.join(subdir, file)
                new_file = os.path.join(r"D:\_MACIEK_\python_proby\zasilenie_mockup\photos", file)
                try:
                    shutil.copy2(old_file, new_file)
                except FileExistsError:
                    exists.append(os.path.join(subdir, file))
                except:
                    print(os.path.join(subdir, file))
print(exists)
