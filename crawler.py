#id를 입력 받으면 입력된 id의 유튜버 정보를 가져올 수 있어야 함
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver import Chrome
import re
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from elasticsearch import Elasticsearch
from datetime import datetime
import daemon

#elaseicsearch 연결
es = Elasticsearch(hosts="localhost", port=9200)
channel_id = input("채널 ID 입력\n")

#채널의 기본적인 정보를 BeautifulSoup을 이용해 가져오고 getViews()를 실행함
def getChannelData(chanel_id):
    req = requests.get("https://www.youtube.com/channel/" + chanel_id)
    print(req)
    html = req.text
    soup = BeautifulSoup(html, "html.parser")
    # 구독자
    subscriber = soup.select(".subscribed")[0].text if soup.select(".subscribed") != [] else -1
    # 이름
    name = soup.select("meta[itemprop='name']")[0].get('content')

    #전체 데이터
    data = {
        "id": chanel_id, #채널 id
        "name": name, #이름
        "subscriber": subscriber, #구독자
        "date": str(datetime.now())[:-7], #수집 일시 (datetime)
        "videos": getVideos(chanel_id) #getView 함수 실행
    }
    return data

#selenium chrome 드라이버를 사용하여 비디오 전체 (스크롤 20번 분량)만큼을 가져와 조회수를 기록함
def getVideos(channel_id):
    #chromeDriver 옵션
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("disable-gpu")
    options.add_argument('window-size=1920x1080')
    delay = 3
    ##selenium 기본 세팅
    browser = Chrome("/Users/joyumin/MyProject/youtubeTrand/chromedriver", chrome_options=options)
    browser.implicitly_wait(delay)
    start_url = "https://www.youtube.com/channel/" + channel_id + "/videos"
    browser.get(start_url)
    browser.maximize_window()
    body = browser.find_element_by_tag_name('body')

    #비디오 목록 스크롤
    lastScrollY = -1 #마지막 스크롤 위치 저장
    while True:
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(2)
        scrollY = browser.execute_script('return window.scrollY') #현재 화면 최상단 위치값 가져옴
        if lastScrollY == scrollY: #이전 위치값과 같다면 == 더이상 스크롤이 없다면
            break
        lastScrollY = scrollY
    print("크롤링 완료")
    html0 = browser.page_source
    html = BeautifulSoup(html0, 'html.parser') #크롤링된 값을 bs4로 변환

    videos = []
    for x in html.select("ytd-grid-video-renderer"):
        #조회수 파싱
        a = x.select("a[aria-label]")[0].get("aria-label")
        view = int(a[a.index("조회수") + 4:-1].replace(",", ""))
        #url 파싱
        url = x.select("a")[0].get("href")
        videos.append({"url" : url, "view" : view})
    return videos

#uploadData 함수를 실행하면 
def uploadData(channel_id):
    try:
        data = getChannelData(channel_id)
    except:
        print("수집 오류")
        return
    # print(data)
    es.index(index="youtuber", body=data)
    print("입력 완료" + str(datetime.now()))
    
uploadData(channel_id)