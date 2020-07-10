import cv2
import os

sprawdzanie = r"D:\cyfryzacja_zambrowski\proby"

for subdir, dirs, files in os.walk(sprawdzanie):
    dirs.sort()
    folder_glowny = subdir
    for file in sorted(files):
        if file.endswith(".jpg") or file.endswith(".jpeg"):
            pierwotne = file
            original = cv2.imread(os.path.join(folder_glowny, pierwotne))
            pierwsze = os.path.join(folder_glowny, pierwotne)
            for subdir, dirs, files in os.walk(sprawdzanie):
                dirs.sort()
                for file in sorted(files):
                    if file.endswith(".jpg") or file.endswith(".jpeg"):
                        porownane = file
                        drugie = os.path.join(subdir, porownane)
                        if pierwsze == drugie:
                            continue
                        else:
                            image_to_compare = cv2.imread(
                                os.path.join(subdir, porownane)
                            )

                            # 1) Check if 2 images are equals
                            try:
                                if original.shape == image_to_compare.shape:
                                    difference = cv2.subtract(
                                        original, image_to_compare
                                    )
                                    b, g, r = cv2.split(difference)

                                    if (
                                        cv2.countNonZero(b) == 0
                                        and cv2.countNonZero(g) == 0
                                        and cv2.countNonZero(r) == 0
                                    ):
                                        print(
                                            os.path.join(
                                                folder_glowny, pierwotne
                                            )
                                            + " and "
                                            + os.path.join(subdir, porownane)
                                            + " are completely Equal"
                                        )
                                    else:
                                        print(
                                            os.path.join(
                                                folder_glowny, pierwotne
                                            )
                                            + "\t"
                                            + os.path.join(subdir, porownane)
                                            + "\tnot the same"
                                        )

                                else:
                                    print(
                                        os.path.join(folder_glowny, pierwotne)
                                        + "\t"
                                        + os.path.join(subdir, porownane)
                                        + "\tnot the same"
                                    )

                            except:
                                print(
                                    os.path.join(folder_glowny, pierwotne)
                                    + " Nie porownano "
                                    + os.path.join(subdir, porownane)
                                )
