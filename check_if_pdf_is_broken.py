import io
import os
import fitz

path = r"I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614\ZADANIE 2\GNIEWKOWO"  # noqa
write_out = r"I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614\ZADANIE 2\GNIEWKOWO\Kontrole\puste PDF\puste_uszkodzone.txt"  # noqa
write_out_big = r"I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614\ZADANIE 2\GNIEWKOWO\Kontrole\ciezsze_niz_500.txt"  # noqa
write_out_xmls = r"I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614\ZADANIE 2\GNIEWKOWO\Kontrole\wiecej_niz_1_xml.txt"  # noqa
count = 1

for subdir, dirs, files in os.walk(path):
    if not os.path.basename(subdir).startswith("P."):
        continue
    xmls = 0
    print(count)
    count += 1
    for file in files:
        if file.upper().endswith(".PDF"):
            pdf_file = os.path.join(subdir, file)
            try:
                doc = fitz.open(os.path.join(subdir, file))
                doc.close()
                if os.path.getsize(pdf_file) == 0:
                    with io.open(
                        write_out, "a", encoding="utf-8"
                    ) as write_errors:
                        write_errors.write(
                            str(os.path.getsize(pdf_file))
                            + "\t"
                            + pdf_file
                            + "\n"
                        )
            except RuntimeError:
                with io.open(write_out, "a", encoding="utf-8") as write_errors:
                    write_errors.write(
                        str(os.path.getsize(pdf_file)) + "\t" + pdf_file + "\n"
                    )
            except Exception as e:
                print(e)
            if os.path.getsize(pdf_file) > 500000000:
                with io.open(
                    write_out_big, "a", encoding="utf-8"
                ) as write_errors:
                    write_errors.write(pdf_file + "\n")

        elif file.upper().endswith(".XML"):
            xmls += 1
    if xmls > 1:
        with io.open(write_out_xmls, "a", encoding="utf-8") as write_xmls:
            write_xmls.write(str(xmls) + "\t" + subdir + "\n")
