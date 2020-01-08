# -*- coding: cp1250 -*-
from PIL import Image
import os
rootdir = '2111.1-3-2007'
separa = (' ')
A4 = 0
A3 = 0
for subdir, dirs, files in os.walk(rootdir):
	for file in files:
		if file.endswith('.jpg'):
			filename = os.path.join(subdir, file)
			img = Image.open(filename)
			width, height = img.size
			if width >= 2460 and width <= 2482 and height >= 3500 and height <= 3510 or width >= 3500 and width <= 3510 and height >= 2460 and height <= 2482:
				A4 += 1
				if img.info.get('dpi'):
					xdpi, ydpi = img.info['dpi']
					print xdpi
			elif width >= 3500 and width <= 3515 and height >= 4950 and height <= 5005 or width >= 4950 and width <= 5005 and height >= 3500 and height <= 3515:
				A3 += 1
			else:
				print width, '-', height, separa, filename
print 'A4:', A4, 'A3:', A3
