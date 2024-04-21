import pickle
import os
from tqdm import tqdm
from collections import Counter
from scraping import NaverFinalUrl, Naver_selenium_scraper
from openai import OpenAI


#url scraping
keyword = input("Search KeyWord 입력:") #질기지 않은 1등급 무항생제 스테이크용 한우 안심을 사고 싶어.
n_top = int(input("검색 상위 N값 입력:"))


#keyword_agent
input_keyword = [] #scraper 가 사용할 키워드
decision_keyword = [] #decision agent가 사용할 키워드

#TODO : Option 키워드 분리하는 작업 
client = OpenAI(api_key='')

#voting 구현
n_select = 1
n_sh_lst = []
n_dc_lst = []
print('Keyword 분류 작업 실행')
for i in tqdm(range(n_select), ascii=True):
  completion = client.chat.completions.create(
      model="ft:gpt-3.5-turbo-0125:personal-shopper-gpt::98le9oZL",#네이버 잘 안돼서 컬리 모델로 바꿈.
      messages=[
        {"role": "system", "content": "You are an agent that classifies input into words suitable for shopping searches "},
        {"role": "user", "content": keyword}
      ]
    )
  ret = completion.choices[0].message.content.split('\n')
  sh_keyword = ret[0].split(':')[1].split(",")
  dc_keyword = ret[1].split(':')[1].split(",")
  for sk in sh_keyword:
    n_sh_lst.append(sk)
  for dk in dc_keyword: 
    n_dc_lst.append(dk)


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

#분리된 키워드로 scraping 실행하기
print('scraping 작업 실행')
final_link_lst = NaverFinalUrl(keyword,n_top)

url_path = os.path.join("cache", "finalLink.pickle")

with open(url_path, "wb") as fw_url:
    pickle.dump(final_link_lst, fw_url)
print("scraping 완료!!")



#product detail_scraping
data_details = []
for idx,url in enumerate(final_link_lst):
    os.makedirs('./database', exist_ok=True)
    scrapped_data_path = os.path.join("database", "Naver_item_"+str(idx+1)+".bin")
    # data_details.append(f"product number : {idx+1} ")
    result = Naver_selenium_scraper(url, scrapped_data_path)
    result['product_number'] = idx+1 
    data_details.append(result)

#decision_agent : use gpt api

#Step 1. select gpt 
input_strings = '\n'.join(list(str(i) for i in data_details))
prompt_text = '''
Among the products below, please return the product numbers that meet all the conditions of the user request according to the format.If there are multiple user requests, all conditions must be met.
For example, if product 3 and product 5 satisfy the conditions, print 3 5
If none of the products meet the conditions, please return empty string and nothing else.
'''
prompt_text = prompt_text + f"user_request : {','.join(decision_keyword)}\n "
prompt_text +=  input_strings
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

for idx, data in enumerate(data_details) :
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


save_final_path = os.path.join("cache", "result_url.txt")
for idx, url in enumerate(final_link_lst) :
    if (idx + 1) == int(result) : 
        with open(save_final_path, "w") as file :
            file.write(url)


