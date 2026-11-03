from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import datetime
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from collections import defaultdict
import random

def login():   
    my_id = 'YOUR_ID'
    my_pw = 'YOUR_PASSWORD'
    #전체화면용 옵션
    options = webdriver.ChromeOptions()
    #전체화면으로 키기
    options.add_argument("--start-maximized")
    wd = webdriver.Chrome(options=options)
    wd.get("https://thevc.kr/")
    time.sleep(random.randint(2,5))
    login_button = wd.find_element(By.CSS_SELECTOR, 'button.box-button.main.medium')
    login_button.click()
    time.sleep(5)
    id_box = wd.find_element(By.ID,'email')
    id_box.send_keys(my_id)
    pw_box = wd.find_element(By.ID,'password')
    pw_box.send_keys(my_pw)
    time.sleep(3)
    log_button = wd.find_element(By.CSS_SELECTOR,'button.box-button.main.large.mt-40.w-full')
    log_button.click()
    html = wd.page_source
    get_t=BeautifulSoup(html,'html.parser')
    time.sleep(2)
    return wd

#주간 월간 일간
def next_dayl(wd,i):
    lank_button = wd.find_element(By.CSS_SELECTOR, 'h2.text-20 .dropdown-wrap button.text-button')
    wd.execute_script("arguments[0].scrollIntoView({block: 'center'});", lank_button)
    time.sleep(3)
    wd.execute_script("arguments[0].click();", lank_button)
    time.sleep(3)
    buttons_l = wd.find_elements(By.CSS_SELECTOR, 'h2.text-20 .list-20 button')
    buttons_l[i].click()
def next_daym(wd,i):
    element = wd.find_element(By.XPATH, f"//h2[contains(., '{"투자/M&A 랭킹"}')]")
    mn_button = element.find_element(By.CSS_SELECTOR, 'button.text-button')
    wd.execute_script("arguments[0].scrollIntoView({block: 'center'});", mn_button)
    time.sleep(3)
    wd.execute_script("arguments[0].click();", mn_button)
    time.sleep(3)
    buttons_m = element.find_elements(By.CSS_SELECTOR, '.list-20 button')
    buttons_m[i].click()


#다음 카테고리 클릭하고 실행
def next_tabl(wd,lank_tabs_l,current_index_l):
    if current_index_l < len(lank_tabs_l):
        target_tab = lank_tabs_l[current_index_l]
        cat_name = target_tab.text
        wd.execute_script("arguments[0].click();", target_tab)
        time.sleep(3)
        html = wd.page_source
        get_t=BeautifulSoup(html,'html.parser')
        return get_t ,cat_name
    else:
        return None, None
    # # start_tab = wd.find_element(By.CSS_SELECTOR,'div.tab-content')
    # # start_tab.click()
    # time.sleep(3)
    
#csv파일로 순위 저장
def con_csv(all_data, j, catagory):

    flat_data = []
    for tab in all_data:
        tab_name = tab['tab_name']
        for rank_item in tab['rank']:
            # rank_item은 {'기업명': '제품명'} 형태입니다.
            for company, product in rank_item.items():
                flat_data.append({
                    "탭이름": tab_name,
                    "기업명": company,
                    "제품명": product
                })

    df = pd.DataFrame(flat_data)

    df.to_csv(f"{catagory}_{j}.csv", index=False, encoding='cp949')

    print("CSV저장")

#더보기 있으면 클릭하기 rank
def more_data(wd):
    # more = wd.find_element(By.CSS_SELECTOR, 'button.text-button.small.gray.paddingless')
    # if more:
    #     wd.execute_script("arguments[0].click();", more)
    # '조회수 랭킹'이라는 텍스트를 가진 h2가 포함된 부모 div를 찾고, 그 안의 버튼을 클릭
    more_btn = wd.find_elements(By.CSS_SELECTOR, "div[data-v-ecce4443] > button.text-button.small.gray.paddingless:last-child")
    if len(more_btn) > 0:
        wd.execute_script("arguments[0].scrollIntoView({block: 'center'});", more_btn[0])
        time.sleep(3)
        wd.execute_script("arguments[0].click();", more_btn[0])
        return True
    return False

#더보기 있으면 클릭하기 m&a
def more_datam(wd):
    # more = wd.find_element(By.CSS_SELECTOR, 'button.text-button.small.gray.paddingless')
    # if more:
    #     wd.execute_script("arguments[0].click();", more)
    # '조회수 랭킹'이라는 텍스트를 가진 h2가 포함된 부모 div를 찾고, 그 안의 버튼을 클릭
    more_btn = wd.find_elements(By.CSS_SELECTOR, ".extra >div:nth-child(2) >div > button")
    if len(more_btn) > 0:
        wd.execute_script("arguments[0].scrollIntoView({block: 'center'});", more_btn[0])
        time.sleep(3)
        wd.execute_script("arguments[0].click();", more_btn[0])
        return True
    return False

#더보기 들어가서 총 유치금액, 총 투자금액 뽑아오기
def c_all(wd):
    try:
        price_block = wd.find_elements(By.CSS_SELECTOR, ".summary-wrap")
        price_text = price_block[0].find_element(By.CSS_SELECTOR, "b").text
        total_com = price_block[1].find_element(By.CSS_SELECTOR, 'b').text
        # print(f"총 유치 금액: {price_text}")
        # print(f"총 투자 대상:{total_com}")
        return price_text, total_com
    except Exception as e:
        return "정보없음", "정보없음"
    
    #헤더들 뽑아오기

#테이블 헤더 가져오기
def c_data_all(wd):
    all_table = wd.find_elements(By.CSS_SELECTOR, "div.table-wrap.is-full-width tr > th")
    head = []
    for span in all_table:
        head.append(span.text)
    print(head)
    return head

#더보기 테이블 데이터 긁어오기
def c_data(wd):
    rows = wd.find_elements(By.CSS_SELECTOR, "div.table-wrap.is-full-width tbody > tr")
    extracted_data = []
    for row in rows:
        cells = row.find_elements(By.CSS_SELECTOR, "td, th")
        
        row_data = [cell.text.strip() for cell in cells]

        if row_data:
            extracted_data.append(row_data)
    return extracted_data

#더보기 데이터 csv 파일로 저장하기
def save_to_csv(headers, data, filename):
    df = pd.DataFrame(data, columns=headers)
    
    # CSV로 저장 (인코딩은 한글 깨짐 방지를 위해 cp949 또는 utf-8-sig 사용)
    df.to_csv(f"{filename}.csv", index=False, encoding='utf-8-sig')
    print(f"{filename}.csv 저장 완료!")

    #다음 페이지로 넘기고 만약 팝업창이 뜨면 끄고 원래 페이지로 복귀

#페이지에서 유로플랜결제 팝업창 끄기
def close_modal(wd):
    try:
        close_btn = wd.find_element(By.CSS_SELECTOR, "button.icon-button.medium.paddingless.close-button")
        wd.execute_script("arguments[0].click();", close_btn)
        time.sleep(3)
        return True
    except:
        return False

#더보기 창에서 다음 페이지로 넘어가기
def next_page(wd,num):
    button_next = wd.find_elements(By.CSS_SELECTOR, "div.pagination > button")
    wd.execute_script("arguments[0].click();", button_next[num])
    time.sleep(3)
    if close_modal(wd):
        return False
    return True

#더보기 창 크롤링
def collect_all(wd,head_columns):
    num = 1
    collect_data = []
    total_price, total_target = c_all(wd)
    head = c_data_all(wd)
    final_head = head_columns+ head
    while(1):
        current_data = c_data(wd)
        for row in current_data:
            final_row = [total_price, total_target] + row
            collect_data.append(final_row)
        
        if not next_page(wd,num):
            break
        num += 1
        
    print(f"헤더 개수: {len(final_head)}")
    print(f"헤더 내용: {final_head}")

    for i, row in enumerate(collect_data):
        if len(row) != len(final_head):
            print(f"에러 발생! {i}번째 행의 길이는 {len(row)}인데 헤더는 {len(final_head)}입니다.")
            print(f"문제의 데이터: {row}")
    return final_head, collect_data

#조회수 순위 데이터 크롤링
def rank_c(wd):
    for j in range(3):
        next_dayl(wd,j)
        #카테고리 위치
        # print(tabs)
        # for i, tab in enumerate(tabs):
        #     print(f"{i}번째 탭 이름: {tab.text}")
        #랭킹 별로 저장하기
        all_data = []
        for i in range(11):
            time.sleep(3)
            tabs = wd.find_elements(By.CSS_SELECTOR, 'div.tab-content')
            lank_tabs = tabs[15:26]
            idx = i
            result = next_tabl(wd,lank_tabs,idx)
            get_t, cat_name = result
            items = get_t.select('ol.list-wrap > li')
        # print(items)
            now_tab = []
            for item in items[:10]:
                link_tag = item.select_one('a')
                name = link_tag.select_one('div.text-truncate.text-16')
                company = name.contents[0].strip()
                product = name.select_one('div.text-truncate')
                    # print(company)
                    # print(product.text)
                now_tab.append({company:product.text})
            all_data.append({"tab_name":cat_name,
                            "rank": now_tab})    

            if more_data(wd):
                time.sleep(5)
                head, all_page_data = collect_all(wd,["총 유치 금액","총 투자 회사"])
                if head and all_page_data:
                    save_to_csv(head, all_page_data, f"rank_detail_{cat_name}_{j}")
                wd.get("https://thevc.kr/")
                time.sleep(5)
                next_dayl(wd, j)
        print(all_data)
        con_csv(all_data, j,"rank_data")
    return None

#M&A 순위 데이터 크롤링
def ma_c(wd):    
    for j in range(3):
        next_daym(wd,j)
        #카테고리 위치
        # print(tabs)
        # for i, tab in enumerate(tabs):
        #     print(f"{i}번째 탭 이름: {tab.text}")
        #랭킹 별로 저장하기
        all_data = []
        for i in range(2):
            time.sleep(3)
            tabs = wd.find_elements(By.CSS_SELECTOR, 'div.tab-content')
            lank_tabs_m = tabs[26:28]
            idx = i
            result = next_tabm(wd,lank_tabs_m,idx)
            get_t, cat_name = result
            items = get_t.select('ol.list-wrap > li')
        # print(items)
            now_tab = []
            for item in items[10:20]:
                link_tag = item.select_one('a')
                if not link_tag:
                    continue
                name = link_tag.select_one('div.text-truncate.text-16')
                if name:
                    company = name.contents[0].strip()
                    product_tag = name.select_one('div.text-truncate')
                    if product_tag:    
                        product_text = product_tag.text.strip()
                    else:
                        product_text = "정보없음"
                    # print(company)
                    # print(product.text)
                    now_tab.append({company:product_text})
                else:
                    continue
            all_data.append({"tab_name":cat_name,
                            "rank": now_tab})
            if more_datam(wd):
                time.sleep(5)
                head, all_page_data = collect_all(wd,["총 투자 금액","총 투자 건수"])
                if head and all_page_data:
                    save_to_csv(head, all_page_data, f"m&a_detail_{cat_name}_{j}")
                wd.get("https://thevc.kr/")
                time.sleep(5)
                next_daym(wd, j)
        print(all_data)
        con_csv(all_data,j,"d&m_data")
    return None

#메인함수
def main():
    wd = login()

    print("투자 랭킹")
    rank_c(wd)
    print("m&a 랭킹")
    ma_c(wd)


if __name__ == "__main__":
    main()
