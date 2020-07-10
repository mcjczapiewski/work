import os
import regex

for subdir, dirs, files in os.walk(
    r"P:\cyfryzacja_powiat_inowroclawski\SKANY_III\20200527\040707_5\prawne"
):
    numbers_count = {}
    if "merge" not in os.listdir(subdir):
        continue
    for file in files:
        if file.upper().endswith(".PDF"):
            doc_number = regex.search("_(.+?)-[A-Z]", file)[1]
            if doc_number not in numbers_count:
                numbers_count[doc_number] = 1
            else:
                numbers_count[doc_number] += 1
    for key in numbers_count:
        if numbers_count[key] > 1:
            print(subdir)
            break
