import os
from natsort import natsort_keygen

nkey = natsort_keygen()

xmls = r"\\Waw-dt1409\h\Inowrocław"  # noqa
count = how_much = 1
previous = ""


def if_xmls_or_pdfs(write_out, exists_extension, noexists_extension, file_name):
    if any(
        fname.upper().endswith(exists_extension)
        for fname in os.listdir(subdir)
    ) and not any(
        fname.upper().endswith(noexists_extension)
        for fname in os.listdir(subdir)
    ):
        with open(
            os.path.join(write_out, f"{file_name}.txt"),
            "a",
            encoding="utf-8",
        ) as bx:
            bx.write(subdir + "\n")


write_out = r"I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614\ZADANIE 4\kontrole_2020-07-06"
with open(
    r"I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614\ZADANIE 4\kontrole_2020-07-06\sciezki.txt",
    "r",
    encoding="utf-8",
) as sciezki:
    for line in sciezki:
        xmls = line.strip()

        for subdir, dirs, files in os.walk(xmls):
            dirs.sort(key=nkey)
            if how_much > 1:
                with open(
                    os.path.join(write_out, "ponad_1_xml_w_folderze.txt"),
                    "a",
                    encoding="utf-8",
                ) as nowy:
                    nowy.write(str(how_much) + "\t" + previous + "\n")
            if_xmls_or_pdfs(write_out, ".PDF", ".XML", "sa_pdf_brak_xml")
            if_xmls_or_pdfs(write_out, ".XML", ".PDF", "jest_xml_brak_pdf")
            how_much = 0
            for file in files:
                if file.upper().endswith(".XML"):
                    print(count)
                    count += 1
                    how_much += 1
            previous = subdir
