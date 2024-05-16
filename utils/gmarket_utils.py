from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

#스크롤 위로 올리는 함수
def scroll_up_to_end(driver):
    driver.execute_script("window.scrollTo(0, 200);")
    
    
def GmarketClickOption(driver):
    opt_btn_lst = driver.find_elements(By.CSS_SELECTOR, "button.select-item_option")
    selected_opt = []
    opt_n_lst = []
    if not opt_btn_lst:
        e = driver.find_elements(By.CSS_SELECTOR, "#coreTotalPrice")
        if e:
            print("선택 옵션이 없습니다. 구매를 진행하겠습니다.")
            return
    
    for i in range(len(opt_btn_lst)//2):
        opt_btn_lst[i].click()
        opt_name_lst = driver.find_elements(By.CSS_SELECTOR, "a > span.text__name")
        opt_price_lst = driver.find_elements(By.CSS_SELECTOR, "span.text__price-num")
        
        opt_lst = []
        opt_text_lst = []
        idx_count = 1
        
        opt_name = opt_btn_lst[i].find_element(By.CSS_SELECTOR, "span.txt").text
        opt_n_lst.append(opt_name)
        
        for (e_n, e_p) in zip(opt_name_lst, opt_price_lst):
            if not e_n.text:
                continue
            option_name = e_n.text + "(가격: " + e_p.text + ")"
            opt_text_lst.append((idx_count, option_name))
            idx_count += 1
            opt_lst.append(e_n)
        
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
                print(f"1부터 {len(opt_text_lst)} 범위의 숫자를 입력해주세요:")
                
        selected_opt.append(opt_text_lst[s_opt-1][1])
        opt_lst[s_opt-1].click()

    for idx, opt in enumerate(selected_opt):
        print(f"내가 선택한 {idx+1}옵션: {opt}")
    print("*"*20)
    
    
    return selected_opt


def OptionConfigCheck(driver, i, deep_info):
    '''
    return 'A', opt_text_lst(해당 옵션 정보) : 계층적 옵션
    return 'B, opt_text_lst(해당 옵션 정보): 단층적 옵션
    return False : 선택이 안되는 옵션
    '''
    #옵션 버튼 클릭
    opt_btn_lst =driver.find_elements(By.CSS_SELECTOR,  "button.select-item_option")   
    
    if not opt_btn_lst:
        return False, [], []
    
    opt_btn_lst[i].click()
    driver.implicitly_wait(1)
    
    #옵션 항목 불러오기
    opt_name_lst = driver.find_elements(By.CSS_SELECTOR, "a > span.text__name")
    opt_price_lst = driver.find_elements(By.CSS_SELECTOR, "span.text__price-num")
    
    opt_text_lst = []
    idx_count = 1
    selected_opt = []
    
    for idx, (e_n, e_p) in enumerate(zip(opt_name_lst, opt_price_lst)):
        if not e_n.text:
            continue
        option_name = e_n.text + "(가격: " + e_p.text + ")"
        opt_text_lst.append((idx_count, option_name))
        selected_opt.append(idx)
        idx_count += 1
    
    if not selected_opt:
        return False, [], []
    
    #첫번째 옵션 선택
    opt_name_lst[selected_opt[0]].click()
    driver.implicitly_wait(1)
    scroll_up_to_end(driver)
    
    #옵션 종류 구분
    optino_type = 'B'
    
    #옵션 선택 후 가격 element가 나오는지 여부 확인
    e_text = driver.find_elements(By.CSS_SELECTOR, "#coreTotalPriceP > span")[0].text
    if not e_text:
        optino_type = 'A'
    
    #선택된 옵션 삭제             
    while True:
        try:
            driver.find_element(By.CSS_SELECTOR, "li > div.choose_result > button.close.sp_vipgroup").click()
            driver.implicitly_wait(1)
            break
        except:
            e_text = driver.find_elements(By.CSS_SELECTOR, "#coreTotalPriceP > span")[0].text
            if not e_text:
                break
            
    return optino_type, opt_text_lst, selected_opt
    

#옵션 항목을 dictionary 형태로 가져오기
def GmarketOptionGet(driver, idx, deep_info, option_info):
    opt_btn_lst = driver.find_elements(By.CSS_SELECTOR, "button.select-item_option") 
    opt_name = opt_btn_lst[idx].find_element(By.CSS_SELECTOR, "span.txt").text
    
    #옵션 종류 체크, 옵션 항목 불러오기
    option_type, opt_text_lst, select_opt = OptionConfigCheck(driver, idx, deep_info)
    scroll_up_to_end(driver)
    if option_type=='A':
        option_info[opt_name] = dict()
        for opt_idx, opt_text in enumerate(opt_text_lst):
            if deep_info: 
                for oi, ii in deep_info:
                    opt_btn_lst[oi].click()
                    driver.implicitly_wait(1)        
                    opt_ele_lst =driver.find_elements(By.CSS_SELECTOR, "a > span.text__name")
                    opt_ele_lst[ii].click()
                    driver.implicitly_wait(1)
            opt_btn_lst =driver.find_elements(By.CSS_SELECTOR, "button.select-item_option")
            opt_btn_lst[idx].click()
            driver.implicitly_wait(1)
            opt_ele_lst =driver.find_elements(By.CSS_SELECTOR, "a > span.text__name")
            opt_ele_lst[select_opt[opt_idx]].click()
            driver.implicitly_wait(1)
            scroll_up_to_end(driver)
            option_info[opt_name][opt_text] =dict()
            deep_info.append((idx, select_opt[opt_idx]))
            GmarketOptionGet(driver, idx+1, deep_info[:], option_info[opt_name][opt_text])
            deep_info.pop()
    elif option_type=='B':
        option_info[opt_name] = opt_text_lst
        scroll_up_to_end(driver)
    return


