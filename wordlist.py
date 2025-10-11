import os
import json
class Wordlist:
    def __init__(self, filename):
        dirname = os.path.dirname(__file__)
        self.path = os.path.join(dirname, filename)
        self.data = {}
        self.loadWords()
        

    def loadWords(self):
        with open(self.path, "r") as file:
            self.data = json.load(file)


    def saveWords(self):
        with open(self.path, "w") as file:
            json.dump(self.data, file, indent=2)

    
    def removeWords(self, words) -> None:
        for word in words:
            del self.data[word]


    def addWords(self, words) -> None:
        for word in words:
            self.data[word] = 1
        self.saveWords()
