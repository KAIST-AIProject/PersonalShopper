import os


def download_image(image_url, image_path):
# 다운받을 이미지 url
    url = image_url

    # 이미지 url에서 '(', ')' 제거
    url = url.replace('(', '').replace(')', '')
    
    # time check
    # curl 요청
    try: 
        os.system("curl --silent " + url + " > " + image_path)
        return True
    except:    
        return False






def image_for_gpt(img_num, img_url, path):
    img_count=1
    img_list = []
    while img_count<=img_num:
        if img_count>len(img_url):
            break
        save_path = os.path.join(path, f"{img_count}.jpg")
        result = download_image(img_url[img_count-1], save_path)
        if result==True:
            memory = os.path.getsize(save_path)
            if memory <5:
                continue
            if memory<pow(2, 20)*10:
                img_count+=1
                img_list.append(save_path)

    return img_list

if __name__ == '__main__':
    image_url = ['http://allienco.img9.kr/yumbox/yumbox_large.jpg',
                 'http://allienco.img9.kr/yumbox/yumbox_large.jpg',
                 'http://allienco.img9.kr/yumbox/yumbox_large.jpg',
                 'http://allienco.img9.kr/yumbox/yumbox_large.jpg',
                 'http://allienco.img9.kr/yumbox/yumbox_large.jpg',
                 'http://allienco.img9.kr/yumbox/yumbox_large.jpg'
    ] 
    image_path = "image"
    # download_image(image_url, image_path)
    print(image_for_gpt(10, image_url, image_path))