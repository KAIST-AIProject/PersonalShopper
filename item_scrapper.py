import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pickle

from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup

def check_exists_element_and_return_text(driver, selector):
    try:
        element = driver.find_element(By.CSS_SELECTOR, selector)
    except NoSuchElementException:
        return None
    return element.text


def collect_reviews(driver, review_num):
    review_list = []
    driver.find_element(By.CSS_SELECTOR, '#_productFloatingTab > div > div._27jmWaPaKy._1dDHKD1iiX > ul > li:nth-child(2) > a').click()
    while review_num>0: 

        for page in range(2, 12): # 1~ 10페이지 반복문
            try: 
                driver.find_element(By.CSS_SELECTOR, f'#REVIEW > div > div._2LvIMaBiIO > div._2g7PKvqCKe > div > div > a:nth-child({str(page)}').click() # 각 페이지 클릭

                for review_number in range(1,20+1): # 리뷰 1페이지당 최대 20개의 리뷰가 있음. 
                    review_table = driver.find_elements(By.CSS_SELECTOR, f'#REVIEW > div > div._2LvIMaBiIO > div._2g7PKvqCKe > ul > li:nth-child({str(review_number)}')
                    for review in review_table:
                        # df.loc[df_idx] = [review.find_element(By.CSS_SELECTOR, f'div._3z6gI4oI6l').text, "-" , "-"] # 코드를 크롤링 하여 DataFrame에 넣음.
                        # df_idx += 1
                        
                        review_list.append(review.find_element(By.CSS_SELECTOR, f'div._3z6gI4oI6l').text)
                    review_num-=1
                    if review_num<=0:
                        break

            except: # 페이지가 더 없는 경우
                # print("마지막 페이지")
                review_num=-1
                break
            
            if review_num<=0:
                        break

        try: 
            driver.find_element(By.CSS_SELECTOR, f'#REVIEW > div > div._2LvIMaBiIO > div._2g7PKvqCKe > div > div > a.fAUKm1ewwo._2Ar8-aEUTq').click() # [다음 >] 클릭
            # next_list_count -= 1 # 사용자가 미리 설정한 list_count임. 

        except: # 리뷰의 마지막 페이지까지 올 경우 [다음 >] 버튼이 없으므로 오류 발생함. 더이상의 반복은 무의미하므로 반복문 탈출
            # print("마지막 목록")
            break
    return review_list


def Naver_selenium_scraper(url, save_path_item, save_path_quality):
    # co = Options()
    # co.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(3) ## 연결 후 3초간 기다리기


    
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
    # driver.implicitly_wait(3) ## 연결 후 3초간 기다리기

    info_list = dict()
    info_list['상품명'] = '#content > div > div._2-I30XS1lA > div._2QCa6wHHPy > fieldset > div._3k440DUKzy > div._1eddO7u4UC > h3'
    info_list['할인율'] = '#content > div > div._2-I30XS1lA > div._2QCa6wHHPy > fieldset > div._3k440DUKzy > div.WrkQhIlUY0 > span'
    info_list['할인 전 가격'] = '#content > div > div._2-I30XS1lA > div._2QCa6wHHPy > fieldset > div._3k440DUKzy > div.WrkQhIlUY0 > div > del > span._1LY7DqCnwR'
    info_list['배송 정보'] = '#INTRODUCE > div > div.bd_2UeeQ'
    info_list['상품 정보 1'] = '#INTRODUCE > div > div.attribute_wrapper > div > div._2E4i2Scsp4._copyable > table > tbody'
    info_list['상품 정보 2'] = '#INTRODUCE > div > div.attribute_wrapper > div > div.detail_attributes > div > table > tbody'
    info_list['상품정보 제공고시'] = '#INTRODUCE > div > div.product_info_notice > div > table'

    item_info = dict()
    
    
    for key, value in info_list.items():
        element = check_exists_element_and_return_text(driver, value)
        if element != None:
            item_info[key] = element
        else:
            item_info[key] = "정보 없음"
    
    driver.find_element(By.CSS_SELECTOR, '#_productFloatingTab > div > div._27jmWaPaKy._1dDHKD1iiX > ul > li:nth-child(3) > a').send_keys(Keys.ENTER)
    # driver.implicitly_wait(3)

    print(item_info)

    quality_info = dict()
    quality_info['총 평점'] = check_exists_element_and_return_text(driver, "#REVIEW > div > div._1f93qA0ngZ > div._7sK3cGXIH0._2tbImjE0Ih > div > div._3vokcktRs0._29BVF0J3DO > div")
    quality_info['리뷰 수'] = check_exists_element_and_return_text(driver, '#REVIEW > div > div._1f93qA0ngZ > div._7sK3cGXIH0._2tbImjE0Ih > div > div._3vokcktRs0._2iNVRGXEA6')
    # # print(quality_info)
    # reviews = []
    # # print(check_exists_element_and_return_text(driver, '#REVIEW > div > div._2LvIMaBiIO > div._2g7PKvqCKe '))

    # review_number = 1
    # review_table = driver.find_elements(By.CSS_SELECTOR, f'#REVIEW > div > div._2LvIMaBiIO > div._2g7PKvqCKe > ul > li:nth-child({str(review_number)}')
    # print(len(review_table))
    
    review_list = collect_reviews(driver, 10)
    quality_info['리뷰'] = review_list
    
    with open(save_path_item,'wb') as item_file:
        pickle.dump(item_info, item_file, pickle.HIGHEST_PROTOCOL)

    with open(save_path_quality, 'wb') as quality_file:
        pickle.dump(quality_info, quality_file, pickle.HIGHEST_PROTOCOL )


    return item_info, quality_info



if __name__ == '__main__':
    
    url1 = "https://smartstore.naver.com/mewansungmall/products/8206341003?n_campaign_type=50&NaPm=ci%3D4jC48doklFQQ2CKfPdWeProg%7Ctr%3Dgfa%7Cct%3Dlv6ghqy6%7Chk%3Dff2fd71e460cf9db0bfa394d84768f9ab846ff12"
    url2 = "https://smartstore.naver.com/authentico/products/5909442580?"
    
    save_path_item = "Naver_item1.bin"
    save_path_quality = "Naver_item1_quality.bin"
    Naver_selenium_scraper(url2, save_path_item, save_path_quality)