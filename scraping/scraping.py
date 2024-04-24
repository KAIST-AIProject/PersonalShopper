import requests
import json
import pickle
import time
from tqdm import tqdm
from urllib  import parse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from .item_scrapper import *
from utils import NaverOptionGet
from agent import *
import os
from agent import *
import config

################쿠팡 HTML 불러오기################
def CoupangLinkGet(url_kword, n_top=10,):
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36', "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3"}
    url_query = 'https://www.coupang.com/np/search?component=&q='
    url_tail1 = '&channel=user'
    url = url_query+url_kword+url_tail1
    result = requests.get(url, headers=headers)
    result.raise_for_status() # 웹페이지 정상 확인
    html = result.text

    #html parsing
    soup = BeautifulSoup(html, 'html.parser')
    root = 'https://www.coupang.com'
    coupang_ntop_url = []
    qurey_arr = soup.select('ul#productList li.search-product a:has(span.number)')
    for i in range(n_top):
        coupang_ntop_url.append(root+qurey_arr[i]['href'])
    return coupang_ntop_url

################네이버 JSON으로 상품정보 불러오기################
def NaverLinkGet(keyword, n_top=10):
    cookies = {
        'NNB': 'ESR5XBYFS3EWK',
        'NaverSuggestUse': 'use%26unuse',
        'ba.uuid': '9adcad84-733c-4d75-ba08-eca11ac2f99f',
        'SHP_BUCKET_ID': '8',
        'ASID': '7d8348d20000018e4ed4c1b500000044',
        'nid_inf': '681918093',
        'NID_AUT': 'LggIIkHiBVYi8m+B3B5US8s0hCgcaDnq1dUvX/j7Pi/b3xufMZcNy6CFaKkA9V7M',
        'NID_JKL': 'olBG2UWLCzvlsOzgnUsqtbp7MfoHPQC1FecUifcOAM8=',
        '_fwb': '52sfFMFCjkeuzFDts5zf8v.1711078526612',
        'page_uid': 'iQ9/qwqo1fssst0CUmwsssssscZ-350591',
        'spage_uid': 'iQ9%2Fqwqo1fssst0CUmwsssssscZ-350591',
        'NID_SES': 'AAABp5aKU1Dx/9njC0kZkcUNIMS2sZUWBSXJeDz+L2GrUDdHDQABfhaAIuQ+ngQPngeFn+mhASDETX5bta7hhUsQ2rD0kjMazIbl5pxaYTH0o6EtntpFP2OCNw1M2LKz+PGxGoIMovHjQUHjC4sR5yA1ZHytm4askuWsBIBorP92EKyiGSzY7LpGy5XXjoS7MV0uUnIXeaLklIKDH7Gws+cFGpw40Dw4aoEj+s/4KO6D0gQQ2mKpp72V081LUr4HtickbKgrxQE1t3cxm+FGpsUPCZcw4BcVsu1mgx5IvwXqGkrwLQp7rdiZ1h4BUjVhTqDOucieeULFV9ulv65K7IJg+RX/Q3z6O0aE7z5u6hu0u2/1P072IUddyCahDLQuLcQCa31jZpNcsPhGPQv0tMmUGm+zXh5ZYKgyKW2cUi5OP34MYjXkHKRGxeArtOLBl4xPCMHvxlFIVc7pUizU6J2XN+9IzG38fzJuN8kvSRbpnINphRrayKC84nHteeHOCO3LZWvL+TnZsgnjgc7zPqLSk8pQVD5HCqBpXXw8r+xHbz70MFvnpzTpvheIXzL2rc+h/w==',
        'ncpa': '10649105|lu4ubre8|420007bd90e02cacee49ff8e941e54edf04f5934|s_82adb61b9957|03302ec774b93adea1b4fd3cf258d33ad9875bcb:95694|lu4uzwzs|97df903bf2c74e33331584f7db0d6cef340ee66e|95694|81c6b5666b88d6353ad6df668d8298d1641b4fcf',
    }

    headers = {
        'authority': 'search.shopping.naver.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'logic': 'PART',
        'referer': 'https://search.shopping.naver.com/search/all?adQuery=%EA%B3%BC%EC%9E%90&origQuery=%EA%B3%BC%EC%9E%90&pagingIndex=1&pagingSize=40&productSet=total&query=%EA%B3%BC%EC%9E%90&sort=rel&timestamp=&viewType=list',
        'sbth': '174c1dee39685f585269b5c6212d77176cac147635352267fec659d028fa7ec2bb28d53c7b95642bce426a8c5fd8519e',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sec-ch-ua-arch': '"arm"',
        'sec-ch-ua-bitness': '"64"',
        'sec-ch-ua-full-version-list': '"Chromium";v="122.0.6261.129", "Not(A:Brand";v="24.0.0.0", "Google Chrome";v="122.0.6261.129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"macOS"',
        'sec-ch-ua-platform-version': '"14.4.0"',
        'sec-ch-ua-wow64': '?0',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    }

    params = {
        'adQuery': f'{keyword}',
        'eq': '',
        'iq': '',
        'origQuery': f'{keyword}',
        'pagingIndex': '1',
        'pagingSize': '40',
        'productSet': 'checkout',
        'query': f'{keyword}',
        'sort': 'review_rel',
        'viewType': 'list',
        'xq': '',
    }

    response = requests.get('https://search.shopping.naver.com/api/search/all', params=params, cookies=cookies, headers=headers)

    data = json.loads(response.text)
    itemlist = data['shoppingResult']['products']  
    naver_ntop_url = []

    for i in range(n_top):
        naver_ntop_url.append(itemlist[i]['crUrl'])
    return naver_ntop_url

################네이버 URL 체크하기 불러오기################
def NaverFinalUrl(keyword, n_top):

    url_list = NaverLinkGet(keyword, 30)
    
    chrome_options = Options() ## 옵션 추가를 위한 준비
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222") ## 디버깅 옵션 추가
    # chrome_options.add_argument("headless")
    driver = webdriver.Chrome(options=chrome_options)
    n_top =n_top
    count = 0
    naver_url_lst = []
    

    data_details = []
    data_compare = []

    
    with tqdm(total=n_top, ascii=True) as pbar:
        for url in url_list:
            if count==n_top:
                break
            driver.get(url)
            driver.implicitly_wait(3)    
            if driver.find_elements(By.CSS_SELECTOR, "a._3C8i4VFUIv._3SXdE7K-MC.N\=a\:GNB\.shopping._nlog_click"):
                scrapped_data_path = os.path.join("database", "Naver_item_"+str(count+1)+".bin")
                review_data_path = os.path.join("database", "Naver_item_review_"+str(count+1)+".bin")
                result_detail, result_review = Naver_selenium_scraper(driver, scrapped_data_path, review_data_path)
                result_detail['product_number'] = count+1 #product number 라는 key 값 추가
                
                #옵션 가져오기
                opt_btn_lst =driver.find_elements(By.CSS_SELECTOR, '[data-shp-area-id*=opt]._nlog_impression_element')
                option_info = {'options':dict()}
                for i in range(len(opt_btn_lst)//2):
                    NaverOptionGet(driver, i, [], option_info['options'])
                    driver.refresh()
                result_detail.update(option_info)


                #review score 
                if config.review_compare_mode : #한 개씩 리뷰의 점수를 평가한 후 평균낸 점수
                    review_score = review_rating_one(result_review['리뷰']) # 리뷰들의 평균 점수 return
                else : #한 번에 10개의 리뷰를 모두 고려한 점수
                    review_score = review_rating_all(result_review['리뷰']) # 리뷰들의 평균 점수 return

                #brand score 
                brand_score = brand_rating(result_detail['상품명'])

                #compare_information : compare agent에게 제공할 정보 : 이름, 가격, 할인율, 번호, 리뷰 평균 점수...
                compare_information = {"product_number":count+1, "Product_name" : result_detail["상품명"], "discount_rate" : result_detail["할인율"], "price" : result_detail["현재 가격"], "review_positivity_score" : review_score, 'number of reviews' : result_review['리뷰 수'], "Star rating" : result_review['총 평점'], "brand score" : brand_score }

                data_details.append(result_detail) 
                data_compare.append(compare_information)
                naver_url_lst.append(url)
                count+=1
                pbar.update(1)
            
    driver.quit()
    return naver_url_lst, data_details, data_compare


################컬리 HTML 불러오기################
#컬리는 CSR 방식이라 Selenium을 통해 접근 한 후 HTML 불러와야함
def KurlyLinkGet(url_kword, n_top=10):
    url_query = "https://www.kurly.com/search?sword="
    url_tail1 = '&page=1&per_page=96&sorted_type=4'
    url = url_query+url_kword+url_tail1

    # 옵션 생성
    options = webdriver.ChromeOptions()
    # 창 숨기는 옵션 추가
    # options.add_argument("headless")
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222") ## 디버깅 옵션 추가

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.implicitly_wait(5)

    html = driver.page_source

    # driver 종료
    driver.quit()

    #html parsing
    soup = BeautifulSoup(html, 'html.parser')
    root = 'https://www.kurly.com'
    kurly_ntop_url = []

    qurey_arr = soup.select('div.css-11kh0cw a')
    for i in range(min(len(qurey_arr),n_top)):
        kurly_ntop_url.append(root+qurey_arr[i]['href'])
    return kurly_ntop_url

################Gmarket HTML 불러오기################
def GmarketLinkGet(url_kword, n_top=10):
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36', "Accept-Language": "ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3"}
    url_query = 'https://browse.gmarket.co.kr/search?keyword='
    url_tail1 = '&s=8'
    url = url_query+url_kword+url_tail1

    result = requests.get(url, headers=headers)
    result.raise_for_status() # 웹페이지 정상 확인
    html = result.text

    #html parsing
    soup = BeautifulSoup(html, 'html.parser')
    gmarket_ntop_url = []
    qurey_arr = soup.select('div.box__item-title span a.link__item')
    for i in range(n_top):
        gmarket_ntop_url.append(qurey_arr[i]['href'])
    return gmarket_ntop_url


if __name__ == '__main__':
    
    #Parameter Set
    keyword = input("Search KeyWord 입력:")
    n_top = int(input("검색 상위 N값 입력:"))

    #keyword parsing
    url_kword = parse.quote(keyword)
    
    #Get Links
    # func_arr = [CoupangLinkGet, NaverFinalUrl, KurlyLinkGet, GmarketLinkGet]
    # fina_link_lst = []
    # for f in tqdm(func_arr):
    #     if f==NaverFinalUrl:
    #         fina_link_lst+=f(keyword, n_top)
    #     else:
    #         fina_link_lst+=f(url_kword, n_top)
    #Create txt file   
    
    #Get Links-> 네이버만
    fina_link_lst = NaverFinalUrl(keyword,n_top)
    
    with open("./finalLink.pickle", "wb") as fw:
        pickle.dump(fina_link_lst, fw)
    print("완료!!")