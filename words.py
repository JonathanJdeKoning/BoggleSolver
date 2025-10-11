import json
from boggletrie import BoggleTrie


def loadWords(filepath: str) -> BoggleTrie:
    myTrie = BoggleTrie()
    with open(filepath, "r") as file:
        jsonData = json.load(file)
        for word in jsonData:
            myTrie.add(word)
    return myTrie


def removeWords(filepath: str, invalidWords: set[str]) -> None:
    with open(filepath, "r") as file:
        jsonData = json.load(file)
    for word in invalidWords:
        del jsonData[word]

    with open(filepath, "w") as file:
        json.dump(jsonData, file, indent=2)

def addWords(filepath: str, missedWords: list[str]) -> None:
    with open(filepath, "r") as file:
        jsonData = json.load(file)
    for word in missedWords:
        jsonData[word] = 1

    with open(filepath, "w") as file:
        json.dump(jsonData, file, indent=2)
