import os
from natsort import natsort_keygen

nkey = natsort_keygen()
again = "y"

path = input("\nEnter the path: ")
thumbs = input("Scan for and delete any 'Thumbs.db' file?  y/n: ")
print("\n")

while again == "y":
    delete = []
    number = 0

    # iterates through folders and adding to list empty once
    # deleting thumbs beforehand if user want it
    for subdir, dirs, _ in os.walk(path):
        dirs.sort(key=nkey)
        if "zrobione" not in subdir.lower():
            if thumbs.lower() == "y":
                thumb = os.path.join(subdir, "Thumbs.db")
                if os.path.exists(thumb):
                    os.remove(thumb)
            if not os.listdir(subdir):
                delete.append(subdir)
                print(str(number) + "\t" + subdir)
                number += 1

    # if there is something in list, ask to delete them
    if delete:
        is_it = input(
            """
Delete the listed folders? - y
End the program without deleting? - n
Remove some directories from list? - r
y/n/r: """
        )

        # iterates through list to remove some entries
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
                print(
                    ("\nNone directory was deleted. Action aborted.").upper()
                )
                pass
            is_it = input(
                """
Delete the remaining folders? - y
End the program without deleting? - n
Remove more directories from list? - r
y/n/r: """
            )
            # if user wants to remove more from list,
            # its printing the list
            if is_it.lower() == "r":
                number = 0
                for item in delete:
                    print(str(number) + "\t" + item)
                    number += 1

        # removing directories if user said so
        if is_it.lower() == "y":
            ile = 1
            for item in delete:
                os.rmdir(item)
                print(ile)
                ile += 1
            print("~~~THE END.~~~\n")
        # ends if user don't want to delete
        else:
            print("~~~THE END.~~~\n")

    else:
        print("~~~NO EMPTY FOLDERS.~~~\n")
        break

    # looping after deleting folders
    again = input("Again?  y/n: ")

print("~~~EXITED.~~~\n")
