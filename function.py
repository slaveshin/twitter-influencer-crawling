from unittest import result
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains
from datetime import datetime
import collections
import time


# 크롬드라이버 set 함수, 자기 컴퓨터의 chromedriver를 가져와서 쓰게함
def setChromeDriver():
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=chrome_options)
    return driver


# 로딩된 한 페이지 단위로 추출함
def get_page(page_source):
    result = []
    html = page_source
    soup = BeautifulSoup(page_source, "html.parser")
    # 게시물의 한개의 단위를 post로 봄
    post = soup.find_all('article')

    for i in range(len(post)):
        date = format_date(post[i].find('time').text)
        contents = is_content_none(post[i].find(
            'div', {'data-testid': 'tweetText'}))
        reply = post[i].find('div', {'data-testid': 'reply'}).text
        retweet = post[i].select_one('div[aria-label$=리트윗]').text
        like = post[i].select_one('div[aria-label$=들어요]').text
        result.append({'date': date, 'contents': contents, 'reply': reply,
                      'retweet': retweet, 'like': like})
    return result


# 마지막 Element로 이동하는 함수
def scroll_to_last_element(driver):
    action = ActionChains(driver)
    post_list = driver.find_elements_by_tag_name('article')
    action.move_to_element(post_list[-1]).perform()


# 리스트 안에 중복되는 요소들을 제거 해줌
def deduplication(array):
    result = list(map(dict, collections.OrderedDict.fromkeys(
        tuple(sorted(d.items())) for d in array)))

    return result


# 마지막 게시물의 날짜를 추출해주는 함수
def format_date(date):
    if(len(date) < 5):
        return datetime.today().strftime("%Y년 %m월 %d일")
    elif(len(date) < 8):
        return datetime.today().strftime("%Y년 ") + date
    else:
        return date


# 지정한 날짜보다 지난 날짜는 모두 제거하는 함수
def remove_except_selected_date(array, start_date, end_date):

    while True:
        last_date = time.strptime(array[-1].get('date'), '%Y년 %m월 %d일')

        if (last_date < start_date):
            del array[-1]
        else:
            break

    return array


def is_content_none(content):
    if content is None:
        return "None"
    else:
        return content.text
