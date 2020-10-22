import os

main_dir = r"\\waw-dt1409\h\Inowrocław"
podgik_dir = r"I:\INOWROCŁAW\DANE PODGiK\SKANY OPERATÓW\gmina Inowroclaw\!OPERATY_KTÓRE_ODDAJEMY"  # noqa
list_of_folders = []
count = 1

for subdir, dirs, _ in os.walk(main_dir):
    print(count)
    count += 1
    if any(fname.upper().endswith(".PDF") for fname in os.listdir(subdir)):
        list_of_folders.append(os.path.basename(subdir))
    if os.path.basename(subdir) in os.listdir(podgik_dir):
        main_subdir = subdir
        if len([name for name in os.listdir(subdir)]) == len(
            [
                nam
                for nam in os.listdir(
                    os.path.join(podgik_dir, os.path.basename(subdir))
                )
            ]
        ):
            main_list = []
            podgik_list = []
            for subdir, dirs, files in os.walk(subdir):
                for file in files:
                    main_list.append(file)
            for subdir, dirs, files in os.walk(
                os.path.join(podgik_dir, os.path.basename(subdir))
            ):
                for file in files:
                    podgik_list.append(file)
            if not main_list == podgik_list:
                with open(
                    r"\\waw-dt1409\h\Inowrocław\!! KONTROLE\OPERATY_Z_PODGIK\tyle_samo_plikow_rozne_nazwy.txt",  # noqa
                    "a",
                    encoding="utf-8",
                ) as write_out:
                    write_out.write(
                        main_subdir
                        + "\t"
                        + os.path.join(podgik_dir, os.path.basename(subdir))
                        + "\n"
                    )
            else:
                with open(
                    r"\\waw-dt1409\h\Inowrocław\!! KONTROLE\OPERATY_Z_PODGIK\tyle_samo_plikow_identyczne_nazwy.txt",  # noqa
                    "a",
                    encoding="utf-8",
                ) as write_out:
                    write_out.write(
                        main_subdir
                        + "\t"
                        + os.path.join(podgik_dir, os.path.basename(subdir))
                        + "\n"
                    )
        elif len([name for name in os.listdir(subdir)]) > len(
            [
                nam
                for nam in os.listdir(
                    os.path.join(podgik_dir, os.path.basename(subdir))
                )
            ]
        ):
            with open(
                r"\\waw-dt1409\h\Inowrocław\!! KONTROLE\OPERATY_Z_PODGIK\wiecej_plikow_na_zewnetrznym.txt",  # noqa
                "a",
                encoding="utf-8",
            ) as write_out:
                write_out.write(
                    subdir
                    + "\t"
                    + os.path.join(podgik_dir, os.path.basename(subdir))
                    + "\n"
                )
        elif len([name for name in os.listdir(subdir)]) < len(
            [
                nam
                for nam in os.listdir(
                    os.path.join(podgik_dir, os.path.basename(subdir))
                )
            ]
        ):
            with open(
                r"\\waw-dt1409\h\Inowrocław\!! KONTROLE\OPERATY_Z_PODGIK\wiecej_plikow_z_podgik.txt",  # noqa
                "a",
                encoding="utf-8",
            ) as write_out:
                write_out.write(
                    subdir
                    + "\t"
                    + os.path.join(podgik_dir, os.path.basename(subdir))
                    + "\n"
                )

for subdir, dirs, _ in os.walk(podgik_dir):
    if os.path.basename(subdir) not in list_of_folders:
        with open(
            r"\\waw-dt1409\h\Inowrocław\!! KONTROLE\OPERATY_Z_PODGIK\operaty_z_podgik_brak_na_zewnetrznym.txt",  # noqa
            "a",
            encoding="utf-8",
        ) as write_out:
            write_out.write(subdir + "\n")
