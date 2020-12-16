import os
import shutil

import regex
from natsort import natsorted

names_list = []
changed_files_list = []
path = r"Y:\PIOTRKÓW_TRYB_OSNOWA\DANE_TEREN\07.12.2020\Damian\Foteczki"
names_file_dest = os.path.join(path, "names.txt")
missing_names = os.path.join(path, "missing_names.txt")
photos_dest = os.path.join(path, "org")
new_photos_dest = os.path.join(path, "zmienione")
changed_names = os.path.join(new_photos_dest, "jak_zmienione_nazwy.txt")


def create_dest_folder():
    if os.path.exists(new_photos_dest):
        shutil.rmtree(new_photos_dest)
    os.mkdir(new_photos_dest)
    if os.path.exists(missing_names):
        os.remove(missing_names)


def read_names_list_from_file():
    with open(names_file_dest, "r", encoding="utf-8") as new_names:
        for line in new_names:
            if "\t" in line:
                old_name, new_name = line.strip().split("\t")
                names_list.append([old_name, new_name])


def switch_rome_to_arab(parts_list):
    for item in parts_list:
        if any(i == item.lower() for i in switcher):
            place_in_list = parts_list.index(item)
            parts_list[place_in_list] = switcher[item.lower()]


def join_parts_in_name(parts_list):
    return "-".join(str(x) for x in parts_list).lower() + "-"


def write_to_log(log_file_path, message):
    with open(log_file_path, "a", encoding="utf-8",) as log_file:
        log_file.write(message)


def set_document_number(next_number):
    if name[0] == previous_name:
        next_number += 1
    else:
        next_number = 1
    return next_number


def copy_file():
    try:
        shutil.copy2(old_file, new_file)
    except:
        raise


switcher = {
    "i": 1,
    "ii": 2,
    "iii": 3,
    "iv": 4,
    "v": 5,
}

create_dest_folder()
read_names_list_from_file()

for subdir, _, files in os.walk(photos_dest):
    how_much_left = len(os.listdir(subdir)) - 1
    previous_name = ""
    next_number = 1
    for file in natsorted(files):
        for name in names_list:
            all_name_parts = regex.split(r"\.|_|-", name[0])
            all_file_parts = regex.split(r"\.|_|-", file.lower())
            switch_rome_to_arab(all_name_parts)
            switch_rome_to_arab(all_file_parts)
            name_joined = join_parts_in_name(all_name_parts)
            filename_joined = join_parts_in_name(all_file_parts)
            if filename_joined.startswith(name_joined):
                print(how_much_left)
                how_much_left -= 1
                next_number = set_document_number(next_number)
                new_filename = f"{name[1]}-{next_number}{os.path.splitext(file)[1]}"
                old_file = os.path.join(subdir, file)
                new_file = os.path.join(new_photos_dest, new_filename)
                write_to_log(
                    changed_names, f"{file}\t{name[0]}\t{new_filename}\n",
                )
                if os.path.exists(new_file):
                    raise FileExistsError(f"{file}\t{name}")
                copy_file()
                previous_name = name[0]
                changed_files_list.append(file)
                break
    for file in natsorted(files):
        if file not in changed_files_list and file.lower().endswith((".jpg", ".jpeg")):
            write_to_log(missing_names, f"{file}\t\n")
