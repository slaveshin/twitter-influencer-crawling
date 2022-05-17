import time
from function import *

# 사전 설정
START_DATE = "2021년 11월 1일"
URL = "https://twitter.com/BTS_twt"


def main():
    result = []
    start_date = time.strptime(START_DATE, "%Y년 %m월 %d일")

    # get driver and go to ULR
    driver = setChromeDriver()
    driver.implicitly_wait(3)
    driver.get(URL)

    while True:
        time.sleep(3)
        result += get_page(driver.page_source)
        scroll_to_last_element(driver)

        # 설정한 날짜보다 더가면 크롤링 중단
        last_posting_date = time.strptime(
            result[-1].get('date'), '%Y년 %m월 %d일')
        if(last_posting_date < start_date):
            break

    # 중복 제거
    result = deduplication(result)

    # 지정한 날짜 이 외의 날짜 모두 제거
    result = remove_except_selected_date(result, start_date)

    for i in result:
        print(i)


main()
