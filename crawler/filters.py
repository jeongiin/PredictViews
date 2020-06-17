import re


#crawler에서만 필요한 코드(년, 개월 단위 영상은 취급하지 않음)
def sub(keyword) :

    if '년' in keyword or '개월' in keyword:
        return -1

    else : return 1


# 조회수, 구독자, 댓글, 좋아요는 int형으로 바꿔줌
# 데이터 프라임에 저장하기 쉽게 스트링으로 바꿔줌
def stoi(keyword) :
    keyword = keyword.replace(',','')

    if '만' in keyword:
        digit = re.findall("\d+", keyword)
        i = float(digit[0]) * 10000
        return int(i)

    elif '천' in keyword:
        digit = re.findall("\d+", keyword)
        i = float(digit[0]) * 1000
        return int(i)

    elif '개' in keyword or '회' in keyword or '명' in keyword:
        digit = re.findall("\d+", keyword)
        return int(digit[0])

    elif '없음' in keyword:
        return 0

    else : return int(keyword)
