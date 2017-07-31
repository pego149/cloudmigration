from globalMethods import GlobalMethods
import MainWindow as MainWindow


class OpenStack(GlobalMethods):

    def __init__(self):
        self.name = "OpenStack class"

    def printName(self):
        print(self.name)

    def readFromFile(self, paFile):
        try:
            file = open(paFile, 'r')
        except IOError:
            MainWindow.infoWindow("error", "Error in parsing YAML file - " + self.name)
            return False

        return file.read()
