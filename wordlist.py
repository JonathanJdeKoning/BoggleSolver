import os
import json
class Wordlist:
    def __init__(self, filename):
        dirname = os.path.dirname(__file__)
        self.path = os.path.join(dirname, filename)
        self.data = set()
        self.invalidWords = []
        self.unsolvedWords = []
        self.loadWords()
        

    def loadWords(self):
        with open(self.path, "r") as file:
            for line in file.readlines():
                self.data.add(line.strip())


    def saveWords(self):
        with open(self.path, "w") as file:
            for word in self.data:
                file.write(f"{word}\n")

    
    def removeWords(self, words) -> None:
        for word in words:
            self.data.discard(word)


    def addWords(self, words) -> None:
        for word in words:
            if word[0] == "*": continue
            if word in self.data:
                print(f"Freaky Word: {word}")
            self.data.add(word.replace("qu", "q"))

    def updateWordlist(self):
        self.addWords(self.unsolvedWords)
        self.removeWords(self.invalidWords)
        self.unsolvedWords = []
        self.invalidWords = []
        self.saveWords()
