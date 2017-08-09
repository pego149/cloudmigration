from globalMethods import GlobalMethods
import MainWindow as MainWindow
import json, yaml


class Generic(GlobalMethods):

    def __init__(self):
        self.name = "Generic class"

    def printName(self):
        print(self.name)

    def readFromFile(self, paFile):
        try:
            with open(paFile) as data_file:
                return data_file.read()

        except IOError:
            MainWindow.infoWindow("error", "Error in parsing JSON file - " + self.name)
            return ""

    def saveToFile(self, paFile, paString):
        try:
            file = open(paFile, 'w')
            file.write(paString)
        except IOError:
            MainWindow.infoWindow("error", "Error in saving file " + paFile)
            return False

        return True
