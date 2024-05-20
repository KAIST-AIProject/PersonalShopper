import config
from openai import OpenAI
from tqdm import tqdm
import base64
import requests

client = OpenAI(api_key=config.api_key)
def rating_keyword_sorting(review_list, rating_keyword_lst) :
    keyword = ['price', 'review positivity' ] 
    keyword.append(rating_keyword_lst)
    print(f"input product : {review_list['Product_name']}")

    base_prompt = " Look at the product_information and give a score between 0 and 100 for each of the 5 rating_keywords. In the return format, five scores are splited by @.  For example, if each score is 100,90,80,70,60, please return '100@90@80@70@60'. Please don't print anything except the score and @.  " 
    prompt_text = base_prompt + f"rating_keywords = {' '.join(rating_keyword_lst)}, product_reviews = {review_list}"
    response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content":prompt_text},    
    ],
    temperature =0.5,
    max_tokens=10
    )
    result = response.choices[0].message.content
    try : 
        scores = result.split("@")
        scores = [int(s) for s in scores]
        print(f"rating_keywords = {' '.join(rating_keyword_lst)}, score = {scores}")
    except :
        print(f"rating error : {result}")
    

    return scores


def review_rating_all(review_list,rating_keyword_lst ) : #review의 positive-negative 정도를 0~100 사이의 값을 가지는 점수로 변환해서 평균 내는 함수
    base_prompt_text = "Score the positive level of the review by an integer from 0 to 100. Don't ever print anything other than the score"
    
    
    prompt_text = base_prompt_text + f"\nReview : {review_list}"
    response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content":prompt_text},    
    ],
    temperature =0,
    max_tokens=10
    )

    result = response.choices[0].message.content
    print(f"10개의 리뷰를 한 번에 평가한 점수 = {int(result)}")

    return int(result)


def review_rating_one(review_list, rating_keyword_lst) : #review의 positive-negative 정도를 0~100 사이의 값을 가지는 점수로 변환해서 평균 내는 함수
    base_prompt_text = "Score the positive level of the review by an integer from 0 to 100. Don't ever print anything other than the score"

    review_score_list = []
    for i in range(len(review_list)) :
        prompt_text = base_prompt_text + f"\nReview : {review_list[i]}"
        response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content":prompt_text},    
        ],
        temperature =0,
        max_tokens=10
        )

        result = response.choices[0].message.content
        review_score_list.append(int(result))
    print(f"리뷰를 한 개씩 평가해서 평균낸 점수 : {sum(review_score_list)/len(review_list)}")
    return int(result)/len(review_list)


#TODO : price 점수 함수
def price_rating(price_details) : #할인율, 할인 전 가격, 할인 후 가격 등 가격 관련 정보를 받아 rating 하는 함수
    price_score = []

    return price_score

#TODO : product name을 보고 brand 명성 점수를 내는 함수 (GPT 이용)

############################Keyword Agent############################
def KeywordAgentVoting(n_select, client, keyword):
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
    return n_sh_lst, n_dc_lst

############################Select Agent############################
def SelectAgent(prompt) :
    prompt_text = prompt
    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content":prompt_text},
    
    ],
    temperature = 0,
    max_tokens=50
    )
    result = response.choices[0].message.content
    return result

def SelectNumbers(data_details, decision_keyword) :
    print(f"==============================Select Agent 실행==============================")
    
    select_list = []
    N = 5  #한 번에 select agent가 고려할 상품의 개수 
    L = len(data_details)
    _prompt_text = '''
    The data_details contain the number of each product and the detailed information of the product. The user request key word is a condition that the product must be satisfied.
    Among the products below, please return the product numbers that meet all the conditions of the user request keyword according to the format.If there are multiple user requests keyword, all conditions must be met. If the user request keyword is None, return all products numbers.
    if there are multiple product numbers to return, then return the numbers with a character '@' between them. 
    For example, if product 3 and product 5 satisfy the conditions, return '3@5'
    If none of the products meet the conditions, please return empty string and nothing else. You should not print out the product numbers that are not in the product_info.
    please dont say anything other than specific format. 
    ''' 
    
    _prompt_text = _prompt_text + f"user_request  : {','.join(decision_keyword)}\n "
    
    for s in range(L//N) :   #한 번에 N개씩 select agent에 넣어서 선택 
        data_details_N =  '\n'.join(list(str(d) for d in data_details[s*N:2*s*N]))
        prompt_text = _prompt_text + "/n data_details : " + data_details_N
        answer = SelectAgent(prompt_text)
        # print(f"##########{s}번째 select_agent prompt : {prompt_text}")
        print(f"select_agent answer {s+1} : {answer}")
        try : 
            select_list.extend(list(map(int,answer.split('@'))))
        except :
            print(f"run select agent one more time")
            prompt_text += "You should never print anything but numerers.For example, if products 1 and 4 are selected among products 1 to 10, please return 1@4."
            answer = SelectAgent(prompt_text)
            select_list.extend(list(map(int,answer.split('@'))))
    if L%N != 0 : #N개씩 처리한 후 나머지 처리
        data_details_N = '\n'.join(list(str(i) for i in data_details[(L//N)*N:]))
        prompt_text = _prompt_text + "/n data_details :"+ data_details_N
        answer = SelectAgent(prompt_text)
        # print(f"##########나머지 처리 select_agent prompt : {prompt_text}")
        print(f"나머지 select_agent answer: {answer}")
        try : 
                select_list.extend(list(map(int,answer.split('@'))))
        except :
            print(f"run select agent one more time")
            prompt_text += "You should never print anything but numerers.For example, if products 1 and 4 are selected among products 1 to 10, please return 1@4."
            answer = SelectAgent(prompt_text)
            select_list.extend(list(map(int,answer.split('@'))))
    print(f"최종 select_agent result : {select_list}")
    return select_list

def NewSelectNumbers(data_details, decision_keyword) :
    print(f"==============================Select Agent 실행==============================")
    L = len(data_details) #product 개수
    _prompt_text = '''
    The data_details contain the number of each product and the detailed information of the product. The user request key word is a condition that the product must be satisfied. If the product satisfies the condition, return 'True' and if not, return 'False'. Please do not say any thing other than 'True' or 'False'.
    '''
    selected = []
    _prompt_text = _prompt_text + f"user_request  : {','.join(decision_keyword)}\n "
    for s in range(L) :
        prompt_text = _prompt_text + f"data_details : {data_details[s]}" 
        count=0
        while(count<2):
            answer = SelectAgent(prompt_text)
            if answer == 'True' or answer == "true" : #answer가 'True' 라면
                selected.append(s+1)
                count=2
                prompt_text += "Response must be either 'True' or 'False.'"
            elif answer == 'False' or answer == "false" : #answer가 'False' 라면 
                count=2
                prompt_text += "Response must be either 'True' or 'False.'"
            count+=1       

    
    print(f"최종 select_agent result : {selected}")
    return selected






############################Compare Agent############################
def CompareAgent(data_reviews,select_numbers) :
    final_number = 0
    prompt_text = "Among the products below, please recommend one of the best products that are cheap, high-quality, and have good reviews. and Print out the selected product number and the reason for selecting the product according to the format  If there is only 1 product, choose that one product. Don't print out anything other than the number and reason. Please return the string that connects the number and reason with @. For example, if product 3 is selected, print 3@reason."
    
    for idx, data in enumerate(data_reviews) :
        if (idx + 1) in select_numbers : 
            prompt_text += str(data)

    response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content":prompt_text},
        
    ],
    temperature =0,
    max_tokens=50
    )

    result = response.choices[0].message.content
    final_number, reason = result.split('@')

    return final_number, reason

############################Rating Agent############################
def rating(review_list, rating_keyword_lst) :
    # print(f"input product : {review_list['Product_name']}")
    base_prompt = " Look at the product_information and give a score between 1 and 5 for each of the 4 rating_keywords. (score type : integer)In the return format, four scores are splited by @. The higher score indicates better quality of the product.  For example, if each score is 2,3,1,5 please return '2@3@1@5'. Please don't print anything except the score and @ and please always give all four scores. " 
    prompt_text = base_prompt + f"rating_keywords = {' '.join(rating_keyword_lst)}, product_reviews = {review_list}"
    response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content":prompt_text},    
    ],
    temperature =0.5,
    max_tokens=10
    )
    result = response.choices[0].message.content
    try : 
        scores = result.split("@")
        scores = [int(s) for s in scores]
        
    except :
        print(f"rating error : {result}")
    

    return scores

def feedback_rating(review, key_dict) :
        """
        rating 결과를 받아 feedback을 반환하는 함수
        """
        base_prompt = "Each element of key_dicts represents the evaluation criteria and the score that the product received. Refer to the product review information in product_info, determine whether it is reasonable for the product to receive the corresponding score, indicate the validity of the score with 'True' or 'False', and explain the reason why. Each score is a number from 1 to 5. The higher the number, the more positive the evaluation is. Please do not say anything other than True or False and the reason. Reasons must be written in Korean. Connect the four reasons with the letter @. Example : 'True@reason@False@reason@True@reason@False@reason'."
        prompt_text = base_prompt + f"key_dicts = {key_dict}, product_info = {review}"
        response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a teacher who checks that scores are reasonably scored for each category."},
            {"role": "user", "content":prompt_text},    
        ],
        temperature =1,
        max_tokens=1000
        )
        result = response.choices[0].message.content
        # print(f"feedback_rating_result = {result}")
        return result.split("@")

def re_rating(review, feedback_dict) :
    """
    feedback 결과를 받아서 False인 경우에 대해 다시 rating을 받는 함수
    """

    base_prompt = "product_info contains information including the price and review of the product. feedback_dict is each evaluation criterion, the score of the evaluation criterion, and the result of a True/False test to see if the score is correct, and the reason for the test. The score ranges from 1 to 5, and the higher the score, the better. score type : integer. If the test result is true, return the score as it is, and if it is false, refer to the product info and feedback to score a new score. Please split the new score to '@' according to each inspection standard and return it. example : '4@3@5@5' Please don't print anything other than the set format. please don't say a reason why you determine the score."
    prompt_text = base_prompt + f"product_info = {review}, feedback_dict = {feedback_dict}"
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a teacher who checks that scores are reasonably scored for each category."},
            {"role": "user", "content":prompt_text},    
        ],
        temperature =1,
        max_tokens=1000
        )
    result = response.choices[0].message.content
    # print(f"re_rating_result = {result}")
    return result.split("@")

def scoring_agent(product_info, keyword_lst) :
    """
    product_info와 keyword_lst를 받아서 각 keyword에 대한 점수를 반환하는 함수
    """
    keyword = ["review positivity"]
    keyword.extend(keyword_lst)

    # 개별 product에 대해. 
    
    score = rating(product_info, keyword) #rating score 받아오기
    print(f"## 최초 score = {score}")
    key_dict = {}
    for key, s in zip(keyword, score) :
        key_dict[key] = s
    feedback = feedback_rating(product_info, key_dict) #rating score에 대한 feedback 받아오기
    feedback_dict = {}
    for key, j in zip(keyword, range(len(keyword))) :
        feedback_dict[key] = [score[j], feedback[j*2], feedback[j*2+1]] # key : 판단 기준 keyword, value : [score, True/False, reason(feedback)]
    print(f"## 최초 feedback = {feedback_dict}")
    check = [] #feedback 결과가 모두 True인지 확인
    for key in keyword :
        check.append(feedback_dict[key][1])
    print(f"## check = {check}")
    #모두 True가 될 때까지 feedback - rating loop 
    loop_num = 0 #loop 횟수
    if "False" in check :
        print(f"===========1개 이상의 False가 있기 때문에 feedback loop를 시작합니다.==============")
    while 'False' in check and loop_num < 5:
        false_keyword = []
        false_dict = {}
        #전체 키워드 중에서, False를 받은 키워드에 대해서만 false dict와 false keyword 만들기.
        for j in range(len(keyword)) :
            if check[j] == 'False' : 
                false_keyword.append(keyword[j])
                false_dict[keyword[j]] = feedback_dict[keyword[j]]
        
        loop_num += 1
        
        new_score = re_rating(product_info, false_dict) 
        # length = len(false_keyword)  #false keyword 개수
        
        score_dict  = {} #feedback의 input으로 들어갈 score dict. 각 키워드에 대한 score를 넣어줌.

        for key, s in zip(false_keyword, new_score) :
            score_dict[key] = s
        # print(f"new_score = {score_dict}")
        feedback = feedback_rating(product_info, score_dict)         
        #feedback_dict 업데이트
        for j, key in zip(range(len(false_keyword)), false_keyword) :
            feedback_dict[key] = [score_dict[key], feedback[j*2], feedback[j*2+1]]
        #check 업데이트
        for j in range(len(keyword)) :
            check[j] = feedback_dict[keyword[j]][1]
        print(f"## {loop_num} 번째 loop를 통해 변경된 score= {score_dict}, feedback = {feedback_dict}")
    #모두 True가 되거나, loop가 5번 이상 돌았을 경우
    score = []
   
    for j in range(len(keyword)) :
        score.append(int(feedback_dict[keyword[j]][0])) #i 번째 product의 최종 score를 float list로 반환. 
    if loop_num != 0 : #loop를 돌았을 경우
        print()
        print("==========================================================================")
        print(f"## 총 {loop_num}번의 feedback loop 를 돌고 난 후 최종 score = {score}, 최종 feedback = {feedback_dict}")
    else :
        print(f"## 처음 부터 모두 True를 받았기 때문에, score는 변하지 않고 {score}로 최종 결정되었음.")
    return  score, feedback_dict


########################### Vision GPT ###########################
def vision_gpt(result_image_url) :
    """
    image url을 받아서 vision gpt를 이용하여 상품의 상세 정보를 추출하는 함수
    """
    _messages=[
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": " I will give you several images with detailed information of a product, but ignore the photos without text information. Please organize meaningful information that users can refer to for purchase among photos with text information. It doesn't matter if you tell me in words without telling me in perfect sentences. ex) Microwaveable, made of premium silicone, hard exterior, convenient cleaning, antibiotic-free use, etc.  Don't say anything other than information",
            },
        ],
        }
    ]
    for i in range(len(result_image_url[:3])) :    
        _messages[0]['content'].append({"type" : "image_url", "image_url" : {"url" : result_image_url[i]}})
    response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages= _messages,
    max_tokens=200,
    )
    result = response.choices[0]
    # print(result)
    return result

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def local_vision_gpt(image_path) :
    """
    local에 저장된 image path를 받아서 vision gpt를 이용하여 상품의 상세 정보를 추출하는 함수
    """
    # Getting the base64 string
    base64_image = list(encode_image(path) for path in image_path)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config.api_key}"
    }
    messages = [
        {
            "role": "user",
            "content": [
            {
                "type": "text",
                "text":  " I will give you several images with detailed information of a product, but ignore the photos without text information. Please organize meaningful information that users can refer to for purchase among photos with text information. It doesn't matter if you tell me in words without telling me in perfect sentences. ex) Microwaveable, made of premium silicone, hard exterior, convenient cleaning, antibiotic-free use, etc.  Don't say anything other than information"
            }
            ]
        }
        
    ]

    #image 추가
    for i in range(len(base64_image)) :
        messages[0]["content"].append(
            {
                "type": "image_url",
                "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image[i]}"
                }
            }
        )



    payload = {
        "model": "gpt-4-turbo",
        "messages": messages,
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    # Extracting the content from the response
    content = response.json().get('choices')[0]['message']['content']
    return content


def rating_keyword_agent(input_keyword, decision_keyword):
    feature = ''
    for k in decision_keyword:
        feature+=k+', '
    
    prompt_text = f'''
    온라인 쇼핑몰에서 {input_keyword}을 구매하려고 하는데 구매 시 중요하게 고려해야 할 요소 3가지를 알려주세요. 이때 {feature} 등을 구매에 고려해야 합니다. 혹시 가격이나 디자인 요소가 있다면 그것 외에 다른 것을 선택해주세요. 예시로 도시락통을 구매해야 한다고 하면 '안정성,재질,용량'만을 반환해주세요. 다른 말은 하지 말아주세요 제발.
    '''
    response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content":prompt_text},    
    ],
    temperature =0,
    max_tokens=50
    )

    result = response.choices[0].message.content
    return result.split(',')

    
