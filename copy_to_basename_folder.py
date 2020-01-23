import os
import io
import shutil

_list = r"D:\_MACIEK_\python_proby\powtarzajace_operaty\lista.txt"
_dest = input("Enther the path to copy files to: ")
_count = 1

with io.open(_list, "r", encoding="utf-8") as _takeit:
    for line in _takeit:
        _from = line.split("\n")[0]
        _to = os.path.join(
            _dest,
            os.path.basename(_from),
            _from.split("cyfryzacja_powiat_wloclawski\\")[1],
        )
        print(_to)
        shutil.copytree(_from, _to)
