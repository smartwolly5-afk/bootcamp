from bs4 import BeautifulSoup
import urllib.request, pandas as pd, datetime

region_name = {
    '162' : '전국',
    '75c' : '서울',
    '760' : '광주특별시',
    '75d' : '부산',
    '75e' : '대구',
    '75f' : '인천',
    '761' : '대전',
    '762' : '울산',
    '763' : '세종',
    '764' : '경기',
    '765' : '강원',
    '766' : '충북',
    '767' : '충남',
    '768' : '전북',
    '76a' : '경북',
    '76b' : '경남',
    '76c' : '제주'
}
r = list(region_name.keys())

def election_news():
    news_list = []
    for region in r:
        news_url = (f"https://news.naver.com/election/region2026/poll/region?componentId={region}")
        print(news_url)

        html = urllib.request.urlopen(news_url)
        soupNews = BeautifulSoup(html,"html.parser")

        articles = soupNews.select("a.article_text_area")

        for article in articles:
            title = (article.select_one("span.article_title").text.strip())
            link = article.get("href")
            time = (article.select_one("div.time").text.strip())
            news_dict = {"지역": region_name[region],"기사 제목": title,"기사 링크": link,"시간": time}

            news_list.append(news_dict)

    df = pd.DataFrame(news_list)
    return df

df = election_news()
print(df.to_string(index=False))

df.to_csv("지방여론뉴스.csv",encoding="utf-8-sig",index=False)