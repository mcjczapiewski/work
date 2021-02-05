import os
from PIL import Image, ImageFont, ImageDraw

path = input("PATH:\n> ")

for subdir, dirs, files in os.walk(path):
    left_in_folder = len(os.listdir(subdir))
    for file in files:
        if file.lower().endswith((".jpg", ".jpeg")):
            print(left_in_folder)
            left_in_folder -= 1

            image_path = os.path.join(subdir, file)
            desired_format = "RGB"
            try:
                img = Image.open(image_path).convert(desired_format)
            except:
                print(file)
                continue
            img_w, img_h = img.size

            if img_w > 3000:
                font_size = int(img_w * img_h * 0.000015)
            elif img_w > 2000:
                font_size = int(img_w * img_h * 0.0000205)
            else:
                font_size = int(img_w * img_h * 0.000028)
            font_name = "calibri.ttf"
            title_font = ImageFont.truetype(font_name, font_size)
            state = os.path.basename(subdir)
            if state == "1":
                title_text = "istniejący"
            elif state == "2":
                title_text = "istniejący brak dostępu"
            elif state == "3":
                title_text = "zniszczony"
            elif state == "bez_stanu":
                continue

            img_editable = ImageDraw.Draw(img)
            text_w, text_h = img_editable.textsize(title_text, title_font)
            canva_size = (text_w, text_h)
            canva_color = (0, 0, 0, 0)
            canva_color_format = "RGBA"
            text_canva = Image.new(canva_color_format, canva_size, canva_color)

            text_image_to_rotate = ImageDraw.Draw(text_canva)
            placing_xy = (0, 0)
            text_color = (184, 22, 22, 160)
            text_image_to_rotate.text(placing_xy, title_text, text_color, font=title_font)

            rotation_value = 90
            text_image_rotated = text_canva.rotate(rotation_value, expand=1)
            text_image_rotated.load()
            # img =
            paste_in_x = int(img_w - text_h - img_w * 0.002)
            paste_in_y = int(img_h - text_w - img_h * 0.12)
            img.paste(
                text_image_rotated, (paste_in_x, paste_in_y), mask=text_image_rotated.split()[3],
            )
            img.save(image_path)
