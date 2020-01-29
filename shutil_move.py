import os
import shutil
import io

i = 1
my_file = r"P:\cyfryzacja_powiat_wloclawski\ETAP_3\wloclawek_gmina\przenies.txt"  # noqa

with io.open(my_file, "r", encoding="utf-8") as paths:
    for line in paths:
        from_here = line.split("\t")[0]
        there = (line.split("\t")[1]).split("\n")[0]
        print(i)
        try:
            if not os.path.exists(os.path.dirname(there)):
                os.makedirs(os.path.dirname(there))
            shutil.move(from_here, there)
        except:
            print(
                str(i)
                + "\t~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\
~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                + line
            )
        i += 1
