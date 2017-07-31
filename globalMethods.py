from abc import ABC, abstractmethod
import MainWindow as MainWindow


class GlobalMethods(ABC):

    @abstractmethod
    def readFromFile(self, paFile):
        raise NotImplemented

    @staticmethod
    def saveToFile(paFile, paString):
        try:
            file = open(paFile, 'w')
            file.write(paString)
        except IOError:
            MainWindow.infoWindow("error", "Error in saving file " + paFile)
            return False

        return True

    @abstractmethod
    def printName(self):
        raise NotImplemented

