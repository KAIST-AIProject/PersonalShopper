# 네이버 블로그 자동 글발행
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pyperclip


def NaverSession(id, pw, url):
    #url은 구매 가능한 상세페이지로 시작, 추후 작업 진행
    naver_id = id
    naver_pw = pw

    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(5)

    pyperclip.copy(naver_id) # COMMAND+c가 된 상태
    e = driver.find_element(By.NAME, 'id')
    e.send_keys(Keys.COMMAND, 'v') # COMMAND+v
    time.sleep(2)

    pyperclip.copy(naver_pw) # COMMAND+c
    e = driver.find_element(By.NAME, 'pw')
    e.send_keys(Keys.COMMAND, 'v') # cCOMMAND+v
    time.sleep(2)

    driver.find_element(By.CLASS_NAME, 'btn_login').click()
    driver.implicitly_wait(10)
    
    # driver 종료
    time.sleep(10)
    driver.quit()


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
    
    
def KurlySession(id, pw, url):
    #url은 구매 가능한 상세페이지로 시작, 추후 작업 진행
    kurly_id = id
    kurly_pw = pw

    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(10)

    pyperclip.copy(kurly_id) # COMMAND+c가 된 상태
    e = driver.find_element(By.NAME, 'id')
    e.send_keys(Keys.COMMAND, 'v') # COMMAND+v
    time.sleep(2)

    pyperclip.copy(kurly_pw) # COMMAND+c
    e = driver.find_element(By.NAME, 'password')
    e.send_keys(Keys.COMMAND, 'v') # cCOMMAND+v
    time.sleep(2)

    driver.find_element(By.CSS_SELECTOR , 'button.css-qaxuc4.e4nu7ef3').click()
    driver.implicitly_wait(10)

    # driver 종료
    time.sleep(10)
    driver.quit()
    
def GmarketSession(id, pw, url):
    gmarket_id = id
    gmarket_pw = pw

    driver = webdriver.Chrome()
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
    site = "coupang"
    ID = 'dwkim8155@naver.com'
    PW = 'clsrn+ad7733'
    url = 'https://www.coupang.com/vp/products/6667719?itemId=29571747&vendorItemId=3043948891&sourceType=SDW_TOP_SELLING_WIDGET_V2&searchId=c24816ed1925446aa9d5977713584fed&q=%EA%B3%BC%EC%9E%90&isAddedCart='
    
    function_dict[site](ID, PW, url)