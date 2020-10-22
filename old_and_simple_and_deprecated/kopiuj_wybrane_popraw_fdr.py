import os
import shutil

jest = ["00_000_okładka.JPG", "01_001_spis treści.JPG", "03_003_inny.JPG"]

for subdir, dirs, files in os.walk(
    r"F:\operaty_do_poprawy\N\045\P.0418.2010.1511"
):
    for file in files:
        if file not in jest:
            shutil.copy2(os.path.join(subdir, file), r"F:\_old\SKAN\1967.33")
