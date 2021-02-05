import os
import regex

duplicates = {}

for subdir, dirs, files in os.walk(r"D:\_MACIEK_\python_proby\PIOTRKÓW_TRYB_OSNOWA\pedeefy"):
    for file in files:
        if not file.lower().endswith(".pdf"):
            continue
        filename = regex.search("^(.+)-[1-9]\..+", file)[1]
        if filename not in duplicates:
            duplicates[filename] = 1
        else:
            duplicates[filename] += 1
            try:
                os.rename(
                    os.path.join(subdir, file),
                    os.path.join(subdir, f"{filename}-{duplicates[filename]}{os.path.splitext(file)[1]}"),
                )
            except FileExistsError:
                duplicates[filename] += 1
                os.rename(
                    os.path.join(subdir, file),
                    os.path.join(subdir, f"{filename}-{duplicates[filename]}{os.path.splitext(file)[1]}"),
                )

