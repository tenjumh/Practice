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


# In[12]:


df_total_hit = pd.read_excel("./backup/df_total_hit_2012.xlsx")
df_total_field = pd.read_excel("./backup/df_total_field_2012.xlsx")

player_hit_data = df_total_hit
player_field_data = df_total_field

# 불필요한 컬럼 삭제

player_hit_data = player_hit_data.drop(['Unnamed: 0', 'RK', 'del', 'del2', 'GO_AO', 'G'], axis=1)
player_field_data = player_field_data.drop(['Unnamed: 0', 'RK', 'del', 'del2', 'G', 'GS', 'SB', 'CS', 'SBPCT','PB','C_WP'], axis=1)

# column Player & Team $ Position 기준 병합

df_total = pd.merge(player_hit_data, player_field_data, on=['Player', 'Team', 'Pos']) # how='outer')
df_total.columns
#df_total.to_excel("test.xlsx")

# 컬럼 조건문으로 행 추출하기 Position 컬럼에서 "1B", "2B", "3B", "SS"

# 하나의 조건문이라면 "해당 컬럼 == 하나조건"으로 하면 되지만, "해당컬럼.isin([여러조건])"
# df_total_hit_infld = df_total_hit[df_total_hit['Pos'] == "2B"]
df_total_infld = df_total[df_total['Pos'].isin(["1B", "2B", "3B", "SS"])]

# 타석수와 수비이닝의 최소값 제한

df_total_infld = df_total_infld[df_total_infld['AB'] >= 50]
df_total_infld = df_total_infld[df_total_infld['INN'] >= 50]

# In[13]:


# Null 여부 확인

df_total_infld.isnull().count()


# In[14]:


# Playe와 Team 컬럼 삭제

df_total_infld.drop(['Player', 'Team'], axis=1, inplace=True)
df_total_infld.drop(['AB', 'INN'], axis=1, inplace=True)
# df_total_infld.drop(['AVG', 'OBP', 'SLG', 'FPCT'], axis=1, inplace=True)

df_total_infld['AVG'] = df_total_infld['AVG'].astype(float)
df_total_infld['OBP'] = df_total_infld['OBP'].astype(float)
df_total_infld['SLG'] = df_total_infld['SLG'].astype(float)
df_total_infld['FPCT'] = df_total_infld['FPCT'].astype(float)
df_total_infld.info()


# In[15]:


# label 데이터 레이블 인코딩
# from sklearn.preprocessing import OneHotEncoder
# from sklearn.preprocessing import LabelEncoder

encoder = LabelEncoder()
encoder.fit(df_total_infld['Pos'])
df_total_infld['Pos'] = encoder.transform(df_total_infld['Pos'])
#labels = labels.reshape(-1, 1)
#print(df_total_infld[:5])

# 데이터 세트 분리 (피처 데이터 and 라벨 데이터)

y_test = df_total_infld['Pos']
x_test = df_total_infld.drop('Pos', axis=1)
