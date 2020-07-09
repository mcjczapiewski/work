import os
import shutil

count = 1

for subdir, dirs, _ in os.walk(r'D:\_MACIEK_\python_proby\20200528'):
    merge = os.path.join(subdir, os.path.basename(subdir), "merge")
    if os.path.exists(merge):
        print(count)
        count += 1
        main_folder = subdir
        for _, _, files in os.walk(merge):
            for file in files:
                if file.lower().endswith(".jpg"):
                    from_here = os.path.join(merge, file)
                    shutil.move(from_here, main_folder)
        sub_folder = os.path.join(main_folder, os.path.basename(main_folder))
        if os.path.exists(sub_folder):
            shutil.rmtree(sub_folder)
