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
    if driver.find_elements(By.CSS_SELECTOR, "fieldset > div > div:nth-child(1) > div > div > button:nth-child(1)"):
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
    #이부분 나중에 데이터베이스 연결
    ID = id
    PW = pw
    ret = NaverLogin(ID, PW, driver, main_handle)
    #########################################################
    #구매진행
    if ret:
        NaverAddressCheck(driver,main_handle)


def CoupangSession(id, pw, url):
    #url은 구매 가능한 상세페이지로 시작, 추후 작업 진행
    user_agent = "'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    
    coupang_id = id
    coupang_pw = pw
    
    # 옵션 생성
    options = webdriver.ChromeOptions()
    # user-agent 설정
    options.add_argument(f"--user-agent={user_agent}")
    
    #URL 접근
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(2)
    driver.implicitly_wait(20)
    
    #로그인 버튼 누르기
    driver.find_element(By.CSS_SELECTOR , 'div.clearFix > ul > li.my-coupang.more > a').click()
    time.sleep(3)

    e = driver.find_element(By.CSS_SELECTOR, 'input[type=email]')
    p = driver.find_element(By.CSS_SELECTOR, 'input[type=password]')
    while e.get_attribute('value')=='' and p.get_attribute('value')=='' :
        pyperclip.copy(coupang_id) # COMMAND+c가 된 상태
        e.send_keys(Keys.COMMAND, 'v') # COMMAND+v
        time.sleep(4)
        pyperclip.copy(coupang_pw) # COMMAND+c
        p.send_keys(Keys.COMMAND, 'v') # cCOMMAND+v
        time.sleep(2)

    driver.find_element(By.CSS_SELECTOR , 'button.login__button.login__button--submit').click()
    driver.implicitly_wait(10)
    time.sleep(3)

    #url 재접근
    driver.get(url)
    driver.implicitly_wait(10)
    
    # driver 종료
    time.sleep(10)
    driver.quit()
    
    
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
    driver.implicitly_wait(10)

    pyperclip.copy(gmarket_id) # COMMAND+c가 된 상태
    e = driver.find_element(By.CSS_SELECTOR, 'input#typeMemberInputId')
    e.send_keys(Keys.COMMAND, 'v') # COMMAND+v
    time.sleep(2)

    pyperclip.copy(gmarket_pw) # COMMAND+c
    e = driver.find_element(By.CSS_SELECTOR, 'input#typeMemberInputPassword')
    e.send_keys(Keys.COMMAND, 'v') # cCOMMAND+v
    time.sleep(2)

    driver.find_element(By.CSS_SELECTOR , 'button#btn_memberLogin').click()
    driver.implicitly_wait(10)

    # driver 종료
    time.sleep(10)
    driver.quit()


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