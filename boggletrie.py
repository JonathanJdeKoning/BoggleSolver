class BoggleTrie:
    def __init__(self, words={}):
        self.root = {}
        self.addWords(words)

    def addWord(self, word: str) -> None:
        head = self.root
        for i, c in enumerate(word):
            toAdd = c

            if c == "q" and i < len(word) - 1 and word[i + 1] == "u":
                toAdd = "qu"
            if c == "u" and i > 0 and word[i - 1] == "q":
                continue

            if toAdd not in head:
                head[toAdd] = {}
            head = head[toAdd]
        head["."] = word

    def addWords(self, words):
        for word in words:
            self.addWord(word)
