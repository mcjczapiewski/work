# musi byc w folderze, w ktorym zawieraja sie podfoldery, folder nie moze
# nazywac sie 'test' ani byc tylko liczba

import os

for root, dirs, files in os.walk(r'D:\GESUT_BDOT_Otwock\TESTY\FOLDERY'):
    for file in files:
        if file.endswith('.txt'):
            # print file
            path = os.path.join(root, file)
            with open(path, 'a') as f:
                f.write('R:')
