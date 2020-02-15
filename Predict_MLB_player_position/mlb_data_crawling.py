#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# 기폰 패키지
import pandas as pd
import numpy as np
from selenium import webdriver
from bs4 import BeautifulSoup
from html_table_parser import parser_functions as parser
import time
import matplotlib.pyplot as plt


# In[ ]:


# 셀레니움(selenium)으로 브라우저를 컨트를하기 위해서는 webdriver를 설치해야 한다
# 구글크롬은 chromedriver로 검색하면 exe파일을 다운로드 할 수 있다.
# webdriver 설치 위치를 정의한다.
browser = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver')

def crawling(url):
    # 셀레니움(selenium)으로 브라우저를 컨트를하기 위해서는 webdriver를 설치해야 한다
    # 구글크롬은 chromedriver로 검색하면 exe파일을 다운로드 할 수 있다.
    # webdriver 설치 위치를 정의한다.
    browser = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver')
    # 불러오고자하는 url을 .get으로 호출한다.
    browser.get(url)
    
    # page_source파라미터를 이용하면 HTML정보를 가지고 온다.
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')   # 뷰티풀숩으로 HTML을 파싱하고 필요한 데이터 수집
    table_tags = soup.find_all("table")   # find_all함수를 이용하면, TABLE태그로 지정된 곳만 뽑아서, 배열 형태로 저장
    table = table_tags[0]    # html상에서 table 순서, 첫번째 테이블 가지고 와야 함.
    p=parser.make2d(table)

    df_total=pd.DataFrame(p[1:],columns=p[0])    # 데이터 프레임으로 저장

    num = soup.find_all("button")[5].text   # 5번째 button에 페이지수 정보가 있음
    for j in range(1, int(num)):
        btn = browser.find_element_by_class_name('paginationWidget-next')
        btn.click()     # 버튼 클릭
        time.sleep(5)

        # 2페이지 이후 데이터 병합
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        table_tags = soup.find_all("table")
        table = table_tags[0]
        p = parser.make2d(table)

        df = pd.DataFrame(p[1:], columns=p[0])
        df_total = pd.concat([df_total, df], 0)
        
    return df_total
        # 엑셀로 다운로드
        # df_total.to_excel("test.xlsx")


# In[ ]:


list_url = ["http://mlb.mlb.com/stats/sortable.jsp?c_id=mlb#elem=%5Bobject+Object%5D&tab_level=child&click_text=Sortable+Player+hitting&game_type='R'&season=2019&season_type=ANY&league_code='MLB'&sectionType=sp&statType=hitting&page=1&ts=1580532864437&playerType=ALL",
"http://mlb.mlb.com/stats/sortable.jsp?c_id=mlb#elem=%5Bobject+Object%5D&tab_level=child&click_text=Sortable+Player+fielding&game_type='R'&season=2019&season_type=ANY&league_code='MLB'&sectionType=sp&statType=fielding&page=1&ts=1580539033522&playerType=ALL"]

df_total_hit_2012 = crawling(list_url[0])
df_total_field_2012 = crawling(list_url[1])


# In[ ]:


# 컬럼 rename
df_total_hit_2012 = df_total_hit_2012.rename(columns={'RK':'RK', 'Player':'Player', 'Team':'Team', 
                                            '':'del', '▲':'del2', 'Pos':'Pos', 'G▼':'G', 'AB▼':'AB', 'R▼':'R',
                                            'H▼':'H', '2B▼':'2B', '3B▼':'3B', 'HR▼':'HR',
                                            'RBI▼':'RBI', 'BB▼':'BB', 'SO▼':'SO', 'SB▼':'SB',
                                            'CS▼':'CS', 'AVG▼':'AVG', 'OBP▼':'OBP',
                                            'SLG▼':'SLG', 'OPS▼':'OPS', 'IBB▼':'IBB',
                                            'HBP▼':'HBP', 'SAC▼':'SAC', 'SF▼':'SF', 
                                            'TB▼':'TB', 'XBH▼':'XBH', 'GDP▼':'GDP',
                                            'GO▼':'GO', 'AO▼':'AO', 'GO_AO▼':'GO_AO',
                                            'NP▼':'NP', 'PA▼':'PA'})
df_total_field_2012 = df_total_field_2012.rename(columns={'RK':'RK', 'Player':'Player', 'Team':'Team', '':'del',
                                            '▲':'del2', 'Pos':'Pos', 'G▼':'G', 'GS▼':'GS',
                                            'INN▼':'INN', 'TC▼':'TC', 'PO▼':'PO', 'A▼':'A',
                                            'E▼':'E', 'DP▼':'DP', 'SB▼':'SB', 'CS▼':'CS',
                                            'SBPCT▲':'SBPCT', 'PB▼':'PB', 'C_WP▼':'C_WP',
                                            'FPCT▼':'FPCT', 'RF▼':'RF'})


# In[ ]:


hit_data = df_total_hit_2012.to_excel("./backup/df_total_hit.xlsx")
field_data = df_total_field_2012.to_excel("./backup/df_total_field.xlsx")

