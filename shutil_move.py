import os
import shutil

counter = 1
my_file = r"P:\cyfryzacja_powiat_inowroclawski\SKANY_II\040701_1\syt-wys_trasy\przenies.txt"  # noqa

with open(my_file, "r", encoding="utf-8") as paths:
    for line in paths:
        from_here, there = line.strip().split("\t")
        print(counter)
        try:
            if not os.path.exists(os.path.dirname(there)):
                os.makedirs(os.path.dirname(there))
            shutil.move(from_here, there)
        except:
            print(
                str(counter)
                + "\t~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\
~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                + line
            )
        counter += 1
