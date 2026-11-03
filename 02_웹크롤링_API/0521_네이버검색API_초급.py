#초급
import os
import sys
import time
import json
import urllib.request
import datetime

client_id = "YOUR_NAVER_CLIENT_ID"
client_secret = "YOUR_NAVER_CLIENT_SECRET"

#웹크롤링 메인함수
def main():
    node = 'news'
    srcText = input('검색어를 입력하세요:')
    cnt = 0
    jsonResult = []

#100번을 가져옴 그냥 정보자체를 100개 가져옴
    jsonResponse = getNaverSearch(node,srcText,1,100)
    total = jsonResponse['total']

#100개인지를 확인하기 위한 조건인듯 items 딕셔너리를 받아옴
    while((jsonResponse != None) and (jsonResponse['display']!=0)):
        for post in jsonResponse['items']:
            cnt += 1
            getPostData(post, jsonResult, cnt)
        start = jsonResponse['start'] + jsonResponse['display']
        if start > total or start > 1000:
            break
        jsonResponse = getNaverSearch(node, srcText, start, 100)
    print('전체 검색: %d 건' %total)

    with open('%s_naver_%s.json' % (srcText, node),'w',encoding = 'utf8') as outfile:
        jsonFile = json.dumps(jsonResult, indent =4, sort_keys = True, ensure_ascii = False)

        outfile.write(jsonFile)

    print("가져온 데이터: %d 건" %(cnt))
    print('%s_naver_%s.json SAVED' % (srcText,node))

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
    
def getPostData(post, jsonResult, cnt):
    title = post['title']
    description = post['description']
    org_link = post['originallink']
    link = post['link']

    pDate = datetime.datetime.strptime(post['pubDate'], '%a, %d %b %Y %H:%M:%S +0900')
    if pDate.date() == datetime.datetime.now().date():
        pDate = pDate.strftime('%Y-%m-%d %H:%M:%S')
        jsonResult.append({'cnt':cnt, 'title':title, 'description':description, 'org_link':org_link, 'link':org_link, 'pDate':pDate})
    return

#이게 그 네이버 뉴스 크롤링 api를 활용하는 방식이네 url 만드는법
#꼭 찾아서 들어가서 보고 플랫폼 마다 다름
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