from globalMethods import GlobalMethods
import MainWindow as MainWindow


class Generic(GlobalMethods):

    def __init__(self):
        self.name = "Generic class"

    def printName(self):
        print(self.name)

    def readFromFile(self, paFile):
        try:
            file = open(paFile, 'r')
        except IOError:
            MainWindow.infoWindow("error", "Error in parsing YAML file - " + self.name)
            return False

        return file.read()

    def saveToFile(self, paFile, paString):
        try:
            file = open(paFile, 'w')
            file.write(paString)
        except IOError:
            MainWindow.infoWindow("error", "Error in saving file " + paFile)
            return False

        return True
