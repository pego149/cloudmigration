from abc import ABC, abstractmethod


def pprint(*args, **kwargs):
    printToConsole = 0
    if printToConsole:
        print(*args, **kwargs)


class GlobalMethods(ABC):

    @abstractmethod
    def readFromFile(self, paFile):
        raise NotImplemented

    @abstractmethod
    def saveToFile(self, paFile, paString):
        raise NotImplemented

    @abstractmethod
    def printName(self):
        raise NotImplemented

