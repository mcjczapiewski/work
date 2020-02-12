import os
import regex
import io
from natsort import natsorted, natsort_keygen

nkey = natsort_keygen()

path = r"I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614\DĄBROWA BISKUPIA"
# path = r'D:\_MACIEK_\python_proby\p33\aktualizacja_xml\xml'
my_list = r"D:\_MACIEK_\python_proby\p33\aktualizacja_xml\my_list.txt"
count = 1

for subdir, dirs, files in os.walk(path):
    dirs.sort(key=nkey)
    if not any(fname.upper().endswith(".XML") for fname in os.listdir(subdir)):
        continue
    for file in natsorted(files):
        if file.upper().endswith(".XML"):
            my_lines = []
            xml = os.path.join(subdir, file)
            with io.open(my_list, "r", encoding="utf-8") as o_my_list:
                for line in o_my_list:
                    operat, pzg, jedn, nr, rok, sepnr, seprok = line.split(
                        "\t"
                    )
                    seprok = seprok.split("\n")[0]
                    if os.path.splitext(file)[0] == operat:
                        print(count)
                        count += 1
                        # with io.open(xml, "r", encoding="utf-8") as oxml:
                        #     for line in oxml:
                        #         if "pzg_idZgloszenia" in line:
                        #             line = regex.sub(
                        #                 r"(^.+?\>)(.*?)(\<.+$)",
                        #                 r"\g<1>" + pzg + r"\g<3>",
                        #                 line,
                        #             )
                        #             my_lines.append(line)
                        #         elif "idZgloszeniaJedn" in line:
                        #             line = regex.sub(
                        #                 r"(^.+?\>)(.*?)(\<.+$)",
                        #                 r"\g<1>" + jedn + r"\g<3>",
                        #                 line,
                        #             )
                        #             my_lines.append(line)
                        #         elif "idZgloszeniaNr" in line:
                        #             line = regex.sub(
                        #                 r"(^.+?\>)(.*?)(\<.+$)",
                        #                 r"\g<1>" + nr + r"\g<3>",
                        #                 line,
                        #             )
                        #             my_lines.append(line)
                        #         elif "idZgloszeniaRok" in line:
                        #             line = regex.sub(
                        #                 r"(^.+?\>)(.*?)(\<.+$)",
                        #                 r"\g<1>" + rok + r"\g<3>",
                        #                 line,
                        #             )
                        #             my_lines.append(line)
                        #         elif "idZgloszeniaSepJednNr" in line:
                        #             line = regex.sub(
                        #                 r"(^.+?\>)(.*?)(\<.+$)",
                        #                 r"\g<1>" + sepnr + r"\g<3>",
                        #                 line,
                        #             )
                        #             my_lines.append(line)
                        #         elif "idZgloszeniaSepNrRok" in line:
                        #             line = regex.sub(
                        #                 r"(^.+?\>)(.*?)(\<.+$)",
                        #                 r"\g<1>" + seprok + r"\g<3>",
                        #                 line,
                        #             )
                        #             my_lines.append(line)
                        #         else:
                        #             my_lines.append(line)
                        # with io.open(xml, "w", encoding="utf-8") as wxml:
                        #     for i in my_lines:
                        #         wxml.write(i)

            with io.open(xml, "r", encoding="utf-8") as oxml:
                if not any(
                    regex.match(r"^.*<nazwa></nazwa>.*$", line)
                    for line in oxml
                ):
                    continue
                print(count)
                count += 1
                oxml.seek(0)
                for line in oxml:
                    if "<nazwa></nazwa>" in line:
                        line = regex.sub(
                            r"(^.+?[>])(.*?)([<].+$)",
                            r"\g<1>TWÓRCA NIEZNANY\g<3>",
                            line,
                        )
                        my_lines.append(line)
                    else:
                        my_lines.append(line)
            with io.open(xml, "w", encoding="utf-8") as wxml:
                for i in my_lines:
                    wxml.write(i)
