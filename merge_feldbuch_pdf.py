import os
import shutil
import regex
from natsort import natsort_keygen, natsorted
from PyPDF2 import PdfFileMerger

possible_file_names = (
    "-AKN-",
    "-AWZ-",
    "-AMZ-",
    "-ADEB-",
    "-ADEL-",
    "-MATR-",
    "-DEC-",
    "-DOK-IN-",
    "-DOK-WYJ-",
    "-DOK-OBL-",
    "-DZ-P-",
    "-DZ-R-",
    "-K-BUD-",
    "-K-PAR-",
    "-M-KL-",
    "-M-IN-",
    "-M-KAT-",
    "-M-WYN-",
    "-M-UZ-",
    "-M-WYW-",
    "-M-PROJ-",
    "-M-WPROJ-",
    "-MPZP-",
    "-ZGL-ODP-",
    "-OPIN-",
    "-OIM-",
    "-OTOP-",
    "-ORZ-",
    "-OSW-",
    "-POST-",
    "-P-KW-",
    "-P-G-",
    "-P-IN-",
    "-P-KAT-",
    "-R-IN-",
    "-R-GPS-",
    "-REJ-ARCH-",
    "-REJ-IN-",
    "-REJ-SCAL-",
    "-SK-D-",
    "-SK-W-",
    "-SPIS-",
    "-S-TECH-",
    "-STR-TYT-",
    "-SZK-INN-",
    "-SZK-KAT-",
    "-SZK-OSN-",
    "-SZK-POL-",
    "-SZK-PRZ-",
    "-TR-PKT-",
    "-UGO-",
    "-UPOW-",
    "-WNI-IN-",
    "-WNI-PRZ-",
    "-W-S-",
    "-W-WSP-",
    "-W-WYW-",
    "-W-ZDE-",
    "-Z-KAT-",
    "-Z-POM-",
    "-ZASW-",
    "-ZAW-ZGL-",
    "-ZAW-IN-",
    "-ZAW-KW-",
    "-ZGL-PRAC-",
    "-ZW-",
)


def save_merged_pdf(pdf_name):
    merger.write(os.path.join(subdir, "__merge", os.path.basename(pdf_name)))
    merger.close()


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
        changes("dokumentów", doc_numbers_to_change)

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
        changes("stron", page_numbers_to_change)

    if not doc_numbers_to_change and not page_numbers_to_change:
        print(" --- NAJPIERW POPRAW --- ")
    else:
        print(" --- GOTOWE --- ")


def changes(change_type, numbers_to_change):
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


# with open(
#     r"P:\cyfryzacja_powiat_inowroclawski\SKANY_III\20200527\040707_5\prawne\040707_5.0005\zmiana.txt",
#     "r",
#     encoding="UTF-8",
# ) as lista:
#     for line in lista:
#         folder_path = line.strip()

folder_path = (
    r"P:\cyfryzacja_powiat_inowroclawski\SKANY_III\20200528\040707_5\prawne"
)
for subdir, dirs, files in os.walk(folder_path):
    dirs.sort(key=natsort_keygen())
    if "FELDBU" not in subdir:
        continue
    if not subdir.endswith(
        f"{os.path.basename(subdir)}\\{os.path.basename(subdir)}"
    ):
        continue
    if not any(
        regex.search(r'-.+-', fname) for fname in os.listdir(subdir)
    ):
        continue
    print(subdir)
    new_feldbuch = 0
    stop_it = 0
    dirs.sort(key=natsort_keygen())
    merge_existed = os.path.join(subdir, "merge")

    names = {}
    for file in natsorted(files):
        if not file.upper().endswith(".PDF"):
            continue
        name = regex.search(r"-([A-Z].*[A-Z])-", file)[0]
        if "NEW_FELD" in name:
            name = "-DOK-IN-"
            new_feldbuch += 1
        if name not in possible_file_names:
            print(f"Niepoprawna nazwa: {file}")
            stop_it = 1
            break
        if "DOK-IN" in name:
            name = f"-DOK-IN-__{new_feldbuch}__"
        if name not in names:
            names[name] = [os.path.join(subdir, file)]
        else:
            names[name].append(os.path.join(subdir, file))
    if stop_it:
        break

    if os.path.exists(merge_existed):
        shutil.rmtree(merge_existed)

    new_merge = os.path.join(subdir, "__merge")
    if not os.path.exists(new_merge):
        os.mkdir(new_merge)

    for key, val in names.items():
        merger = PdfFileMerger()
        continue_loop = 0
        for item in natsorted(val):
            if "-M-" in item or "-SZK-" in item or "-Z-" in item:
                merger.append(item)
                save_merged_pdf(item)
                merger = PdfFileMerger()
                continue_loop = 1
            else:
                merger.append(item)
        if continue_loop == 1:
            continue
        else:
            if "NEW_FELD" in names[key][0]:
                new_pdf_name = names[key][0]
                new_pdf_name = regex.sub(
                    r"(^.*)NEW_FELD(.*)", r"\g<1>DOK-IN\g<2>", new_pdf_name
                )
                save_merged_pdf(new_pdf_name)
            else:
                save_merged_pdf(names[key][0])

    fix_numbers(subdir)
