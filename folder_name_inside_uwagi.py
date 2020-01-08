import os

print ('Podaj ścieżkę do fodleru:')
uwaga = input()

for subdir, dirs, files in os.walk(uwaga):
    for file in files:
        if file == 'uwagi.txt' or file == 'UWAGI.txt' or (file.endswith('.txt') and file.startswith('P.')):
            path = os.path.join(subdir, file)
            print(path)
            with open(path, 'r') as r:
                old = r.read()
            with open(path, 'w') as f:
                f.seek(0)
                f.write(subdir+'\n'+old)
