import MainWindow as MainWindow
import tkinter as tk
import glob


def doTransformation(fromFile, fromModule, toFile, toModule):
    # Checks
    if fromModule == toModule:
        MainWindow.infoWindow("error", "Unable to convert into same template.", "Error in types")
        return 1

    # From module
    if fromModule == "AWS":
        from mod_AWS import AWS as module1
    elif fromModule == "OpenStack":
        from mod_OpenStack import OpenStack as module1
    else:
        from Generic import Generic as module1

    # To module
    if toModule == "AWS":
        from mod_AWS import AWS as module2
    elif toModule == "OpenStack":
        from mod_OpenStack import OpenStack as module2
    else:
        from Generic import Generic as module2

    # make instances from modules
    mod1 = module1()
    mod2 = module2()

    # Creating generic JSON from original file
    genericString = mod1.readFromFile(fromFile)

    # Saving into platform specific file
    mod2.saveToFile(toFile, genericString)

    MainWindow.infoWindow("info", "Successfully done!")

    exit(0)

    return 0


def showLoadableModules(paModules):
    """
    Search for all modules. If the name of directory starts with "mod_", it is treated as a python module and the name
    is appended to the array get by the parameter.
    :param paModules: array, to which are names of modules appended
    :return: array given by parameter with module names added
    """

    # Find everything, what starts with "mod_"
    for moduleName in glob.glob("mod_*"):
        # append substring started with fourth letter (cut the "mod_" part)
        paModules.append(moduleName[4:])

    return paModules


# Main method
if __name__ == "__main__":

    # Create main window
    root = tk.Tk()

    # Array with module names
    modules = ["Generic"]

    if not MainWindow.setWindowProperties(root, showLoadableModules(modules)):
        MainWindow.infoWindow("error", "Error in creating main window.")
        exit(1)

    root.mainloop()
