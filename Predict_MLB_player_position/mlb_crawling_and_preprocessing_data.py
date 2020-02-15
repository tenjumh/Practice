#!/usr/bin/env python
# coding: utf-8

# In[1]:


# 기폰 패키지
import pandas as pd
import numpy as np
from selenium import webdriver
from bs4 import BeautifulSoup
from html_table_parser import parser_functions as parser
import time
import matplotlib.pyplot as plt

# 전처리 패키지
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from keras.utils import to_categorical
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import MinMaxScaler

# 모델 패키지
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import export_graphviz
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
import keras
from keras import models
from keras import layers


# In[4]:


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


# In[5]:


list_url = ["http://mlb.mlb.com/stats/sortable.jsp?c_id=mlb#elem=%5Bobject+Object%5D&tab_level=child&click_text=Sortable+Player+hitting&game_type='R'&season=2012&season_type=ANY&league_code='MLB'&sectionType=sp&statType=hitting&page=1&ts=1580532864437&playerType=ALL",
"http://mlb.mlb.com/stats/sortable.jsp?c_id=mlb#elem=%5Bobject+Object%5D&tab_level=child&click_text=Sortable+Player+fielding&game_type='R'&season=2012&season_type=ANY&league_code='MLB'&sectionType=sp&statType=fielding&page=1&ts=1580539033522&playerType=ALL"]

df_total_hit_2012 = crawling(list_url[0])
df_total_field_2012 = crawling(list_url[1])


# In[8]:


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


# In[9]:


df_total_hit_2012.to_excel("./backup/df_total_hit_2012.xlsx")
df_total_field_2012.to_excel("./backup/df_total_field_2012.xlsx")


# In[12]:


df_total_hit_2012 = pd.read_excel("./backup/df_total_hit_2012.xlsx")
df_total_field_2012 = pd.read_excel("./backup/df_total_field_2012.xlsx")

player_hit_data_2012 = df_total_hit_2012
player_field_data_2012 = df_total_field_2012

# 불필요한 컬럼 삭제

player_hit_data_2012 = player_hit_data_2012.drop(['Unnamed: 0', 'RK', 'del', 'del2', 'GO_AO', 'G'], axis=1)
player_field_data_2012 = player_field_data_2012.drop(['Unnamed: 0', 'RK', 'del', 'del2', 'G', 'GS', 'SB', 'CS', 'SBPCT','PB','C_WP'], axis=1)

# column Player & Team $ Position 기준 병합

df_total_2012 = pd.merge(player_hit_data_2012, player_field_data_2012, on=['Player', 'Team', 'Pos']) # how='outer')
df_total_2012.columns
#df_total.to_excel("test.xlsx")

# 컬럼 조건문으로 행 추출하기 Position 컬럼에서 "1B", "2B", "3B", "SS"

# 하나의 조건문이라면 "해당 컬럼 == 하나조건"으로 하면 되지만, "해당컬럼.isin([여러조건])"
# df_total_hit_infld = df_total_hit[df_total_hit['Pos'] == "2B"]
df_total_infld_2012 = df_total_2012[df_total_2012['Pos'].isin(["1B", "2B", "3B", "SS"])]
df_total_infld_2012
print(df_total_infld_2012.shape)

# 타석수와 수비이닝의 최소값 제한

df_total_infld_2012 = df_total_infld_2012[df_total_infld_2012['AB'] >= 50]
print(df_total_infld_2012.shape)
df_total_infld_2012 = df_total_infld_2012[df_total_infld_2012['INN'] >= 50]
print(df_total_infld_2012.shape)


# In[13]:


# Null 여부 확인

df_total_infld_2012.isnull().count()


# In[14]:


# Playe와 Team 컬럼 삭제

df_total_infld_2012.drop(['Player', 'Team'], axis=1, inplace=True)
df_total_infld_2012.drop(['AB', 'INN'], axis=1, inplace=True)
# df_total_infld.drop(['AVG', 'OBP', 'SLG', 'FPCT'], axis=1, inplace=True)

df_total_infld_2012['AVG'] = df_total_infld_2012['AVG'].astype(float)
df_total_infld_2012['OBP'] = df_total_infld_2012['OBP'].astype(float)
df_total_infld_2012['SLG'] = df_total_infld_2012['SLG'].astype(float)
df_total_infld_2012['FPCT'] = df_total_infld_2012['FPCT'].astype(float)
df_total_infld_2012.info()


# In[15]:


# label 데이터 레이블 인코딩
# from sklearn.preprocessing import OneHotEncoder
# from sklearn.preprocessing import LabelEncoder

encoder = LabelEncoder()
encoder.fit(df_total_infld_2012['Pos'])
df_total_infld_2012['Pos'] = encoder.transform(df_total_infld_2012['Pos'])
#labels = labels.reshape(-1, 1)
#print(df_total_infld_2012[:5])

# 데이터 세트 분리 (피처 데이터 and 라벨 데이터)

y_test_1 = df_total_infld_2012['Pos']
x_test_1 = df_total_infld_2012.drop('Pos', axis=1)


# In[ ]:





# In[ ]:




