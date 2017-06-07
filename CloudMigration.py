import MainWindow as MainWindow
import tkinter as tk
import glob


def wheel(param1, param2, param3, param4):
    # Checks
    if param2 == param4:
        MainWindow.infoWindow("error", "Unable to convert into same template.", "Error in types")
        return 1

    if param2 != 'Generic' and param4 != 'Generic':
        MainWindow.infoWindow("error", "One template format has to be \"Generic\"")
        return 1

    print("From: " + param1 + ", system " + param2)
    print("To: " + param3 + ", system " + param4)

    #pom1 = __import__(param2)
    #pom1.tests()

    # From module
    if param2 == "AWS":
        from mod_AWS import AWS as module1
    elif param2 == "OpenStack":
        from mod_OpenStack import OpenStack as module1
    else:
        from Generic import Generic as module1

    # To module
    if param4 == "AWS":
        from mod_AWS import AWS as module2
    elif param4 == "OpenStack":
        from mod_OpenStack import OpenStack as module2
    else:
        from Generic import Generic as module2

    mod1 = module1()
    mod1.printName()

    mod2 = module2()
    mod2.printName()

    return 0


def showLoadableModules(paramModules):

    for moduleName in glob.glob("mod_*"):
        moduleName = moduleName.partition("_")[2]
        paramModules.append(moduleName)

    return modules


# Main method
if __name__ == "__main__":

    # Create main window
    root = tk.Tk()

    modules = ["Generic"]

    if not MainWindow.setWindowProperties(root, showLoadableModules(modules)):
        MainWindow.infoWindow("error", "Error in creating main window.")
        exit(1)

    root.mainloop()
