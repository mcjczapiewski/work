import os
from natsort import natsort_keygen

nkey = natsort_keygen()

path = input("\nEnter the path: ")
print("\n")
delete = []
number = 0

for subdir, dirs, _ in os.walk(path):
    dirs.sort(key=nkey)
    if "zrobione" not in subdir.lower() and not os.listdir(subdir):
        delete.append(subdir)
        print(str(number) + "\t" + subdir)
        number += 1

if delete:
    is_it = input(
        """
Delete the listed folders? - y
End the program without deleting? - n
Remove some directories from list? - r
y/n/r: """
    )

    while is_it.lower() == "r":
        which = input(
            """
Which line do you want to delete?
Press any key but number from list if you want to abort.
Go from the last to first number while deleting: """
        )
        try:
            delete.pop(int(which))
        except (ValueError, IndexError):
            print(("\nNone directory was deleted. Action aborted.").upper())
            pass
        is_it = input(
            """
Delete the remaining folders? - y
End the program without deleting? - n
Remove more directories from list? - r
y/n/r: """
        )
        if is_it.lower() == "r":
            number = 0
            for item in delete:
                print(str(number) + "\t" + item)
                number += 1

    if is_it.lower() == "y":
        ile = 1
        for item in delete:
            os.rmdir(item)
            print(ile)
            ile += 1
        print("~~~THE END.~~~\n")

    else:
        print("~~~THE END.~~~\n")

else:
    print("~~~NO EMPTY FOLDERS.~~~\n")
