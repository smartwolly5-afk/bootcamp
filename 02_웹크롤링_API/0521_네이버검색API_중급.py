#중급
import urllib.request
import json
import time
import datetime

client_id = "YOUR_NAVER_CLIENT_ID"
client_secret = "YOUR_NAVER_CLIENT_SECRET"

def main():
    node = 'news'
    a = {}
    for i in range(3):
        srcText = input('검색어를 입력하세요:')
        cnt = 0
        jsonResult = []

    #100번을 가져옴 그냥 정보자체를 100개 가져옴
        jsonResponse = getNaverSearch(node,srcText,1,100)
        total = jsonResponse['total']

        print('전체 검색: %d 건' %total)
        a[srcText] = total

    sorted_a = sorted(a.items(), key = lambda x: x[1] ,reverse = True )
    num = 0
    for k, t in sorted_a:
        print(f"{k}이(가) {t}개로 {num+1}번째")
        num += 1

def getRequestUrl(url):
    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id",client_id)
    req.add_header("X-Naver-Client-Secret",client_secret)
        
    #에러 났을때 로그를 남겨주는 부분 
    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            print("[%s] Url Request Success" % datetime.datetime.now())
            return response.read().decode('utf-8')
    except Exception as e:
        print(e)
        print("[%s] Error for URL:%s" % (datetime.datetime.now(),url))
        return None
    
def getNaverSearch(node,srcText, page_start, display):
    base = "https://openapi.naver.com/v1/search"
    node = "/%s.json" % node
    parameters = "?query=%s&start=%s&display=%s&sort=date" % (urllib.parse.quote(srcText),page_start,display)

    url = base + node + parameters
    responseDecode = getRequestUrl(url)

    if(responseDecode == None):
        return None
    else:
        return json.loads(responseDecode)
    
if __name__ == "__main__":
    main()