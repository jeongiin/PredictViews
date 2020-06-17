
# 유투브 조회수 예측하기 프로젝트

![https://s3-us-west-2.amazonaws.com/secure.notion-static.com/f7787d3f-6c76-4da3-9cfb-3a4f7142b99c/Untitled.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/f7787d3f-6c76-4da3-9cfb-3a4f7142b99c/Untitled.png)

🗂파일 소개

---

📂 crawler

- filters : 유투브 크롤링 시 조회수, 좋아요수, 댓글수에 해당하는 정보가 문자열로 얻어지는 문제 해결 및 'N만' 으로 표현되는 단어를 N*10000 정수형으로 변환
- keyword_crawler : 유투브에 키워드를 입력하고 범위를 오늘 내 영상으로 설정하여 원하는 정보를 크롤링 함
- youtuber_info_crawler : 특정 유투버의 영상 정보와 계정 정보를 크롤링 하는 시스템이나 본 주제와 맞지 않아 코드만 작성하고 사용하지 않음

📁 data

- data_preprocessing : 결측값, 중복행 제거 등을 위한 데이터 전처일 파일
- *.csv : outlier가 정리된 크롤링으로 수집한 데이터 파일

  → 총 4개의 키워드가 있으며 각 키워드 당 2000행 이상의 데이터를 수집하였으나 전처리 과정에서 반 이상 제거됨

📂 model

- result_model : 데이터 split과 정확도가 포함된 모델 코드
- vlog_multi_variable_regression : 브이로그 데이터만으로 예측 결과 점검 시 사용해본 다항 선형 회귀 코드

📁 service

- predict_view : 실제 유투버인 user가 서비스를 이용하고자 할 시 사용할 수 있는 프로그램 코드
