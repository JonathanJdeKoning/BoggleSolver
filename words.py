import json
from boggletrie import BoggleTrie


def loadWords(filepath: str) -> BoggleTrie:
    myTrie = BoggleTrie()
    with open(filepath, "r") as file:
        jsonData = json.load(file)
        for word in jsonData:
            myTrie.add(word)
    return myTrie


def removeInvalidWords(filepath: str, invalidWords: set) -> None:
    with open(filepath, "r") as file:
        jsonData = json.load(file)
    for word in invalidWords:
        del jsonData[word]

    with open(filepath, "w") as file:
        json.dump(jsonData, file, indent=2)
