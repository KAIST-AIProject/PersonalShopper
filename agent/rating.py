from openai import OpenAI
import config

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
