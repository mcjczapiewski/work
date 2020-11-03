import datetime
import os
import shutil

import fitz
import regex
from natsort import natsort_keygen, natsorted

count = 1
nkey = natsort_keygen()
characters = r"[A-Z0-9]|!| |:|\.|-|_|\\|Ą|Ę|Ó|Ś|Ł|Ż|Ź|Ć|Ń"


def write_results(file_name, message):
    with open(
        os.path.join(write_out, file_name), "a", encoding="utf-8",
    ) as result_file:
        result_file.write(message)


def if_xmls_more_than_one():
    how_much_xmls = len(
        [
            fname
            for fname in os.listdir(subdir)
            if fname.upper().endswith(".XML")
        ]
    )
    if how_much_xmls > 1:
        write_results(
            "ponad_1_xml_w_folderze.txt", f"{str(how_much_xmls)}\t{subdir}\n"
        )


def if_xmls_or_pdfs(
    write_out, exists_extension, noexists_extension, file_name
):
    if any(
        fname.upper().endswith(exists_extension)
        for fname in os.listdir(subdir)
    ) and not any(
        fname.upper().endswith(noexists_extension)
        for fname in os.listdir(subdir)
    ):
        write_results(file_name, f"{subdir}\n")


def strange_chars_in_subdir():
    for char in subdir:
        if not regex.match(characters, char.upper()):
            write_results("dziwne_znaki_w_folderach.txt", f"{subdir}\n")


def strange_chars_in_filename():
    for char in file:
        if not regex.match(characters, char.upper()):
            write_results(
                "dziwne_znaki_w_plikach.txt",
                f"{os.path.join(subdir, file)}\n",
            )


def if_no_wkt_for_file(copy_from_main):
    if regex.match(
        r".+((-M-)|(-SZK-)|(-Z-KAT-)|(-Z-POM-)|(-MPZP-)).+\.PDF", file.upper()
    ):
        new_wkt = os.path.join(subdir, os.path.splitext(file)[0] + ".wkt")
        if not os.path.exists(new_wkt):
            if not copy_from_main:
                write_results("brak_wkt_dla_plikow.txt", f"{new_wkt}\n")
            elif copy_from_main:
                try:
                    shutil.copy(wkt_operatu, new_wkt)
                except:
                    write_results(
                        "nie_udalo_sie_skopiowac_z_glownej_wkt.txt",
                        f"{new_wkt}\n",
                    )


def if_not_match_for_wkt_exists(wkt):
    if file != (os.path.basename(subdir) + ".wkt") and not any(
        i in file for i in ["-M-", "-SZK-", "-Z-KAT-", "-Z-POM-", "-MPZP-"]
    ):
        write_results("wkt_do_niewlasciwych_plikow.txt", f"{wkt}\n")
    elif (
        not os.path.exists((wkt.split(".wkt")[0]) + ".PDF")
        and os.path.basename(subdir) != file.split(".wkt")[0]
    ):
        write_results("wkt_do_nieistniejacych_plikow.txt", f"{wkt}\n")


def count_pages_in_sketch_files():
    pdf_file = os.path.join(subdir, file)
    try:
        doc = fitz.open(pdf_file)
        pdf_pages = doc.pageCount
        if not pdf_pages == 1:
            write_results(
                "wiecej_niz_1_strona_pdf.txt",
                f"{str(pdf_pages)}\t{pdf_file}\n",
            )
    except:
        write_results("nie_udalo_sie_policzyc_stron.txt", f"{pdf_file}\n")


start_time = datetime.datetime.now()
print("~~~~~~START~~~~~~\t" + str(start_time).split(".")[0])

paths_file = input("Enter the path to file with paths (sciezki.txt):\n> ")
write_out = os.path.join(r'D:\_MACIEK_\python_proby', "kontrole")
paths_file = os.path.join(paths_file, "sciezki.txt")

if not os.path.exists(write_out):
    os.mkdir(write_out)

with open(paths_file, "r", encoding="utf-8",) as file_with_paths:
    for line in file_with_paths:
        path = line.strip()

        for subdir, dirs, files in os.walk(path):
            dirs.sort(key=nkey)

            strange_chars_in_subdir()

            if_xmls_more_than_one()
            if_xmls_or_pdfs(write_out, ".PDF", ".XML", "sa_pdf_brak_xml.txt")
            if_xmls_or_pdfs(write_out, ".XML", ".PDF", "jest_xml_brak_pdf.txt")

            if not any(
                fname.upper().endswith(".PDF") for fname in os.listdir(subdir)
            ):
                continue

            wkt_operatu = os.path.join(
                subdir, os.path.basename(subdir) + ".wkt"
            )
            print(count)
            count += 1

            if os.path.exists(wkt_operatu):
                for file in natsorted(files):
                    if_no_wkt_for_file(copy_from_main=True)
            else:
                write_results("brak_wkt_dla_operatu.txt", f"{subdir}\n")
                if any(
                    fname.upper().endswith(".WKT")
                    for fname in os.listdir(subdir)
                ):
                    write_results(
                        "brak_glownej_jest_do_pliku.txt", f"{subdir}\n"
                    )

            for file in natsorted(files):
                strange_chars_in_filename()
                if_no_wkt_for_file(copy_from_main=False)

                if file.lower().endswith(".wkt"):
                    wkt = os.path.join(subdir, file)
                    if_not_match_for_wkt_exists(wkt)
                elif file.upper().endswith(".PDF") and regex.match(
                    r"^.+(-SZK-|-M-|-Z-).+\.PDF", file.upper()
                ):
                    count_pages_in_sketch_files()

end_time = datetime.datetime.now()
delta_time = end_time - start_time
elapsed_time = delta_time.total_seconds() / 60
print("Total time elapsed (min):")
print("%.2f" % elapsed_time)
