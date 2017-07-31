import MainWindow as MainWindow
import tkinter as tk
import glob
import gc


def doTransformation(param1, param2, param3, param4):
    # Checks
    if param2 == param4:
        MainWindow.infoWindow("error", "Unable to convert into same template.", "Error in types")
        return 1

    if param2 != 'Generic' and param4 != 'Generic':
        MainWindow.infoWindow("error", "One template format has to be \"Generic\"")
        return 1

    # pom1 = __import__(param2)
    # pom1.tests()

    # From module
    if param2 == "AWS_JSON":
        from mod_AWS_JSON import AWS_JSON as module1
    elif param2 == "AWS_YAML":
        from mod_AWS_YAML import AWS_YAML as module1
    elif param2 == "OpenStack":
        from mod_OpenStack import OpenStack as module1
    else:
        from Generic import Generic as module1

    # To module
    if param4 == "AWS_JSON":
        from mod_AWS_JSON import AWS_JSON as module2
    elif param4 == "AWS_YAML":
        from mod_AWS_YAML import AWS_YAML as module2
    elif param4 == "OpenStack":
        from mod_OpenStack import OpenStack as module2
    else:
        from Generic import Generic as module2

    mod1 = module1()
    mod2 = module2()


    # string = mod1.readFromFile(param1)
    # if not string:
    #     return 1

    mod1.saveToFile(param3, mod1.readFromFile(param1))

    # print(string)

    # mod2.printName()




    # saves string to file
    # mod2.saveToFile(param3, string)

    MainWindow.infoWindow("info", "Successfully done!")

    exit(0)

    return 0


def showLoadableModules(paramModules):
    """

    :param paramModules:
    :return:
    """

    # Find everything, what starts with "mod_"
    for moduleName in glob.glob("mod_*"):
        moduleName = moduleName.partition("_")[2]
        paramModules.append(moduleName)

    return modules


# Main method
if __name__ == "__main__":

    gc.set_debug(0)

    # Create main window
    root = tk.Tk()

    # Array with module names
    modules = ["Generic"]

    if not MainWindow.setWindowProperties(root, showLoadableModules(modules)):
        MainWindow.infoWindow("error", "Error in creating main window.")
        exit(1)

    root.mainloop()
