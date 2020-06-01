import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def model(key):
    data_name = "../data/model_youtube_crawling_data_"+key+"_outlier.csv"
    data = pd.read_csv(data_name)


    data.View = pd.to_numeric(data.View)
    data.Coment = pd.to_numeric(data.Coment)
    data.Like = pd.to_numeric(data.Like)
    data.Subscriber = pd.to_numeric(data.Subscriber)

    # 1. 조회수 데이터 읽기
    X = np.c_[data['Coment'], data['Like'],data['Subscriber']]
    y = data['View']
    m = len(data) # 정보 개수(행 개수)

    # numpy array 형태로 변환, 형태 변환(m) -> (m,1)
    X = (np.array(X)).reshape(m,3)
    y = (np.array(y)).reshape(m,1)
    #print(X.shape,y.shape)

    # # 2. 그래프 그리기
    # plt.plot(X[:0].reshape(-1), y, 'b.') #X[:,1].reshape(-1) : 한 줄로 피기. (47,)->(47)
    # plt.xlabel("# coment") # 댓글 수
    # plt.ylabel("Views") # 조회수
    # plt.show()
    #
    # plt.plot(X[:,1].reshape(-1), y, 'b.')
    # plt.xlabel("# like") # 좋아요 수
    # plt.ylabel(" Views") # 조회수
    # plt.show()
    #
    # plt.plot(X[:,1].reshape(-1), y, 'b.')
    # plt.xlabel("# subscriber") # 구독자 수
    # plt.ylabel("Views") # 조회수
    # plt.show()

    # 3. 특징 정규화
    def featureNormalize(X):  # X(47,2)
        # 1. 각 feature 의 평균, 표준편차 계산
        mu = np.mean(X, axis=0)  # (47,2)->(1,2)
        std = np.std(X, axis=0)  # (47,2)->(1,2)

        # 2. (각 값 - 평균)/ 표준편차
        X_norm = (X - mu) / std

        return X_norm, mu, std

    X, mu, std = featureNormalize(X)
    #print (X.shape)

    # 4. Gradient Descent
    X_b = np.c_[np.ones((m,1)),X] # 모든 샘플에 x0=1 추가
    # c_: concatenation. 배열을 옆으로 붙이기

    learning_rate = 0.01 # 학습률(learning rate)
    n_iter = 1000

    theta = np.random.randn(4,1) # 무작위 초기화
    gradients = np.zeros((4,1))

    for i in range(n_iter):
        gradients = 2.0/m * X_b.T.dot(X_b.dot(theta)-y)
        theta = theta - learning_rate * gradients

    #print ("theta:")
    #print (theta)
    return theta, mu, std


# 5. 임의의 구독자 수에 대한 조회수 예측
def predict(coment, like, subc, key):
    theta,mu,std = model(key)
    X_mine = np.array([[coment, like, subc]]) # 구독자 100명일 때
    X_mine = (X_mine-mu)/std #feature normalization
    #print(X_mine)

    X_mine_b = np.c_[np.ones((1,1)), X_mine] # 모든 샘플에 x0 = 1을 추가
    y_predict = X_mine_b.dot(theta)
    #print(y_predict+"회")
    return y_predict[0][0]

#y_pred = predict(50,16,100)
#print("약 "+str(round(y_pred,2))+"회")

