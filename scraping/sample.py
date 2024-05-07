
def sampling(path):

    f = open(path, "r", encoding='UTF8')

    contents = f.read()
    info = contents.split('#')
    # print(info)
    item_info=dict()
    item_info['상품명']=info[0]
    item_info['현재 가격']=info[1]
    item_info['할인 전 가격']=info[2]
    quality_info = dict()
    quality_info['총 평점']=info[3]
    quality_info['리뷰 수']=info[4]
    quality_info['리뷰']=info[5].split('@')

    # quality_info['리뷰'].append(info[5].split('@'))
    return item_info, quality_info  
    

if __name__ == '__main__':
    path = "sample_txt/item1.txt"
    item_info, quality_info=sampling(path)
    print(item_info)
    print(quality_info)