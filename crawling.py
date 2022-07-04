from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from pymongo import MongoClient
import requests
import os
import pprint
import urllib.request
# DB접근 관련
client = MongoClient('mongodb+srv://team_project:sparta1234@cluster0.10xkhtt.mongodb.net/?retryWrites=true&w=majority')
db = client.team_project

# 크롤링 위한 chrome 세팅
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-setuid-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome('chromedriver', options=chrome_options)


# 암묵적으로 웹 자원 로드를 위해 3초까지 기다려 준다.
driver.implicitly_wait(3)

# url 에 접근한다.
driver.get('https://www.cgv.co.kr/')

# 동적으로 행동하기 위한 것
action = ActionChains(driver)


# print 이쁘게 만들어서 보기
pp = pprint.PrettyPrinter(indent=4)


# 페이지 이동하는 함수
def move_to_page(num):
    item = driver.find_elements(By.CSS_SELECTOR, "div.swiper-slide-movie")[num]
    action.move_to_element(item).perform()
    item.find_element(By.CSS_SELECTOR, "div.movieChart_btn_wrap > a").send_keys(Keys.ENTER)

# 데이터 크롤링해서 가져오는 함수
def get_data():
    info = driver.find_element(By.CSS_SELECTOR, "div.box-contents")
    title = info.find_element(By.CSS_SELECTOR, "div.title > strong").text
    spec = info.find_element(By.CSS_SELECTOR, "div.spec>dl")
    thumbnail_route = driver.find_element(By.CSS_SELECTOR, "span.thumb-image > img").get_attribute('src')
    description = driver.find_element(By.CSS_SELECTOR, "div.sect-story-movie").text
    booking_rate = driver.find_element(By.CSS_SELECTOR,"div.score>strong").text
    print(booking_rate)
    return title, spec, thumbnail_route, description, booking_rate


# 데이터 가공하는 함수
def processing_data(title, spec, thumbnail,description,booking_rate):
    key = []
    value = []
    key_check = True
    doc = {}
    table = str.maketrans("/: ", "   ")
    specs = spec.text.translate(table).split("\n")
    # 각영화 상세정보 crawling 한 내용 key - value 맞춰서 각각 대입
    for data in specs:
        data = data.strip()
        if key_check is True:
            if "장르" in data:
                try:
                    genre = data.split("   ")
                    key.append(genre[0])
                    value.append(genre[1])
                    key_check = True
                except IndexError:
                    value.append(" ")
                    key_check = True
            else:
                key.append(data)
                key_check = False
        else:
            value.append(data)
            key_check = True
    for j in range(0, len(key)):
        doc[key[j]] = value[j]
    doc['영화제목'] = title
    doc['포스터'] = thumbnail
    doc['영화설명'] = description.replace("\n", "")
    try :
        doc['예매율'] = booking_rate.split(" ")[1]
    except IndexError:
        doc['예매율'] = ""
    pp.pprint(doc)
    return doc


# DB에 데이터 넣기
def save_in_DB(movie_data, status):
#     status = False 면 처음 넣는것
    if status is False:
        db.movieDatas.insert_one(movie_data)
    else:
        rank = movie_data['순위']
        db.movieDatas.replace_one({'순위': str(rank)}, movie_data, upsert=True)


# 현재 DB에 처음 데이터를 넣는 것인지 갈아치우는 것인지 알아야함
def check_DB_status():
    collection_list = db.list_collection_names()
    check_collection = True
    if 'movieDatas' not in collection_list:
        check_collection = False
    return check_collection


def start_crawling():
    # 영화 상세보기 페이지로 이동.
    items = len(list(driver.find_elements(By.CSS_SELECTOR, "div.swiper-slide-movie")))
    status = check_DB_status()
    for i in range(0, items-1):
        # 페이지 이동 함수
        move_to_page(i)
        driver.implicitly_wait(1.5)
        # 데이터 가져오기
        title, spec, thumbnail, description, booking_rate = get_data()
        movie_data = processing_data(title, spec, thumbnail,description,booking_rate)
        movie_data['순위'] = str(i+1)
        # 영화 DB에 저장하기
        save_in_DB(movie_data,status)
        driver.back()
        driver.implicitly_wait(3)
    driver.quit()
    exit()


start_crawling()

