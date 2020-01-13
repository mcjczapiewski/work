import os
import regex

sciezka = input('Scieżka: ')
count = 1

for subdir, dirs, files in os.walk(sciezka):
    for file in files:
        if (file.upper().endswith(('.JPG', '.JPEG')) and not
                regex.match('^.+_.+_.+', file)):
            print(count)
            count += 1
