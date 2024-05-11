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


