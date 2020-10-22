import datetime
import io
import os
import shutil

import chardet
import regex
from chardet.universaldetector import UniversalDetector
from natsort import natsort_keygen, natsorted

nkey = natsort_keygen()


def execute_proper_function(function_number, path, error_file_path):
    if function_number == 1:
        move_wkt_files_to_their_folders(path, error_file_path)
    elif function_number == 2:
        add_precinct_name_to_folder(path)
    elif function_number == 3:
        move_wkt_for_files_to_main_wkt(path, error_file_path)
    elif function_number == 4:
        delete_parenthesis_if_not_multipolygon(path)
    elif function_number == 5:
        match_wkt_folders_to_operat_folder(path, error_file_path)
    elif function_number == 6:
        check_if_all_operat_from_list_matched(path, error_file_path)
    elif function_number == 7:
        find_duplicate_lines_in_cdc_file(path, error_file_path)
    elif function_number == 8:
        remove_from_cdc_lines_moved_to_duplicated(path, error_file_path)
    elif function_number == 9:
        copy_wkt_to_corresponding_operat_folder(path, error_file_path)
    elif function_number == 10:
        delete_successfuly_moved_files(path, error_file_path)
    elif function_number == 11:
        cleanup_more_than_one_fit(path, error_file_path)
    elif function_number == 12:
        check_for_pdf_equivalent_for_wkt(path, error_file_path)
    elif function_number == 13:
        check_error_wkt_creation_date(path, error_file_path)
    elif function_number == 14:
        check_wkt_structure(path, error_file_path)
    elif function_number == 15:
        merge_wkt_with_wrong_structure(path, error_file_path)
    elif function_number == 16:
        check_file_encoding_chardet(path, error_file_path)
    elif function_number == 17:
        check_file_encoding_universal_detector(path, error_file_path)
    elif function_number == 18:
        save_files_with_utf_8(path)
    elif function_number == 19:
        copy_wkt_files_to_sketches(path)
    elif function_number == 20:
        copy_wkt_files_to_required_documents(path, error_file_path)
    elif function_number == 21:
        check_for_wkt_to_wrong_files(path, error_file_path)
    elif function_number == 22:
        check_wkt_files_for_required_documents(path, error_file_path)
    elif function_number == 23:
        check_for_any_wkt_if_main_not_exists(path, error_file_path)
    elif function_number == 24:
        check_if_there_is_main_wkt(path, error_file_path)
    elif function_number == 25:
        move_modernization_wkt(path, error_file_path)


def txt_list_based_or_path_based():
    print(
        "If you want to provide list of paths, enter the path to folder\
 where paths.txt file is.\n\
Otherwise just paste in main folder path."
    )
    file_or_single_path = input("> ")
    paths_file = os.path.join(file_or_single_path, "paths.txt")
    if os.path.exists(paths_file):
        paths_list = []
        with open(paths_file, "r", encoding="utf-8") as read_paths:
            for line in read_paths:
                paths_list.append(line.strip())
        return paths_list
    else:
        return list(file_or_single_path)


def move_wkt_files_to_their_folders(path, error_file_path):
    count = 1
    for subdir, _, files in os.walk(path):
        for file in natsorted(files):
            from_here = os.path.join(subdir, file)
            move_there = os.path.join(
                subdir,
                file.split("__")[0],
                (file.split("__")[1]).split(".wkt")[0],
                file,
            )
            folder = os.path.join(
                subdir,
                file.split("__")[0],
                (file.split("__")[1]).split(".wkt")[0],
            )
            if not os.path.exists(folder):
                os.makedirs(folder)
            try:
                shutil.move(from_here, move_there)
                print(count)
                count += 1
            except:
                errors_file = os.path.join(
                    error_file_path, "wkt_not_moved.txt"
                )
                with open(errors_file, "a", encoding="utf-8") as write_errors:
                    write_errors.write(from_here)


def add_precinct_name_to_folder(path):
    for subdir, dirs, _ in os.walk(path):
        dirs.sort(key=nkey)
        if regex.match(r".*2\.00..$", subdir):
            precincts_dict = os.path.join(
                input(
                    """
            Where is precincts_dict.txt?
            > """
                ),
                "precincts_dict.txt",
            )
            with open(precincts_dict, "r", encoding="utf-8") as dictionary:
                for line in dictionary:
                    if (
                        os.path.basename(subdir)
                        == (line.split("\t")[1]).split("\n")[0]
                    ):
                        os.rename(subdir, subdir + "_" + line.split("\t")[0])


def move_wkt_for_files_to_main_wkt(path, error_file_path):
    count = 1
    operats_path = input("Path to operat wkt folder:\n> ")
    documents_path = input("Path to documents wkt folder:\n> ")
    for subdir, dirs, files in os.walk(operats_path):
        dirs.sort(key=nkey)
        for file in natsorted(files):
            operat_path = subdir
            document_path = file.split(".wkt")[0]
            for subdir, _, files in os.walk(documents_path):
                for file in natsorted(files):
                    new_name = regex.sub(
                        r"^(.+)?(?=(_.-|_..-)|_...-).+", "\\1", file
                    )
                    if new_name.endswith(".wkt"):
                        new_name = new_name.split(".wkt")[0]
                    if new_name == document_path:
                        from_here = os.path.join(subdir, file)
                        move_there = os.path.join(operat_path, file)
                        try:
                            shutil.move(from_here, move_there)
                            print(count)
                            count += 1
                        except:
                            errors_file = os.path.join(
                                error_file_path, "documents_wkt_not_moved.txt"
                            )
                            with open(
                                errors_file, "a", encoding="utf-8"
                            ) as write_errors:
                                write_errors.write(from_here)


def delete_parenthesis_if_not_multipolygon(path):
    for subdir, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".wkt"):
                temporary_lines = ""
                wkt_file = os.path.join(subdir, file)
                with open(wkt_file, "r", encoding="utf-8") as wkt:
                    for line in wkt:
                        if regex.match(r"^POLYGON.+", line):
                            new_line = regex.sub(
                                r"(^.+)\((\(\(.+\)\))\)", "\\1\\2", line
                            )
                            temporary_lines += new_line
                if temporary_lines:
                    with open(
                        wkt_file, "w", encoding="utf-8"
                    ) as update_wkt_file:
                        update_wkt_file.write(temporary_lines)


def match_wkt_folders_to_operat_folder(path, error_file_path):
    count = 1
    wkt_files_list_path = os.path.join(error_file_path, "wkt_list.txt")
    pdf_files_list_path = os.path.join(error_file_path, "pdf_list.txt")
    with open(wkt_files_list_path, "r", encoding="utf-8",) as from_here:
        for line in from_here:
            print(count)
            count += 1
            full_line_wkt = line.strip()
            name_wkt = (
                os.path.basename(
                    os.path.dirname(os.path.dirname(full_line_wkt))
                )
                + os.path.basename(os.path.dirname(full_line_wkt))
                + os.path.basename(full_line_wkt)
            )
            with open(
                pdf_files_list_path, "r", encoding="utf-8",
            ) as move_there:
                for line in move_there:
                    full_line_pdf = line.strip()
                    name_pdf = (
                        os.path.basename(
                            os.path.dirname(os.path.dirname(full_line_pdf))
                        )
                        + os.path.basename(os.path.dirname(full_line_pdf))
                        + os.path.basename(full_line_pdf)
                    )
                    if name_pdf == name_wkt:
                        print(name_wkt)
                        print("\t" + name_pdf)
                        matched_files_list = os.path.join(
                            error_file_path, "matched_wkt_to_pdf.txt"
                        )
                        with open(
                            matched_files_list, "a", encoding="utf-8",
                        ) as what_to_what:
                            what_to_what.write(
                                full_line_wkt + "\t" + full_line_pdf + "\n"
                            )


def check_if_all_operat_from_list_matched(path, error_file_path):
    matched_lines = set()
    with open(
        os.path.join(error_file_path, "matched_wkt_to_pdf.txt"),
        "r",
        encoding="utf-8",
    ) as cdc:
        for line in cdc:
            matched_lines.add(line.split("\t")[0])
    with open(
        os.path.join(error_file_path, "wkt_list.txt"), "r", encoding="utf-8",
    ) as from_here:
        for line in from_here:
            if not line.strip() in matched_lines:
                with open(
                    os.path.join(error_file_path, "unmatched_wkt.txt"),
                    "a",
                    encoding="utf-8",
                ) as unmatched:
                    unmatched.write(line.strip() + "\n")


def find_duplicate_lines_in_cdc_file(path, error_file_path):
    previous = first = ""
    with open(
        os.path.join(error_file_path, "matched_wkt_to_pdf.txt"),
        "r",
        encoding="utf-8",
    ) as cdc:
        for line in cdc:
            linia = line.split("\t")[0]
            if previous == "":
                first = line
                previous = linia
                czy1 = 1
                continue
            if linia != previous:
                first = line
                czy1 = 1
                previous = linia
                continue
            elif previous == linia:
                if czy1 == 1:
                    with open(
                        os.path.join(error_file_path, "several_matches.txt"),
                        "a",
                    ) as kilka:
                        kilka.write(first)
                    czy1 = 0
                with open(
                    os.path.join(error_file_path, "several_matches.txt"), "a",
                ) as kilka:
                    kilka.write(line)


def remove_from_cdc_lines_moved_to_duplicated(path, error_file_path):
    remove_them = set()
    with open(
        os.path.join(error_file_path, "several_matches.txt"),
        "r",
        encoding="utf-8",
    ) as several_matches:
        for line in several_matches:
            remove_them.add(line)
    with open(
        os.path.join(error_file_path, "matched_wkt_to_pdf.txt"),
        "r",
        encoding="utf-8",
    ) as cdc:
        for line in cdc:
            if line not in remove_them:
                with open(
                    os.path.join(
                        error_file_path, "new_matche_wkt_to_pdf.txt"
                    ),  # noqa
                    "a",
                ) as ncdc:
                    ncdc.write(line)


def copy_wkt_to_corresponding_operat_folder(path, error_file_path):
    count = 1
    with io.open(
        os.path.join(error_file_path, "new_matched_wkt_to_pdf.txt"),
        "r",
        encoding="utf-8",
    ) as cdc:
        for line in cdc:
            print(count)
            count += 1
            from_here = line.split("\t")[0]
            move_there = (line.split("\t")[1]).strip()
            for _, _, files in os.walk(from_here):
                for file in natsorted(files):
                    if file.upper().endswith(".WKT"):
                        wkt_file = os.path.join(from_here, file)
                        destination = os.path.join(move_there, file)
                        if not os.path.exists(destination):
                            try:
                                shutil.copy2(wkt_file, destination)
                                with io.open(
                                    os.path.join(
                                        error_file_path, "can_be_removed.txt"
                                    ),
                                    "a",
                                    encoding="utf-8",
                                ) as remove_them:
                                    remove_them.write(wkt_file + "\n")
                            except:
                                with io.open(
                                    os.path.join(
                                        error_file_path, "copying_errors.txt"
                                    ),
                                    "a",
                                    encoding="utf-8",
                                ) as errors:
                                    errors.write(wkt_file + "\n")
                        else:
                            with io.open(
                                os.path.join(
                                    error_file_path, "wkt_already_exists.txt"
                                ),
                                "a",
                                encoding="utf-8",
                            ) as already_exists:
                                already_exists.write(wkt_file + "\n")


def delete_successfuly_moved_files(path, error_file_path):
    count = 1
    with open(
        os.path.join(error_file_path, "can_be_removed.txt"),
        "r",
        encoding="utf-8",
    ) as remove_them:
        for line in remove_them:
            print(count)
            count += 1
            try:
                os.remove(line.strip())
            except:
                with open(
                    os.path.join(error_file_path, "cant_be_deleted.txt"),
                    "a",
                    encoding="utf-8",
                ) as errors:
                    errors.write(line)


def cleanup_more_than_one_fit(path, error_file_path):
    with open(
        os.path.join(error_file_path, "several_matches.txt"),
        "r",
        encoding="utf-8",
    ) as several_matches:
        for line in several_matches:
            precinct = (
                regex.sub(
                    r"^.+do_operatow.+\.[0-9][0-9][0-9][0-9](.+?)\t.+",
                    "\\1",
                    line,
                )
            ).strip()
            if precinct.upper() in (line.split("\t")[1]).upper():
                with io.open(
                    os.path.join(
                        error_file_path, "several_matches_cleared.txt"
                    ),
                    "a",
                    encoding="utf-8",
                ) as clean:
                    clean.write(line)


def check_for_pdf_equivalent_for_wkt(path, error_file_path):
    count = 1
    for subdir, dirs, files in os.walk(path):
        dirs.sort(key=nkey)
        for file in natsorted(files):
            if file.endswith(".wkt"):
                wkt_file = os.path.join(subdir, file)
                print(str(count))
                count += 1
                if (
                    not os.path.exists((wkt_file.split(".wkt")[0]) + ".PDF")
                    and os.path.basename(subdir) != file.split(".wkt")[0]
                ):
                    with io.open(
                        os.path.join(
                            error_file_path, "wkt_without_pdf_equivalent.txt"
                        ),
                        "a",
                        encoding="utf-8",
                    ) as missing_equivalent:
                        missing_equivalent.write(wkt_file + "\n")


def check_error_wkt_creation_date(path, error_file_path):
    with open(
        os.path.join(error_file_path, "wkt_without_pdf_equivalent.txt"),
        "r",
        encoding="utf-8",
    ) as missing_equivalent:
        for line in missing_equivalent:
            wkt_file_path = line.strip()
            creation_date = (
                str(
                    datetime.datetime.fromtimestamp(
                        os.path.getmtime(wkt_file_path)
                    )
                )
            ).split(" ")[0]
            with open(
                os.path.join(error_file_path, "wkt_creation_date.txt"),
                "a",
                encoding="utf-8",
            ) as wkt_date:
                wkt_date.write(wkt_file_path + "\t" + creation_date + "\n")


def check_wkt_structure(path, error_file_path):
    count = 1
    wrong_wkt_structure = 0
    for subdir, dirs, files in os.walk(path):
        dirs.sort(key=nkey)
        for file in natsorted(files):
            if file.endswith(".wkt"):
                print(count)
                count += 1
                wkt_file = os.path.join(subdir, file)
                with open(wkt_file, "r", encoding="utf-8") as check_this:
                    for line in check_this:
                        if not regex.match(r"^POLYGON|MULTI.*", line.upper()):
                            wrong_wkt_structure += 1
                            print("\t\t" + str(wrong_wkt_structure))
                            with open(
                                os.path.join(
                                    error_file_path, "wkt_wrong_structure.txt",
                                ),
                                "a",
                            ) as errors:
                                errors.write(wkt_file + "\n")
                        break


def merge_wkt_with_wrong_structure(path, error_file_path):
    with open(
        os.path.join(error_file_path, "wkt_wrong_structure.txt"),
        "r",
        encoding="utf-8",
    ) as wrong_structure:
        for line in wrong_structure:
            files_separator_on_off = 1
            wkt_file_path = line.strip()
            with open(wkt_file_path, "r", encoding="utf-8") as wkt_file:
                for line in wkt_file:
                    with open(
                        os.path.join(
                            error_file_path, "merged_wkt_wrong_structure.txt"
                        ),
                        "a",
                        encoding="utf-8",
                    ) as errors:
                        if files_separator_on_off == 1:
                            errors.write(
                                "\n~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                                + wkt_file_path
                                + "\n\n"
                            )
                            files_separator_on_off = 0
                        errors.write(line)


def check_file_encoding_chardet(path, error_file_path):
    count = 1
    for subdir, dirs, files in os.walk(path):
        dirs.sort(key=nkey)
        for file in natsorted(files):
            if file.endswith(".wkt"):
                print(count)
                count += 1
                wkt_file_path = os.path.join(subdir, file)
                rawdata = open(wkt_file_path, "rb").read()
                result = chardet.detect(rawdata)
                print(result)
                charenc = result["encoding"]
                with open(
                    os.path.join(error_file_path, "files_encoding.txt"),
                    "a",
                    encoding="utf-8",
                ) as encoding:
                    encoding.write(wkt_file_path + "\t" + charenc + "\n")


def check_file_encoding_universal_detector(path, error_file_path):
    count = 1
    detector = UniversalDetector()
    for subdir, dirs, files in os.walk(path):
        dirs.sort(key=nkey)
        for file in natsorted(files):
            if file.endswith(".xml"):
                print(count)
                count += 1
                wkt_file_path = os.path.join(subdir, file)
                detector.reset()
                with open(wkt_file_path, "rb") as check_it:
                    for line in check_it:
                        detector.feed(line)
                        if detector.done:
                            break
                detector.close()
                if "utf-8" not in str(detector.result):
                    with open(
                        os.path.join(error_file_path, "files_encoding.txt"),
                        "a",
                        encoding="utf-8",
                    ) as encoding:
                        encoding.write(
                            wkt_file_path + "\t" + str(detector.result) + "\n"
                        )


def save_files_with_utf_8(path):
    for subdir, dirs, files in os.walk(path):
        dirs.sort(key=nkey)
        for file in natsorted(files):
            from_here = os.path.join(subdir, file)
            with open(from_here, "r", encoding="utf-16") as get_content:
                content = get_content.read()
            with open(
                from_here + ".new", "w", encoding="utf-8", errors="ignore"
            ) as write_content:
                write_content.write(content)


def copy_wkt_files_to_sketches(path):
    count = 1
    for subdir, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".PDF") and "SZK-POL" in file:
                if not os.path.exists(
                    os.path.join(subdir, os.path.splitext(file)[0] + ".wkt")
                ):
                    wkt_file = file
                    if any(
                        fname.endswith(".wkt") and "SZK-POL" in fname
                        for fname in os.listdir(subdir)
                    ):
                        for file in files:
                            if file.endswith(".wkt") and "SZK-POL" in file:
                                wkt_file_path = os.path.join(subdir, file)
                                new_wkt_file = os.path.join(
                                    subdir,
                                    os.path.splitext(wkt_file)[0] + ".wkt",
                                )
                                print(count)
                                count += 1
                                shutil.copy(wkt_file_path, new_wkt_file)


def copy_wkt_files_to_required_documents(path, error_file_path):
    count = 1
    for subdir, dirs, files in os.walk(path):
        dirs.sort(key=nkey)
        main_wkt_file = os.path.join(subdir, os.path.basename(subdir) + ".wkt")
        if os.path.exists(main_wkt_file):
            for file in natsorted(files):
                if regex.match(
                    r".+((-M-)|(-SZK-)|(-Z-KAT-)|(-Z-POM-)|(-MPZP-)).+\.PDF",
                    file.upper(),
                ):
                    new_wkt = os.path.join(
                        subdir, os.path.splitext(file)[0] + ".wkt"
                    )
                    if os.path.exists(new_wkt):
                        continue
                    else:
                        try:
                            shutil.copy(main_wkt_file, new_wkt)
                            print(str(count) + "\t" + new_wkt)
                            count += 1
                        except:
                            with open(
                                os.path.join(
                                    error_file_path,
                                    "failed_to_create_wkt.txt",
                                ),
                                "a",
                                encoding="utf-8",
                            ) as errors:
                                errors.write(new_wkt + "\n")
        else:
            if any(
                fname.upper().endswith(".PDF") for fname in os.listdir(subdir)
            ):
                with open(
                    os.path.join(error_file_path, "missing_main_wkt.txt"),
                    "a",
                    encoding="utf-8",
                ) as errors:
                    errors.write(subdir + "\n")


def check_for_wkt_to_wrong_files(path, error_file_path):
    count = 1
    for subdir, dirs, files in os.walk(path):
        dirs.sort(key=nkey)
        if not any(
            fname.upper().endswith(".WKT") for fname in os.listdir(subdir)
        ):
            continue
        print(count)
        count += 1
        for file in files:
            if file.endswith(".wkt") and (
                file != (os.path.basename(subdir) + ".wkt")
                and "-M-" not in file
                and "-SZK-" not in file
                and "-Z-KAT-" not in file
                and "-Z-POM-" not in file
                and "-MPZP-" not in file
            ):
                with open(
                    os.path.join(error_file_path, "wkt_for_wrong_files.txt",),
                    "a",
                    encoding="utf-8",
                ) as errors:
                    errors.write(os.path.join(subdir, file) + "\n")


def check_wkt_files_for_required_documents(path, error_file_path):
    count = 1
    for subdir, dirs, files in os.walk(path):
        dirs.sort(key=nkey)
        if not any(
            fname.upper().endswith(".PDF") for fname in os.listdir(subdir)
        ):
            continue
        print(count)
        count += 1
        main_wkt_file = os.path.join(subdir, os.path.basename(subdir) + ".wkt")
        for file in natsorted(files):
            if regex.match(
                r".+((-M-)|(-SZK-)|(-Z-KAT-)).+\.PDF", file.upper()
            ):
                new_wkt = os.path.join(
                    subdir, os.path.splitext(file)[0] + ".wkt"
                )
                if not os.path.exists(new_wkt):
                    with open(
                        os.path.join(
                            error_file_path, "missing_document_wkt.txt"
                        ),
                        "a",
                        encoding="utf-8",
                    ) as errors:
                        errors.write(new_wkt + "\n")
        if not os.path.exists(main_wkt_file):
            with open(
                os.path.join(error_file_path, "missing_main_wkt.txt"),
                "a",
                encoding="utf-8",
            ) as errors:
                errors.write(subdir + "\n")


def check_for_any_wkt_if_main_not_exists(path, error_file_path):
    count = 1
    for subdir, dirs, _ in os.walk(path):
        if any(
            fname.upper().endswith(".WKT") for fname in os.listdir(subdir)
        ) and not os.path.exists(
            os.path.join(subdir, os.path.basename(subdir) + ".wkt")
        ):
            with open(
                os.path.join(
                    error_file_path,
                    "missing_main_wkt_but_there_is_something.txt",
                ),
                "a",
                encoding="utf-8",
            ) as errors:
                errors.write(subdir + "\n")
            print(count)
            count += 1


def check_if_there_is_main_wkt(path, error_file_path):
    for subdir, dirs, _ in os.walk(path):
        if not os.path.exists(
            os.path.join(subdir, os.path.basename(subdir) + ".wkt")
        ):
            with open(
                os.path.join(error_file_path, "missing_main_wkt.txt"),
                "a",
                encoding="utf-8",
            ) as errors:
                errors.write(subdir + "\n")


def move_modernization_wkt(path, error_file_path):
    count = 1
    for subdir, dirs, files in os.walk(path):
        dirs.sort(key=nkey)
        if "-00" in subdir:
            main_folder = subdir
            precinct_number = subdir.split("\\")[5].split("-")[1]
            for file in natsorted(files):
                if file.upper().endswith(".PDF"):
                    pdf_file = os.path.splitext(file)[0]
                    for subdir, dirs, files in os.walk(
                        os.path.join(error_file_path, "do_operatow")
                    ):
                        dirs.sort(key=nkey)
                        if ".00" in subdir:
                            precinct = subdir.split("\\")[5].split(".")[1]
                            if precinct_number == precinct:
                                for file in natsorted(files):
                                    if file.upper().endswith(".WKT"):
                                        wkt_file = os.path.splitext(file)[0]
                                        if wkt_file == pdf_file:
                                            from_here = os.path.join(
                                                subdir, file
                                            )
                                            move_there = os.path.join(
                                                main_folder, file
                                            )
                                            try:
                                                shutil.copy(
                                                    from_here, move_there
                                                )
                                                print(
                                                    str(count)
                                                    + "\t"
                                                    + precinct
                                                    + "_"
                                                    + file
                                                )
                                                count += 1
                                            except:
                                                raise


# def main():
error_file_path = input(
    "Where should I save errors files (onetime input)?\n> "
)
while True:
    paths_list = txt_list_based_or_path_based()
    function_number = int(
        input(
                """
Choose one of the following:

    (1)   move_wkt_files_to_their_folders
    (2)   add_precinct_name_to_folder
    (3)   move_wkt_for_files_to_main_wkt
    (4)   delete_parenthesis_if_not_multipolygon
    (5)   match_wkt_folders_to_operat_folder
    (6)   check_if_all_operat_from_list_matched
    (7)   find_duplicate_lines_in_cdc_file
    (8)   remove_from_cdc_lines_moved_to_duplicated
    (9)   copy_wkt_to_corresponding_operat_folder
    (10)  delete_successfuly_moved_files
    (11)  cleanup_more_than_one_fit
    (12)  check_for_pdf_equivalent_for_wkt
    (13)  check_error_wkt_creation_date
    (14)  check_wkt_structure
    (15)  merge_wkt_with_wrong_structure
    (16)  check_file_encoding_chardet
    (17)  check_file_encoding_universal_detector
    (18)  save_files_with_utf_8
    (19)  copy_wkt_files_to_sketches
    (20)  copy_wkt_files_to_required_documents
    (21)  check_for_wkt_to_wrong_files
    (22)  check_wkt_files_for_required_documents
    (23)  check_for_any_wkt_if_main_not_exists
    (24)  check_if_there_is_main_wkt
    (25)  move_modernization_wkt
> """
        )
    )
    for path in paths_list:
        execute_proper_function(function_number, path, error_file_path)


# if __name__ == "__main__":
#     main()
