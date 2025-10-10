class BoggleTrie:
    def __init__(self):
        self.root = {}

    def add(self, word):
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
