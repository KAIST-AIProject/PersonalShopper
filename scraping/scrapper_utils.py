import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import pickle
from bs4 import BeautifulSoup
import re


def check_exists_element_and_return_text(driver, selector):
    try:
        element = driver.find_element(By.CSS_SELECTOR, selector)
    except NoSuchElementException:
        return None
    return element.get_attribute("textContent")

def scroll_down_to_end(driver, height = -1):
    SCROLL_PAUSE_TIME = 0.7

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
    if height!=-1:
        driver.execute_script("window.scrollTo(0, {})".format(last_height-height))

def cost_only_number(cost_s):
    cost_num = re.sub(pattern=r'\D',repl='', string=cost_s)
    return cost_num

def cal_sale(currcost_s, precost_s):
    currcost = int(currcost_s)
    precost = int(precost_s)

    sale = str((precost-currcost)/precost*100) + "%"
    return sale