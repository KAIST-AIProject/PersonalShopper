import time
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from utils import *

#debugging mode 실행 터미널 명령어
#/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="/Users/Woo/Applications/Google Chrome.app/
 
def NaverSession(id, pw, url, debug_mode=True):
    chrome_options = Options() ## 옵션 추가를 위한 준비
    if debug_mode:
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222") ## 디버깅 옵션 추가

    # 크롬 드라이버 생성
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    driver.implicitly_wait(3) ## 연결 후 3초간 기다리기
    
    #########################################################    
    #옵션 선택
    if driver.find_elements(By.CSS_SELECTOR, "#content > div > div._2-I30XS1lA > div._2QCa6wHHPy > fieldset > div.bd_1jsdQ > div:nth-child(1) > div > div > button"):
        select_opt = NaverClickOption(driver)
    else:
        if driver.find_elements(By.CSS_SELECTOR, "fieldset > div > ul > li > div > div > div > input"):
            select_opt = ''
            print("선택 옵션이 없습니다.")
        else:
            select_opt = NaverBtnOption(driver)
            
    #########################################################
    #구매 버튼 선택
    driver.find_element(By.CSS_SELECTOR, 'fieldset > div > div:nth-child(1) > div > a').click()

    # 팝업창 '확인' 클릭
    from selenium.webdriver.common.alert import Alert
    main_handle = driver.current_window_handle
    da = Alert(driver)

    try:
        da.accept()
        print("로그인을 진행하겠습니다.")
    except:
        print("로그인을 진행하겠습니다.")
        
    driver.implicitly_wait(3)
    
    #배송지 선택    
    NaverAddressCheck(driver,main_handle)


def CoupangSession(id, pw, url, debug_mode=True):    
    chrome_options = Options() ## 옵션 추가를 위한 준비
    if debug_mode:
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222") ## 디버깅 옵션 추가
   
    # 크롬 드라이버 생성
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    driver.implicitly_wait(3) ## 연결 후 3초간 기다리기
    
    #옵션 선택
    radio_opt_lst = driver.find_elements(By.CSS_SELECTOR, "div.option-table-list__option-radio")
    if radio_opt_lst:
        selected_opt = CoupangRadioOption(driver)
    else:
        selected_opt = CoupangClickOption(driver)

    #구매 버튼 선택
    driver.find_element(By.CSS_SELECTOR, "button.prod-buy-btn").click()

    #로그인 시도
    coupang_id = config.coupang_id
    coupang_pw = config.coupang_pw

    e = driver.find_element(By.CSS_SELECTOR, 'input[type=email]')
    p = driver.find_element(By.CSS_SELECTOR, 'input[type=password]')

    e.send_keys(coupang_id) 
    driver.implicitly_wait(1)
        
    p.send_keys(coupang_pw)
    driver.implicitly_wait(1)

    driver.find_element(By.CSS_SELECTOR , 'button.login__button.login__button--submit').click()
    driver.implicitly_wait(3)
    
    
def KurlySession(id, pw, url, debug_mode=True):
    #url은 구매 가능한 상세페이지로 시작, 추후 작업 진행
    kurly_id = id
    kurly_pw = pw

    chrome_options = Options() ## 옵션 추가를 위한 준비
    if debug_mode:
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222") ## 디버깅 옵션 추가

    # 크롬 드라이버 생성
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    driver.implicitly_wait(3) ## 연결 후 3초간 기다리


    #옵션 불러오기
    price = driver.find_element(By.CSS_SELECTOR, "#product-atf > section > div.css-1bp09d0.e17iylht1 > div.css-9y0nwt.e17iylht0 > div > div.css-yhijln.eebc7rx7 > span.css-x4cdgl.eebc7rx5").text

    if price=="0":
        selected_opt = KurlyClickOption(driver)

    #장바구니 담기
    cartin_btn = driver.find_element(By.CSS_SELECTOR, "button.cart-button.css-1qirdbn.e4nu7ef3")
    cartin_btn.click()    
        
    #장바구니로 이동
    cartgo_btn = driver.find_element(By.CSS_SELECTOR, "button.css-g25h97.e14oy6dx1")
    cartgo_btn.click()
            
    #로그인 버튼 클릭
    login_btn = driver.find_element(By.CSS_SELECTOR, "button.css-fwelhw.e4nu7ef3")
    login_btn.click()

    #로그인 시도
    e = driver.find_element(By.NAME, 'id')
    e.send_keys(kurly_id) # COMMAND+v

    e = driver.find_element(By.NAME, 'password')
    e.send_keys(kurly_pw) # cCOMMAND+v

    driver.find_element(By.CSS_SELECTOR , 'button.css-qaxuc4.e4nu7ef3').click()
    driver.implicitly_wait(1)

    #주문하기 버튼 클릭
    driver.find_element(By.CSS_SELECTOR, "button.css-fwelhw.e4nu7ef3").click()
    
def GmarketSession(id, pw, url, debug_mode=True):
    gmarket_id = id
    gmarket_pw = pw
    
    chrome_options = Options() ## 옵션 추가를 위한 준비
    if debug_mode:
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222") ## 디버깅 옵션 추가

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    driver.implicitly_wait(3)

    while True:
        GmarketClickOption(driver)
        driver.implicitly_wait(3)
    
        #구매버튼 클릭
        driver.find_element(By.CSS_SELECTOR, "#coreInsOrderBtn").click()
        driver.implicitly_wait(1)
    
        try:
            driver.switch_to.alert.accept()
            print("구매에 제한이 있는 상품입니다. 구매 시 인증이 필요하기 때문에 다른 상품을 선택해주세요.")
            driver.get(url)
            driver.implicitly_wait(3)
        except:
            break
        
    GmarketLogin(gmarket_id, gmarket_pw, driver)

from session import *

#구매 진행 함수
def purchase_process(final_link):
    if "naver" in final_link:
        login_id=config.naver_id
        login_pw=config.naver_pw
        NaverSession(login_id, login_pw, final_link)
    elif "kurly" in final_link:
        login_id=config.kurly_id
        login_pw=config.kurly_pw
        KurlySession(login_id, login_pw, final_link)
    elif "coupang" in final_link:
        login_id=config.coupang_id
        login_pw=config.ciupang_pw
        CoupangSession(login_id, login_pw, final_link)
    elif "gmarket" in final_link:
        login_id=config.gmarket_id
        login_pw=config.gmarket_pw
        GmarketSession(login_id, login_pw, final_link)
    else:
        print("지원하지 않는 사이트입니다.")
    


if __name__ == "__main__":
    login_site = {"naver":'https://nid.naver.com/nidlogin.login?mode=form&url=https://www.naver.com/',
                  "coupang": "https://login.coupang.com/login/login.pang?login_challenge=87eba72465a143cfa0a70e78e761899e",
                  "kurly": "https://www.kurly.com/member/login",
                  "gmarket": 'https://signin.gmarket.co.kr/LogIn/LogIn?URL=http://myg.gmarket.co.kr/'}
    
    
    
    function_dict = {"naver":NaverSession,
                  "coupang": CoupangSession,
                  "kurly": KurlySession,
                  "gmarket": GmarketSession}
    
    # test
    site = "naver"
    ID = 'dwkim8155@naver.com'
    PW = 'dwkim+ad7733'
    url = 'https://smartstore.naver.com/solsweet/products/5211086676?NaPm=ct%3Dluusxza8%7Cci%3Dc336f02cc3423697e362eecbdea60b76e158f9f3%7Ctr%3Dsls%7Csn%3D1166073%7Chk%3Dfe6355fb05713726c54f98e47fd7bbc551af1bd8'
    
    function_dict[site](ID, PW, url)