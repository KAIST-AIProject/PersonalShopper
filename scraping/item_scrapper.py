import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pickle

from selenium.common.exceptions import NoSuchElementException

def check_exists_element(driver, selector):
    try:
        driver.find_element(By.CSS_SELECTOR, selector)
    except NoSuchElementException:
        return False
    return True



def Naver_selenium_scraper(url, save_path):
    co = Options()
    co.add_experimental_option("debuggerAddress", "127.0.0.1:9222") ## 
    driver = webdriver.Chrome(options=co)
    driver.get(url)
    # driver.implicitly_wait(3) ## 연결 후 3초간 기다리기


    
    #문서 끝까지 스크롤
    SCROLL_PAUSE_TIME = 0.5

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


    item_info = dict()

    item_info['상품명'] = driver.find_element(By.CSS_SELECTOR, '#content > div > div._2-I30XS1lA > div._2QCa6wHHPy > fieldset > div._3k440DUKzy > div._1eddO7u4UC > h3').text
    if check_exists_element(driver, '#content > div > div._2-I30XS1lA > div._2QCa6wHHPy > fieldset > div._3k440DUKzy > div.WrkQhIlUY0 > span'):
        item_info['할인율'] = driver.find_element(By.CSS_SELECTOR, '#content > div > div._2-I30XS1lA > div._2QCa6wHHPy > fieldset > div._3k440DUKzy > div.WrkQhIlUY0 > span').text
    if check_exists_element(driver, '#content > div > div._2-I30XS1lA > div._2QCa6wHHPy > fieldset > div._3k440DUKzy > div.WrkQhIlUY0 > div > del > span._1LY7DqCnwR'): 
        item_info['할인 전 가격'] = driver.find_element(By.CSS_SELECTOR, '#content > div > div._2-I30XS1lA > div._2QCa6wHHPy > fieldset > div._3k440DUKzy > div.WrkQhIlUY0 > div > del > span._1LY7DqCnwR').text
    # item_info['판매가'] = driver.find_element(By.CSS_SELECTOR,'#content > div > div._2-I30XS1lA > div._2QCa6wHHPy > fieldset > div._3k440DUKzy > div.WrkQhIlUY0 > div > strong > span._1LY7DqCnwR').text
    # item_info['배송 정보'] = driver.find_element(By.CSS_SELECTOR, '#content > div > div._2-I30XS1lA > div._2QCa6wHHPy > fieldset > div._1rGSKv6aq_ > div.bd_1rmnr.bd_C8Tz1').text
    # item_info['배송 추가 정보'] = driver.find_element(By.CSS_SELECTOR, '#content > div > div._2-I30XS1lA > div._2QCa6wHHPy > fieldset > div._1rGSKv6aq_ > p').text
    # item_info['도착 예정 시간'] = driver.find_element(By.CSS_SELECTOR, '#INTRODUCE > div > div.bd_2UeeQ > div.bd_2kugS.bd_1gvyg > div.bd_lOeYy > div > span.bd_2OsjX').text
    # item_info['상품번호'] = driver.find_element(By.CSS_SELECTOR, '#INTRODUCE > div > div.attribute_wrapper > div > div._2E4i2Scsp4._copyable > table > tbody > tr:nth-child(1) > td:nth-child(2) > b').text
    # item_info['상품상태'] = driver.find_element(By.CSS_SELECTOR, '#INTRODUCE > div > div.attribute_wrapper > div > div._2E4i2Scsp4._copyable > table > tbody > tr:nth-child(1) > td:nth-child(4)').text
    # item_info['제조사'] = driver.find_element(By.CSS_SELECTOR, '').text
    # item_info['상품 정보 1']= driver.find_element(By.CSS_SELECTOR, '#INTRODUCE > div > div.attribute_wrapper > div > div._2E4i2Scsp4._copyable > table').text
    # item_info['상품 정보 2']= driver.find_element(By.CSS_SELECTOR, '#INTRODUCE > div > div.attribute_wrapper > div > div.detail_attributes > div > table > tbody').text
    # item_info[''] = driver.find_element(By.CSS_SELECTOR, '').text






    # print(item_info)

    with open(save_path,'wb') as file:
        pickle.dump(item_info, file, pickle.HIGHEST_PROTOCOL)


    return item_info



if __name__ == '__main__':
    
    url1 = "https://smartstore.naver.com/mewansungmall/products/8206341003?n_campaign_type=50&NaPm=ci%3D4jC48doklFQQ2CKfPdWeProg%7Ctr%3Dgfa%7Cct%3Dlv6ghqy6%7Chk%3Dff2fd71e460cf9db0bfa394d84768f9ab846ff12"
    url2 = "https://smartstore.naver.com/authentico/products/5909442580?"
    
    save_path = "Naver_item1.bin"
    Naver_selenium_scraper(url1, save_path)