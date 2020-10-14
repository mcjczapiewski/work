import os
from natsort import natsorted

count = 1
koniecWersji_date = input(
    "\nPodaj pełną datę końca wersji lub wciśnij ENTER\n\
Wciśnięcie ENTER ustawi datę na 2020-08-03T00:00:00\n> "
)
if not koniecWersji_date:
    koniecWersji_date = "2020-08-03T00:00:00"

xmls_path = input("Podaj ścieżkę do folderu z plikami xml:\n> ")

for _, _, files in os.walk(xmls_path):
    for file in natsorted(files):
        xml_path = os.path.join(xmls_path, file)
        xml_type = file.split("__")[1]
        ids_from_user = input(
            f"Wklej numery ID oddzielone przecinkami dla {xml_type}:\n> "
        )
        ids_list = [item_id for item_id in ids_from_user.split(",")]
        extracted_items = os.path.join(xmls_path, xml_type)

        with open(xml_path, "r", encoding="utf-8") as open_xml:
            temp_data = []
            skip_lines = 1
            for line in open_xml:
                if temp_data and skip_lines == 1:
                    with open(extracted_items, "a", encoding="utf-8",) as here:
                        print(count)
                        count += 1
                        for item in temp_data:
                            here.write(item)
                        temp_data.clear()
                if "</gml:featureMember>" in line and skip_lines == 0:
                    temp_data.append(line)
                    skip_lines = 1
                    continue
                if "<gml:featureMember>" in line and skip_lines == 1:
                    temp_data.append(line)
                    skip_lines = 0
                    continue
                elif (
                    not any(single_id in line for single_id in ids_list)
                    and skip_lines == 0
                    and "lokalnyId" in line
                ):
                    temp_data.clear()
                    skip_lines = 1
                elif "</bt:BT_CyklZyciaInfo>" in line and skip_lines == 0:
                    koniecWersji = f"\t\t\t\t\t<bt:koniecWersjiObiektu>\
{koniecWersji_date}</bt:koniecWersjiObiektu></bt:BT_CyklZyciaInfo>\n"
                    temp_data.append(koniecWersji)
                elif skip_lines == 0:
                    temp_data.append(line)
