import os

count = 1
p_operat = p_grupa = ""

# with open(
#     r"D:\_MACIEK_\python_proby\grupa_po_wloclawek\lista.txt", "r"
# ) as lista:
#     for line in lista:
#         uid, operat, grupa, nic = line.split("\t")
#         print(count)
#         count += 1
#         usun = 0
#         nowy = os.path.join(
#             r"D:\_MACIEK_\python_proby\grupa_po_wloclawek\nowe",
#             str(operat) + ".txt",
#         )
#         if operat == p_operat:
#             if grupa > p_grupa:
#                 with open(nowy, "w") as nowe:
#                     nowe.write(
#                         str(uid)
#                         + "\t"
#                         + str(operat)
#                         + "\t"
#                         + str(grupa)
#                         + "\n"
#                     )
#                 p_grupa = grupa
#                 continue
#             elif grupa == p_grupa and int(grupa) != 1:
#                 with open(nowy, "a") as nowe:
#                     nowe.write(
#                         str(uid)
#                         + "\t"
#                         + str(operat)
#                         + "\t"
#                         + str(grupa)
#                         + "\n"
#                     )
#         else:
#             p_operat = operat
#             p_grupa = grupa


with open(
    r"D:\_MACIEK_\python_proby\grupa_po_wloclawek\nowe.txt", "a"
) as nowe:
    for _, _, files in os.walk(
        r"D:\_MACIEK_\python_proby\grupa_po_wloclawek\nowe"
    ):
        for file in files:
            stad = os.path.join(
                r"D:\_MACIEK_\python_proby\grupa_po_wloclawek\nowe", file
            )
            with open(stad, "r") as stad:
                for line in stad:
                    nowe.write(line.split("\t")[0] + "\n")
