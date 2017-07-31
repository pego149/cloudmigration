from globalMethods import GlobalMethods
import MainWindow as MainWindow
import yaml
from jsonschema import validate


class AWS_YAML(GlobalMethods):

    def __init__(self):
        self.name = "AWS YAML class"

    def printName(self):
        print(self.name)

    def readFromFile(self, paFile):
        try:
            file = open(paFile, 'r')
        except IOError:
            MainWindow.infoWindow("error", "Error in opening file " + paFile)
            return False

        try:
            string = file.read()
            #validate(yaml(string))

        except:
            MainWindow.infoWindow("error", "Error in parsing YAML file - " + self.name)
            return False

        return string


