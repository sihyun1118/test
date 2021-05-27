import pandas as pd
data = pd.read_excel('C:/Users/sihyun/Desktop/빅데이터 센터/세코닉스/data/SN084JA2 측정/SN084JA2 3,4,5월 외경공정.xlsx', sheet_name='6차', engine='openpyxl')

def OuterDiameter(data):
    data.dropna(how='all', inplace=True)
    ind=0
    df_final = pd.DataFrame()
    for i in range(6):
        data_v1 = data.iloc[ind:ind + 19].T
        data_v1.dropna(how='all', inplace=True)
        data_v1.columns = data_v1.iloc[0, :]
        # 파일명에서 렌즈와 차수정보 가져오기
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

count_list = ['6차', '8차', '9차', '10차', 'S1차']
data_final = pd.DataFrame()
for i in count_list:
    data = pd.read_excel('C:/Users/sihyun/Desktop/빅데이터 센터/세코닉스/data/SN084JA2 측정/SN084JA2 3,4,5월 외경공정.xlsx',
                         sheet_name=i, engine='openpyxl')
    df_count = OuterDiameter(data)
    data_final = pd.concat([data_final, df_count])

data_final.columns = ['LOT', 'DATE', 'CAV1', 'CAV2', 'CAV3', 'CAV4', 'CAV5', 'CAV6', 'CAV7', ' CAV8', ' CAV9', 'CAV10',
                    'CAV11', 'CAV12', 'CAV13', 'CAV14', 'CAV15', 'CAV16', 'Count', 'Lens']
data_final['LOT'] = data_final['LOT'].str.lstrip()
data_final.reset_index(drop=True, inplace=True)


# 날짜 처리
for i in range(len(data_final)):

    if len(data_final.loc[i, 'DATE'].split('/')[0]) == 1:
        f = str('0') + data_final['DATE'][i].split('/')[0]
    else:
        f = data_final.loc[i, 'DATE'].split('/')[0]
    if len(data_final.loc[i, 'DATE'].split('/')[1]) == 1:
        s = str('0') + data_final.loc[i, 'DATE'].split('/')[0]
    else:
        s = data_final.loc[i, 'DATE'].split('/')[1]
    data_final.loc[i, 'DATE'] = f + s


