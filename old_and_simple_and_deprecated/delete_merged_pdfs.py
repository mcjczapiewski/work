import os
import regex
import shutil

for subdir, dirs, files in os.walk(
    r"D:\_MACIEK_\cyfryzacja_inowroclawski\kontrola_2020-04-17\040701_2"
):
    if any(
        regex.search(r".+_.+-.+-", fname) for fname in os.listdir(subdir)
    ) and "merge" in os.listdir(subdir):
        shutil.rmtree(os.path.join(subdir, "merge"))

    for file in files:
        if not regex.search("-.+-", file):
            os.remove(os.path.join(subdir, file))

    if os.listdir(subdir) == [os.path.basename(subdir)]:
        docelowy = subdir
        for subdir, dirs, files in os.walk(
            os.path.join(docelowy, os.path.basename(docelowy))
        ):
            if "merge" in subdir:
                shutil.move(
                    os.path.join(
                        docelowy, os.path.basename(docelowy), "merge"
                    ),
                    docelowy,
                )
            else:
                for file in files:
                    shutil.move(
                        os.path.join(
                            docelowy, os.path.basename(docelowy), file
                        ),
                        docelowy,
                    )
