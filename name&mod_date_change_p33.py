import datetime
import os
import io

those_files = r"D:\_MACIEK_\python_proby\p33\dysk_zew.txt"
with_those = r"D:\_MACIEK_\python_proby\p33\dysk_v.txt"
differences = r"D:\_MACIEK_\python_proby\p33\wkt_differences.txt"
to_compare = r"D:\_MACIEK_\python_proby\p33\compare.txt"


def write_diffs():
    with io.open(differences, "a", encoding="utf-8") as diffs:
        diffs.write(line + "\n")


print("MAKING THE LIST...")
with io.open(those_files, "r", encoding="utf-8") as original:
    for line in original:
        ori_path = line.split("\n")[0]
        ori_number = (
            os.path.basename(os.path.dirname(ori_path))
            + "__"
            + os.path.basename(ori_path)
        )
        with io.open(with_those, "r", encoding="utf-8") as newer:
            for line in newer:
                new_path = line.split("\n")[0]
                new_number = (
                    os.path.basename(os.path.dirname(new_path))
                    + "__"
                    + os.path.basename(new_path)
                )
                if ori_number == new_number:
                    with io.open(to_compare, "a", encoding="utf-8") as compare:
                        compare.write(ori_path + "\t" + new_path + "\n")

print("COMPARING...")
with io.open(to_compare, "r", encoding="utf-8") as compare:
    for line in compare:
        original, new = line.split('\n')[0].split('\t')
        ori_wkt = new_wkt = break_it = 0
        for subdir, dirs, files in os.walk(original):
            ori_sub = subdir
            for file in files:
                if file.lower().endswith(".wkt"):
                    ori_name = file
                    ori_wkt_path = os.path.join(ori_sub, ori_name)
                    new_wkt_path = os.path.join(new, ori_name)
                    if not os.path.exists(new_wkt_path):
                        write_diffs()
                        break_it = 1
                        break
                    else:
                        ori_wkt_date = (
                            str(
                                datetime.datetime.fromtimestamp(
                                    os.path.getmtime(ori_wkt_path)
                                )
                            )
                        ).split(" ")[0]
                        new_wkt_date = (
                            str(
                                datetime.datetime.fromtimestamp(
                                    os.path.getmtime(new_wkt_path)
                                )
                            )
                        ).split(" ")[0]
                        if not ori_wkt_date == new_wkt_date:
                            write_diffs()
                            break_it = 1
                            break
                    ori_wkt += 1
            if break_it == 1:
                break
        for subdir, dirs, files in os.walk(new):
            for file in files:
                if file.lower().endswith(".wkt"):
                    new_wkt += 1
        if not new_wkt == ori_wkt:
            write_diffs()
            continue
        for subdir, dirs, files in os.walk(new):
            new_sub = subdir
            for file in files:
                if file.lower().endswith(".wkt"):
                    new_name = file
                    new_wkt_path = os.path.join(new_sub, new_name)
                    ori_wkt_path = os.path.join(original, new_name)
                    if not os.path.exists(ori_wkt_path):
                        write_diffs()
                        break_it = 1
                        break
                    else:
                        new_wkt_date = (
                            str(
                                datetime.datetime.fromtimestamp(
                                    os.path.getmtime(new_wkt_path)
                                )
                            )
                        ).split(" ")[0]
                        ori_wkt_date = (
                            str(
                                datetime.datetime.fromtimestamp(
                                    os.path.getmtime(ori_wkt_path)
                                )
                            )
                        ).split(" ")[0]
                        if not new_wkt_date == ori_wkt_date:
                            write_diffs()
                            break_it = 1
                            break
                    new_wkt += 1
            if break_it == 1:
                break

print("THE END.")
