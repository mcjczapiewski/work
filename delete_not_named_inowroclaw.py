import os

count = 1

for subdir, dirs, files in os.walk(
    r"P:\cyfryzacja_powiat_inowroclawski\SKANY_III\20200527\040707_5\prawne\040707_5.0008"
):
    dirs.sort()
    if (
        os.path.basename(subdir) in os.listdir(subdir)
        and "merge" not in subdir
    ):
        # if subdir.split("\\")[6] not in (
        #     "040707_5.0001",
        #     "040707_5.0009",
        #     "040707_5.0013",
        #     "040707_5.0014",
        #     "040707_5.0015",
        # ):
        #     continue
        print(count)
        count += 1
        for file in files:
            if "wpg" not in file:
                os.remove(os.path.join(subdir, file))
