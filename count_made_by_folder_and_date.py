import os
import datetime
import regex

count_all = 0
path = r"P:\cyfryzacja_powiat_inowroclawski\SKANY_III"  # noqa
made_by_folder = {}
made_by_day = {}
previous_folder = ""
first_run = True
current_time = datetime.datetime.now().time()


def count_files_in_folder(count_all):
    for file in files:
        if file.upper().endswith(".PDF"):
            count_all += 1
            if current_folder not in made_by_folder:
                made_by_folder[current_folder] = 1
            else:
                made_by_folder[current_folder] += 1
    return count_all


print(f"\n{current_time.hour}:{str(current_time.minute).zfill(2)}")
for subdir, dirs, files in os.walk(path):
    if os.path.basename(subdir) in os.listdir(subdir):
        folder_creation_time = datetime.date.fromtimestamp(
            os.path.getctime(os.path.join(subdir, os.path.basename(subdir)))
        )
        folder_creation_time = regex.sub(
            r"^.+\((.+?), (.*?), (.+?)\).*",
            r"\g<1>-\g<2>-\g<3>",
            str(folder_creation_time),
        )
        subdir_splitted = subdir.split("\\")
        current_folder = fr"{subdir_splitted[3]}\{subdir_splitted[4]}\{subdir_splitted[5]}\{subdir_splitted[6]}"
        if first_run:
            previous_folder = current_folder
            the_day_before = folder_creation_time
            first_run = False

        if folder_creation_time == the_day_before:
            count_all = count_files_in_folder(count_all)
        else:
            if the_day_before in made_by_day:
                for key in made_by_folder:
                    if key in made_by_day[the_day_before]:
                        made_by_day[the_day_before][key] += made_by_folder[key]
                    else:
                        made_by_day[the_day_before][key] = made_by_folder[key]
            else:
                made_by_day[the_day_before] = made_by_folder
            the_day_before = folder_creation_time
            made_by_folder = {}
            count_all = count_files_in_folder(count_all)
if the_day_before in made_by_day:
    for key in made_by_folder:
        if key in made_by_day[the_day_before]:
            made_by_day[the_day_before][key] += made_by_folder[key]
        else:
            made_by_day[the_day_before][key] = made_by_folder[key]
else:
    made_by_day[the_day_before] = made_by_folder
# made_by_day[the_day_before] = made_by_folder
for key, value in sorted(made_by_day.items()):
    print(key)
    for item in sorted(value):
        print(f"\t\t{item}: {value[item]}")
print(count_all)
