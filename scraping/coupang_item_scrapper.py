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


def scroll_to_review(driver):
    button_flag=False
    next_page_num=2

    review_list = []
    trial_count = 0
    while button_flag==False:
        try:
            button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable(
                                (By.CSS_SELECTOR, '#btfTab > ul.tab-titles > li:nth-child(2)')
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

def coupang_collect_reviews(driver, review_num):
    next_page_num=2

    review_list = []
    scroll_to_review(driver)
    while review_num>0:
        scroll_down_to_end(driver, 4000)
        try: 
                    
            for review_number in range(3, 5+3):  
                review = driver.find_element(By.CSS_SELECTOR, f'#btfTab > ul.tab-contents > li.product-review.tab-contents__content > div > div.sdp-review__article.js_reviewArticleContainer > section.js_reviewArticleListContainer > article:nth-child({str(review_number)}) > div.sdp-review__article__list__review.js_reviewArticleContentContainer').text
                review_list.append(review.replace('\n', ' '))
                review_num-=1
                if review_num<=0:
                    break
    
        except: # 페이지가 더 없는 경우

            review_num = -1
            break
        try: 
            if next_page_num<=10:
                button = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable(
                                    (By.CSS_SELECTOR, f'#btfTab > ul.tab-contents > li.product-review.tab-contents__content > div > div.sdp-review__article.js_reviewArticleContainer > section.js_reviewArticleListContainer > div.sdp-review__article__page.js_reviewArticlePagingContainer > button:nth-child({str(next_page_num+1)})')
                                )
                            )
                driver.execute_script("arguments[0].click();", button)
                next_page_num+=1
            else: 
                next_page_num=2
                button = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable(
                                    (By.CSS_SELECTOR, '#btfTab > ul.tab-contents > li.product-review.tab-contents__content > div > div.sdp-review__article.js_reviewArticleContainer > section.js_reviewArticleListContainer > div.sdp-review__article__page.js_reviewArticlePagingContainer > button.sdp-review__article__page__next.js_reviewArticlePageNextBtn')
                                )
                            )
                driver.execute_script("arguments[0].click();", button)


        except: 
            break
    return review_list



def coupang_image_url_scrapper(driver):
    
    try:
        button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, '#productDetail > div.product-detail-seemore > div')
                    )
                )
        driver.execute_script("arguments[0].click();", button)
        scroll_down_to_end(driver, 4000)

        # button = WebDriverWait(driver, 10).until(
        #             EC.element_to_be_clickable(
        #                 (By.CSS_SELECTOR, '#vip-tab_detail > div.box__detail-view.js-toggle-content > div.box__detail-more > button')
        #             )
        #         )
        # driver.execute_script("arguments[0].click();", button)
        # scroll_down_to_end(driver)
    except: 
        # print("button not found")
        pass

    
    # driver.switch_to.frame('detail1')
    container = driver.find_element(By.CLASS_NAME, 'product-detail-content-inside')
    scroll_down_to_end(driver,8000)
    links = []
    images = container.find_elements(By.CLASS_NAME, 'subType-IMAGE > img')
    # print(len(images))
    texts = container.text
    # print(texts)
    
    for image in images:

        src = image.get_attribute("src")
        if src!=None and "jpg" in src:
                links.append(src)


            
        
    return links, texts




def Coupang_selenium_scraper(driver, save_path_item, save_path_quality):
    # co = Options()
    # co.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
    # driver = webdriver.Chrome()
    # driver.get(url)
    # driver.implicitly_wait(3) ## 연결 후 3초간 기다리기

    
    #문서 끝까지 스크롤
    scroll_down_to_end(driver)
    # driver.implicitly_wait(3) ## 연결 후 3초간 기다리기

    info_list = dict()
    # info_list['상품명'] = '#contents > div.prod-atf > div.prod-atf-main > div.prod-buy.new-oos-style.not-loyalty-member.eligible-address.without-subscribe-buy-type.DISPLAY_0.has-loyalty-exclusive-price.fix-verdor-section-display.move-atc-and-buy-now-ctas-atf.update-price-section-style-with-rds > div.prod-buy-header > h2'
    # info_list['현재 가격'] = '#contents > div.prod-atf > div.prod-atf-main > div.prod-buy.new-oos-style.not-loyalty-member.eligible-address.without-subscribe-buy-type.DISPLAY_0.has-loyalty-exclusive-price.fix-verdor-section-display.move-atc-and-buy-now-ctas-atf.update-price-section-style-with-rds > div.prod-price-container > div.prod-price > div > div.prod-sale-price.price-align.wow-only-coupon > span.total-price > strong'
    # info_list['할인 전 가격'] = '#contents > div.prod-atf > div.prod-atf-main > div.prod-buy.new-oos-style.not-loyalty-member.eligible-address.without-subscribe-buy-type.DISPLAY_0.has-loyalty-exclusive-price.fix-verdor-section-display.move-atc-and-buy-now-ctas-atf.update-price-section-style-with-rds > div.prod-price-container > div.prod-price > div > div.prod-origin-price > span.origin-price'
    # info_list['할인율'] = '#contents > div.prod-atf > div.prod-atf-main > div.prod-buy.new-oos-style.not-loyalty-member.eligible-address.without-subscribe-buy-type.DISPLAY_0.has-loyalty-exclusive-price.fix-verdor-section-display.move-atc-and-buy-now-ctas-atf.update-price-section-style-with-rds > div.prod-price-container > div.prod-price > div > div.prod-origin-price > span.discount-rate'
    # info_list['상품정보 제공고시'] = '#itemBrief > div > table'

    info_list['상품명'] = 'div.prod-buy-header > h2'
    info_list['현재 가격'] = 'span.total-price > strong'
    info_list['할인 전 가격'] = 'div.prod-price > div > div.prod-origin-price > span.origin-price'
    info_list['할인율'] = 'span.discount-rate'
    info_list['상품정보 제공고시'] = '#itemBrief > div > table'


    item_info = dict()
    
    
    for key, value in info_list.items():
        element = check_exists_element_and_return_text(driver, value)
        if element != None:
            item_info[key] = element
        else:
            if key=="할인율":
                item_info[key] = "0%"
                item_info['할인 전 가격'] = item_info['현재 가격']
            else:
                item_info[key] = "정보 없음"
    
    # print(item_info)

    if item_info['현재 가격']!="정보 없음":
        item_info['현재 가격'] = cost_only_number(item_info['현재 가격'])
    if item_info['할인 전 가격']!="정보 없음":
        item_info['할인 전 가격'] = cost_only_number(item_info['할인 전 가격']) 
    

    quality_info = dict()
    scroll_to_review(driver)

    rating = check_css_element(driver, 'div.sdp-review__average__total-star__info > div.sdp-review__average__total-star__info-gray > div')
    if rating!=None:
        quality_info['총 평점'] = rating.get_attribute("data-rating")
    else:
        quality_info['총 평점'] = "정보 없음"
    quality_info['리뷰 수'] =check_exists_element_and_return_text(driver, 'div.sdp-review__average__total-star__info > div.sdp-review__average__total-star__info-count')
    quality_info['리뷰'] = coupang_collect_reviews(driver, 10)
    image_links, detail_texts = coupang_image_url_scrapper(driver)

    item_info['상세 정보 문구'] = detail_texts
    with open(save_path_item,'wb') as item_file:
        pickle.dump(item_info, item_file, pickle.HIGHEST_PROTOCOL)

    with open(save_path_quality, 'wb') as quality_file:
        pickle.dump(quality_info, quality_file, pickle.HIGHEST_PROTOCOL )


    return item_info, quality_info, image_links



if __name__ == '__main__':
    # naver
    urls = [
        'https://www.coupang.com/vp/products/130924213?itemId=847502340&vendorItemId=5154927733&isAddedCart=',
        # 'https://www.coupang.com/vp/products/5166844155?itemId=7119619991&vendorItemId=74411448862&sourceType=cmgoms&omsPageId=s189740&omsPageUrl=s189740&isAddedCart=',
        'https://www.coupang.com/vp/products/7400367877?itemId=20405085300&vendorItemId=87431312803&q=%EC%95%84%EC%9D%B4%ED%8C%A8%EB%93%9C+%EC%BC%80%EC%9D%B4%EC%8A%A4&itemsCount=36&searchId=bf534d93a0b645c6b05b13b22867bb15&rank=33&isAddedCart=',
        'https://www.coupang.com/vp/products/1464545785?itemId=2518829089&vendorItemId=70821446248&q=%EC%9E%90%EC%A0%84%EA%B1%B0&itemsCount=36&searchId=6336bcc416f34b1e96eae0be576f2581&rank=2&isAddedCart='
           ]
    chrome_options = Options() ## 옵션 추가를 위한 준비
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222") ## 디버깅 옵션 추가

    # 크롬 드라이버 생성
    driver = webdriver.Chrome(options=chrome_options)
    for url in urls: 
        driver.get(url)
        driver.implicitly_wait(3) ## 연결 후 3초간 기다리기
        save_path_item = "coupang_item1.bin"
        save_path_quality = "coupang_item1_review.bin"
        # print(url)
        Coupang_selenium_scraper(driver, save_path_item, save_path_quality)