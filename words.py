import json
from trie import Trie

def loadWords(filepath):
    myTrie = Trie()
    with open(filepath, "r") as file:
        jsonData = json.load(file)
        for word in jsonData:
            myTrie.add(word)
    return myTrie
