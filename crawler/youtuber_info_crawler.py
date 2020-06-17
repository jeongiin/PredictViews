from bs4 import BeautifulSoup
import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
import csv
from crawler import filters

#import urllib.reequest
#import pandas as pd


# 1. url을 불러오기 위한 사전 작업 실행s
delay=3
browser = Chrome('d:\Downloads\chromedriver_win32\chromedriver.exe')
browser.implicitly_wait(delay)


# 2. 유투브 url로 접속 query에 검색하고 싶은 유투버 이름 입력
start_url  = 'https://www.youtube.com/results?search_query='


# 3. 작성될 파일 열기
csvfile = open("youtube_crawling_data_pretreatment.csv", "a", encoding="utf-8", newline="")


# 4. 크롤링 및 데이터 쓰기
def crawling(keyword) :

    # 1. 유투브 채널 url 생성
    browser.get(start_url + keyword)

    # 2. 이동한 화면에서 유투버 채널 클릭
    browser.find_elements_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-channel-renderer/div/div[2]/a/div[1]/ytd-channel-name/div/div/yt-formatted-string')[0].click()

    # 3. 동영상 카테고리 클릭
    browser.find_element_by_xpath('//*[@class="scrollable style-scope paper-tabs"]/paper-tab[2]').click()

    # 4. 스크롤 내리는 작업
    body = browser.find_element_by_tag_name('body')  # 스크롤하기 위해 소스 추출

    num_of_pagedowns = 3 # 최신 데이터만 필요하므로 많이 내릴 필요 없음

    # num_of_pagedowns번 밑으로 내리는 것
    while num_of_pagedowns:
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(2)
        num_of_pagedowns -= 1

    # 5. 원하는 정보 수집
    page = browser.page_source
    soup = BeautifulSoup(page, 'lxml')

    # 5.1. title 뽑기
    all_title = soup.find_all('a', 'yt-simple-endpoint style-scope ytd-grid-video-renderer')
    title = [soup.find_all('a', 'yt-simple-endpoint style-scope ytd-grid-video-renderer')[n].string for n in range(0, len(all_title))]


    # 5.2. 구독자 수 뽑기
    sub_num = soup.find('yt-formatted-string', 'style-scope ytd-c4-tabbed-header-renderer').string


    # 5.3. 조회수, 올린지 얼마나 되었는지(업로드 시점)
    c = soup.find_all('span', 'style-scope ytd-grid-video-renderer')
    view_num = [soup.find_all('span', 'style-scope ytd-grid-video-renderer')[n].string for n in range(0, len(c))]


    # 5.4. 댓글 수 뽑기
    

    # 5.4. 현재 시간 뽑기
    extract_date = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())


    # 6. 데이터 합치기
    youtube_video_list = []
    x = 0  # 조회수 index
    y = 1  # 업로드 시점의 index

    for i in range(0, len(all_title)):
        if filter.sub(view_num[y]) != -1 :
            rows = []
            rows.append(keyword)
            rows.append(title[i])
            rows.append(filter.stoi(sub_num)) # 구독자
            rows.append(filter.stoi(view_num[x]))
            x += 2  # 조회수만 append
            rows.append(view_num[y])
            y += 2  # 업로드 시점만 append
            rows.append(extract_date)
            youtube_video_list.append(rows)
            # rows.append(chennel)
            # roww.append(video_time[i].strip()) 비디오 재생 시간

        else :
            break

    # 6. 저장
    csvwriter = csv.writer(csvfile)
    for row in youtube_video_list:
        csvwriter.writerow(row)
    csvwriter.writerow("")



# 크롤링 원하는 검색어
# 일상 유투버 조회수
# keyword_list = ['냥숲', '오눅', '슛뚜', '시나기','글룩스필츠','송이송이']
# keyword_list = ['샒의삶', '톰과나', '윤그린', '유네린','김갈릭','소소']
keyword_list = ['희주','유진','연우','오드','혜쁨','달님']

# 5. 일괄 크롤링
for key in keyword_list:
    crawling(key)
    print(key + " finished")

# 6. 파일 닫기
csvfile.close()


# 잘 끝났다면
print("everything is ok")