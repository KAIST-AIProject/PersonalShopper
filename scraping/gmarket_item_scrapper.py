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




def gmarket_collect_reviews(driver, review_num):
    button_flag=False
    next_page_num=2

    review_list = []
    trial_count = 0
    while button_flag==False:
        try:
            button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable(
                                (By.CSS_SELECTOR, '#txtReviewTotalCount')
                            )
                        )
            driver.execute_script("arguments[0].click();", button)
            button_flag=True
            # print("click success")
            # print(driver.find_element(By.CSS_SELECTOR, '#txtReviewTotalCount').text)
            
        except TimeoutException:
            trial_count+=1
            if trial_count>3:
                review_list.append("리뷰를 읽을 수 없습니다.")
                return review_list
            print("Page is now too slow. I'll refresh the page once.")
            driver.refresh()
            driver.get(driver.current_url)
            scroll_down_to_end(driver, 5000)
    scroll_down_to_end(driver, 2000)
    while review_num>0:
        scroll_down_to_end(driver, 3000)
        try: 
            for review_number in range(1, 5+1):  
                review = driver.find_element(By.CSS_SELECTOR, f'#premium-wrapper > table > tbody > tr:nth-child({str(review_number)}) > td.comment-content > a > p.con').text

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
            if next_page_num<=10:
                # print(next_page_num)
                button = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable(
                                    (By.CSS_SELECTOR, f'#premium-pagenation-wrap > div.board_pagenation > ul > li:nth-child({str(next_page_num)}) > a')
                                )
                            )
                driver.execute_script("arguments[0].click();", button)
                # driver.execute_script("arguments[0].click();", button)

                next_page_num+=1
            else: 
                next_page_num=2
                button = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable(
                                    (By.CSS_SELECTOR, '#premium-pagenation-wrap > div.board_pagenation > a.next > span')
                                )
                            )
                driver.execute_script("arguments[0].click();", button)

            # scroll_down_to_end(driver, 2000)

        except: # 리뷰의 마지막 페이지까지 올 경우 [다음 >] 버튼이 없으므로 오류 발생함. 더이상의 반복은 무의미하므로 반복문 탈출
            # print("마지막 목록")
            # print("next inavailable")
            break
    return review_list


def gmarket_image_url_scrapper(driver):
    #SE-045e95f9-00a0-4c9d-94a9-b228e35fb938 > div > div > div > a
    #SE-676d8e7e-22ea-4a72-ba94-8549108b1434 > div > div > div > a
    
    try:
        button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, f'#container > div.vip-tabwrap.uxetabs > div.vip-tabnavi.uxeposfix.fixed > ul > li.uxetabs_menu > a')
                    )
                )
        driver.execute_script("arguments[0].click();", button)
        scroll_down_to_end(driver, 4000)

        button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, '#vip-tab_detail > div.box__detail-view.js-toggle-content > div.box__detail-more > button')
                    )
                )
        driver.execute_script("arguments[0].click();", button)
        scroll_down_to_end(driver)
    except: 
        print("button not found")

    
    driver.switch_to.frame('detail1')
    container = driver.find_element(By.ID, 'basic_detail_html')
    scroll_down_to_end(driver)
    # container = container_.find_element(By.ID, 'basic_detail_html')
    # links_selector = driver.find_elements(By.CSS_SELECTOR, '#SE-045e95f9-00a0-4c9d-94a9-b228e35fb938 > div > div > div > a')
    #basic_detail_html > img:nth-child(1)
    #skip-item-detail
    # print(links_selector)
    # print(containers.text)
    # print(container.get_attribute('innerHTML'))
    links = []
    images = container.find_elements(By.CSS_SELECTOR, 'img')
    # print(len(images))
    texts = container.text
    print(texts)
    for image in images:
        srcs = image.get_attribute("src")
        if srcs!=None:
            src_link_split = srcs.split('"')
            for src in src_link_split:
                if "jpg" in src:
                    links.append(src)
                    # print(src)


            
        
        # print("주소2: ", link.get_attribute("data-src"))
    return links, texts


def gmarket_selenium_scraper(driver, save_path_item, save_path_quality):
    scroll_down_to_end(driver, 1000)
    button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '#vip-tab_detail > div.vip-detailarea_productinfo.box__product-notice.js-toggle-content > div.box__product-notice-more > button')
            )
        )
    driver.execute_script("arguments[0].click();", button)

    info_list = dict()
    info_list['상품명'] = '#itemcase_basic > div.box__item-title > h1'
    info_list['현재 가격'] = '#itemcase_basic > div.box__item-title > div.price > span:nth-child(2) > strong'
    info_list['할인 전 가격'] = '#itemcase_basic > div.box__item-title > div.price > span:nth-child(2) > span.price_original > span.text__price'
    # info_list['할인율'] = '#product-atf > section > h2 > span.css-5nirzt.e1q8tigr3'
    info_list['배송 정보'] = '#container > div.item-topinfowrap > div.item-topinfo.item-topinfo--additional.box__item-info--vip > div.box__item-detailinfo.box__item-detailinfo--additional > ul > li.list-item__delivery-predict.uxeslide_item'
    # info_list['상품 정보 1'] = '#product-atf > section > p'
    # info_list['상품 정보 2'] = '#product-atf > section > ul'
    info_list['상품정보 제공고시'] = '#vip-tab_detail > div.vip-detailarea_productinfo.box__product-notice.js-toggle-content.on > div.box__product-notice-list'

    item_info = dict()
    
    
    for key, value in info_list.items():
        # print(key, value)
        element = check_exists_element_and_return_text(driver, value)
        if element != None:
            item_info[key] = element
        else:
            if key=='할인 전 가격':
                item_info[key] = item_info['현재 가격']
            else:
                item_info[key] = "정보 없음"
    # print(item_info)    
    if item_info['할인 전 가격']!="정보 없음":
        item_info['할인 전 가격'] = cost_only_number(item_info['할인 전 가격']) 
    if item_info['현재 가격']!="정보 없음":
        item_info['현재 가격'] = cost_only_number(item_info['현재 가격'])
        item_info['할인율'] = cal_sale(item_info['현재 가격'], item_info['할인 전 가격'])
    
    # print(item_info)
    quality_info = dict()


    # while check_exists_element_and_return_text(driver, "#container > div.vip-tabwrap.uxetabs > div.vip-tabnavi.uxeposfix.fixed > ul > li.uxetabs_menu.on") == False:
    #     scroll_down_to_end(driver, 4000)
    quality_info['총 평점'] = check_exists_element_and_return_text(driver, "#itemcase_basic > div.box__item-title > div.box__rating-information > div > span")
    quality_info['리뷰 수'] = check_exists_element_and_return_text(driver, '#txtReviewTotalCount')
    
    quality_info['리뷰'] = gmarket_collect_reviews(driver, 30)

    # print(len(quality_info['리뷰']))
    # # print(item_info)
    # print(quality_info)
    image_links, detail_texts = gmarket_image_url_scrapper(driver)
    
    # # print(len(image_links))
    # # print(detail_texts)
    item_info['상세 정보 문구'] = detail_texts

    print(item_info)
    print(quality_info)
    print(image_links)


    with open(save_path_item,'wb') as item_file:
        pickle.dump(item_info, item_file, pickle.HIGHEST_PROTOCOL)

    with open(save_path_quality, 'wb') as quality_file:
        pickle.dump(quality_info, quality_file, pickle.HIGHEST_PROTOCOL )


    return item_info, quality_info, image_links



if __name__ == '__main__':

    # kurly
    urls = [
        # 'https://item.gmarket.co.kr/Item?goodscode=2080799823&ver=20240502',
        'https://item.gmarket.co.kr/Item?goodscode=3419825675&ver=20240502',
        'https://item.gmarket.co.kr/Item?goodscode=3257659996&ver=20240502',
        'https://item.gmarket.co.kr/item?goodscode=3684952203&gate_id=8651FC2C-5EAE-4905-83BD-BD6D9B0815C5'
             ]

    driver = webdriver.Chrome()
    for url in urls: 
        driver.get(url)
        driver.implicitly_wait(3) ## 연결 후 3초간 기다리기
        save_path_item = "gmarket_item1.bin"
        save_path_quality = "gmarket_item1_review.bin"
        print(url)
        gmarket_selenium_scraper(driver, save_path_item, save_path_quality)