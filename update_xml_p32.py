import os

# import shutil
import lxml.etree as ET

paths = []

for path in paths:
    for subdir, dirs, files in os.walk(path):
        for file in files:
            if not file.endswith(".xml"):
                continue
            # shutil.copy(os.path.join(subdir, file), r'D:\_MACIEK_\python_proby')
            lines = ""
            xml_file = os.path.join(subdir, file)
            my_namespaces = dict(
                [
                    node
                    for _, node in ET.iterparse(xml_file, events=["start-ns"])
                ]
            )

            with open(xml_file, "r", encoding="utf-8") as xml:
                wodgik = "Wojewódzki Ośrodek Dokumentacji Geodezyjnej i Kartograficznej w Łodzi"
                marszalek = "Marszałek"
                wodgik_count = 0
                skip = 0
                ulica = 0
                for line in xml:
                    if wodgik in line:
                        wodgik_count += 1
                    if "<gmd:pointOfContact>" in line and wodgik_count == 2:
                        lines += line
                        skip = 1
                        continue
                    elif "</gmd:pointOfContact>" in line and skip == 1:
                        lines += line
                        skip = 0
                        continue
                    elif skip == 1:
                        continue
                    elif marszalek in line:
                        ulica = 1
                        lines += line
                        continue
                    elif ulica == 1 and "ul. Solna 14" in line:
                        lines += "\t\t\t\t\t\t\t\t\t\t<gco:CharacterString>al. Piłsudskiego 8</gco:CharacterString>\n"
                        continue
                    elif ulica == 1 and "91-423" in line:
                        lines += "\t\t\t\t\t\t\t\t\t\t<gco:CharacterString>90-051</gco:CharacterString>\n"
                        ulica = 0
                        continue
                    else:
                        lines += line

            with open(xml_file, "w", encoding="utf-8") as xml:
                xml.write(lines)

            ET.register_namespace = my_namespaces
            tree = ET.parse(xml_file)

            with open(xml_file, "wb") as openfile:
                tree.write(openfile, encoding="UTF-8", xml_declaration=True)
