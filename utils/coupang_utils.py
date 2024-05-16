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
            if driver.find_elements(By.CSS_SELECTOR, "div.option-table-list__option-radio"):
                opt_text_lst = [' '.join(opt_text_lst)]
            
            if not opt_text_lst:
                break       
        
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
        selec_opt_lst[s_opt-1].click()

    for idx, opt in enumerate(selected_opt):
        print(f"내가 선택한 {idx+1}옵션: {opt}")
    print("*"*20)
    
    return selected_opt


def CoupangRaidoOption(driver):
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
        