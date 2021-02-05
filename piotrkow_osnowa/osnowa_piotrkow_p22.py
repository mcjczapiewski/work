import os
import shutil

import regex
from natsort import natsorted


def restartable():
    names_list = []
    changed_files_list = []
    path = input("PATH:\n> ")
    names_file_dest = os.path.join(path, "names.txt")
    missing_names = os.path.join(path, "missing_names.txt")
    photos_dest = os.path.join(path, "org")
    found_folder = os.path.join(photos_dest, "znalezione")
    new_photos_dest = os.path.join(path, "zmienione")
    changed_names = os.path.join(new_photos_dest, "jak_zmienione_nazwy.txt")

    def move_back_from_found_folder():
        if os.listdir(found_folder):
            for _, _, files in os.walk(found_folder):
                for file in files:
                    shutil.move(os.path.join(found_folder, file), photos_dest)

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
                    old_name, new_name = regex.split(r"\t{1,}", line.strip())
                    names_list.append([old_name, new_name])

    def change_name_structure():
        all_name_parts = split_name_to_parts(name[0])
        switch_rome_to_arab(all_name_parts)
        name_joined = join_parts_in_name(all_name_parts)
        names_list[names_list.index(name)][0] = name_joined

    def split_name_to_parts(name_to_split):
        return regex.split(r"\.|_|-| |,", name_to_split.lower())

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
        if name[0].lower() == previous_name.lower():
            next_number += 1
        else:
            next_number = 1
            if name_from_list_to_delete in names_list:
                names_list.remove(name_from_list_to_delete)
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

    if os.path.exists(found_folder):
        move_back_from_found_folder()
    create_dest_folder()
    read_names_list_from_file()

    for _, _, files in os.walk(photos_dest):
        how_much_left = len(os.listdir(photos_dest)) - 1
        previous_name = ""
        name_from_list_to_delete = ""
        next_number = 1
        for name in names_list:
            change_name_structure()
        for file in natsorted(files):
            all_file_parts = split_name_to_parts(file)
            switch_rome_to_arab(all_file_parts)
            filename_joined = join_parts_in_name(all_file_parts)
            for name in names_list:
                if filename_joined.startswith(name[0]):
                    print(how_much_left)
                    how_much_left -= 1
                    next_number = set_document_number(next_number)
                    new_filename = (
                        f"{name[1]}-{next_number}{os.path.splitext(file)[1]}"
                    )
                    old_file = os.path.join(photos_dest, file)
                    new_file = os.path.join(new_photos_dest, new_filename)
                    write_to_log(
                        changed_names, f"{file}\t{name[0]}\t{new_filename}\n",
                    )
                    if os.path.exists(new_file):
                        print((f"FileExistsError {file}\t{name}"))
                        restartable()
                    copy_file()
                    previous_name = name[0]
                    name_from_list_to_delete = name
                    changed_files_list.append(file)
                    break
        for file in natsorted(files):
            if file not in changed_files_list and file.lower().endswith(
                (".jpg", ".jpeg")
            ):
                write_to_log(missing_names, f"{file}\t\n")
            else:
                old_file = os.path.join(photos_dest, file)
                found_file = os.path.join(found_folder, file)
                if not os.path.exists(found_folder):
                    os.mkdir(found_folder)
                shutil.move(old_file, found_file)
        break


restartable()
