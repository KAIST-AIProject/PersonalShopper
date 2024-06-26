import time
import pyperclip
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


#계측적인지 단층적인지 옵션 종류 판단
def OptionConfigCheck(driver, i, deep_info):
    '''
    return 'A', opt_text_lst(해당 옵션 정보) : 계층적 옵션
    return 'B, opt_text_lst(해당 옵션 정보): 단층적 옵션
    return False : 선택이 안되는 옵션
    '''
    
    
    #옵션 버튼 클릭
    while True:
        try:
            opt_btn_lst =driver.find_elements(By.CSS_SELECTOR, '[data-shp-area-id*=opt]._nlog_impression_element')   
            opt_btn_lst[i].click()
            driver.implicitly_wait(1)
            break
        except:
            continue
        
    #옵션 항목 불러오기
    opt_ele_lst =driver.find_elements(By.CSS_SELECTOR, 'li[role=presentation].bd_1y1pd > a[role="option"]')
    if not opt_ele_lst:
        return False, []
    
    #오셥 항목 이름 불러오기
    opt_text_lst = []    
    for idx, e in enumerate(opt_ele_lst):
        opt_text_lst.append((idx+1,e.text))
    
    for e in opt_ele_lst:
        if '품절' in e.text:
            continue
        e.click()
        driver.implicitly_wait(1)
        total_price = driver.find_element(By.CSS_SELECTOR, "div.bd_3XvVU > strong > span.bd_32Qz_").text        
        break
    else:
        total_price = 10000000
        opt_btn_lst[i].click()
        driver.refresh()
        
    
    #옵션 종류 구분
    optino_type = 'B'
    if total_price == "0":
        optino_type = 'A'
    
    #선택된 옵션 삭제             
    try:
        driver.find_element(By.CSS_SELECTOR, "button.bd_2I3cR._nlog_click").click()
    except:
        pass     
    return optino_type, opt_text_lst
    

#옵션 항목을 dictionary 형태로 가져오기
def NaverOptionGet(driver, idx, deep_info, option_info):
    opt_btn_lst =driver.find_elements(By.CSS_SELECTOR, '[data-shp-area-id*=opt]._nlog_impression_element')
    opt_e = opt_btn_lst[idx]
    opt_name = opt_e.text
    
    #옵션 종류 체크, 옵션 항목 불러오기
    option_type, opt_text_lst = OptionConfigCheck(driver, idx, deep_info)
    if option_type=='A':
        option_info[opt_name] = dict()
        for opt_idx, opt_text in enumerate(opt_text_lst):
            if deep_info: 
                for oi, ii in deep_info:
                    opt_btn_lst[oi].click()        
                    opt_ele_lst =driver.find_elements(By.CSS_SELECTOR, 'a[role="option"]')
                    opt_ele_lst[ii].click()
            opt_btn_lst =driver.find_elements(By.CSS_SELECTOR, '[data-shp-area-id*=opt]._nlog_impression_element')
            opt_btn_lst[idx].click()
            opt_ele_lst =driver.find_elements(By.CSS_SELECTOR, 'a[role="option"]')
            opt_ele_lst[opt_idx].click()
            
            option_info[opt_name][opt_text] =dict()
            deep_info.append((idx, opt_idx))
            NaverOptionGet(driver, idx+1, deep_info[:], option_info[opt_name][opt_text])
            deep_info.pop()
    elif option_type=='B':
        option_info[opt_name] = opt_text_lst
    return

#backend에서 input을 받아 옵션을 선택하는 함수
def NaverBtnOption(driver):
    opt_btn_lst =driver.find_elements(By.CSS_SELECTOR, '[data-shp-area-id*=opt]._nlog_impression_element')
    selected_opt = []
    for i in range(len(opt_btn_lst)//2):
        opt_btn_lst[i].click()
        opt_ele_lst =driver.find_elements(By.CSS_SELECTOR, 'a[role="option"]')
        opt_text_lst = []
        for idx, e in enumerate(opt_ele_lst):
            opt_text_lst.append((idx+1,e.text))
        opt_name = opt_btn_lst[i].text
        print(f"{i+1}번 옵션:{opt_name}")
        for opt in opt_text_lst:
            print(f"{opt[0]}. {opt[1]}")
        print("*"*20)
        while True:
            try:
                s_opt = int(input("위 옵션 중 번호를 선택해주세요:"))
            except:
                print("정수형태의 번호로 다시 입력해주세요")
                continue
            
            if "품절" in opt_text_lst[s_opt-1][1]:
                print("품절된 옵션입니다. 다시 선택해주세요")
                continue
            
            if 1<=s_opt<=len(opt_ele_lst):
                break
            else:
                print(f"1부터 {len(opt_ele_lst)} 범위의 숫자를 입력해주세요:")
            
                
        selected_opt.append((opt_name,opt_text_lst[s_opt-1][1]))
        opt_ele_lst[s_opt-1].click()

    for idx, opt in enumerate(selected_opt):
        print(f"내가 선택한 {opt[0]} 옵션: {opt[1]}")
    print("*"*20)
    return selected_opt


def NaverClickOption(driver):
    opt_btn_lst =driver.find_elements(By.CSS_SELECTOR, '[data-shp-area-id*=opt]._nlog_impression_element')
    selected_opt = []
    opt_name_lst = []
    for i in range(len(opt_btn_lst)//2):
        
        click_opt_lst = opt_btn_lst[i].find_elements(By.CSS_SELECTOR, "button._nlog_click")
        opt_text_lst = []
        
        opt_name = click_opt_lst[0].get_attribute("data-shp-contents-type")
        opt_name_lst.append(opt_name)
        
        for idx, e in enumerate(click_opt_lst):
            opt_text_lst.append((opt_name, e.get_attribute("data-shp-contents-id")))
        
        print(f'{i+1}번 옵션:{opt_name}')
        for opt in opt_text_lst:
            print(f"{opt[0]}. {opt[1]}")
        print("*"*20)
        while True:
            try:
                s_opt = input("위 옵션 중 번호를 선택해주세요:")
                s_opt = int(s_opt)
            except:
                if s_opt == "":
                    break
                print("정수형태의 번호로 다시 입력해주세요")
                continue
            if 1<=s_opt<=len(opt_text_lst):
                break
            else:
                print(f"1부터 {len(opt_text_lst)}범위의 숫자를 입력해주세요")
            
        selected_opt.append(opt_text_lst[s_opt-1])
        click_opt_lst[s_opt-1].click()

    for idx, opt in enumerate(selected_opt):
        print(f"내가 선택한 {opt_name_lst[idx]} 옵션: {opt[1]}")
    print("*"*20)
    return selected_opt


def NaverLogin(ID, PW, driver):
    
   #로그인 버튼 누르기
    driver.find_element(By.CSS_SELECTOR, '#gnb_login_button').click()
    driver.implicitly_wait(3)
    
    e = driver.find_element(By.CSS_SELECTOR, '#id')
    e.click()
    driver.implicitly_wait(3)
    cnt=0
    while not e.get_attribute('value'):
        if cnt>=3:
            e.send_keys(ID)
            continue
        pyperclip.copy(ID) # COMMAND+c가 된 상태
        driver.implicitly_wait(3)
        e.click()
        e.send_keys(Keys.COMMAND, 'v') # COMMAND+v
        driver.implicitly_wait(2)
        cnt+=1
    
    e = driver.find_element(By.CSS_SELECTOR, '#pw')
    e.click()
    driver.implicitly_wait(3)
    while not e.get_attribute('value'):    
        if cnt>=3:
            e.send_keys(PW)
            continue
        pyperclip.copy(PW) # COMMAND+c
        e.click()
        driver.implicitly_wait(3)
        e.send_keys(Keys.COMMAND, 'v') # cCOMMAND+v
        driver.implicitly_wait(2)

    driver.find_element(By.CSS_SELECTOR , 'button.btn_login').click()
    driver.implicitly_wait(10)
  
  

def clearText(driver):
    input_e = driver.find_element(By.CSS_SELECTOR, 'div > div.article > div > div > div.InputBoxSearch_article__ckXvT > div.InputBoxSearch_section-input__C7oz4 > div > div > input')
    driver.implicitly_wait(3)
    for i in range(len(input_e.get_attribute('value'))):
        input_e.send_keys(Keys.BACKSPACE)
    driver.implicitly_wait(3)
    
    
def NaverCreateAddress(driver):
    #배송지 신규입력 버튼 클릭
    driver.find_element(By.CSS_SELECTOR, "#content > div > button").click()
    while True:
        address1 = input("동, 호수를 제외한 주소를 입력해주세요:")
        if address1.lower() == 'e':
            return
        input_e = driver.find_element(By.CSS_SELECTOR, 'div.InputBoxSearch_section-input__C7oz4 > div > div > input')
        input_e.send_keys(address1)
        driver.find_element(By.CSS_SELECTOR, "div.InputBoxSearch_section-button__1Y3FN > button").click()
        #주소 유효성 체크
        e = driver.find_elements(By.CSS_SELECTOR, "div.AddressSearchResult_article__2wP2s > div > ul > li > div > button")

        if e:
            if len(e)>1:
                print("주소가 여러개 검색됩니다. 더 상세한 주소를 입력해주세요.")  
                driver.implicitly_wait(5)                
                clearText(driver)
            else:
                driver.find_element(By.CSS_SELECTOR,'div.AddressSearchResult_article__2wP2s > div > ul > li > div > button').click()
                break
        else:
            print("주소가 검색되지 않습니다. 정확한 주소를 입력해주세요.")
            driver.implicitly_wait(5)
            clearText(driver)
            continue
            
    address2 = input("상세주소를 입력해주세요:")
    e = driver.find_element(By.CSS_SELECTOR, '#address-detail')
    e.send_keys(address2)

    #최종확인버튼 누르기
    driver.find_element(By.CSS_SELECTOR, "div.ButtonRegister_article__1Yh2t > button").click()

    #받는이 적기
    name = input("받는 이를 입력해주세요:")
    e = driver.find_element(By.CSS_SELECTOR, "#receiver")
    e.send_keys(name)
    e.send_keys(Keys.ENTER)

    #연락처 적기
    contact = input("받는 이를 입력해주세요:")
    e = driver.find_element(By.CSS_SELECTOR, "#contact-1")
    e.send_keys(contact)
    e.send_keys(Keys.ENTER)

    #주소 저장하기
    driver.find_element(By.CSS_SELECTOR, "div.ButtonRegister_article__1Yh2t > button").click()
    driver.close()


def NaverSelectAdderss(driver, main_handle):        
    #저장된 주소 목록에서 선택하기
    driver.implicitly_wait(5)
    address_ele_lst = driver.find_elements(By.CSS_SELECTOR, "div[class*=DeliveryList_area-address__]")
    ad_arr =[]
    print("저장된 주소 목록")
    print("*"*20)
    for idx, ad in enumerate(address_ele_lst):
        adr = ad.find_element(By.CSS_SELECTOR, "p").text
        ad_arr.append(adr)
        print(f"{idx+1}. {adr}")

    while True:
        ad_flag = input("이 배송지 목록에서 배송지를 선택하려면 'yes'를, 새로운 주소를 추가하시려면 'no'를 입력해주세요:")
        if ad_flag=="yes":
            while True:
                try:
                    s_num = int(input("선택할 배송지의 번호를 선택해주세요:"))
                except:
                    print("정수형태의 번호로 다시 입력해주세요")
                    continue
                if 1<=s_num<=len(address_ele_lst):
                    break
                else:
                    print(f"1부터 {len(address_ele_lst)}범위의 번호를 입력해주세요")
            address_ele_lst[s_num-1].find_element(By.CSS_SELECTOR, "button.DeliveryList_button-address__1mS3A").click()
            return ad_arr[s_num-1]
            
        elif ad_flag=="no":
            NaverCreateAddress(driver)
            print("주소를 추가하였습니다. 주소 선택 과정을 다시 진행해주세요")
            print("*"*20)
            driver.switch_to.window(main_handle)
            while driver.current_window_handle != main_handle:
                driver.switch_to.window(main_handle)
            
            #주소 변경 클릭
            driver.implicitly_wait(5)
            time.sleep(2)
            driver.find_element(By.CSS_SELECTOR, "div.DeliveryContent_area-button__jJ5eK > button").click()
            driver.implicitly_wait(3)
            
            #windows check
            while True:
                if len(driver.window_handles)==1:
                    continue
                else:
                    break
            #창 전환
            for w in driver.window_handles:
                if w != main_handle:
                    driver.switch_to.window(w)
                    break
            
            return NaverSelectAdderss(driver,main_handle)
        elif ad_flag == 'e':
            break
        else:
            print("입력 형식이 잘못 되었습니다.다시 입력해주세요")
        
#기본 배송지 확인
def NaverAddressCheck(driver, main_handle):
    address = driver.find_element(By.CSS_SELECTOR, "div.DeliveryContent_area-address__3llA_").text
    print("*"*20)
    flag = input(f"{address}로 배송을 원하시면\n 'yes'를 다른 배송지를 원하면 'no'를 입력해주세요:")
    if flag.lower()=="yes":
        driver.find_element(By.CSS_SELECTOR, 'div.SubmitButton_article__133Dz.SubmitButton_type-pc__Vwp7H > button').click()
    elif flag.lower()=="no":
        #주소 변경 클릭
        driver.implicitly_wait(5)
        driver.find_element(By.CSS_SELECTOR, "div.DeliveryContent_area-button__jJ5eK > button").click()
        driver.implicitly_wait(3)
        
        #windows check
        while True:
            if len(driver.window_handles)==1:
                continue
            else:
                break
        #창 전환
        for w in driver.window_handles:
            if w != main_handle:
                driver.switch_to.window(w)
                break
            
        select_address = NaverSelectAdderss(driver,main_handle)
        print(f"선택된 주소\n{select_address}")
        driver.switch_to.window(main_handle)
        driver.find_element(By.CSS_SELECTOR, 'div.SubmitButton_article__133Dz.SubmitButton_type-pc__Vwp7H > button').click()
    elif flag =='e':
        return
    else:
        print("입력 형식이 잘못 되었습니다.다시 입력해주세요")
        NaverAddressCheck(driver, main_handle)
    
    