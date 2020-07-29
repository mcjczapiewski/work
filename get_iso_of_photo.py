import os
from PIL import Image, ExifTags

for subdir, dirs, files in os.walk(r"D:\2019-11-18_RYN\zdjecia"):
    for file in files:
        img = Image.open(os.path.join(subdir, file))
        exif = {
            ExifTags.TAGS[k]: v
            for k, v in img._getexif().items()
            if k in ExifTags.TAGS
        }
        for item in exif:
            if "ISO" in item:
                iso = exif[item]
        img.close()
        print(iso)
        # os.rename(
        #     os.path.join(subdir, file),
        #     os.path.join(subdir, f"iso{iso}_{file}"),
        # )
