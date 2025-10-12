from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from time import sleep
from itertools import batched

from typing import Any

class BoggleDriver:
    def __init__(self):
        service = Service(ChromeDriverManager().install())
        chromeOptions = Options()
        chromeOptions.page_load_strategy = "eager"
        chromeOptions.add_experimental_option("detach", True)

        driver = webdriver.Chrome(service=service, options=chromeOptions)
        driver.maximize_window()
        
        self.driver = driver
       

    def goto(self, url):
        self.driver.get(url)
        self.inputElement = self.findInputElement()
        self.scoreElement = self.findScoreElement()



    def findBoard(self, size: int) -> list[str]:
        letterElements = []
        while len(letterElements) != size * size:
            letterElements = self.driver.find_elements(By.CLASS_NAME, "diceface")
            sleep(1)
        letters = [element.text.lower() for element in letterElements]
        board = list(batched(letters, size))
        return board


    def findInputElement(self) -> Any:
        return self.driver.find_element(By.ID, "wordInput")


    def findScoreElement(self) -> Any:
        return self.driver.find_element(By.CLASS_NAME, "score-points-value")
    

    def findNewPuzzleButton(self):
        return self.driver.find_element(By.ID, "btnNew");


    def newPuzzle(self):
        newPuzzleButton = self.findNewPuzzleButton()
        newPuzzleButton.click()

    def clickDoneButton(self):
        doneButton = self.driver.find_element(By.ID, "btnReady")
        doneButton.click()
    
    def clickSolutionButton(self):
        showSolutionLink = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div[3]/div[2]/a"))
        )
        showSolutionLink.click()
    
    def waitForWordElements(self):
        solvedWord = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".word.solved"))
        )
    

    def findUnsolvedWordsElements(self):
        return self.driver.find_elements(By.CSS_SELECTOR, "div.word:not(div.word.solved)")

    def getUnsolvedWords(self):
        self.clickDoneButton()
        self.clickSolutionButton()
        self.waitForWordElements()
        unsolvedWordsElements = self.findUnsolvedWordsElements() 
        unsolvedWords = [element.text.strip().split()[0] for element in unsolvedWordsElements]
        return unsolvedWords


    def getScore(self):
        return self.scoreElement.text

    
    def inputWord(self, word: str) -> bool:
        oldScore = self.getScore()
        self.inputElement.send_keys(word)
        self.inputElement.send_keys(Keys.RETURN)
        newScore = self.getScore()
        return newScore != oldScore

