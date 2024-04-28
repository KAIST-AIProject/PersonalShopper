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
from .scrapper_utils import *




def kurly_collect_reviews(driver, review_num):
    button_flag=False
    review_th = 2

    review_list = []
    trial_count = 0
    while button_flag==False:
        try:
            button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable(
                                (By.CSS_SELECTOR, '#top > div.css-n48rgu.ex9g73v0 > div.css-16c0d8l.e1brqtzw0 > nav > ul > li:nth-child(3)')
                            )
                        )
            driver.execute_script("arguments[0].click();", button)
            button_flag=True
            # print("click success")
        except TimeoutException:
            trial_count+=1
            if trial_count>3:
                review_list.append("리뷰를 읽을 수 없습니다.")
                return review_list
            print("Page is now too slow. I'll refresh the page once.")
            driver.refresh()
            driver.get(driver.current_url)
            scroll_down_to_end(driver, 1000)
    # driver.implicit_wait(10)
    #review > section > div:nth-child(3) > div:nth-child(4)
    #review > section > div:nth-child(3) > div:nth-child(13)
    while review_num>0: 
        #review > section > div:nth-child(3) > div:nth-child(4)
        #review > section > div:nth-child(3) > div:nth-child(13)
        try: 
            # print("review_num: {}".format(review_num))
            # review_table = driver.find_elements(By.CSS_SELECTOR, "#review > section > div:nth-child(3)")
            for review_number in range(4, 13+1):  #리뷰 1페이지 당 최대 10개dml 리뷰가 있음
                # print(review_number)
                #review > section > div:nth-child(3) > div:nth-child(9) > article > div > p
                review = driver.find_element(By.CSS_SELECTOR, f'#review > section > div:nth-child(3) > div:nth-child({str(review_number)}) > article > div > p').text
                review_list.append(review)
                # print(review_num)
                # print(review)
                review_num-=1
                if review_num<=0:
                    break
    
        except: # 페이지가 더 없는 경우
            # print("exception1")
            review_num = -1
            break

        try: 
            scroll_down_to_end(driver, 3000)
            button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable(
                                (By.CSS_SELECTOR, '#review > section > div:nth-child(3) > div.css-jz9m4p.ebs5rpx3 > button.css-1orps7k.ebs5rpx0')
                            )
                        )
            driver.execute_script("arguments[0].click();", button)
            scroll_down_to_end(driver, 2000)

            # print(check_exists_element_and_return_text(driver, '#review > section > div:nth-child(3) > div.css-jz9m4p.ebs5rpx3 > button.css-1orps7k.ebs5rpx0'))
            # driver.find_element(By.CSS_SELECTOR, '#review > section > div:nth-child(3) > div.css-jz9m4p.ebs5rpx3 > button.css-1orps7k.ebs5rpx0').click() # [다음 >] 클릭
            # next_list_count -= 1 # 사용자가 미리 설정한 list_count임. 
            #inquiry > div > div.css-18ad0gx.e9e6ap50 > div > button.css-1jwilit.e1pk9060
            #review > section > div:nth-child(3) > div.css-jz9m4p.ebs5rpx3 > button.css-1orps7k.ebs5rpx0
            #review > section > div:nth-child(3) > div.css-jz9m4p.ebs5rpx3 > button.css-xzvv6n.ebs5rpx1

        except: # 리뷰의 마지막 페이지까지 올 경우 [다음 >] 버튼이 없으므로 오류 발생함. 더이상의 반복은 무의미하므로 반복문 탈출
            # print("마지막 목록")
            # print("next inavailable")
            break
    return review_list


def kurly_image_url_scrapper(driver):
    scroll_down_to_end(driver)
    #INTRODUCE > div > div._3osy73V_eD._1Hc_ju_IXp > button
    # print("urlscrapper")
    containers = driver.find_elements(By.ID, 'description')
    # links_selector = driver.find_elements(By.CSS_SELECTOR, '#SE-045e95f9-00a0-4c9d-94a9-b228e35fb938 > div > div > div > a')
    # print(links_selector)
    links = []
    texts = ""
    for container in containers:
        words = container.find_elements(By.CLASS_NAME, 'words')
        for word in words:
            texts = texts + word.text + "\n"
        images = container.find_elements(By.CLASS_NAME, 'pic > img')
        # print(len(images))
        for image in images:
            # print(images)
            srcs = image.get_attribute("src")
            links.append(srcs)
            

        # print("주소2: ", link.get_attribute("data-src"))
    return links, texts


def kurly_selenium_scraper(driver, save_path_item, save_path_quality):
    scroll_down_to_end(driver, 1000)


    info_list = dict()
    info_list['상품명'] = '#product-atf > section > div.css-1qy9c46.ezpe9l12'
    info_list['현재 가격'] = '#product-atf > section > h2 > span.css-9pf1ze.e1q8tigr2'
    info_list['할인 전 가격'] = '#product-atf > section > span > span'
    info_list['할인율'] = '#product-atf > section > h2 > span.css-5nirzt.e1q8tigr3'
    info_list['배송 정보'] = '#product-atf > section > ul > li:nth-child(1) > dd'
    info_list['상품 정보 1'] = '#product-atf > section > p'
    info_list['상품 정보 2'] = '#product-atf > section > ul'
    info_list['상품정보 제공고시'] = '#detail > div.css-1vc740i.e11kghol1 > ul'

    item_info = dict()
    
    
    for key, value in info_list.items():
        # print(key, value)
        element = check_exists_element_and_return_text(driver, value)
        if element != None:
            item_info[key] = element
        else:
            if key=="할인율":
                item_info[key] = "0%"
                item_info['할인 전 가격'] = item_info['현재 가격']
            else:
                item_info[key] = "정보 없음"
    
    quality_info = dict()

    while check_exists_element_and_return_text(driver, "#top > div.css-n48rgu.ex9g73v0 > div.css-16c0d8l.e1brqtzw0 > nav > ul > li:nth-child(3)") == False:
        scroll_down_to_end(driver)
    quality_info['총 평점'] = check_exists_element_and_return_text(driver, "#REVIEW > div > div._1f93qA0ngZ > div._7sK3cGXIH0._2tbImjE0Ih > div > div._3vokcktRs0._29BVF0J3DO > div")
    quality_info['리뷰 수'] = check_exists_element_and_return_text(driver, '#top > div.css-n48rgu.ex9g73v0 > div.css-16c0d8l.e1brqtzw0 > nav > ul > li:nth-child(3) > a > span.count')
    
    quality_info['리뷰'] = kurly_collect_reviews(driver, 10)
    # print(len(quality_info['리뷰']))
    # print(item_info)
    # print(quality_info)
    image_links, detail_texts = kurly_image_url_scrapper(driver)
    # print(len(image_links))
    # print(detail_texts)
    item_info['상세 정보 문구'] = detail_texts



    with open(save_path_item,'wb') as item_file:
        pickle.dump(item_info, item_file, pickle.HIGHEST_PROTOCOL)

    with open(save_path_quality, 'wb') as quality_file:
        pickle.dump(quality_info, quality_file, pickle.HIGHEST_PROTOCOL )


    return item_info, quality_info, image_links



if __name__ == '__main__':

    # kurly
    urls = ['https://www.kurly.com/goods/1000441195',
             "https://www.kurly.com/goods/1000125253",
             "https://www.kurly.com/goods/1000316128"
             ]

    driver = webdriver.Chrome()
    for url in urls: 
        driver.get(url)
        driver.implicitly_wait(3) ## 연결 후 3초간 기다리기
        save_path_item = "kurly_item1.bin"
        save_path_quality = "kurly_item1_review.bin"
        print(url)
        kurly_selenium_scraper(driver, save_path_item, save_path_quality)