import pickle
import os
from tqdm import tqdm
from collections import Counter
from scraping import *
from openai import OpenAI
from session import *
from agent import *
import config


######################################### 쇼핑 검색어 input 받기 #########################################
#url scraping
keyword = input("Search KeyWord 입력:") #질기지 않은 1등급 무항생제 스테이크용 한우 안심을 사고 싶어.
n_top = int(input("검색 상위 N값 입력:"))


######################################### Keyword Agent #########################################
#keyword_agent
input_keyword = [] #scraper 가 사용할 키워드
decision_keyword = [] #decision agent가 사용할 키워드

#voting 구현
n_select = 1
n_sh_lst, n_dc_lst = KeywordAgentVoting(n_select, client, keyword)


#앙상블 중 가장 많이 나온 키워드만 추출
input_keyword.append(Counter(n_sh_lst).most_common(1)[0][0])
decision_keyword = list(set(n_dc_lst))

#decision_keyword에 여러 키워드가 존재하면 None 값 제외시키기
if len(decision_keyword) > 1:
  try:
    decision_keyword.remove('None')
  except:
    pass

print()
print(f"input_keyword:{input_keyword}")
print(f"decision_keyword:{decision_keyword}")
print()

#TODO:#### Scarping 실행 #### 
rating_keyword_lst =  rating_keyword_agent(input_keyword, decision_keyword)
print(rating_keyword_lst)



# ######################################### Scarping 실행 #########################################
# #분리된 키워드로 scraping 실행하기
# print('scraping 작업 실행')

# url_path = os.path.join("cache", "finalLink.pickle")

# # func_arr = [NaverFinalUrl, KurlyLinkGet]
# # fina_link_lst = []

#scraping 결과
final_link_lst = []
data_details = []
data_reviews = []


final_link_lst_naver, data_details_naver, data_reviews_naver = NaverFinalUrl(input_keyword[0],n_top)
final_link_lst.append(final_link_lst_naver)
data_details.append(data_details_naver)
data_reviews.append(data_reviews_naver)

final_link_lst_kurly, data_details_kurly, data_reviews_kurly = KurlyFinalUrl(input_keyword[0], n_top)
final_link_lst.append(final_link_lst_kurly)
data_details.append(data_details_kurly)
data_reviews.append(data_reviews_kurly)

with open(url_path, "wb") as fw_url:
    pickle.dump(final_link_lst, fw_url)





print("scraping 완료!!")
print()


# ######################################### Decision Agent 실행 #########################################
# #decision_agent : use gpt api
# #Step 1. select gpt 
# select_numbers=Select_numbers(data_details, decision_keyword)
# print(f"select_numbers = {select_numbers}")
# #TODO : 현재 상태 : 만약 아무 상품도 조건을 만족하지 않는다면 empty string return됨. -> 이때 어떤 방식을 취할지 결정하고, 코드 만들기 (사용자에게 알리거나, 필터를 줄여서 다시 필터링 시도하거나....)

# #Step 2. compare gpt : 위의 select agent에서 선택된 number의 product들 중 가장 "좋은" 상품을 compare 하여 최종적으로 단 하나의 product의 url을 반환한다. 
# final_number, reason = CompareAgent(data_reviews, select_numbers)

# print()
# print(f"결정 이유 : {reason}")
# print()
# print(f"Final_Link_number:{final_number}번 링크")
# print()
# #TODO : gpt의 불확실성 때문에 하나의 숫자외에 다른게 output으로 나온다면, 오류 control 하는 코드

# #final url text file로 저장하는 코드
# # save_final_path = os.path.join("cache", "result_url.txt")
# # for idx, url in enumerate(final_link_lst) :
# #     if (idx + 1) == int(final_number) : 
# #         with open(save_final_path, "w") as file :
# #             file.write(url)

# ######################################### Back End #########################################
# final_link = final_link_lst[int(final_number)-1]
# print(f"최종 선택 사이트 URL: {final_link}")
# print()
# print('상기 사이트의 ID, PW를 입력해주세요')
# login_id = config.naver_id
# login_pw = config.naver_pw
# # login_id = input("ID:")
# # login_pw = input("PW:")
# print()


# NaverSession(login_id, login_pw, final_link)