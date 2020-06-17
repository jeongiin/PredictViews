import numpy as np
import pandas as pd
from sklearn import preprocessing

keyword = "vlog"
data_name = "./model_youtube_crawling_data_vlog.csv "#각자 데이터가 있는 위치
df = pd.read_csv(data_name) #game에 해당하는 model 데이터


#==================================================================
# 이상치 제거 (IQR : Inter Quantile Range - 사분위 값의 편차를 이용)
def removeOutliers(x):
    # Q1, Q3구하기
    q1 = x.quantile(0.25)
    q3 = x.quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - (iqr*1.5)
    upper_bound = q3 + (iqr*1.5)
    # 원래 데이터 복제
    y = x
    # 이상치를 NA로 변환
    y[(x > upper_bound)|(x < lower_bound)] = None
    return x

#==================================================================
#함수 실행
removeOutliers(df) # 이상치 제거 함수
df = df.dropna() # NA값 제거
#print(df)
df.to_csv('model_youtube_crawling_data_'+keyword+'_outlier.csv',mode='w',encoding='utf-8-sig',index=False)
print("Finish")



# import numpy as np
# import pandas as pd
#
# keyword = 'vlog' ######이부분만 바꾸시면 정상 작동 영어로 작성##########
#
# data_name = "./model_youtube_crawling_data_"+keyword+".csv" #각자 데이터가 있는 위치
# df = pd.read_csv(data_name) #game에 해당하는 model 데이터
#
# #==================================================================
# # 이상치 제거 (IQR : Inter Quantile Range - 사분위 값의 편차를 이용)
# def removeOutliers(x):
#     # Q1, Q3구하기
#     q1 = x.quantile(0.25)
#     q3 = x.quantile(0.75)
#     iqr = q3 - q1
#     lower_bound = q1 - (iqr*1.5)
#     upper_bound = q3 + (iqr*1.5)
#     # 원래 데이터 복제
#     y = x
#     # 이상치를 NA로 변환
#     y[(x > upper_bound)|(x < lower_bound)] = np.nan
#     return x
#
# #==================================================================
# #함수 실행
# removeOutliers(df) # 이상치 제거 함수
# #df = df.dropna() # NA값 제거
# mean = df.mean().astype(int)
# df.fillna(mean,inplace=True)
# #print(df)
# df.to_csv('model_youtube_crawling_data_'+keyword+'_outlier_mean.csv',mode='w',encoding='utf-8-sig',index=False)
# print("Finish")