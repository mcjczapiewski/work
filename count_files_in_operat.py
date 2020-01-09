import os

for subdir, dirs, files in os.walk(r'H:\ETAP_2.1_WLOCLAWEK\SKANY'):
    if not any(fname.upper().endswith('.JPG') for fname in os.listdir(subdir))\
            or 'DOKUM' in subdir:
        continue
    count = 0
    for file in files:
        if file.upper().endswith('.JPG'):
            count += 1
    print(os.path.basename(subdir) + '\t' + str(count))
