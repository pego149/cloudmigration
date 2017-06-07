from abc import ABC, abstractmethod


class GlobalMethods(ABC):

    def readFromFile(self):
        pass

    def saveToFile(self):
        pass

    @abstractmethod
    def printName(self):
        raise NotImplemented

