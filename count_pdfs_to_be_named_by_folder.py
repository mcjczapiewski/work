import os
import regex

path = r"P:\cyfryzacja_powiat_inowroclawski\SKANY_III\20200528\040707_5"  # noqa

files_by_folder = {}
count_all = 0

for subdir, dirs, files in os.walk(path):
    if not any(
        regex.search("-.+-", fname) for fname in os.listdir(subdir)
    ) and any(fname.upper().endswith(".PDF") for fname in os.listdir(subdir)):
        count = sum(
            1 for x in os.listdir(subdir) if x.upper().endswith(".PDF")
        )
        count_all += count
        current_folder = subdir.split("\\")[6]
        if current_folder not in files_by_folder:
            files_by_folder[current_folder] = count
        else:
            files_by_folder[current_folder] += count
for key in sorted(files_by_folder):
    print(f"{key}: {files_by_folder[key]}")
print(count_all)
