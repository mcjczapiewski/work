import os
import regex

for subdir, dirs, files in os.walk(r"D:\_MACIEK_\python_proby\PIOTRKÓW_TRYB_OSNOWA"):
    for file in files:
        filename = regex.sub(r"\.", r"___", os.path.splitext(file)[0])
        os.rename(os.path.join(subdir, file), os.path.join(subdir, filename + os.path.splitext(file)[1]))
