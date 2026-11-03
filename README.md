# Bootcamp — 데이터 분석 · AI 부트캠프 코드 모음

2026년 4월 ~ 9월 부트캠프에서 작성한 실습 코드를 커리큘럼 순서대로 정리한 저장소입니다.
파이썬 기초부터 웹 크롤링, 데이터 분석·시각화, 통계, 머신러닝·딥러닝, 컴퓨터 비전까지 다룹니다.

## 커리큘럼 한눈에 보기

| # | 폴더 | 기간 | 주요 내용 | 주요 라이브러리 |
|---|---|---|---|---|
| 01 | [파이썬기초](01_파이썬기초) | 04.29 ~ 05.14 | 자료형, 조건·반복문, 함수, 재귀, 클래스, SQL 기초 | Python, turtle |
| 02 | [웹크롤링_API](02_웹크롤링_API) | 05.21 ~ 05.29 | 네이버 검색 API, 공공데이터·서울 열린데이터 API, 정적/동적 크롤링 | urllib, requests, BeautifulSoup, Selenium |
| 03 | [미니프로젝트_크롤링](03_미니프로젝트_크롤링) | 06.01 ~ 06.04 | 포인핸드·THE VC 동적 크롤링 (2조 미니 프로젝트) | Selenium, pandas |
| 04 | [데이터분석_시각화](04_데이터분석_시각화) | 06.08 ~ 07.02 | pandas 집계·groupby, matplotlib/seaborn 시각화, 통계분석, NETFLIX 분석 | pandas, matplotlib, seaborn, statsmodels |
| 05 | [텍스트_지도분석](05_텍스트_지도분석) | 06.15 ~ 06.26 | 영어/한글 단어 빈도, 워드클라우드, 주소 데이터 지도 시각화 | nltk, konlpy, kiwipiepy, wordcloud, folium |
| 06 | [머신러닝_회귀_분류_군집](06_머신러닝_회귀_분류_군집) | 06.22 ~ 06.24 | 선형회귀, 로지스틱회귀, 결정트리, K-Means 군집 | scikit-learn |
| 07 | [중간프로젝트_APT분석](07_중간프로젝트_APT분석) | 07.06 ~ 07.14 | 국가배후 APT 공격기법 분석 (개인 작업분) | Selenium, pandas, folium, plotly |
| 08 | [통계](08_통계) | 07.20 ~ 07.23 | 기술통계, 이상치, 표본추출, 확률분포 | numpy, scipy |
| 09 | [머신러닝_딥러닝](09_머신러닝_딥러닝) | 08.04 ~ 08.12 | 회귀·분류 실습, 퍼셉트론, MLP, 오토인코더 | scikit-learn, TensorFlow/Keras, XGBoost, LightGBM |
| 10 | [컴퓨터비전](10_컴퓨터비전) | 08.27 ~ 09.08 | OpenCV 영상처리, SIFT 특징점, PyQt5 앱, YOLO 객체탐지, 분할 | OpenCV, PyQt5, TensorFlow, PyTorch |
| 99 | [기타](99_기타) | — | 수집 문서 본문 필터 스크립트 | — |

## 폴더별 파일

<details>
<summary><b>01_파이썬기초</b></summary>

| 파일 | 내용 |
|---|---|
| 0429_출력_자료형_연산자 | print, 문자열 인덱싱, 리스트, 산술 연산, 변수, input |
| 0430_문자열_조건문 | format, find, 논리 연산, if 조건문 |
| 0504_리스트_반복문_딕셔너리 | 리스트 조작, for/while, 딕셔너리 |
| 0506 / 0507 _함수 | 함수 정의, 매개변수, 가변 인자 |
| 0508_재귀_클래스기초 | 팩토리얼·피보나치 재귀, 클래스 기초 |
| 0511_연습문제 | 369 게임, 로또, 이동평균 등 |
| 0512_클래스_모듈 | 클래스 실습, 외부 모듈, 간단한 크롤링 맛보기 |
| 0513_클래스_매직메서드_turtle | `__eq__`, `__gt__` 등 매직 메서드, turtle |
| 0513_SQL_기초 | CREATE / ALTER / UPDATE / SELECT |
| 0514_turtle_그리기 | turtle 그림 그리기 |
</details>

<details>
<summary><b>02_웹크롤링_API</b></summary>

| 파일 | 내용 |
|---|---|
| 0521_네이버검색API (+ 초급/중급/고급 .py) | 네이버 검색 Open API 호출 → JSON 저장 |
| 0522_관광통계API | 네이버 API + 한국관광공사 출입국 관광통계 |
| 0527_공공데이터API / 교량시설 / 따릉이 | data.go.kr, 서울 열린데이터광장 API |
| 0527_정적크롤링_BeautifulSoup | 한빛미디어, 할리스 매장, 위키 크롤링 |
| 0528_포켓몬_위키크롤링 | 위키백과 포켓몬 목록 크롤링 |
| 0529_동적크롤링_Selenium | 커피빈 매장, quotes.toscrape 동적 크롤링 |
| 0529_선거뉴스_크롤링.py | 네이버 뉴스 크롤링 |
| 오픈스카이_API | OpenSky 항공기 위치 API |
| 10장_대기오염데이터_API수집 | 에어코리아 대기오염 데이터 수집 |
</details>

<details>
<summary><b>03_미니프로젝트_크롤링</b></summary>

2조 미니 프로젝트. **포인핸드**(유기동물 보호소·실종 제보)와 **THE VC**(스타트업 투자 정보)를 Selenium으로 동적 크롤링했습니다.

```text
login()
 ├─ rank_c(wd)  : 조회수 랭킹 탭 순회 → next_dayl / next_tabl → more_data → con_csv
 └─ ma_c(wd)    : 투자유치·M&A 탭 순회 → next_daym / next_tabm → more_datam → con_csv
```

| 파일 | 내용 |
|---|---|
| 미니프로젝트_THEVC_최종 | THE VC 랭킹·투자 데이터 크롤링 최종본 |
| 0601_포인핸드_THEVC_크롤링 | 포인핸드 보호소/실종 데이터 + THE VC 크롤링 |
| 0601_THEVC_랭킹크롤링 | 일간/주간 조회수 랭킹 수집 |
| 0604_THEVC_크롤링_함수모음.py | 크롤링 함수 모듈화 |
| 0604_수집데이터_분석 | 수집 CSV 분석·시각화 |
</details>

<details>
<summary><b>04 ~ 06 데이터분석 · 텍스트 · 머신러닝</b></summary>

| 파일 | 내용 |
|---|---|
| 0608 ~ 0611 pandas | DataFrame 생성, value_counts, groupby, pd.cut (titanic, tips, flights) |
| matplotlib_시각화 / seaborn_회귀플롯_penguins | 기본 차트, OLS 회귀선 |
| 7장_통계분석_와인품질 | t-검정, 회귀분석 |
| NETFLIX_데이터분석 | 장르·국가·등급 분석, 네트워크·레이더 차트 |
| 0630 / 6조_데이터시각화실습 / 0702 발표 | 학생 데이터 시각화 팀 실습 |
| 8장 영어/한글 텍스트빈도분석, 0615, 0616 | 토큰화, 불용어, 워드클라우드, 채용공고 기술스택 추출 |
| 9장_주소데이터_지도분석, 0621 | 커피 매장·도서관 데이터 지도/블록맵 |
| 0626_도서데이터_전처리 | 결측치·형식 정리, ISBN 보완 |
| 0622 / 10장 / 0623 | 선형회귀 (자동차 연비, 미세먼지, CO2 배출량) |
| 11장 / 0624 | 로지스틱 회귀, 결정트리, 신용카드 연체, titanic |
| 12장_KMeans_군집분석 | 온라인 리테일 고객 군집, 실루엣 계수 |
</details>

<details>
<summary><b>07_중간프로젝트_APT분석</b></summary>

CFR Cyber Operations Tracker 크롤링과 MITRE ATT&CK 데이터로 북한·중국·러시아·이란 APT 공격기법을 분석한 6조 중간 프로젝트의 개인 작업분입니다.
팀 전체 코드와 발표자료는 [6midterm](https://github.com/smartwolly5-afk/6midterm) 저장소에 있습니다.
</details>

<details>
<summary><b>08 ~ 10 통계 · 딥러닝 · 컴퓨터비전</b></summary>

| 파일 | 내용 |
|---|---|
| 0720 ~ 0723 | 이상치(IQR), 도수분포, 2차원 확률분포, 기댓값·분산, 포아송 |
| 0804 ~ 0810 | 학생성적 회귀, 신용연체 로지스틱, 수료 예측, 항공 지연 예측 |
| 0805_퍼셉트론_논리게이트 | AND/OR/NAND/XOR, MLP |
| 0805 / 0806 신경망 | Keras Dense 분류, 결정경계, 와인 MLP |
| 0812_오토인코더_FashionMNIST | 오토인코더 |
| 0827 ~ 0831 | OpenCV 그리기·마우스 이벤트, 감마 보정, 필터 |
| 0901_특징점검출_SIFT | 코너 검출, SIFT 기술자 |
| 0902 ~ 0904 PyQt5 | 영상 캡처 앱, 이미지 효과(카툰 등) 앱, 숫자 인식 앱 |
| 0907_객체탐지_YOLO | YOLOv3 / YOLOv5 |
| 0908_분할_전이학습 | Oxford Pets 분할, Mask R-CNN |
</details>

## 참고

- **데이터·모델 파일은 포함하지 않았습니다.** CSV, 이미지, `.h5`/`.pt` 모델 가중치, 대용량 zip은 용량 문제로 제외했습니다.
  노트북에 남아 있는 출력 결과로 실행 결과를 확인할 수 있습니다.
- **API 키와 로그인 정보는 지웠습니다.** 직접 실행하려면 `YOUR_NAVER_CLIENT_ID`, `YOUR_DATA_GO_KR_KEY`, `YOUR_SEOUL_API_KEY`,
  `YOUR_GEMINI_API_KEY`, `YOUR_ID` / `YOUR_PASSWORD` 자리에 본인 키를 넣어 주세요.
- 실행 환경: Python 3.12, Jupyter Notebook, Windows (한글 폰트 `Malgun Gothic`)
