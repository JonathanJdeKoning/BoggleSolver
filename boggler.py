from boggledriver import BoggleDriver
from wordlist import Wordlist
import time
import subprocess
class Boggler:
    def __init__(self):
        self.boggleDriver = BoggleDriver()
        self.wordlist = Wordlist("wordlist.txt")
        self.board = []

    def getFormattedURL(self, size, difficulty):
        url = f"https://www.puzzle-words.com/boggle-{size}x{size}"
        if difficulty != "easy":
            url += f"-{difficulty}"
        url += "/"
        return url

    def playPuzzle(self, size, difficulty):
        url = self.getFormattedURL(size, difficulty)
        self.boggleDriver.goto(url)
        self.board = self.boggleDriver.findBoard(size)

        foundWords = self.findAllWords("turboBoggler.exe", size, self.board)

        self.inputWords(foundWords)
        print(f"Invalid: {self.wordlist.invalidWords}")
        self.wordlist.unsolvedWords = self.boggleDriver.getUnsolvedWords()
        print(f"Unsolved: {self.wordlist.unsolvedWords}")
        
        self.wordlist.updateWordlist()
        self.boggleDriver.newPuzzle()

    def inputWords(self, words):
        for word in words:    
            isValid = self.boggleDriver.inputWord(word)
            if not isValid:
                self.wordlist.invalidWords.append(word)

    def findAllWords(self, scriptName, size, board):
        boardString = "".join(["".join(row) for row in board])
        boardString = boardString.replace("qu", "q")
        process = subprocess.run([scriptName, boardString], shell=True, capture_output=True, text=True)
        output = process.stdout.split()
        print(output[0])
        return output[1:]