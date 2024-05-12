import config
from .naver_utils import *
from .kurly_utils import *
from .gmarket_utils import *
from .multi_threading import *
from session import *


#구매 진행 함수
def purchase_process(final_link):
    if "naver" in final_link:
        login_id=config.naver_id
        login_pw=config.naver_pw
        NaverSession(login_id, login_pw, final_link)
    elif "kurly" in final_link:
        login_id=config.kurly_id
        login_pw=config.kurly_pw
        KurlySession(login_id, login_pw, final_link)
    elif "coupang" in final_link:
        login_id=config.coupang_id
        login_pw=config.ciupang_pw
        CoupangSession(login_id, login_pw, final_link)
    elif "gmarket" in final_link:
        login_id=config.gmarket_id
        login_pw=config.gmarket_pw
        GmarketSession(login_id, login_pw, final_link)
    else:
        print("지원하지 않는 사이트입니다.")
    