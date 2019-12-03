#id를 입력 받으면 입력된 id의 유튜버 정보를 가져올 수 있어야 함
import requests
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver import Chrome
import re
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from elasticsearch import Elasticsearch

def getChannelData(chanel_id):
    req = requests.get("https://www.youtube.com/channel/" + chanel_id)
    html = req.text
    soup = BeautifulSoup(html, "html.parser")
    # 구독자
    subscriber = soup.select(
        ".yt-subscription-button-subscriber-count-branded-horizontal")[0].text
    # 이름
    name = soup.select("meta[content='괴물쥐 유튜브']")[0].get("content")
    # 채널 썸네일 이미지
    thumbnail = soup.select(".appbar-nav-avatar")[0].get("src")
    videos_html = requests.get(
        "https://www.youtube.com/channel/UCDBAVzfX3yZ1hah0FHnOoaA/videos").text
    videos = BeautifulSoup(videos_html, "html.parser")
    sum = 0
    for x in videos.select(".yt-lockup-content"):
        sum += int(x.select(".yt-lockup-meta-info li")
                   [0].text[4:][:-1].replace(",", ""))
    data = {
        "id": chanel_id,
        "name": name,
        "subscriber": subscriber,
        "date": time.time(),
        "views": getViews()
    }
    return data


def getViews():
    delay = 3
    browser = Chrome("/Users/joyumin/MyProject/youtubeTrand/chromedriver")
    browser.implicitly_wait(delay)
    start_url = 'https://www.youtube.com/channel/UCDBAVzfX3yZ1hah0FHnOoaA/videos'
    browser.get(start_url)
    browser.maximize_window()

    body = browser.find_element_by_tag_name('body')

    num_of_pagedowns = 20

    while num_of_pagedowns:
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(2)
        num_of_pagedowns -= 1

    html0 = browser.page_source
    html = BeautifulSoup(html0, 'html.parser')
    views = 0
    for x in html.select("ytd-grid-video-renderer"):
        a = x.select("a[aria-label]")[0].get("aria-label")
        views += int(a[a.index("조회수") + 4:-1].replace(",", ""))
    return views

def uploadData():
    es = Elasticsearch(hosts="localhost", port=9200)
    data = getChannelData(input())
    es.index(index="youtuber", body=data)

uploadData()