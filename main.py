import time
from itertools import batched, pairwise
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from words import loadWords

def startDriver(url):
    try:
        service = Service(ChromeDriverManager().install())
        chrome_options = Options()
        chrome_options.page_load_strategy = 'eager'
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(url)
        time.sleep(2)
        return driver
    except Exception as e:
        print(f"An error occurred: {e}")


def findLetters():
    letterElements = driver.find_elements(By.CLASS_NAME,'diceface')
    letters = [element.text.lower() for element in letterElements]
    return letters


def splitArr(arr, n):
    return list(batched(arr, n))


def findValidWords(letters, trie):
    N = len(letters)
    directions = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

    validWords = set()
    def dfs(y, x, trieNode, path):

        if "." in trieNode:
            validWords.add(trieNode["."])
            del trieNode["."]

        path.add((y, x))

        for dy, dx in directions:
            ny, nx = y+dy, x+dx

            if (ny, nx) in path:
                continue
            if ny<0 or nx<0:
                continue
            if ny==N or nx==N:
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

            dfs(i, j, trie.root[cell], {(i,j)})
    
    return list(validWords)


def inputWords(words):
    inputBox = driver.find_element(By.ID, "wordInput")
    for word in words:
        inputBox.send_keys(word)
        inputBox.send_keys(Keys.RETURN)

if __name__ == "__main__":
    url = "https://www.puzzle-words.com/boggle-5x5-hard/"
    wordsFilepath = "C:/Trash Heap/boggle/wordlist.json"

    driver = startDriver(url)
    letters = splitArr(findLetters(), 5)
    trie = loadWords(wordsFilepath)
    validWords = findValidWords(letters, trie)
    inputWords(sorted(validWords))

