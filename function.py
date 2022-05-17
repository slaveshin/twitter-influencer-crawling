from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains


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
    print(len(post))

    for i in range(len(post)):
        date = post[i].find('time').text
        contents = post[i].find('div', {'data-testid': 'tweetText'}).text
        reply = post[i].find('div', {'data-testid': 'reply'}).text
        retweet = post[i].select_one('div[aria-label$=리트윗]').text
        like = post[i].select_one('div[aria-label$=들어요]').text
        result.append({'date': date, 'contents': contents, 'reply': reply,
                      'retweet': retweet, 'like': like})
    return result


# 마지막 Element로 이동하는 함수
def go_to_final_element(driver):
    action = ActionChains(driver)
    post_list = driver.find_elements_by_tag_name('article')
    action.move_to_element(post_list[-1]).perform()
