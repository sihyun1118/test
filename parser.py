import pandas as pd
import numpy as np
import re
import glob
import datetime

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

def pyeonsim(data,lens,count):
    # 필요한 투과 정보만 selection
    data = data[['Unnamed: 0', 'Unnamed: 16']]
    data = data.dropna(how='all')
    data.reset_index(drop=True, inplace=True)
    # 투과 text 삭제
    drop_index = data[data.iloc[:, 1] == '투과'].index
    data = data.drop(index=drop_index)
    data.reset_index(drop=True, inplace=True)

    # 날짜 가져오기
    data_v1 = data.iloc[:, 0].dropna(how='all')
    data_v1.reset_index(drop=True, inplace=True)

    # 편심, LOT 가져오기
    i = 0
    data_v2 = []
    try:
        while type(data.iloc[i][1]) == type(0.0) or type(data.iloc[i][1]) == type('str'):
            data_v2.append(list(data.iloc[i:i+17, 1]))
            i += 17
    except:
        data_v2 = pd.DataFrame(data_v2)

    # Final DataFrame
    data = pd.concat([data_v1, data_v2], axis=1)
    data.columns = ['DATE', 'LOT_v1', 'CAV1', 'CAV2', 'CAV3', 'CAV4', 'CAV5', 'CAV6', 'CAV7', ' CAV8', ' CAV9', 'CAV10',
                    'CAV11', 'CAV12', 'CAV13', 'CAV14', 'CAV15', 'CAV16']
    # 날짜 변수 변환 (ex. 4월 25일 or 2021-04-25 -> 0425)
    for i in range(len(data)):
        try:
            d = data.iloc[i][0]
            data.loc[i, 'DATE'] = d[0:2]+d[3:5]
        except:
            d = data.iloc[i][0]
            date_string = d.strftime('%Y-%m-%d')
            data.loc[i, 'DATE'] = date_string[5:7] + date_string[8:10]
    data['Lens'] = lens
    data['Count'] = count
    return data

def OuterDiameter(data):
    data.dropna(how='all', inplace=True)
    ind = 0
    df_final = pd.DataFrame()
    for i in range(6):
        data_v1 = data.iloc[ind:ind + 19].T
        data_v1.dropna(how='all', inplace=True)
        data_v1.columns = data_v1.iloc[0, :]
        data_v1['Count'] = data_v1.iloc[0, 0].split(' ')[1]
        data_v1['Lens'] = data_v1.iloc[0, 0].split(' ')[2]

        data_v1 = data_v1.iloc[1:, 1:]
        data_v1.drop(index=data_v1[data_v1.iloc[:, 0] == '최대'].index, inplace=True)
        data_v1.drop(index=data_v1[data_v1.iloc[:, 0] == '최소'].index, inplace=True)
        data_v1.drop(index=data_v1[data_v1.iloc[:, 0] == '최대-최소'].index, inplace=True)
        data_v1.drop(index=data_v1[data_v1.iloc[:, 0] == '로트'].index, inplace=True)
        df_final = pd.concat([df_final, data_v1])
        ind += 19
    df_final.reset_index(drop=True, inplace=True)
    return df_final

def combination_table(data):
    # 데이터 자르기
    drop_index = []
    for i in range(len(data)):
        if data.isna().iloc[i][27] == True:
            drop_index.append(i)
    df = data.drop(data.index[drop_index])
    df = df.iloc[2:, 2:22]

    # 결측치 처리
    df.reset_index(drop=True, inplace=True)
    for i in range(1, len(df)):
        for j in range(len(df.columns)):
            if df.isna().iloc[i][j] == True:
                df.iloc[i][j] = df.iloc[i-1][j]

    # column명 지정
    df.columns = ['라인','차수_L1','차수_L2','차수_L3','차수_L4','차수_L5','차수_L6','LOT_L1','LOT_L2','LOT_L3','LOT_L4','LOT_L5','LOT_L6','CAV_L1','CAV_L2','CAV_L3','CAV_L4','CAV_L5','CAV_L6','BARREL']
    order_columns = ['차수_L1','차수_L2','차수_L3','차수_L4','차수_L5','차수_L6']
    combine_columns = ['CAV_L1','CAV_L2','CAV_L3','CAV_L4','CAV_L5','CAV_L6']
    LOT_columns = ['LOT_L1','LOT_L2','LOT_L3','LOT_L4','LOT_L5','LOT_L6']

    # CAV10 이상 문자 변경
    for i in range(len(df)):
        for j in combine_columns:
            if df[j][i] == 10:
                df[j][i] = 'A'
            elif df[j][i] == 11:
                df[j][i] = 'B'
            elif df[j][i] == 12:
                df[j][i] = 'C'
            elif df[j][i] == 13:
                df[j][i] = 'D'
            elif df[j][i] == 14:
                df[j][i] = 'E'
            elif df[j][i] == 15:
                df[j][i] = 'F'
            elif df[j][i] == 16:
                df[j][i] = 'G'

    # 차수 10이상 문자 변경 + S1 -> S로 변경
    for i in range(len(df)):
        for j in order_columns:
            if df[j][i] == 10:
                df[j][i] = 'A'
            elif df[j][i] == 11:
                df[j][i] = 'B'
            elif df[j][i] == 12:
                df[j][i] = 'C'
            elif df[j][i] == 13:
                df[j][i] = 'D'
            elif df[j][i] == 14:
                df[j][i] = 'E'
            elif df[j][i] == 15:
                df[j][i] = 'F'
            elif df[j][i] == 16:
                df[j][i] = 'G'
            elif df[j][i] == 'S1':
                df[j][i] = 'S'

    # 최종 조합표 DataFrame 확정
    df = df.astype(str)
    df_final = pd.DataFrame()
    df_final['make_line'] = df['라인']
    df_final['lens_order'] = df[order_columns].apply(''.join, axis=1)
    df_final['lens_combine'] = df[combine_columns].apply(''.join, axis=1)
    df_final['lens_LOT_num'] = df[LOT_columns].apply(''.join, axis=1)
    df_final['BARREL'] = df['BARREL']

    # 공백제거
    for i in df_final.columns:
        df_final[i] = df_final[i].str.lstrip()

    return df_final