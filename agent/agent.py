import config
from openai import OpenAI
from tqdm import tqdm


client = OpenAI(api_key=config.api_key)

def review_rating_all(review_list) : #review의 positive-negative 정도를 0~100 사이의 값을 가지는 점수로 변환해서 평균 내는 함수
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


def review_rating_one(review_list) : #review의 positive-negative 정도를 0~100 사이의 값을 가지는 점수로 변환해서 평균 내는 함수
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
def brand_rating(product_name) :
    base_prompt_text = "Look at the product name and return the score from 0 to 100 to see how good the brand of the product is. (you can evaluate the brand based on its popularity, reputation, reliability, etc)  Don't ever print anything other than the score"
    
    
    prompt_text = base_prompt_text + f"\nproduct name : {product_name}"
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
    print(f"brand 명성 점수 = {int(result)}")

    return int(result)

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
    prompt_text = '''
    Among the products below, please return the product numbers that meet all the conditions of the user request according to the format.If there are multiple user requests, all conditions must be met. If the user request is None, return all products.
    review_positivity_score : This score shows the positivity of the review content from 0 to 100 by looking at 10 reviews
    brand_score : This score is a score that shows from 0 to 100 how good the brand of the product is. (reputability, popularity, reliability, etc.)
    For example, if product 3 and product 5 satisfy the conditions, print 3 5
    If none of the products meet the conditions, please return empty string and nothing else.
    ''' 
    
    prompt_text = prompt_text + f"user_request : {','.join(decision_keyword)}\n "
    prompt_text +=  '\n'.join(list(str(i) for i in data_details))

    answer = SelectAgent(prompt_text)
    print(f"select_agent answer : {answer}")
    try : 
        select_list=list(map(int,answer.split(' ')))
    except :
        print(f"run select agent one more time")
        prompt_text += "You should never print anything but numerers.For example, if products 1 and 4 are selected among products 1 to 10, please return 14."
        answer = SelectAgent(prompt_text)
        select_list=list(map(int,answer.split(' ')))
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