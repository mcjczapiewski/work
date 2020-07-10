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
        pass  # TODO: itd.


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
                                error_file_path, "document_wkt_not_moved.txt"
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
    wkt_files_list_path = input("Path to directory with wkt_list.txt:\n> ")
    pdf_files_list_path = input("Path to directory with pdf_list.txt:\n> ")
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
                            error_file_path, "matched_wkt_pdf.txt"
                        )
                        with open(
                            matched_files_list, "a", encoding="utf-8",
                        ) as what_to_what:
                            what_to_what.write(
                                full_line_wkt + "\t" + full_line_pdf + "\n"
                            )


def match_files_based_on_name_not_folder_only(path, error_file_path):
    count = 1
    with open(
        r"D:\_MACIEK_\python_proby\p33\wkt_rozrzucenie\wkt_bez_odpowiednika_pdf.txt",  # noqa
        "r",
        encoding="utf-8",
    ) as stad:
        for line in stad:
            print(count)
            count += 1
            pelne = line.strip()
            nazwa = os.path.basename(pelne).split(".wkt")[0]
            sciezka = os.path.basename(os.path.dirname(pelne))
            with open(
                r"D:\_MACIEK_\python_proby\p33\wkt_rozrzucenie\lista_plikow_p33.txt",  # noqa
                "r",
                encoding="utf-8",
            ) as tutaj:
                for line in tutaj:
                    pelne1 = line.strip()
                    nazwa1 = os.path.basename(pelne1).split(".PDF")[0]
                    sciezka1 = os.path.basename(os.path.dirname(pelne1))
                    if sciezka1 + nazwa1 == sciezka + nazwa:
                        with open(
                            r"D:\_MACIEK_\python_proby\p33\wkt_rozrzucenie\co_do_czego.txt",  # noqa
                            "a",
                        ) as cdc:
                            cdc.write(pelne + "\t" + pelne1 + "\n")


def check_if_all_operat_from_list_matched(path, error_file_path):
    dopasowane = set()
    with open(
        r"D:\_MACIEK_\python_proby\p33\wkt_rozrzucenie\co_do_czego.txt",
        "r",
        encoding="utf-8",
    ) as cdc:
        for line in cdc:
            dopasowane.add(line.split("\t")[0])
    with open(
        r"D:\_MACIEK_\python_proby\p33\wkt_rozrzucenie\lista_wkt.txt",
        "r",
        encoding="utf-8",
    ) as stad:
        for line in stad:
            if not line.strip() in dopasowane:
                with open(
                    r"D:\_MACIEK_\python_proby\p33\wkt_rozrzucenie\niedopasowane_wkt.txt",  # noqa
                    "a",
                    encoding="utf-8",
                ) as niedopasowane:
                    niedopasowane.write(line.strip() + "\n")


def find_duplicate_lines_in_cdc_file(path, error_file_path):
    poprzednia = pierwsza = ""
    with open(
        r"D:\_MACIEK_\python_proby\p33\wkt_rozrzucenie\co_do_czego.txt",
        "r",
        encoding="utf-8",
    ) as cdc:
        for line in cdc:
            linia = line.split("\t")[0]
            if poprzednia == "":
                pierwsza = line
                poprzednia = linia
                czy1 = 1
                continue
            if linia != poprzednia:
                pierwsza = line
                czy1 = 1
                poprzednia = linia
                continue
            elif poprzednia == linia:
                if czy1 == 1:
                    with open(
                        r"D:\_MACIEK_\python_proby\p33\wkt_rozrzucenie\kilka_dopasowan.txt",  # noqa
                        "a",
                    ) as kilka:
                        kilka.write(pierwsza)
                    czy1 = 0
                with open(
                    r"D:\_MACIEK_\python_proby\p33\wkt_rozrzucenie\kilka_dopasowan.txt",  # noqa
                    "a",
                ) as kilka:
                    kilka.write(line)


def remove_from_cdc_lines_moved_to_duplicated(path, error_file_path):
    usunac = set()
    with open(
        r"D:\_MACIEK_\python_proby\p33\wkt_rozrzucenie\kilka_dopasowan.txt",
        "r",
        encoding="utf-8",
    ) as kilka:
        for line in kilka:
            usunac.add(line)
    with open(
        r"D:\_MACIEK_\python_proby\p33\wkt_rozrzucenie\co_do_czego.txt",
        "r",
        encoding="utf-8",
    ) as cdc:
        for line in cdc:
            if line not in usunac:
                with open(
                    r"D:\_MACIEK_\python_proby\p33\wkt_rozrzucenie\n_co_do_czego.txt",  # noqa
                    "a",
                ) as ncdc:
                    ncdc.write(line)


def copy_wkt_to_corresponding_operat_folder(path, error_file_path):
    count = 1
    with io.open(
        r"D:\_MACIEK_\python_proby\p33\wkt_rozrzucenie\co_do_czego.txt",
        "r",
        encoding="utf-8",
    ) as cdc:
        for line in cdc:
            print(count)
            count += 1
            stad = line.split("\t")[0]
            tutaj = (line.split("\t")[1]).split("\n")[0]
            for _, _, files in os.walk(stad):
                for file in natsorted(files):
                    if file.upper().endswith(".WKT"):
                        plik = os.path.join(stad, file)
                        docelowe = os.path.join(tutaj, file)
                        if not os.path.exists(docelowe):
                            try:
                                shutil.copy2(plik, docelowe)
                                with io.open(
                                    r"D:\_MACIEK_\python_proby\p33\wkt_rozrzucenie\mozna_usunac.txt",  # noqa
                                    "a",
                                    encoding="utf-8",
                                ) as usun:
                                    usun.write(plik + "\n")
                            except:
                                with io.open(
                                    r"D:\_MACIEK_\python_proby\p33\wkt_rozrzucenie\bledy_kopiowania.txt",  # noqa
                                    "a",
                                    encoding="utf-8",
                                ) as bledy:
                                    bledy.write(plik + "\n")
                        else:
                            with io.open(
                                r"D:\_MACIEK_\python_proby\p33\wkt_rozrzucenie\wkt_juz_istnieje.txt",  # noqa
                                "a",
                                encoding="utf-8",
                            ) as istnieje:
                                istnieje.write(plik + "\n")


def delete_successfuly_moved_files(path, error_file_path):
    count = 1
    with open(
        r"D:\_MACIEK_\python_proby\p33\wkt_rozrzucenie\mozna_usunac.txt", "r"
    ) as usun:
        for line in usun:
            print(count)
            count += 1
            try:
                os.remove(line.strip())
            except:
                with open(
                    r"D:\_MACIEK_\python_proby\p33\wkt_rozrzucenie\nie_da_sie_usunac.txt",  # noqa
                    "a",
                ) as nds:
                    nds.write(line)


def cleanup_more_than_one_fit(path, error_file_path):
    with open(
        r"D:\_MACIEK_\python_proby\p33\wkt_rozrzucenie\kilka_dopasowan.txt",
        "r",
    ) as kilka:
        for line in kilka:
            obreb = (
                regex.sub(
                    r"^.+do_operatow.+\.[0-9][0-9][0-9][0-9](.+?)\t.+",
                    "\\1",
                    line,
                )
            ).split("\n")[0]
            if obreb.upper() in (line.split("\t")[1]).upper(
                path, error_file_path
            ):
                with io.open(
                    r"D:\_MACIEK_\python_proby\p33\wkt_rozrzucenie\wyczyszczone.txt",  # noqa
                    "a",
                    encoding="utf-8",
                ) as czyste:
                    czyste.write(line)


def check_for_pdf_equivalent_for_wkt(path, error_file_path):
    count = 1
    sciezka = (
        r"\\waw-dt1409\h\Poprawa_Inowrocław_cz.3\INOWROCŁAW\dla_macka_wkt"
    )
    with open(
        r"I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614\ZADANIE 4\kontrole_2020-07-06\sciezki.txt",  # noqa
        "r",
        encoding="utf-8",
    ) as sciezki:
        for line in sciezki:
            sciezka = line.strip()
            for subdir, dirs, files in os.walk(sciezka):
                dirs.sort(key=nkey)
                for file in natsorted(files):
                    if file.endswith(".wkt"):
                        wkt = os.path.join(subdir, file)
                        print(str(count))
                        count += 1
                        if (
                            not os.path.exists((wkt.split(".wkt")[0]) + ".PDF")
                            and os.path.basename(subdir)
                            != file.split(".wkt")[0]
                        ):
                            with io.open(
                                r"I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614\ZADANIE 4\kontrole_2020-07-06\wkt_bez_odpowiednika_pdf.txt",  # noqa
                                "a",
                                encoding="utf-8",
                            ) as brak:
                                brak.write(wkt + "\n")


def check_error_wkt_creation_date(path, error_file_path):
    with open(
        r"D:\_MACIEK_\python_proby\p33\wkt_bez_odpowiednika_pdf.txt", "r"
    ) as braki:
        for line in braki:
            sciezka = line.strip()
            data = (
                str(datetime.datetime.fromtimestamp(os.path.getmtime(sciezka)))
            ).split(" ")[0]
            with open(
                r"D:\_MACIEK_\python_proby\p33\wkt_daty.txt", "a"
            ) as daty:
                daty.write(sciezka + "\t" + data + "\n")


def check_wkt_structure(path, error_file_path):
    count = 1
    braki = 0
    for subdir, dirs, files in os.walk(
        r"I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\Zmiana_kodowania_test"
    ):
        dirs.sort(key=nkey)
        for file in natsorted(files):
            if file.endswith(".wkt"):
                zeruj = 0
                print(count)
                count += 1
                wkt = os.path.join(subdir, file)
                with open(wkt, "r") as sprawdz:
                    for line in sprawdz:
                        if zeruj == 0:
                            zeruj = 1
                            if not regex.match(
                                r"^POLYGON|MULTI.*", line.upper()
                            ):
                                braki += 1
                                print("\t\t" + str(braki))
                                with open(
                                    r"D:\_MACIEK_\python_proby\p33\wkt_bledne_struktuaaary.txt",  # noqa
                                    "a",
                                ) as brak:
                                    brak.write(wkt + "\n")
                        else:
                            continue


def merge_wkt_with_wrong_structure(path, error_file_path):
    with open(
        r"D:\_MACIEK_\python_proby\p33\wkt_bledne_struktury.txt", "r"
    ) as braki:
        for line in braki:
            bb = 0
            sciezka = line.strip()
            with open(sciezka, "r") as wkt:
                for line in wkt:
                    with open(
                        r"D:\_MACIEK_\python_proby\p33\wkt_bledne_zlaczone.txt",  # noqa
                        "a",
                    ) as bledne:
                        if bb == 0:
                            bledne.write(
                                "\n~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                                + sciezka
                                + "\n\n"
                            )
                            bb = 1
                        bledne.write(line)


def check_file_encoding_chardet(path, error_file_path):
    count = 1
    for subdir, dirs, files in os.walk(r"W:\dla Maćka\przykłady wkt"):
        dirs.sort(key=nkey)
        for file in natsorted(files):
            if file.endswith(".wkt"):
                print(count)
                count += 1
                wkt = os.path.join(subdir, file)
                rawdata = open(wkt, "rb").read()
                result = chardet.detect(rawdata)
                print(result)
                charenc = result["encoding"]
                with open(
                    r"D:\_MACIEK_\python_proby\p33\kodowania_plikow.txt", "a"
                ) as kodowanie:
                    kodowanie.write(wkt + "\t" + charenc + "\n")


def check_file_encoding_universal_detector(path, error_file_path):
    count = 1
    detector = UniversalDetector()
    for subdir, dirs, files in os.walk(
        r"I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614\DĄBROWA BISKUPIA\RADOJEWICE"  # noqa
    ):
        dirs.sort(key=nkey)
        for file in natsorted(files):
            if file.endswith(".xml"):
                print(count)
                count += 1
                wkt = os.path.join(subdir, file)
                detector.reset()
                with open(wkt, "rb") as sprawdz:
                    for line in sprawdz:
                        detector.feed(line)
                        if detector.done:
                            break
                detector.close()
                if "utf-8" not in str(detector.result):
                    with open(
                        r"D:\_MACIEK_\python_proby\p33\numer_p_do_xml\kodowania_plikow.txt",  # noqa
                        "a",
                    ) as kodowanie:
                        kodowanie.write(
                            wkt + "\t" + str(detector.result) + "\n"
                        )


def save_files_with_utf_8(path, error_file_path):
    for subdir, dirs, files in os.walk(
        r"W:\dla Maćka\przykłady wkt\P.0410.1999.241"
    ):
        dirs.sort(key=nkey)
        for file in natsorted(files):
            stad = os.path.join(subdir, file)
            with io.open(stad, "r", encoding="utf-16") as pobierz:
                tresc = pobierz.read()
            with io.open(
                stad + ".new", "w", encoding="utf-8", errors="ignore"
            ) as zapisz:
                zapisz.write(tresc)


def copy_wkt_files_to_sketches(path, error_file_path):
    count = 1
    for subdir, dirs, files in os.walk(
        r"I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614\INOWROCŁAW"
    ):
        for file in files:
            if file.endswith(".PDF") and "SZK-POL" in file:
                if not os.path.exists(
                    os.path.join(subdir, os.path.splitext(file)[0] + ".wkt")
                ):
                    plik = file
                    if any(
                        fname.endswith(".wkt") and "SZK-POL" in fname
                        for fname in os.listdir(subdir)
                    ):
                        for file in files:
                            if file.endswith(".wkt") and "SZK-POL" in file:
                                wkt = os.path.join(subdir, file)
                                new = os.path.join(
                                    subdir, os.path.splitext(plik)[0] + ".wkt"
                                )
                                print(count)
                                count += 1
                                shutil.copy(wkt, new)


def copy_wkt_files_to_required_documents(path, error_file_path):
    count = 1
    sciezka = r"I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614\ZADANIE 2\10.06.2020\INOWROCŁAW"  # noqa
    with open(
        r"P:\cyfryzacja_powiat_inowroclawski\kontrole_2020-07-06\sciezki.txt",
        "r",
        encoding="utf-8",
    ) as sciezki:
        for line in sciezki:
            sciezka = line.strip()
            for subdir, dirs, files in os.walk(sciezka):
                dirs.sort(key=nkey)
                wkt_operatu = os.path.join(
                    subdir, os.path.basename(subdir) + ".wkt"
                )
                if os.path.exists(wkt_operatu):
                    for file in natsorted(files):
                        if regex.match(
                            r".+((-M-)|(-SZK-)|(-Z-KAT-)|(-Z-POM-)|(-MPZP-)).+\.PDF",  # noqa
                            file.upper(),
                        ):
                            new_wkt = os.path.join(
                                subdir, os.path.splitext(file)[0] + ".wkt"
                            )
                            if os.path.exists(new_wkt):
                                continue
                            else:
                                try:
                                    shutil.copy(wkt_operatu, new_wkt)
                                    print(str(count) + "\t" + new_wkt)
                                    count += 1
                                except:
                                    with open(
                                        r"P:\cyfryzacja_powiat_inowroclawski\kontrole_2020-07-06\nie_udalo_sie_utworzyc_wkt.txt",  # noqa
                                        "a",
                                        encoding="utf-8",
                                    ) as bledy:
                                        bledy.write(new_wkt + "\n")
                else:
                    if any(
                        fname.upper().endswith(".PDF")
                        for fname in os.listdir(subdir)
                    ):
                        with open(
                            r"P:\cyfryzacja_powiat_inowroclawski\kontrole_2020-07-06\brak_wkt_operatu.txt",  # noqa
                            "a",
                            encoding="utf-8",
                        ) as bledy:
                            bledy.write(subdir + "\n")


def check_for_wkt_to_wrong_files(path, error_file_path):
    count = 1
    with open(
        r"I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614\ZADANIE 4\kontrole_2020-07-06\sciezki.txt",  # noqa
        "r",
        encoding="utf-8",
    ) as sciezki:
        for line in sciezki:
            sciezka = line.strip()
            for subdir, dirs, files in os.walk(sciezka):
                dirs.sort(key=nkey)
                if not any(
                    fname.upper().endswith(".WKT")
                    for fname in os.listdir(subdir)
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
                            r"I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614\ZADANIE 4\kontrole_2020-07-06\wkt_do_niewlasciwych_plikow.txt",  # noqa
                            "a",
                            encoding="utf-8",
                        ) as bledy:
                            bledy.write(os.path.join(subdir, file) + "\n")


def check_wkt_files_for_required_documents(path, error_file_path):
    count = 1
    with open(
        r"I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614\ZADANIE 4\kontrole_2020-07-06\sciezki.txt",  # noqa
        "r",
        encoding="utf-8",
    ) as sciezki:
        for line in sciezki:
            sciezka = line.strip()
            for subdir, dirs, files in os.walk(sciezka):
                dirs.sort(key=nkey)
                if not any(
                    fname.upper().endswith(".PDF")
                    for fname in os.listdir(subdir)
                ):
                    continue
                print(count)
                count += 1
                wkt_operatu = os.path.join(
                    subdir, os.path.basename(subdir) + ".wkt"
                )
                for file in natsorted(files):
                    if regex.match(
                        r".+((-M-)|(-SZK-)|(-Z-KAT-)).+\.PDF", file.upper()
                    ):
                        new_wkt = os.path.join(
                            subdir, os.path.splitext(file)[0] + ".wkt"
                        )
                        if not os.path.exists(new_wkt):
                            with open(
                                r"I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614\ZADANIE 4\kontrole_2020-07-06\brak_wkt_dla_plikow.txt",  # noqa
                                "a",
                                encoding="utf-8",
                            ) as bledy:
                                bledy.write(new_wkt + "\n")
                if not os.path.exists(wkt_operatu):
                    with open(
                        r"I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614\ZADANIE 4\kontrole_2020-07-06\brak_wkt_dla_operatu.txt",  # noqa
                        "a",
                        encoding="utf-8",
                    ) as bledy:
                        bledy.write(subdir + "\n")


def check_for_any_wkt_if_main_not_exists(path, error_file_path):
    count = 1
    with open(
        r"I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614\ZADANIE 4\kontrole_2020-07-06\sciezki.txt",  # noqa
        "r",
        encoding="utf-8",
    ) as sciezki:
        for line in sciezki:
            sciezka = line.strip()
            for subdir, dirs, _ in os.walk(sciezka):
                if any(
                    fname.upper().endswith(".WKT")
                    for fname in os.listdir(subdir)
                ) and not os.path.exists(
                    os.path.join(subdir, os.path.basename(subdir) + ".wkt")
                ):
                    with open(
                        r"I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614\ZADANIE 4\kontrole_2020-07-06\brak_glownej_jest_do_pliku.txt",  # noqa
                        "a",
                        encoding="utf-8",
                    ) as bledy:
                        bledy.write(subdir + "\n")
                    print(count)
                    count += 1


def check_if_there_is_main_wkt(path, error_file_path):
    with open(r"D:\_MACIEK_\python_proby\p33\spis.txt", "r") as spis:
        for line in spis:
            sciezka = line.strip()
    for subdir, dirs, _ in os.walk(sciezka):
        if not os.path.exists(
            os.path.join(subdir, os.path.basename(subdir) + ".wkt")
        ):
            print(subdir)


def move_modernization_wkt(path, error_file_path):
    count = 1
    for subdir, dirs, files in os.walk(
        r"I:\INOWROCŁAW\DANE PODGiK\SKANY OPERATÓW\!modernizacja inowrocław"
    ):
        dirs.sort(key=nkey)
        if "-00" in subdir:
            glowny = subdir
            nrobr = subdir.split("\\")[5].split("-")[1]
            for file in natsorted(files):
                if file.upper().endswith(".PDF"):
                    pdf = os.path.splitext(file)[0]
                    for subdir, dirs, files in os.walk(
                        r"D:\_MACIEK_\python_proby\p33\do_operatow"
                    ):
                        dirs.sort(key=nkey)
                        if ".00" in subdir:
                            obreb = subdir.split("\\")[5].split(".")[1]
                            if nrobr == obreb:
                                for file in natsorted(files):
                                    if file.upper().endswith(".WKT"):
                                        wkt = os.path.splitext(file)[0]
                                        if wkt == pdf:
                                            stad = os.path.join(subdir, file)
                                            nowy = os.path.join(glowny, file)
                                            try:
                                                shutil.copy(stad, nowy)
                                                print(
                                                    str(count)
                                                    + "\t"
                                                    + obreb
                                                    + "_"
                                                    + file
                                                )
                                                count += 1
                                            except:
                                                raise


def main():
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
    (6)   match_files_based_on_name_not_folder_only
    (7)   check_if_all_operat_from_list_matched
    (8)   find_duplicate_lines_in_cdc_file
    (9)   remove_from_cdc_lines_moved_to_duplicated
    (10)  copy_wkt_to_corresponding_operat_folder
    (11)  delete_successfuly_moved_files
    (12)  cleanup_more_than_one_fit
    (13)  check_for_pdf_equivalent_for_wkt
    (14)  check_error_wkt_creation_date
    (15)  check_wkt_structure
    (16)  merge_wkt_with_wrong_structure
    (17)  check_file_encoding_chardet
    (18)  check_file_encoding_universal_detector
    (19)  save_files_with_utf_8
    (20)  copy_wkt_files_to_sketches
    (21)  copy_wkt_files_to_required_documents
    (22)  check_for_wkt_to_wrong_files
    (23)  check_wkt_files_for_required_documents
    (24)  check_for_any_wkt_if_main_not_exists
    (25)  check_if_there_is_main_wkt
    (26)  move_modernization_wkt
> """
            )
        )
        for path in paths_list:
            execute_proper_function(function_number, path, error_file_path)


if __name__ == "__main__":
    main()
