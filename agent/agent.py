import config
from openai import OpenAI
from tqdm import tqdm


client = OpenAI(api_key=config.api_key)
def rating_keyword_sorting(review_list, rating_keyword_lst) :
    keyword = ['price', 'review positivity' ] 
    keyword.append(rating_keyword_lst)
    print(f"input _ review_list : {review_list}")

    base_prompt = " rating keywords는 5가지의 평가 기준이고, product information은  한 상품의 가격 정보와 10개의 리뷰들이야. 상품 정보와 리뷰를 고려해서 각각의 rating keyword에 대한 점수를 0부터 100까지의 값을 @로 구분해서 return 해줘. 예를 들어, 다섯개 항목의 점수가 100,90,85,90,77라면, '100@90@85@90@77' 를 return 해줘. 이런 return 형식을 꼭 지켜줘.  "
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
    scores = result.split("@")
    scores = [int(s) for s in scores]
    print(f"rating_keywords = {' '.join(rating_keyword_lst)}, score = {scores}")

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
    model="gpt-4-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content":prompt_text},
    
    ],
    temperature = 0,
    max_tokens=50
    )
    result = response.choices[0].message.content
    return result

def Select_numbers(data_details, decision_keyword) :
    select_list = []
    N = 5  #한 번에 select agent가 고려할 상품의 개수 
    L = len(data_details)
    _prompt_text = '''
    Among the products below, please return the product numbers that meet all the conditions of the user request according to the format.If there are multiple user requests, all conditions must be met. If the user request is None, return all products.
    For example, if product 3 and product 5 satisfy the conditions, print 3 5
    If none of the products meet the conditions, please return empty string and nothing else.
    ''' 
    
    _prompt_text = _prompt_text + f"user_request : {','.join(decision_keyword)}\n "

    for i in range(L//N) :    
        data_details_N =  '\n'.join(list(str(i) for i in data_details[i*N:2*i*N]))
        prompt_text = _prompt_text + data_details_N
        answer = SelectAgent(prompt_text)
        try : 
            select_list.extend(list(map(int,answer.split(' '))))
        except :
            print(f"run select agent one more time")
            prompt_text += "You should never print anything but numerers.For example, if products 1 and 4 are selected among products 1 to 10, please return 14."
            answer = SelectAgent(prompt_text)
            select_list.extend(list(map(int,answer.split(' '))))
    if L%N != 0 :
        data_details_N = '\n'.join(list(str(i) for i in data_details[(L//N)*N:]))
        prompt_text = _prompt_text + data_details_N
        answer = SelectAgent(prompt_text)
        try : 
                select_list.extend(list(map(int,answer.split(' '))))
        except :
            print(f"run select agent one more time")
            prompt_text += "You should never print anything but numerers.For example, if products 1 and 4 are selected among products 1 to 10, please return 14."
            answer = SelectAgent(prompt_text)
            select_list.extend(list(map(int,answer.split(' '))))
    print(f"select_agent answer : {select_list}")
    return select_list

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




########################### Vision GPT ###########################
def vision_gpt(result_image_url) :
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

    
