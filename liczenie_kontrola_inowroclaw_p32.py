import shutil
import datetime
import msvcrt
import os
import regex
from natsort import natsort_keygen, natsorted


def count_if_file_named(path):
    again = "t"
    while again == "t":
        today = datetime.datetime.now().date()
        count_all = count_today = 0
        current_time = datetime.datetime.now().time()
        print(f"\n{current_time.hour}:{str(current_time.minute).zfill(2)}")
        for subdir, dirs, files in os.walk(path):
            if os.path.basename(subdir) in os.listdir(subdir):
                folder_creation_time = datetime.date.fromtimestamp(
                    os.path.getctime(
                        os.path.join(subdir, os.path.basename(subdir))
                    )
                )
                for file in files:
                    count_all += 1
                    if folder_creation_time == today:
                        count_today += 1

        print(f"ZROBIONE OGÓŁEM: {count_all}")
        print(f"ZROBIONE DZISIAJ: {count_today}")
        print("Powtórzyć? t/n\n> ", end="")
        again = msvcrt.getwche().lower()
        print()


def check_if_all_named(path):
    again = "t"
    print()
    while again == "t":
        count = pdfs_to_name = 0
        left_to_name = []
        for subdir, dirs, _ in os.walk(path):
            dirs.sort(key=natsort_keygen())
            if regex.match(r"^.+040701..\.....", subdir):
                get_steps = regex.match(r"^.+040701..\.....", subdir)[0]
            else:
                continue
            if regex.search(r"040701..\.....$", get_steps):
                steps_inside_path = len(get_steps.split("\\")) + 1
            if len(subdir.split("\\")) == steps_inside_path:
                up_to_merge = os.path.join(
                    subdir, os.path.basename(subdir), "merge"
                )
                is_there_basename = os.path.join(
                    subdir, os.path.basename(subdir)
                )
                if os.path.exists(up_to_merge):
                    if not any(
                        fname.upper().endswith(".PDF")
                        for fname in os.listdir(up_to_merge)
                    ):
                        if not any(
                            fname.upper().endswith(".PDF")
                            for fname in os.listdir(is_there_basename)
                        ):
                            pdfs_to_name, count, left_to_name = add_to_counter(
                                count, pdfs_to_name, subdir, left_to_name
                            )
                elif os.path.exists(is_there_basename):
                    if not any(
                        fname.upper().endswith(".PDF")
                        for fname in os.listdir(is_there_basename)
                    ):
                        pdfs_to_name, count, left_to_name = add_to_counter(
                            count, pdfs_to_name, subdir, left_to_name
                        )
                else:
                    pdfs_to_name, count, left_to_name = add_to_counter(
                        count, pdfs_to_name, subdir, left_to_name
                    )

        print(f"Pozostało {count} operatów, {pdfs_to_name} pdfów do nazwania.")
        if count or pdfs_to_name != 0:
            print("Pokazać listę folderów? t/n\n> ", end="")
            show_folders = msvcrt.getwche().lower()
            print()
            if show_folders == "t":
                for name in natsorted(left_to_name):
                    print(name)
        print("\nPowtórzyć? t/n\n> ", end="")
        again = msvcrt.getwche().lower()
        print()


def add_to_counter(count, pdfs_to_name, subdir, left_to_name):
    pdfs_to_name += len(os.listdir(subdir))
    left_to_name.append(subdir)
    count += 1
    return pdfs_to_name, count, left_to_name


def check_for_map_or_sketch(path):
    possible_maps = ["'-M-PROJ-'", "'-M-WPROJ-'", "'-M-UZ-'", "'-M-WYN-'"]
    sketch_coords = ["'-SZK-POL-'", "'-W-WSP-'"]
    again = "t"
    print()
    while again == "t":
        print_results = []
        for subdir, dirs, _ in os.walk(path):
            dirs.sort(key=natsort_keygen())
            if any(
                regex.search(r"-.+-", fname) for fname in os.listdir(subdir)
            ):
                operat = os.path.basename(subdir)
                if "merge" in subdir:
                    operat = os.path.basename(os.path.dirname(subdir))
                for item in sketch_coords:
                    if not any(
                        item.strip("'") in fname.upper()
                        for fname in os.listdir(subdir)
                    ):
                        print_results.append(f"{operat} nie zawiera {item}.")
                if not any(
                    possibility.strip("'") in fname
                    for possibility in possible_maps
                    for fname in os.listdir(subdir)
                ):
                    missing_map = ", ".join(maps for maps in possible_maps)
                    print_results.append(
                        f"{operat} nie zawiera żadnej z map: {missing_map}."
                    )
        for result in sorted(set(print_results)):
            print(result)
        print("Powtórzyć? t/n\n> ", end="")
        again = msvcrt.getwche().lower()
        print("\n")


def move_up_nested_merge(path):
    to_be_moved = []
    for subdir, dirs, _ in os.walk(path):
        dirs.sort(key=natsort_keygen())
        current_dir = subdir
        if regex.match(r"^.+040701..\.....", current_dir):
            get_steps = regex.match(r"^.+040701..\.....", current_dir)[0]
        else:
            continue
        if regex.search(r"040701..\.....$", get_steps):
            steps_inside_path = len(get_steps.split("\\")) + 1
        if len(current_dir.split("\\")) == steps_inside_path:
            operat = os.path.basename(current_dir)
            up_to_merge = os.path.join(current_dir, operat, operat, "merge",)
            is_there_basename = os.path.join(current_dir, operat, operat,)
            if os.path.exists(up_to_merge):
                merge = os.path.join(operat, "merge")
                to_be_moved.append(
                    f"{current_dir}--__--{merge}--__--{up_to_merge}"
                )
            if os.path.exists(is_there_basename):
                if len(os.listdir(is_there_basename)) > 1:
                    to_be_moved.append(
                        f"{current_dir}--__--{operat}--__--{is_there_basename}"
                    )
    if to_be_moved:
        end_script = ""
        while end_script != "0":
            print(
                """
Co chcesz zrobić?
    (1)  Podejrzeć listę zagnieżdżonych katalogów
    (2)  Wyciągnąć zagnieżdżone katalogi
    (0)  Wróć do menu głównego
    """
            )
            end_script = msvcrt.getwche()
            print()
            if end_script == "1":
                print_nested_catalogues(to_be_moved)
            elif end_script == "2":
                move_files_up(to_be_moved)
                print(" --- PRZENIESIONE --- ")
                end_script = "0"
    else:
        print(" --- BRAK ZAGNIEŻDŻEŃ --- ")


def print_nested_catalogues(to_be_moved):
    for line in to_be_moved:
        nested_folder = line.split("--__--")[-1]
        print(nested_folder)


def move_files_up(to_be_moved):
    for line in to_be_moved:
        current_dir, folder_name, nested_folder = line.split("--__--")
        destination = os.path.join(current_dir, folder_name)
        if not os.path.exists(destination):
            os.mkdir(destination)
        for _, _, files in os.walk(nested_folder):
            for file in files:
                shutil.move(
                    os.path.join(nested_folder, file), destination,
                )
        remove_empty_subdir(current_dir)


def remove_empty_subdir(current_dir):
    for subdir, dirs, _ in os.walk(current_dir):
        if not os.listdir(subdir):
            os.rmdir(subdir)
            remove_empty_subdir(current_dir)


def fix_numbers(path):
    doc_numbers_to_change = []
    page_numbers_to_change = []
    for subdir, dirs, files in os.walk(path):
        dirs.sort(key=natsort_keygen())
        if not any(
            regex.search(r"-.+-", fname) for fname in os.listdir(subdir)
        ):
            continue
        operat = os.path.basename(subdir)
        if "merge" in subdir:
            operat = os.path.basename(os.path.dirname(subdir))
        doc_number = 1
        for file in natsorted(files):
            if regex.search(r"-.+-.+.PDF", file.upper()):
                tail = file.split(operat)[1]
                file_doc_number = tail.strip("_").split("-", 1)[0]
                if int(file_doc_number) != doc_number:
                    doc_numbers_to_change.append(
                        f"{subdir}\t{file} --> \
_--_{operat}_{doc_number}-{tail.strip('_').split('-', 1)[1]}"
                    )
                doc_number += 1
    if doc_numbers_to_change:
        make_changes = changes("dokumentów", doc_numbers_to_change)

    for subdir, dirs, files in os.walk(path):
        dirs.sort(key=natsort_keygen())
        if not any(
            regex.search(r"-.+-", fname) for fname in os.listdir(subdir)
        ):
            continue
        operat = os.path.basename(subdir)
        if "merge" in subdir:
            operat = os.path.basename(os.path.dirname(subdir))
        names_seen = {}
        for file in natsorted(files):
            if regex.search(r"-.+-.+.PDF", file.upper()):
                tail = file.split(operat)[1]
                file_type = regex.search(r"[A-Z].*[A-Z]", tail.split(".")[0])[
                    0
                ]
                file_page_number = tail.split(".")[0].split("-")[-1]
                if file_type not in names_seen:
                    names_seen[file_type] = 1
                else:
                    names_seen[file_type] += 1
                if file_page_number != str(names_seen[file_type]).zfill(3):
                    page_numbers_to_change.append(
                        f"{subdir}\t{file} --> \
_--_{operat}{tail.split(file_page_number)[0]}{str(names_seen[file_type]).zfill(3)}\
{tail.split(file_page_number)[1]}"
                    )
    if page_numbers_to_change:
        make_changes = changes("stron", page_numbers_to_change)

    if not doc_numbers_to_change and not page_numbers_to_change:
        print(" --- BRAK BŁĘDÓW --- ")
    elif make_changes == "t":
        print(" --- POPRAWIONO --- ")
    elif make_changes == "n":
        print(" --- POZOSTAWIONO W AKTUALNYM STANIE --- ")


def changes(change_type, numbers_to_change):
    print(
        f"Chcesz zobaczyć zmiany w numerach {change_type}, zanim je zrobię? \
t/n\n> ",
        end="",
    )
    print_changes = msvcrt.getwche().lower()
    print()
    if print_changes == "t":
        for change in natsorted(numbers_to_change):
            names = change.split("\t")[1]
            old_name, new_name = names.split("_--_")
            print(f"{old_name}{new_name}")
    print("\nDokonać zmian? t/n\n> ", end="")
    make_changes = msvcrt.getwche().lower()
    print()
    if make_changes == "t":
        delete_double_underscore = []
        for change in natsorted(numbers_to_change):
            file_path = change.split("\t")[0]
            old_name, new_name = change.split("\t")[1].split(" --> ")
            os.rename(
                os.path.join(file_path, old_name),
                os.path.join(file_path, new_name),
            )
            delete_double_underscore.append(os.path.join(file_path, new_name))
        for underscore in delete_double_underscore:
            os.rename(
                underscore,
                underscore.split("_--_")[0] + underscore.split("_--_")[1],
            )
    return make_changes


def no_missing_names(path):
    no_errors = True
    for subdir, dirs, files in os.walk(path):
        operat = os.path.basename(subdir)
        if subdir.endswith(
            os.path.join(os.path.basename(subdir), os.path.basename(subdir))
        ):
            names_of_files = [
                regex.search(r"-([A-Z].*[A-Z])", x)[1]
                for x in os.listdir(subdir)
                if x.upper().endswith(".PDF")
            ]
            names_of_files = set(names_of_files)
            merge_folder = os.path.join(subdir, "merge")
            if os.path.exists(merge_folder):
                names_of_merged = [
                    regex.search(r"-([A-Z].*[A-Z])", x)[1]
                    for x in os.listdir(merge_folder)
                    if x.upper().endswith(".PDF")
                ]
                names_of_merged = set(names_of_merged)
                for name in names_of_files:
                    if name not in names_of_merged:
                        print(fr"W {operat}\merge brak '{name}'")
                        no_errors = False
                for name in names_of_merged:
                    if name not in names_of_files:
                        print(f"W {operat} brak '{name}'")
                        no_errors = False
    if no_errors is True:
        print(" --- BRAK BŁĘDÓW --- ")


def main():
    # path = r"D:\WPG\inowroclawski\040701_1.0006"
    path = input("\nWklej ścieżkę:\n> ")
    end_script = ""
    while end_script != "0":
        print("\nWybierz jedną z opcji:")
        print(
            """
    (1)  Liczenie nazwanych plików
    (2)  Sprawdzanie czy wszystko zostało nazwane lub ile pozostało do nazwania
    (3)  Sprawdź czy w każdym operacie jest mapa, szkic i wykaz
    (4)  Zagnieżdżone katalogi
    (5)  Popraw numerację dokumentów i stron
    (6)  Czy w merge są wszytkie nazwy plików
    (0)  Wyjście z programu
    """
        )
        end_script = msvcrt.getwche()
        print()
        if end_script == "1":
            count_if_file_named(path)
        elif end_script == "2":
            check_if_all_named(path)
        elif end_script == "3":
            check_for_map_or_sketch(path)
        elif end_script == "4":
            move_up_nested_merge(path)
        elif end_script == "5":
            fix_numbers(path)
        elif end_script == "6":
            no_missing_names(path)
    input("\nWciśnij ENTER lub zamknij okno ręcznie...\n> ")


if __name__ == "__main__":
    main()
