from boggledriver import BoggleDriver
from wordlist import Wordlist
from boggletrie import BoggleTrie

class Boggler:
    def __init__(self):
        self.boggleDriver = BoggleDriver()
        self.wordlist = Wordlist("wordlist.json")
        self.trie = BoggleTrie(self.wordlist.data)
        self.board = []

    def getFormattedURL(self, size, difficulty):
        url = f"https://www.puzzle-words.com/boggle-{size}x{size}"
        if difficulty != "easy":
            url += f"-{difficulty}"
        url += "/"
        return url

    def playPuzzle(self, size, difficulty):
        self.wordlist.loadWords()
        url = self.getFormattedURL(size, difficulty)
        self.boggleDriver.goto(url)
        self.board = self.boggleDriver.findBoard(size)

        foundWords = self.findAllWords()
        self.inputWords(foundWords)
        print(f"Invalid: {self.wordlist.invalidWords}")
        self.wordlist.unsolvedWords = self.boggleDriver.getUnsolvedWords()
        print(f"Unsolved: {self.wordlist.unsolvedWords}")
        
        self.wordlist.updateWordlist()
        self.trie.addWords(foundWords)
        self.boggleDriver.newPuzzle()

    def inputWords(self, words):
        for word in words:    
            isValid = self.boggleDriver.inputWord(word)
            if not isValid:
                self.wordlist.invalidWords.append(word)

    def findAllWords(self) -> set:
        N = len(self.board)
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        foundWords = []

        def dfs(y: int, x: int, trieNode, path) -> None:
            if "." in trieNode:
                foundWords.append(trieNode["."])
                del trieNode["."]

            path.add((y, x))

            for dy, dx in directions:
                ny, nx = y + dy, x + dx

                if (ny, nx) in path:
                    continue
                if ny < 0 or nx < 0:
                    continue
                if ny == N or nx == N:
                    continue
                if self.board[ny][nx] not in trieNode:
                    continue

                dfs(ny, nx, trieNode[self.board[ny][nx]], path)
            path.discard((y, x))

        for i in range(N):
            for j in range(N):
                cell = self.board[i][j]
                if cell not in self.trie.root:
                    continue

                dfs(i, j, self.trie.root[cell], {(i, j)})

        return foundWords 


