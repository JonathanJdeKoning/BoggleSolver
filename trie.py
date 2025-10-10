class Trie:
    def __init__(self):
        self.root = {}
    def add(self, word):
        head = self.root
        for c in word:
            if c not in head:
                head[c] = {}
            head = head[c]
        head["."] = word
