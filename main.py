import time
import os
from itertools import batched, pairwise
from typing import List, Tuple, Any
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from words import loadWords, removeInvalidWords
from boggletrie import BoggleTrie
from collections import defaultdict

driver = None


def startDriver(url: str) -> Any:
    try:
        service = Service(ChromeDriverManager().install())
        chrome_options = Options()
        chrome_options.page_load_strategy = "eager"
        chrome_options.add_experimental_option("detach", True)

        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(url)
        return driver
    except Exception as e:
        print(f"An error occurred: {e}")


def findLetters(N: int) -> List[str]:
    letterElements = []
    while len(letterElements) != N * N:
        letterElements = driver.find_elements(By.CLASS_NAME, "diceface")
        time.sleep(1)
    letters = [element.text.lower() for element in letterElements]
    return letters


def findInput() -> Any:
    return driver.find_element(By.ID, "wordInput")


def findScore() -> Any:
    return driver.find_element(By.CLASS_NAME, "score-points-value")


def splitArr(arr: List[List], n: int) -> List[Tuple[str]]:
    return list(batched(arr, n))


def findWords(letters: List[Tuple[str]], trie: BoggleTrie) -> set:
    N = len(letters)
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    invalidWords = set()

    def dfs(y: int, x: int, trieNode: dict[str], path: set[Tuple[int, int]]) -> None:

        if "." in trieNode:
            word = trieNode["."]
            isValid = inputWord(word)
            if not isValid:
                invalidWords.add(word)

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
            if letters[ny][nx] not in trieNode:
                continue

            dfs(ny, nx, trieNode[letters[ny][nx]], path)
        path.discard((y, x))

    for i in range(N):
        for j in range(N):
            cell = letters[i][j]
            if cell not in trie.root:
                continue

            dfs(i, j, trie.root[cell], {(i, j)})

    return invalidWords


def inputWord(word: str) -> bool:
    oldScore = score.text
    inputBox.send_keys(word)
    inputBox.send_keys(Keys.RETURN)
    newScore = score.text

    return newScore != oldScore


if __name__ == "__main__":
    N = 5
    difficulty = "hard"
    url = f"https://www.puzzle-words.com/boggle-{N}x{N}-{difficulty}/"
    
    dirname = os.path.dirname(__file__)
    wordsFilepath = os.path.join(dirname, 'wordlist.json')

    driver = startDriver(url)
    letters = splitArr(findLetters(N), N)
    inputBox = findInput()
    score = findScore()
    trie = loadWords(wordsFilepath)
    invalidWords = findWords(letters, trie)
    removeInvalidWords(wordsFilepath, invalidWords)
