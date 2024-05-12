import os


def download_image(image_url, image_path):
# 다운받을 이미지 url
    url = image_url

    # time check
    # curl 요청
    try: 
        os.system("curl " + url + " > " + image_path)
        return True
    except:    
        return False

if __name__ == '__main__':
    image_url = 'http://allienco.img9.kr/yumbox/yumbox_large.jpg'
    image_path = './image_data/test.jpg'
    download_image(image_url, image_path)




def image_for_gpt(img_num, img_url, path):
    img_count=1
    img_list = []
    while img_count<=img_num:
        save_path = os.path.join(path, f"{img_count}.jpg")
        result = download_image(img_url[img_count-1], save_path)
        if result==True:
            memory = os.path.getsize(save_path)
            if memory<2**7:
                img_count+=1
                img_list.append(save_path)

    return img_list
