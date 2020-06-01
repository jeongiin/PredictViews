import numpy as np
import pandas as pd
import sklearn

def acurracy(key):

    # 데이터 선택
    data_name = "model_youtube_crawling_data_"+key+"_outlier.csv"
    data = pd.read_csv(data_name)

    # csv파일 0번째 줄이 View, Comment 등 이라서 스킵하고 불러옴
    # data = pd.read_csv('model_youtube_crawling_data_game_outlier.csv', names=['View', 'Coment', 'Like', 'Subscriber'], skiprows=[0])

    data.View = pd.to_numeric(data.View)
    data.Coment = pd.to_numeric(data.Coment)
    data.Like = pd.to_numeric(data.Like)
    data.Subscriber = pd.to_numeric(data.Subscriber)

    x = np.c_[data['Coment'], data['Like'],data['Subscriber']]
    y = data['View']
    m = len(data) # 정보 개수(행 개수)

    x = (np.array(x)).reshape(m,3)
    y = (np.array(y)).reshape(m,1)

    # train, test 데이터 분류 (8대 2)
    from sklearn.model_selection import train_test_split
    x_train, x_test, y_train, y_test = train_test_split(x, y, train_size= 0.8, test_size= 0.2)

    from sklearn.linear_model import LinearRegression
    # train 데이터 훈련
    mlr = LinearRegression()
    mlr.fit(x_train, y_train)

    # 값 예측(댓글, 좋아요, 구독자 순)
    '''my_youtube = [[20, 10, 100]]
    my_predict = mlr.predict((my_youtube))
    print(my_predict)'''

    print(key + " train 데이터의 r2 스코어: ")
    print(mlr.score(x_train, y_train))
    print(key + " test 데이터의 r2 스코어: ")
    print(mlr.score(x_test, y_test))


# key = input()
# acurracy(key)