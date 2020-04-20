import re
import pandas as pd
from bs4 import BeautifulSoup
import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
import csv
import select
import locale


# 1. url을 불러오기 위한 사전 작업 실행
delay = 3
browser = Chrome('d:\Downloads\chromedriver_win32\chromedriver.exe') #자신의 경로로 바꿔줘야함
browser.implicitly_wait(delay)

# 2. 유투브 url로 접속 query에 검색하고 싶은 키워드 입력
start_url = 'https://www.youtube.com/results?search_query='

# 3. 작성될 파일 열기
csvfile = open("youtube_crawling_data_ver2.csv", "a", encoding="utf-8", newline="")
csvwriter = csv.writer(csvfile)

# 4. 크롤링 및 데이터 쓰기
def crawling(keyword):
    # 1. 유투브 채널 url 생성
    browser.get(start_url + keyword)
    browser.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[1]/div[2]/ytd-search-sub-menu-renderer/div[1]/div/ytd-toggle-button-renderer/a/paper-button/yt-formatted-string').click()
    browser.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[1]/div[2]/ytd-search-sub-menu-renderer/div[1]/iron-collapse/div/ytd-search-filter-group-renderer[1]/ytd-search-filter-renderer[3]/a/div/yt-formatted-string').click()


    # 2. 해당 키워드의 첫번째 영상부터 n번째 영상까지 크롤링
    for vindex in range(1,100):
        # vindex 번호 영상 클릭 # 불안정함
        browser.find_elements_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer['+str(vindex)+']/div[1]/div/div[1]/div/h3/a')[0].click()
        time.sleep(3)

        # 스크롤 내리는 작업
        body = browser.find_element_by_tag_name('body')  # 스크롤하기 위해 소스 추출

        num_of_pagedowns = 2  # 최신 데이터만 필요하므로 많이 내릴 필요 없음

        # num_of_pagedowns번 밑으로 내리는 것
        while num_of_pagedowns:
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(2)
            num_of_pagedowns -= 1

        # 페이지 소스 받아오기
        page = browser.page_source
        time.sleep(2)
        soup = BeautifulSoup(page,'lxml')

        # 원하는 정보 수집

        # 1. 채널 이름 error 안되네요ㅠ
        # channel = soup.find('a','yt-simple-endpoint style-scope yt-formatted-string').string #a태그에 해당 클래스
        # channel = soup.find('yt-formatted-string',id="text",class_="style-scope ytd-channel-name").string
        # <yt-formatted-string id="text" title="" class="style-scope ytd-channel-name" has-link-only_=""><a class="yt-simple-endpoint style-scope yt-formatted-string" spellcheck="false" href="/channel/UCUeVdhdq6tF4wIojud9PMdw" dir="auto">이욜 eyol</a></yt-formatted-string>

        # 2. 영상 이름
        title = soup.find('yt-formatted-string','style-scope ytd-video-primary-info-renderer').string

        # 3. 조회수
        view = soup.find('span','view-count style-scope yt-view-count-renderer').string

        # 4. 댓글 수
        coment = soup.find('yt-formatted-string','count-text style-scope ytd-comments-header-renderer').string

        # 5. 좋아요 수
        like = soup.find('yt-formatted-string', attrs={"aria-label":True}, id = 'text', class_='style-scope ytd-toggle-button-renderer style-text').string

        # 6. 구독자 수
        subc = soup.find('yt-formatted-string','style-scope ytd-video-owner-renderer').string


        # 8. 현재 시간 날짜
        now =  time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())

        print("finished")

        # 데이터 행 추가
        row_data=[]
        row_data.append(vindex)
        row_data.append(now)
        row_data.append(title)
        row_data.append(view)
        row_data.append(coment)
        row_data.append(like)
        row_data.append(subc)
        csvwriter.writerow(row_data)

        # 크롤링 완료 후 뒤로 가기
        browser.back()
        time.sleep(1)




# 크롤링 원하는 검색어
keyword_list = ['브이로그']

# 5. 일괄 크롤링
for key in keyword_list:
    crawling(key)
    print(key + " finished")

# data 저장
# 6. 파일 닫기
csvfile.close()
#df.to_pickle("youtube_crawling_data_pkl.pkl")

# 잘 끝났다면
print("everything is ok")