data = pd.read_excel('C:/Users/sihyun/Desktop/빅데이터 센터/세코닉스/data/combination_table/084JA 조합표 05.15 오전.xlsx', sheet_name=1, engine='openpyxl')

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

test_df = combination_table(data)
test_df