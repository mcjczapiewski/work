import os
import regex
from PIL import Image, ImageFont, ImageDraw

path = input("PATH:\n> ")

for subdir, dirs, files in os.walk(path):
    left_in_folder = len(os.listdir(subdir))
    font_size = 150
    font_name = "calibri.ttf"
    title_font = ImageFont.truetype(font_name, font_size)
    for file in files:
        if file.lower().endswith((".jpg", ".jpeg")):
            print(left_in_folder)
            left_in_folder -= 1
            image_path = os.path.join(subdir, file)
            img = Image.open(image_path)
            title_text = regex.search("(^.+)-.+", file)[1]
            img_editable = ImageDraw.Draw(img)
            placing_xy = (50, 50)
            color_rgb = (184, 22, 22)
            img_editable.text(placing_xy, title_text, color_rgb, font=title_font)
            img.save(image_path)
