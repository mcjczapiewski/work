import io
import os
import chardet
from natsort import natsort_keygen

nkey = natsort_keygen()

_all_ = ""
count = 1

for subdir, dirs, _ in os.walk(r"P:\cyfryzacja_powiat_wloclawski\wielkie_ponad_20\DO_BAZY\N"):  # noqa
    dirs.sort(key=nkey)
    opis = os.path.join(subdir, "opis.txt")
    if os.path.exists(opis):
        print(count)
        count += 1
        try:
            with io.open(
                opis,
                "r",
                encoding="utf-8"
            ) as zle:
                _all_ = zle.read()

        except UnicodeDecodeError:
            try:
                with open(
                    opis,
                    "r"
                ) as zle:
                    _all_ = zle.read()

            except UnicodeDecodeError:
                rawdata = open(opis, "rb").read()
                result = chardet.detect(rawdata)
                charenc = result["encoding"]
                if not charenc:
                    charenc = "utf-8"
                elif charenc == "ISO-8859-9":
                    charenc = "Windows-1250"
                elif charenc.startswith("ISO"):
                    charenc = "ISO-8859-2"
                elif charenc.startswith("Windows"):
                    charenc = "Windows-1250"
                try:
                    with io.open(
                        opis,
                        "r",
                        encoding=charenc
                    ) as zle:
                        _all_ = zle.read()
                except:
                    print(subdir)
        except:
            print(subdir)
            continue

        if _all_:
            with io.open(
                opis,
                "w",
                encoding="Windows-1250"
            ) as _good_once:
                _good_once.write(_all_)
