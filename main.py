import time
from function import *

START_DATE = "2021년 1월 1일"
URL = "https://twitter.com/BTS_twt"
result = []

# get driver and go to ULR
driver = setChromeDriver()
driver.implicitly_wait(10)
driver.get(URL)

# result += get_page(driver.page_source)

for i in range(3):
    time.sleep(3)
    result += get_page(driver.page_source)
    go_to_final_element(driver)

for i in result:
    print(i)
