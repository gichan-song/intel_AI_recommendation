import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time
import datetime

options = ChromeOptions()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
options.add_argument('user-agent=' + user_agent)
options.add_argument("lang=ko_KR")
# options.add_argument('headless')
# options.add_argument('window-size=1920X1080')

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
review_driver = webdriver.Chrome(service=service, options=options)
re_compile = re.compile('[^가-힣]')

for i in range(1, 51):
    print('page ', i)
    try:
        #
        #
        #
        # 카테고리만 변경하시면 됩니다 현재 테마소설 진행중
        driver.get(f'https://www.yes24.com/24/Category/Display/001001046012?PageNumber={i}')
        titles = driver.find_elements(By.CLASS_NAME, 'goods_name')
        urls = []
        for title in titles:
            urls.append(title.find_element(By.TAG_NAME, 'a').get_attribute('href'))
        print(urls)

        for url in urls:
            try:
                driver.get(url)
                time.sleep(0.3)
                title = driver.find_element(By.XPATH, '//*[@id="yDetailTopWrap"]/div[2]/div[1]/div/h2').text
                sub_category = driver.find_element(By.XPATH, '//*[@id="yLocation"]/div/div[4]/a').text
                author = driver.find_element(By.CSS_SELECTOR, '.gd_auth a').text
                image_path = driver.find_element(By.CLASS_NAME, 'gImg').get_attribute('src')
                review = ''
                print(title)
                print(image_path)
            except:
                print(sys.exc_info()[0])
            try:
                driver.find_element(By.XPATH, '//*[@id="yDetailTabNavWrap"]/div/div[2]/ul/li[2]/a').click()
                time.sleep(0.3)
                driver.find_element(By.XPATH, '//*[@id="total"]/a').click()
                time.sleep(0.3)
                reviews = driver.find_elements(By.XPATH, '//*[@id="infoset_reviewContentList"]/div[7]/div[1]/div/a')[-1]\
                    .get_attribute('href')
                max_page = reviews.split('PageNumber=')[1].split('&')[0]
                print(max_page)
                time.sleep(0.3)
                review_driver.get(reviews)
                review_pages = review_driver.find_elements(By.XPATH, '//*[@id="infoset_reviewContentList"]/div[1]/div[1]/div/a')
                review_pages[0].click()
                time.sleep(0.3)
                review_pages = review_driver.find_elements(By.XPATH, '//*[@id="infoset_reviewContentList"]/div[1]/div[1]/div/a')
                for ten_pages in range(int(max_page) // 10):
                    for i in range(3, 13):
                        reviews = review_driver.find_elements(By.CSS_SELECTOR, '.reviewInfoBot.origin .review_cont')
                        for review_cont in reviews:
                            review = review + ' ' + re_compile.sub(' ',review_cont.text)
                        review_driver.find_element(By.XPATH, f'//*[@id="infoset_reviewContentList"]/div[1]/div[1]/div/a[{i}]').click()
                        time.sleep(0.3)
                reviews = review_driver.find_elements(By.CSS_SELECTOR, '.reviewInfoBot.origin .review_cont')
                for review_cont in reviews:
                    review = review + ' ' + re_compile.sub(' ',review_cont.text)
                for i in range(3, int(max_page) % 10 + 2):
                    review_driver.find_element(By.XPATH,
                                               f'//*[@id="infoset_reviewContentList"]/div[1]/div[1]/div/a[{i}]').click()
                    reviews = review_driver.find_elements(By.CSS_SELECTOR, '.reviewInfoBot.origin .review_cont')
                    for review_cont in reviews:
                        review = review + ' ' + re_compile.sub(' ',review_cont.text)
                    time.sleep(0.3)

            except NoSuchElementException:
                review = ''
            except:
                print(sys.exc_info()[0])
            book = pd.DataFrame([{'title': title, 'sub_category': sub_category, 'author': author, 'image_path': image_path,
                                   'review': review}])
            book.to_csv(f'./books/{title}.csv', index=False)
            # book = pd.DataFrame()
    except:
        print(sys.exc_info()[0])