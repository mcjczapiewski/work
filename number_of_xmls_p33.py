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


write_out = r"\\waw-dt1407\I\04_KOPIA_PLIKOWA\kontrole_2020-06-30"
with open(
    r"\\waw-dt1407\I\04_KOPIA_PLIKOWA\kontrole_2020-06-30\sciezki.txt",
    "r",
    encoding="utf-8",
) as sciezki:
    for line in sciezki:
        xmls = line.strip()

        for subdir, dirs, files in os.walk(xmls):
            dirs.sort(key=nkey)
            if how_much > 1:
                with open(
                    os.path.join(write_out, "zaneta_4_ponad_1_xml_w_folderze.txt"),
                    "a",
                    encoding="utf-8",
                ) as nowy:
                    nowy.write(str(how_much) + "\t" + previous + "\n")
            if_xmls_or_pdfs(write_out, ".PDF", ".XML", "zaneta_4_sa_pdf_brak_xml")
            if_xmls_or_pdfs(write_out, ".XML", ".PDF", "zaneta_5_jest_xml_brak_pdf")
            how_much = 0
            for file in files:
                if file.upper().endswith(".XML"):
                    print(count)
                    count += 1
                    how_much += 1
            previous = subdir
