import scraping
import pickle
import os
from scraping import NaverFinalUrl
from item_scrapper import Naver_selenium_scraper
from openai import OpenAI


#url scraping
keyword = input("Search KeyWord 입력:")
n_top = int(input("검색 상위 N값 입력:"))

#keyword_agent
input_keyword = [] #scraper 가 사용할 키워드
decision_keyword = ["어린이 사용가능"] #decision agent가 사용할 키워드
#TODO : Option 키워드 분리하는 작업 

final_link_lst = NaverFinalUrl(keyword,n_top)

url_path = os.path.join("cache", "finalLink.pickle")

with open(url_path, "wb") as fw_url:
    pickle.dump(final_link_lst, fw_url)
print("완료!!")



#product detail_scraping
data_details = []
data_reviews = []
for idx,url in enumerate(final_link_lst):
    scrapped_data_path = os.path.join("database", "Naver_item_"+str(idx+1)+".bin")
    review_data_path = os.path.join("database", "Naver_item_review_"+str(idx+1)+".bin")
    # data_details.append(f"product number : {idx+1} ")
    result_detail, result_review = Naver_selenium_scraper(url, scrapped_data_path,review_data_path ) #dictionary 반환
    result_detail['product_number'] = idx+1 #product number 라는 key 값 추가
    result_review['product_number'] = idx+1
    data_details.append(result_detail) 
    data_reviews.append(result_review)

#decision_agent : use gpt api
client = OpenAI(api_key='')

#Step 1. select Agent 
prompt_text = '''
Among the products below, please return the product numbers that meet all the conditions of the user request according to the format.If there are multiple user requests, all conditions must be met.
For example, if product 3 and product 5 satisfy the conditions, print 3 5
If none of the products meet the conditions, please return empty string and nothing else.
'''
#TODO : 현재 상태 : 만약 아무 상품도 조건을 만족하지 않는다면 empty string return됨. -> 이때 어떤 방식을 취할지 결정하고, 코드 만들기 (사용자에게 알리거나, 필터를 줄여서 다시 필터링 시도하거나....)
prompt_text = prompt_text + f"user_request : {','.join(decision_keyword)}\n "
prompt_text +=  '\n'.join(list(str(i) for i in data_details))
# print(f"input_prompt = {prompt_text}")

response = client.chat.completions.create(
  model="gpt-4",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content":prompt_text},
    
  ],
  temperature =0,
  max_tokens=50
)

result = response.choices[0].message.content
#TODO : GPT의 불확실성 때문에 번호가 아닌 다른 말이 포함된다면, 오류 control 하는 코드 (지피티한테 다시 번호만 주라고 시키거나, 시스템 오류로 종료 메시지 넣기)



#Step 2. compare gpt : 위의 select agent에서 선택된 number의 product들 중 가장 "좋은" 상품을 compare 하여 최종적으로 단 하나의 product의 url을 반환한다. 
select_numbers=list(map(int,result.split(' ')))
print(f"select_numbers = {select_numbers}")

prompt_text = "Compare the products below and choose one of the cheapest products and return the url.  If there is only 1 product, choose that one product. Don't print out anything other than the number. For example, if product 3 is selected, print 3"

for idx, data in enumerate(data_reviews) :
    if (idx + 1) in select_numbers : 
        prompt_text += str(data)
        
response = client.chat.completions.create(
  model="gpt-4",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content":prompt_text},
    
  ],
  temperature =0,
  max_tokens=50
)

result = response.choices[0].message.content     
print(result)
#TODO : gpt의 불확실성 때문에 하나의 숫자외에 다른게 output으로 나온다면, 오류 control 하는 코드

save_final_path = os.path.join("cache", "result_url.txt")
for idx, url in enumerate(final_link_lst) :
    if (idx + 1) == int(result) : 
        with open(save_final_path, "w") as file :
            file.write(url)


