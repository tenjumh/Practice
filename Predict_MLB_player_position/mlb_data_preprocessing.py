# 기폰 패키지
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def preprocessing(file1, file2):
    df_total_hit = pd.read_excel(file1)
    df_total_field = pd.read_excel(file2)
    player_hit_data = df_total_hit
    player_field_data = df_total_field
    
    player_hit_data = player_hit_data.rename(columns={'RK':'RK', 'Player':'Player', 'Team':'Team', 
                                            '':'del', '▲':'del2', 'Pos':'Pos', 'G▼':'G', 'AB▼':'AB', 'R▼':'R',
                                            'H▼':'H', '2B▼':'2B', '3B▼':'3B', 'HR▼':'HR',
                                            'RBI▼':'RBI', 'BB▼':'BB', 'SO▼':'SO', 'SB▼':'SB',
                                            'CS▼':'CS', 'AVG▼':'AVG', 'OBP▼':'OBP',
                                            'SLG▼':'SLG', 'OPS▼':'OPS', 'IBB▼':'IBB',
                                            'HBP▼':'HBP', 'SAC▼':'SAC', 'SF▼':'SF', 
                                            'TB▼':'TB', 'XBH▼':'XBH', 'GDP▼':'GDP',
                                            'GO▼':'GO', 'AO▼':'AO', 'GO_AO▼':'GO_AO',
                                            'NP▼':'NP', 'PA▼':'PA'})
    player_field_data = player_field_data.rename(columns={'RK':'RK', 'Player':'Player', 'Team':'Team', '':'del',
                                            '▲':'del2', 'Pos':'Pos', 'G▼':'G', 'GS▼':'GS',
                                            'INN▼':'INN', 'TC▼':'TC', 'PO▼':'PO', 'A▼':'A',
                                            'E▼':'E', 'DP▼':'DP', 'SB▼':'SB', 'CS▼':'CS',
                                            'SBPCT▲':'SBPCT', 'PB▼':'PB', 'C_WP▼':'C_WP',
                                            'FPCT▼':'FPCT', 'RF▼':'RF'})

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
    df_total_infld

    # 타석수와 수비이닝의 최소값 제한
    df_total_infld = df_total_infld[df_total_infld['AB'] >= 50]
    df_total_infld = df_total_infld[df_total_infld['INN'] >= 50]
    df_total_infld.isnull().count()
    # Playe와 Team 컬럼 삭제

    df_total_infld.drop(['Player', 'Team'], axis=1, inplace=True)
    df_total_infld.drop(['AB', 'INN'], axis=1, inplace=True)
    # df_total_infld.drop(['AVG', 'OBP', 'SLG', 'FPCT'], axis=1, inplace=True)

    df_total_infld['AVG'] = df_total_infld['AVG'].astype(float)
    df_total_infld['OBP'] = df_total_infld['OBP'].astype(float)
    df_total_infld['SLG'] = df_total_infld['SLG'].astype(float)
    df_total_infld['FPCT'] = df_total_infld['FPCT'].astype(float)
    
    return df_total_infld


