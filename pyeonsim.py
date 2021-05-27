import glob
import pandas as pd
import datetime
data = pd.read_excel('C:/Users/sihyun/Desktop/빅데이터 센터/세코닉스/data/SN084JA2 측정/SN084JA2 편심/SN084JA2 6차 L3 편심.xlsx',sheet_name='공정',engine='openpyxl')

# 편심 data preprocessing
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

# 폴더 내 전체 파일 전처리 후 DataFrame에 저장
data_final = pd.DataFrame()
file_path = glob.glob(r'C:/Users/sihyun/Desktop/빅데이터 센터/세코닉스/data/SN084JA2 측정/SN084JA2 편심/*')
for i in file_path:
    # 파일명에서 차수 정보 가져오기
    c = i.split('\\')[-1].split(' ')[1]
    # 파일명에서 렌즈 정보 가져오기
    lens = i.split('\\')[-1].split(' ')[2]
    data = pd.read_excel(i, sheet_name='공정', engine='openpyxl')
    data_final = pd.concat([data_final, pyeonsim(data, lens, c)])

data_final.reset_index(drop=True, inplace=True)
data_final['LOT_v1'] = data_final['LOT_v1'].str.lstrip()
data_final['LOT'] = data_final['LOT_v1'].str.split(' ').str[0]
data_final.drop('LOT_v1', axis=1, inplace=True)