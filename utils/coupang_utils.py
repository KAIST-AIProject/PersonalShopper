from utils import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def CoupangClickOption(driver):
    opt_btn_lst = driver.find_elements(By.CSS_SELECTOR, "div.prod-option__selected-container")
    if not opt_btn_lst:
        opt_btn_lst = driver.find_elements(By.CSS_SELECTOR, "div.option-table-list__option")
    iter_num = len(opt_btn_lst)
    selected_opt = []
    for i in range(iter_num):
        opt_btn_lst = driver.find_elements(By.CSS_SELECTOR, "div.prod-option__selected-container")
        if not opt_btn_lst:
            opt_btn_lst = driver.find_elements(By.CSS_SELECTOR, "div.option-table-list__option")
        e = opt_btn_lst[i]
        e.click() 
        selec_opt_lst = driver.find_elements(By.CSS_SELECTOR, "li.prod-option-dropdown-item > a > div > div.prod-option__dropdown-item-title")
        option_lst = e.text.split('\n')
        option_name = option_lst[0]
        opt_text_lst = option_lst[1:]
        if option_name == "수량" and len(opt_text_lst):
            print("단일옵션입니다. 구매를 진행합니다.")
            return selected_opt
        
        if len(opt_text_lst) == 1:
            opt_text_lst = [s_e.text for s_e in selec_opt_lst if s_e.text]
            if not opt_text_lst:
                print("옵션이 없습니다.")
                return []  
        
        for idx, opt in enumerate(opt_text_lst):
            print(f"{idx+1}번 옵션: {opt}")
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
                print(f"1부터 {len(opt_text_lst)} 범위의 숫자를 입력해주세요:")
            
                
        selected_opt.append(opt_text_lst[s_opt-1])
        selec_opt_lst[s_opt].click()

    for idx, opt in enumerate(selected_opt):
        print(f"내가 선택한 {idx+1}옵션: {opt}")
    print("*"*20)
    
    return selected_opt


def CoupangRadioOption(driver):
    opt_btn_lst = driver.find_elements(By.CSS_SELECTOR, "div.option-table-list__option-radio")
    option_name = driver.find_elements(By.CSS_SELECTOR, "div.option-table-list__option-name")
    option_price = driver.find_elements(By.CSS_SELECTOR, "div.option-table-list__option-price")
    selected_opt = []
    opt_text_lst = []
    for n,p in zip(option_name, option_price):
        opt_text_lst.append(n.text + "(가격: " + p.text + ")")
    for idx, opt in enumerate(opt_text_lst):
        print(f"{idx+1}번 옵션: {opt}")
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
            print(f"1부터 {len(opt_text_lst)} 범위의 숫자를 입력해주세요:")
        
            
    selected_opt.append(opt_text_lst[s_opt-1])
    opt_btn_lst[s_opt-1].click()

    for idx, opt in enumerate(selected_opt):
        print(f"내가 선택한 {idx+1}옵션: {opt}")
    print("*"*20)
    
    return selected_opt

def CoupangImgOption(driver):
    selected_opt = []
    option_name= driver.find_elements(By.CSS_SELECTOR, "div.tab-selector__tab-image-title")

    #옵션 종류 이름 
    opt_type_name = driver.find_element(By.CSS_SELECTOR, "span.tab-selector__header-title").text
    opt_lst = []
    for i in range(len(option_name)):
        opt_lst.append(option_name[i].text )

    for idx, opt in enumerate(opt_lst):
        print(f"{idx+1}번 옵션: {opt}")
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
        
        if 1<=s_opt<=len(opt_lst):
            break
        else:
            print(f"1부터 {len(opt_lst)} 범위의 숫자를 입력해주세요:")
        
            
    selected_opt.append(opt_lst[s_opt-1])
    option_name[s_opt-1].click()
    driver.implicitly_wait(1)

    driver.find_elements(By.CSS_SELECTOR, "div.option-table-list__option-radio")[0].click()

    for idx, opt in enumerate(selected_opt):
        print(f"내가 선택한 {idx+1}옵션: {opt}")
    print("*"*20)
        
        
############################################# Option Scraping #############################################
def CoupangContainerOptionGet(driver, option_info):
    opt_btn_lst = driver.find_elements(By.CSS_SELECTOR, "div.prod-option__selected-container > button.prod-option__selected.multiple")
    if not opt_btn_lst:
        opt_btn_lst = driver.find_elements(By.CSS_SELECTOR, "div.option-table-list__option")    
    iter_num = len(opt_btn_lst)

    for i in range(iter_num):
        #옵션 버튼 클릭하면서 세션이 새롭게 열림. 다시 선택해야함
        opt_btn_lst = driver.find_elements(By.CSS_SELECTOR, "div.prod-option__selected-container > button.prod-option__selected.multiple")
        if not opt_btn_lst:
            opt_btn_lst = driver.find_elements(By.CSS_SELECTOR, "div.option-table-list__option")
        e = opt_btn_lst[i]
        e.click()
        opt_name = e.find_element(By.CSS_SELECTOR, "span.title").text 
        selec_opt_lst = driver.find_elements(By.CSS_SELECTOR, "li.prod-option-dropdown-item")
        
        opt_lst = []
        for s_e in selec_opt_lst:
            if not s_e.text:
                continue
            opt_lst.append(s_e.text)
        e.click()
        
        option_info['options'][opt_name] = opt_lst


def CoupangRadioOptionGet(driver, option_info):
    option_name = driver.find_elements(By.CSS_SELECTOR, "div.option-table-list__option-name")
    option_price = driver.find_elements(By.CSS_SELECTOR, "div.option-table-list__option-price")

    #옵션 종류 이름
    opt_type_name = driver.find_elements(By.CSS_SELECTOR, "span.tab-selector__header-title")
    
    opt_lst = []
    for n,p in zip(option_name, option_price):
        opt_lst.append(n.text + "(가격: " + p.text + ")")
    
    if opt_type_name:
        option_info['options'][opt_type_name] = opt_lst
    else:
        option_info['options'] = opt_lst
    

def CoupangImgOptinoGet(driver, option_info):
    option_name= driver.find_elements(By.CSS_SELECTOR, "div.tab-selector__tab-image-title")

    #옵션 종류 이름 
    opt_type_name = driver.find_element(By.CSS_SELECTOR, "span.tab-selector__header-title").text
    opt_lst = []
    for i in range(len(option_name)):
        opt_lst.append(option_name[i].text )
        
    option_info['options'][opt_type_name] = opt_lst


def CoupangOptionGet(driver, option_info):
    radio_opt_lst = driver.find_elements(By.CSS_SELECTOR, "div.option-table-list__option-radio")
    img_opt_lst = driver.find_elements(By.CSS_SELECTOR, "div.tab-selector__tab-image-title")    
    if img_opt_lst:
        CoupangImgOptinoGet(driver,option_info)
    else:
        if radio_opt_lst:
            CoupangRadioOptionGet(driver,option_info)
        else: 
            CoupangContainerOptionGet(driver,option_info)
