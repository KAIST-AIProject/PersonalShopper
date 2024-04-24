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
    print(f"10개를 한 번에 본 결과 = {int(result)}")

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
    print(f"각각 한개씩 점수내서 평균 : {sum(review_score_list)/len(review_list)}")
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