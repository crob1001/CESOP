import sys

import gui

__author__ = "Christian Roberts"

if __name__ == '__main__':
    sys.exit(gui.runGui())
    print(">>> 1: Gui    2: NoGui    3: Quit")
    while(True):
        uIn = input(">>> ")
        match(uIn):
            case "1":
                # subprocess.run(["python", Path(sys.argv[0]).parent.absolute().__str__() + "/GUI.py"])
                sys.exit(gui.runGui())
                break
            