import os

foldery = ['P.0418.1965.150', 'P.0418.1975.275']
sciezka = input('Podaj ścieżkę: ')

for subdir, dirs, _ in os.walk(sciezka):
    if any(fname.upper().endswith(('.JPG', '.JPEG')) for fname in os.listdir(subdir)):
        for i in foldery:
            if os.path.basename(subdir) == i:
                print(subdir)
