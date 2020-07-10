import os

count = 1

for subdir, dirs, files in os.walk(
    r"P:\cyfryzacja_powiat_inowroclawski\SKANY_III\20200527"
):
    dirs.sort()
    if (
        os.path.basename(subdir) in os.listdir(subdir)
        and "merge" not in subdir
    ):
        if subdir.split("\\")[6] not in (
            "040707_5.0010",
            "040707_5.0011",
            "040707_5.0002",
            "040707_5.0003",
            "040707_5.0004",
            "040707_5.0005",
        ):
            continue
        print(count)
        count += 1
        for file in files:
            if "wpg" not in file:
                os.remove(os.path.join(subdir, file))
