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
print('평가 기준 추출 작업 실행')
rating_keyword_lst =  rating_keyword_agent(input_keyword, decision_keyword)
print(f'평가 기준: {rating_keyword_lst}')
print()


######################################### Scarping 실행 #########################################
#분리된 키워드로 scraping 실행하기
print('scraping 작업 실행')

url_path = os.path.join("cache", "finalLink.pickle")
website_name  = ['naver', 'kurly', 'coupang', 'gmarket']
func_arr = [NaverFinalUrl, KurlyFinalUrl]


######################################### Multi-threading #########################################
thread = [MyThread(f, input_keyword[0], n_top) for f in func_arr]

for t in thread:
  t.start()  

for t in thread:
  t.join()
  
#scraping 결과 저장
final_link_dict = dict()
data_details_dict = dict()
data_reviews_dict = dict()

final_link_lst = []
data_details = []
data_reviews = []

for idx, thr_ret in enumerate(thread):
  final_link_dict[idx], data_details_dict[idx], data_reviews_dict[idx] = thr_ret.get_result()
  final_link_lst+=final_link_dict[idx]
  data_details+=data_details_dict[idx]
  data_reviews+=data_reviews_dict[idx]

print(final_link_lst)

with open(url_path, "wb") as fw_url:
    pickle.dump(final_link_lst, fw_url)

print("scraping 완료!!")
print()


######################################### Decision Agent 실행 #########################################
#decision_agent : use gpt api
#Step 1. select gpt 
# print(f"전체 data_details : {data_details}")
if decision_keyword[0] == "None" :
   select_numbers = [i+1 for i in range(len(data_details))]
else :
      select_numbers=Select_numbers(data_details, decision_keyword)
print(f"select_numbers = {select_numbers}") #select agent를 거쳐 filtering 된 product numbers의 리스트 

costs =[] 
for i in range(len(data_reviews)):
    print(data_details[i]['상품명'], data_details[i]['현재 가격'], data_details[i]['할인 전 가격'])
    costs.append(float(int(data_details[i]['현재 가격'])))

cost_min = min(costs)
cost_max = max(costs)
for i in range(len(data_reviews)):
   costs[i] = 5-5*(costs[i]-cost_min)/(cost_max-cost_min)


#rating 점수로 순위 매기기 
final_score = []
for i in range(len(data_reviews)) :
    if i+1 in select_numbers : #select agent에서 선택된 product만 rating 
      print()
      print(f"==============================={i+1} 번째 product scoring 계산 중...================================")
      scores = scoring_agent(data_reviews[i], rating_keyword_lst) 
      scores.append(round(costs[i],3))
      final_score.append([round(sum(scores)/5,2), i+1, scores]) 

final_score.sort( reverse = True)

#최종 순위 출력
final_num=5
if len(final_score)<5:
    final_num=len(final_score)
print()
print(f"## rating keyword : price, review positivity, {rating_keyword_lst[0]}, {rating_keyword_lst[1]}, {rating_keyword_lst[2]}")
for i in range(final_num) :
  print(f"{i+1}순위 : {final_score[i][1]}번 product , scores = {final_score[i][2]}, 평균 점수 : {final_score[i][0]} ")

#TODO : 사용자가 선택한 숫자에 해당하는 링크를 반환. 
user_select_num = int(input("최종 선택할 product의 번호를 입력하세요:"))

print(f"Final_Link_number:{user_select_num}번 링크")
print()

######################################### Back End #########################################
final_link = final_link_lst[user_select_num-1]
print(f"최종 선택 사이트 URL: {final_link}")
print()
login_id = config.naver_id
login_pw = config.naver_pw
# login_id = input("ID:")
# login_pw = input("PW:")

flag = input("구매 진행하시겠습니까? (Y/N):")

while True:
  if flag.upper() == 'Y': 
    purchase_process(final_link)
  elif flag.upper() == 'N':
    print("구매를 종료합니다.")
    break
  else:
    print("입력이 잘못되었습니다. 다시 입력해주세요.")