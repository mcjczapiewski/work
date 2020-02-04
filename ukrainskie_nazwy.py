import os
import regex

for subdir, dirs, files in os.walk(
    r"I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614\ZADANIE 2\KRUSZWICA"
):
    for i in os.path.basename(subdir.lower()):
        if not regex.match(r"[a-zA-Z0-9]| |-|\.|_|\(|\)|ę|ó|ą|ś|ł|ż|ź|ć|ń", i):
            print(subdir)
            break
    for file in files:
        if file == "Thumbs.db":
            continue
        for i in file.lower():
            if not regex.match(
                r"[a-z0-9]| |-|\.|_|\(|\)|ę|ó|ą|ś|ł|ż|ź|ć|ń", i
            ) or not file.lower().endswith((".wkt", ".xml", ".pdf", ".txt")):
                print(os.path.join(subdir, file))
                break
