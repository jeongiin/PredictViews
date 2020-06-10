
from model import vlog_multi_variable_regression
from model import result_model

accuracy = -1
subc = -1
key = -1
go = 1

def init():
    print("조회수 예측 프로그램에 오신 것을 환영합니다!")
    print("당신의 유투브 키워드를 선택하세요!")
    print("1. 브이로그 \n2. 먹방\n3. 게임\n4. 리뷰")
    key = input(":")
    if int(key)>4 or int(key)<1 :
        print("해당 키워드는 준비중입니다.")
        return 0,0,0,0

    else :
        subc = input("구독자수 :")
        coment =input("평균 댓글수 :")
        like = input("평균 좋아요 수 :")

    return key,subc,coment,like


def mypredict(key, subc, coment, like):
    pview = -1
    if int(key)==1:
        # pview = vlog_multi_variable_regression.predict(int(coment), int(like), int(subc),"vlog")
        pview, accuracy = result_model.model("vlog", int(subc),int(coment),int(like))

    elif int(key)==2:
        pview, accuracy = result_model.model("food", int(subc),int(coment),int(like))

    elif int(key)==3:
        pview, accuracy = result_model.model("game", int(subc),int(coment),int(like))

    elif int(key)==4:
        pview, accuracy = result_model.model("review", int(subc),int(coment),int(like))

    else:
        print("")

    #accuracy 추가 필요
    print("당신의 예측 조회수는 "+str(round(accuracy*100,2))+"% 확률로 "+str(round(pview,1))+"회 입니다.")



def program_exit():
    go = int(input("다시하기(1) 종료(0):"))
    print("")
    if go==1 or go ==0:
        return go
    else :
        print("1 혹은 0을 입력해주세요.")
        return program_exit()

while go!=0:
    key,view,coment,like = init()
    mypredict(key,view,coment,like)
    go = program_exit()

