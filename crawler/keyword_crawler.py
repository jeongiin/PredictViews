
import pandas as pd
from bs4 import BeautifulSoup
import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from crawler import filters

# 1. url을 불러오기 위한 사전 작업 실행

delay = 3
browser = Chrome('D:\Downloads\chromedriver_win32 (2)\chromedriver.exe') #자신의 경로로 바꿔줘야함
browser.implicitly_wait(delay)


# 2. 유투브 url로 접속 query에 검색하고 싶은 키워드 입력(밑에 리스트에서 입력)
start_url = 'https://www.youtube.com/results?search_query='

# 3. 작성될 파일 열기
# 처음 파일 생성 시
# data = pd.DataFrame(columns=["Now", "Title", "View", "Coment", "Like", "Subscriber"])


# 크롤링 원하는 검색어
key='리뷰'
key_='review'

# key = '브이로그'
# key_ = 'vlog'

data = pd.read_csv('today_youtube_crawling_data_'+key_+'.csv', sep=',')

all_data = []

# 4. 크롤링 및 데이터 쓰기
def crawling(keyword):

    # 1. 유투브 채널 url 생성 + 오늘 내 영상만 보도록 설정
    browser.get(start_url + keyword)
    browser.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[1]/div[2]/ytd-search-sub-menu-renderer/div[1]/div/ytd-toggle-button-renderer/a/paper-button/yt-formatted-string').click()
    browser.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[1]/div[2]/ytd-search-sub-menu-renderer/div[1]/iron-collapse/div/ytd-search-filter-group-renderer[1]/ytd-search-filter-renderer[2]/a/div/yt-formatted-string').click()
    body = browser.find_element_by_tag_name('body')  # 스크롤하기 위해 소스 추출

    #매끄러운 크롤링을 위한 사전 작업
    for vindex in range(35) :
        body.send_keys((Keys.END))
        time.sleep(1)
    body.send_keys(Keys.HOME) #홈 키로 최상단



    # 2. 해당 키워드의 첫번째 영상부터 n-1번째 영상까지 크롤링
    for vindex in range(1,100):

        # vindex 번호의 영상 클릭
        print(vindex)

        # 20개마다 특정 index가 갱신됨
        i=1
        if vindex % 20 == 0 :
            i+=1

        try :
            video_btn = browser.find_elements_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer['+str(i)+']/div[3]/ytd-video-renderer['+str(vindex%20)+']/div[1]/div/div[1]/div/h3/a')
            browser.implicitly_wait(5)                #/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer[1]/div[3]/ytd-video-renderer[20]/div[1]/div/div[1]/div/h3/a
            video_btn[0].click()                      #/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer[2]/div[3]/ytd-video-renderer[2]/div[1]/div/div[1]/div/h3/a
            time.sleep(5) # 제목이 뜨기전에 정보를 받아오려고 하는 경우가 있어 잠재워줌


        except :
            print("loading...")
            continue

        # 댓글수 확인을 위한 스크롤
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(3)


        # 페이지 소스 받아오기
        page = browser.page_source
        soup = BeautifulSoup(page,'lxml')

        # 원하는 정보 수집
        # 1. 영상 이름
        title = soup.find('yt-formatted-string','style-scope ytd-video-primary-info-renderer').string

        # 2. 조회수
        try :
            view = soup.find('span', 'view-count style-scope yt-view-count-renderer').string
            view = filters.stoi(view)

        except :
            view = None

        # 3. 댓글 수
        try:
            coment = soup.find('yt-formatted-string','count-text style-scope ytd-comments-header-renderer').string
            coment = filters.stoi(coment)
        except:
            coment = None

        # 4. 좋아요 수
        try:
            like = soup.find('yt-formatted-string', attrs={"aria-label":True}, id = 'text', class_='style-scope ytd-toggle-button-renderer style-text').string
            like = filters.stoi(like)
        except:
            like = None

        # 5. 구독자 수
        try:
            subc = soup.find('yt-formatted-string','style-scope ytd-video-owner-renderer').string
            subc = filters.stoi(subc)
        except:
            subc = None

        # 6. 현재 시간 날짜
        now = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())

        print("finished")

        # 데이터 행 추가
        row_data=[]
        row_data.append(now)
        row_data.append(title)
        row_data.append(view)
        row_data.append(coment)
        row_data.append(like)
        row_data.append(subc)
        all_data.append(row_data)

        # 크롤링 완료 후 뒤로 가기
        browser.back()
        time.sleep(2)






# 5. 일괄 크롤링
try :
    crawling(key)
except :
    "Error : save temporariry"


data = pd.DataFrame(all_data, columns=("Now", "Title", "View", "Coment", "Like", "Subscriber"))
print(key + " crawling finished")

# csv 파일에 저장
data.to_csv('today_youtube_crawling_data_temp.csv',mode='w',encoding='utf-8-sig')
data.to_csv('today_youtube_crawling_data_'+key_+'.csv', mode='a',encoding='utf-8-sig')
# data.to_csv('today_youtube_crawling_data_review.csv',mode='a',encoding='utf-8-sig') #리뷰
# 6. 브라우저 닫기
browser.close()

# 잘 끝났다면
print("everything is ok")