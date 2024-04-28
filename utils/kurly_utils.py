import time
import pyperclip
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def KurlyClickOption(driver):
    opt_btn_lst = driver.find_elements(By.CSS_SELECTOR, "#product-atf > section > div.css-1bp09d0.e17iylht1 > div.css-2lvxh7.e1qy0s5w0 > li > dd > div > div > div > div > div")
    selected_opt = []
    for i in range(len(opt_btn_lst)):
        opt_btn_lst[i].click()
        opt_name_lst = driver.find_elements(By.CSS_SELECTOR, "span.css-19h9nlb.e12wapb64")
        opt_price_lst = driver.find_elements(By.CSS_SELECTOR, "div.css-1fvrsoi.e12wapb60")

        opt_text_lst = []
        for idx, (e_n, e_p) in enumerate(zip(opt_name_lst, opt_price_lst)):
            option_name = e_n.text + "(가격: " + e_p.text + ")"
            opt_text_lst.append((idx+1, option_name))
        
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
            
            if 1<=s_opt<=len(opt_text_lst):
                break
            else:
                print(f"1부터 {len(opt_text_lst)} 범위의 숫자를 입력해주세요:")
            
                
        selected_opt.append(opt_text_lst[s_opt-1][1])
        opt_name_lst[s_opt-1].click()

    for idx, opt in enumerate(selected_opt):
        print(f"내가 선택한 {idx+1}옵션: {opt}")
    print("*"*20)
    
    return selected_opt


def KurlyOptionGet(driver, option_info):
    opt_btn_lst = driver.find_elements(By.CSS_SELECTOR, "#product-atf > section > div.css-1bp09d0.e17iylht1 > div.css-2lvxh7.e1qy0s5w0 > li > dd > div > div > div > div > div")
    
    if opt_btn_lst:
        for i in range(len(opt_btn_lst)):
            opt_btn_lst[i].click()
            opt_name_lst = driver.find_elements(By.CSS_SELECTOR, "span.css-19h9nlb.e12wapb64")
            opt_price_lst = driver.find_elements(By.CSS_SELECTOR, "div.css-1fvrsoi.e12wapb60")
            opt_text_lst = []
            for idx, (e_n, e_p) in enumerate(zip(opt_name_lst, opt_price_lst)):
                option_name = e_n.text + "(가격: " + e_p.text + ")"
                opt_text_lst.append((idx+1, option_name))
            opt_idx = str(i+1)+'번 옵션'
            option_info['options'][opt_idx] = opt_text_lst
    else:
        option_name =  driver.find_element(By.CSS_SELECTOR, "div.css-1qdyvok.e1bjklo16 > span").text
        opt_idx = '단일 옵션'
        option_info['options'][opt_idx] = [option_name]
        