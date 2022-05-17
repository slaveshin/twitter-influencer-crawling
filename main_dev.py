#selenium, datetime, time, BeautifulSoup
from webbrowser import get
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver import ActionChains
import collections
import time

# 스크롤링 시작할 날짜
StartDate = time.strptime('2021년 1월 1일', '%Y년 %m월 %d일')

driver = webdriver.Chrome('./driver/chromedriver')

driver.implicitly_wait(3)

URL = "https://twitter.com/BTS_twt"
result = []

driver.get(URL)

# 추출 함수


def get_page():
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    block = soup.find_all('article')

    for i in range(len(block)):
        date = block[i].find('time').text
        reply = block[i].find('div', {'data-testid': 'reply'}).text
        retweet = block[i].select_one('div[aria-label$=리트윗]').text
        like = block[i].select_one('div[aria-label$=들어요]').text
        result.append({'date': date, 'reply': reply,
                      'retweet': retweet, 'like': like})


# 페이지 스크롤 함수
def scroll_page():
    while True:
        time.sleep(3)
        get_page()

        # 마지막 Element로 이동
        action = ActionChains(driver)
        blockList = driver.find_elements_by_tag_name('article')
        action.move_to_element(blockList[-1]).perform()

        # 시작 날짜보다 더가면 break
        date = time.strptime(result[-1].get('date'), '%Y년 %m월 %d일')
        if (date < StartDate):
            break


scroll_page()

# 중복제거
result = list(map(dict, collections.OrderedDict.fromkeys(
    tuple(sorted(d.items())) for d in result)))

# 지정한 날짜보다 지난 날짜 모두 제거
while True:
    if (time.strptime(result[-1].get('date'), '%Y년 %m월 %d일')) < StartDate:
        del result[-1]
    else:
        break

for i in result:
    print(i)
