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
from scrapper_utils import *


def naver_collect_reviews(driver, review_num):
    button_flag=False
    review_th = 2
    for i in range(1, 5):
        button = driver.find_element(By.CSS_SELECTOR, f'#_productFloatingTab > div > div._27jmWaPaKy._1dDHKD1iiX > ul > li:nth-child({str(i)}) > a')
        # print(button.text)
        if "리뷰" in str(button.text):
            review_th = i

    review_list = []
    trial_count = 0
    while button_flag==False:
        try:
            button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable(
                                (By.CSS_SELECTOR, f'#_productFloatingTab > div > div._27jmWaPaKy._1dDHKD1iiX > ul > li:nth-child({str(review_th)}) > a')
                            )
                        )
            driver.execute_script("arguments[0].click();", button)
            button_flag=True
        except TimeoutException:
            trial_count+=1
            if trial_count>3:
                review_list.append("리뷰를 읽을 수 없습니다.")
                return review_list
            print("Page is now too slow. I'll refresh the page once.")
            driver.refresh()
            driver.get(driver.current_url)
            scroll_down_to_end(driver)


    # driver.find_element(By.CSS_SELECTOR, f'#_productFloatingTab > div > div._27jmWaPaKy._1dDHKD1iiX > ul > li:nth-child({str(review_th)}) > a').send_keys(Keys.ENTER)
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


def Naver_image_url_scrapper(driver):
    #SE-045e95f9-00a0-4c9d-94a9-b228e35fb938 > div > div > div > a
    #SE-676d8e7e-22ea-4a72-ba94-8549108b1434 > div > div > div > a
    scroll_down_to_end(driver)
    button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, f'#INTRODUCE > div > div._3osy73V_eD._1Hc_ju_IXp > button')
                )
            )
    driver.execute_script("arguments[0].click();", button)
    # print("button_Click")
    scroll_down_to_end(driver)
    driver.implicitly_wait(3)
    #INTRODUCE > div > div._3osy73V_eD._1Hc_ju_IXp > button
    # print("urlscrapper")
    containers = driver.find_elements(By.CLASS_NAME, 'se-main-container')
    # links_selector = driver.find_elements(By.CSS_SELECTOR, '#SE-045e95f9-00a0-4c9d-94a9-b228e35fb938 > div > div > div > a')
    # print(links_selector)
    # print(containers.text)
    links = []
    texts = ""
    for container in containers:
        texts = texts + container.text + "\n"
        images = container.find_elements(By.CSS_SELECTOR, 'a')
        # print(len(images))
        
        for image in images:
            # print(images)
            srcs = image.get_attribute("data-linkdata")
            # print(srcs.split(","))
            # print(srcs)
            if srcs!=None:
                src_link = srcs.split(",")[1][7:-1]
            # print(src_link)
                links.append(src_link)
            

        # print("주소2: ", link.get_attribute("data-src"))
    return links, texts

def Naver_selenium_scraper(driver, save_path_item, save_path_quality):
    # co = Options()
    # co.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
    # driver = webdriver.Chrome()
    # driver.get(url)
    # driver.implicitly_wait(3) ## 연결 후 3초간 기다리기

    
    #문서 끝까지 스크롤
    scroll_down_to_end(driver)
    # driver.implicitly_wait(3) ## 연결 후 3초간 기다리기

    info_list = dict()
    info_list['상품명'] = '#content > div > div._2-I30XS1lA > div._2QCa6wHHPy > fieldset > div._3k440DUKzy > div._1eddO7u4UC > h3'
    info_list['할인율'] = '#content > div > div._2-I30XS1lA > div._2QCa6wHHPy > fieldset > div._3k440DUKzy > div.WrkQhIlUY0 > span'
    info_list['할인 전 가격'] = '#content > div > div._2-I30XS1lA > div._2QCa6wHHPy > fieldset > div._3k440DUKzy > div.WrkQhIlUY0 > div > del > span._1LY7DqCnwR'
    info_list['현재 가격'] = '#content > div > div._2-I30XS1lA > div._2QCa6wHHPy > fieldset > div._3k440DUKzy > div.WrkQhIlUY0 > div > strong > span._1LY7DqCnwR'
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
            if key=="할인율":
                item_info[key] = "0%"
            else:
                item_info[key] = "정보 없음"

    
    # driver.find_element(By.CSS_SELECTOR, '#_productFloatingTab > div > div._27jmWaPaKy._1dDHKD1iiX > ul > li:nth-child(3) > a').send_keys(Keys.ENTER)
    # driver.implicitly_wait(3)

    # print(item_info)

    quality_info = dict()

    while check_exists_element_and_return_text(driver, "#_productFloatingTab > div > div._27jmWaPaKy._1dDHKD1iiX > ul > li:nth-child(2) > a") == False:
        scroll_down_to_end(driver)
    quality_info['총 평점'] = check_exists_element_and_return_text(driver, "#REVIEW > div > div._1f93qA0ngZ > div._7sK3cGXIH0._2tbImjE0Ih > div > div._3vokcktRs0._29BVF0J3DO > div")
    quality_info['리뷰 수'] = check_exists_element_and_return_text(driver, '#REVIEW > div > div._1f93qA0ngZ > div._7sK3cGXIH0._2tbImjE0Ih > div > div._3vokcktRs0._2iNVRGXEA6')
    # print(quality_info)
    # reviews = []
    # # print(check_exists_element_and_return_text(driver, '#REVIEW > div > div._2LvIMaBiIO > div._2g7PKvqCKe '))

    # review_number = 1
    # review_table = driver.find_elements(By.CSS_SELECTOR, f'#REVIEW > div > div._2LvIMaBiIO > div._2g7PKvqCKe > ul > li:nth-child({str(review_number)}')
    # print(len(review_table))
    
    quality_info['리뷰'] = naver_collect_reviews(driver, 10)
    # print(quality_info['리뷰'])
    # print(len(quality_info['리뷰']))
    image_links, detail_texts = Naver_image_url_scrapper(driver)

    print(detail_texts)
    item_info['상세 정보 문구'] = detail_texts
    print(item_info)
    with open(save_path_item,'wb') as item_file:
        pickle.dump(item_info, item_file, pickle.HIGHEST_PROTOCOL)

    with open(save_path_quality, 'wb') as quality_file:
        pickle.dump(quality_info, quality_file, pickle.HIGHEST_PROTOCOL )
    

    # detail_text = driver.find_element(By.CLASS_NAME, 'se-main-container').text
    # print(detail_text)
    
    # print(image_links)

    # Naver_image_url_scrapper(driver)
    return item_info, quality_info, image_links


if __name__ == '__main__':
    # naver
    urls = ["https://smartstore.naver.com/mewansungmall/products/8206341003?n_campaign_type=50&NaPm=ci%3D4jC48doklFQQ2CKfPdWeProg%7Ctr%3Dgfa%7Cct%3Dlv6ghqy6%7Chk%3Dff2fd71e460cf9db0bfa394d84768f9ab846ff12",
            "https://smartstore.naver.com/authentico/products/5909442580?",
            "https://smartstore.naver.com/itemrepublic/products/5411669555?NaPm=ct%3Dlv94l0ko%7Cci%3Ddd64ace6c3287f4a30440f867f36bbdbc11e6607%7Ctr%3Dslsl%7Csn%3D1241781%7Chk%3D731e5f74f10852cdd48540fbc4bc5853bec0a6c4",
            "https://smartstore.naver.com/beaubebe/products/4868991834?NaPm=ct%3Dlv9birbc%7Cci%3D4550ced922c6169bfce233f1deffa37740841b81%7Ctr%3Dslsl%7Csn%3D442246%7Chk%3D2450f1cf0f9cfff6677a243810f44d2e00a8853b,",
            "https://smartstore.naver.com/eurokitchen/products/7230084092?NaPm=ct%3Dlv9bis34%7Cci%3D16b732ad5d5e22683148397251d5ed4ac272277c%7Ctr%3Dslsl%7Csn%3D294174%7Chk%3D5098f02d03938342eed308565106d887c0ea44da",
            "https://smartstore.naver.com/kongkong2_kim/products/4958118823?NaPm=ct%3Dlv9bisuw%7Cci%3Dee2d850ee311284b34e147f9804fdcea0567d857%7Ctr%3Dslsl%7Csn%3D732111%7Chk%3D78870f37ce9d5b5013149b9c36facb3d66325e16",
            "https://smartstore.naver.com/roshrosh/products/8120763063?NaPm=ct%3Dlv9biueg%7Cci%3D9c55242d68cdd5c2b6b490dae2c9c74c16e1b6f9%7Ctr%3Dslsl%7Csn%3D3150621%7Chk%3D952d955a38b06e3eb2d76870db06fd5d340b274a"
           ]

    driver = webdriver.Chrome()
    for url in urls: 
        driver.get(url)
        driver.implicitly_wait(3) ## 연결 후 3초간 기다리기
        save_path_item = "naver_item1.bin"
        save_path_quality = "naver_item1_review.bin"
        print(url)
        Naver_selenium_scraper(driver, save_path_item, save_path_quality)