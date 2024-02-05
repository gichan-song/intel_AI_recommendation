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

driver.get('https://www.yes24.com/24/Category/Display/001001046011')
titles = driver.find_elements(By.CLASS_NAME, 'goods_name')
urls = []
for title in titles:
    urls.append(title.find_element(By.TAG_NAME, 'a').get_attribute('href'))
print(urls)

df = pd.DataFrame(columns=['title', 'category', 'review', 'author'])
for url in urls:
    driver.get(url)
    title = driver.find_element(By.XPATH, '//*[@id="yDetailTopWrap"]/div[2]/div[1]/div/h2')
    print(title.text)
    # book = pd.DataFrame()