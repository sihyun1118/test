import pandas as pd
import numpy as np
import re
import glob
# import os
# file_name = os.listdir("C:/Users/sihyun/Desktop/빅데이터 센터/세코닉스/data/SN084JA2 측정/SN084JA2 PV형상/SN084JA2 3월 형상공정/")
# dd = pd.read_excel('C:/Users/sihyun/Desktop/빅데이터 센터/세코닉스/data/SN084JA2 측정/SN084JA2 PV형상/SN084JA2 3월 형상공정/SN084JA2 6차 (2021.03~.xlsx', sheet_name='L2', engine='openpyxl')
def PeaktoValley(data, lens, count):
    a=data.dropna(how='all')
    # Cav별 PV preprocessing
    data_v1 = a.iloc[:, 3:19]
    data_v1.columns = list(data_v1.iloc[0])
    # 선별 text 처리
    for i in range(len(data_v1.columns)):
        for j in range(1, len(data_v1)):
            if data_v1.iloc[j - 1][i] == '선별' and data_v1.isna().iloc[j][i] == True:
                data_v1.iloc[j][i] = '선별'
    data_v1 = data_v1.dropna(how='any')
    data_v1.reset_index(drop=True, inplace=True)

    # CAV text를 제거 후 수치값만 가져오기
    for i in range(len(data_v1)):
        if type(data_v1['CAV1'][i]) == type('str'):
            data_v1 = data_v1.drop(index=i, axis=0)

    # 날짜, Lot 가져오기
    data_v2 = a.iloc[:, 0:2]
    for i in range(len(data_v2)):
        if data_v2.isna().iloc[i][0] == True:
            data_v2.iloc[i][0] = data_v2.iloc[i-1][0]
    data_v2 = data_v2.dropna(how='any')
    # date, LOT를 분리 후 column 생성
    data_v2.columns = ['a', 's1s2']
    data_v2['DATE'] = data_v2.a.str.split('\n|    ').str[0]
    data_v2['LOT_v1'] = data_v2.a.str.split('\n|    ').str[1]
    data_v2 = data_v2.drop(['a'], axis=1)
    data_v1.reset_index(drop=True, inplace=True)
    data_v2.reset_index(drop=True, inplace=True)

    # 데이터 병합
    data = pd.concat([data_v2, data_v1], axis=1)
    data = data.dropna(how='any')
    data['Lens'] = lens
    data['Count'] = count
    return data

file_path = glob.glob(r'C:/Users/sihyun/Desktop/빅데이터 센터/세코닉스/data/SN084JA2 측정/SN084JA2 PV형상/**/*')
lens_list = ['L1', 'L2', 'L3', 'L4', 'L5', 'L6']

data_final = pd.DataFrame()
for i in file_path:
    c = i.split('\\')[-1].split(' ')[1]
    df_lens = pd.DataFrame()
    for j in lens_list:
        data = pd.read_excel(i, sheet_name=j, engine='openpyxl')
        df_lens = pd.concat([df_lens, PeaktoValley(data, j, c)])
    data_final = pd.concat([data_final, df_lens])

data_final['LOT_v1'] = data_final['LOT_v1'].str.lstrip()
data_final['LOT'] = data_final['LOT_v1'].str.split(' ').str[0]
data_final.drop('LOT_v1', axis=1, inplace=True)
data_final
