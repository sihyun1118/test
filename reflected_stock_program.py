import pandas as pd

def make_answer_sheet(dat_file):
    stock = pd.read_csv('spacer_stock.csv', index_col=0)

    spacervalue_list_int = [-2, -4, -6, 2, 4, 6]

    stock.index[0]

    spacer_thi_list_v1 = dat_file[0].split(os.sep)[-1].split('_')[-2].split('.')
    spacer_thi_list_v2 = []
    for i in range(len(spacer_thi_list_v1)):
        if '(' in spacer_thi_list_v1[i]:
            temp = spacer_thi_list_v1[i].replace(spacer_thi_list_v1[i], spacer_thi_list_v1[i][:2])
            spacer_thi_list_v2.append(temp)
        else:
            spacer_thi_list_v2.append(spacer_thi_list_v1[i])
    for i in range(4):
        spacer_thi_list_v2[i] = int(spacer_thi_list_v2[i])
    spacer_thi_list_v2[-1] = int(spacer_thi_list_v2[-1])
    spacer_thi_list_v2

    for i in range(len(spacer_thi_list_v2)):
        check_stock = []
        for j in range(len(spacervalue_list_int)):
            check_stock.append(spacer_thi_list_v2[0] + spacervalue_list_int[j])

    sp1_list = []
    for i in range(len(check_stock)):
        try:
            if stock.loc['sp1', str(check_stock[i])] != 0:
                sp1_list.append(spacervalue_list_int[i])
            else:
                pass
        except:
            pass

    sp2_list = []
    for i in range(len(check_stock)):
        try:
            if stock.loc['sp2', str(check_stock[i])] != 0:
                sp2_list.append(spacervalue_list_int[i])
            else:
                pass
        except:
            pass

    sp3_list = []
    for i in range(len(check_stock)):
        try:
            if stock.loc['sp3', str(check_stock[i])] != 0:
                sp3_list.append(spacervalue_list_int[i])
            else:
                pass
        except:
            pass

    sp4_list = []
    for i in range(len(check_stock)):
        try:
            if stock.loc['sp4', str(check_stock[i])] != 0:
                sp4_list.append(spacervalue_list_int[i])
            else:
                pass
        except:
            pass

    sp5_list = []
    for i in range(len(check_stock)):
        try:
            if stock.loc['sp5', str(check_stock[i])] != 0:
                sp5_list.append(spacervalue_list_int[i])
            else:
                pass
        except:
            pass

sp5_list




stock.loc['sp1',str(check_stock[5])]

spacer_list = ['SP1','SP2','SP3','SP4','SP5']
spacervalue_list = ['-2','-4','-6','+2','+4','+6']
change_list = []
for i in spacer_list:
    for j in spacervalue_list:
        change_list.append(i+'_'+j)
dat_file = glob.glob('C:/Users/sihyun/Desktop/빅데이터 센터/세코닉스/data/DAT/SN084JA_SEKO_0601_DAT/SN084JA_SEKO_TH_210601_N2_13#2 _8.8.8.8.8.8_10.5.5.5.5.11_26(6).24(5).30.30.#5 465.30_0.180.180.90.0.90.dat')

def solution(dat_file):
    # DAT 전처리
    # print('Start DAT preprocessing')
    # f.write('Start DAT preprocessing\n')
    DAT, measurement_count = dat_pd_pv_d0(dat_file)
    if sum(DAT['PD_Sag_0.2F']) == 0.0:
        final = pd.DataFrame([dat_file[0].split(os.sep)[-1],'PD X','PD X','PD X','PD X','PD X']).T
        final.columns = ['file_name', 'First_change', 'Second_change', 'spacer', 'yield', 'PD_rate']

    else:
        pd_rate = len(DAT['PD_Sag_0.2F']!=0.0)/measurement_count*100
        result_count = len(DAT[DAT['Result'] == 1])
        DAT.drop(['Result'], axis=1, inplace=True)
        # 수율 계산
        DAT_yield = result_count / measurement_count * 100
        # PD만 가져오기
        DAT_f = DAT.iloc[:,0:8]
        # 단위 맞추기
        # DAT_f = DAT_f.mul(1000)
        # print('get spacer combination')
        # f.write('get spacer combination\n')
        spacer_thi_list_v1 = dat_file[0].split(os.sep)[-1].split('_')[-2].split('.')
        spacer_thi_list_v2 = []
        for i in range(len(spacer_thi_list_v1)):
            if '(' in spacer_thi_list_v1[i]:
                temp = spacer_thi_list_v1[i].replace(spacer_thi_list_v1[i], spacer_thi_list_v1[i][:2])
                spacer_thi_list_v2.append(temp)
            else:
                spacer_thi_list_v2.append(spacer_thi_list_v1[i])
















        measurement_cal = pd.DataFrame()
        change_val = []
        # 거리계산
        # print('calculate distance')
        # f.write('calculate distance\n')
        for i in range(len(DAT_f)):
            for j in range(len(answer_sheet)):
                measurement_cal = pd.concat([measurement_cal, pd.DataFrame(DAT_f.iloc[i,:]).T + answer_sheet.iloc[j,:-1]])
            measurement_cal.reset_index(drop=True, inplace=True)
            # 각 measurement 별 0과의 거리
            ary = scipy.spatial.distance.cdist(measurement_cal, pd.DataFrame([0] * 8).T, metric='euclidean')
            result = answer_sheet.loc[answer_sheet.iloc[:, :-1][ary == np.sort(ary.reshape(1, -1))[0][0]].index]
            change_val.extend(list(result['change_value']))
            measurement_cal = pd.DataFrame()
        # f.write('solve answer count\n')
        change_list=[]
        r = Counter(change_val)
        if len(r) >= 3:
            for i in range(3):
                change_list.append(sorted(r.items(), key=lambda x: x[1], reverse=True)[i][0])
        elif len(r) == 2:
            for i in range(2):
                change_list.append(sorted(r.items(), key=lambda x: x[1], reverse=True)[i][0])
        else:
            for i in range(1):
                change_list.append(sorted(r.items(), key=lambda x: x[1], reverse=True)[i][0])
        final= pd.DataFrame()
        final['file_name'] = dat_file[0].split(os.sep)[-1]
        final = pd.concat([final, pd.DataFrame(change_list)], axis=1)
        final['file_name'] = dat_file[0].split(os.sep)[-1]
        final.columns = ['file_name', 'change_value']
        # 순위 지정
        if len(final) == 3:
            final.index = [1,2,3]
        elif len(final) == 2:
            final.index = [1,2]
        else:
            final.index = [1]
        a = list(final['change_value'])
        first = []
        second = []
        for i in range(len(final)):
            first.append(a[i][0:6])
            second.append(a[i][6:])
        final['First_change'] = first
        final['Second_change'] = second
        final.drop('change_value', axis=1, inplace=True)
        # print('get answer spacer combination')
        # f.write('get answer spacer combination\n')
        spacer_change = []
        for i in range(len(final)):
            spacer_thi_list_v3 = spacer_thi_list_v2.copy()
            if 'SP1_+' in final.iloc[i,1]:
                spacer_thi_list_v3[0] = int(spacer_thi_list_v3[0]) + int(final.iloc[i, 1][5])
            elif 'SP1_-' in final.iloc[i,1]:
                spacer_thi_list_v3[0] = int(spacer_thi_list_v3[0]) - int(final.iloc[i, 1][5])
            elif 'SP2_+' in final.iloc[i,1]:
                spacer_thi_list_v3[1] = int(spacer_thi_list_v3[1]) + int(final.iloc[i, 1][5])
            elif 'SP2_-' in final.iloc[i,1]:
                spacer_thi_list_v3[1] = int(spacer_thi_list_v3[1]) - int(final.iloc[i, 1][5])
            elif 'SP3_+' in final.iloc[i, 1]:
                spacer_thi_list_v3[2] = int(spacer_thi_list_v3[2]) + int(final.iloc[i, 1][5])
            elif 'SP3_-' in final.iloc[i, 1]:
                spacer_thi_list_v3[2] = int(spacer_thi_list_v3[2]) - int(final.iloc[i, 1][5])
            elif 'SP4_+' in final.iloc[i, 1]:
                spacer_thi_list_v3[3] = int(spacer_thi_list_v3[3]) + int(final.iloc[i, 1][5])
            elif 'SP4_-' in final.iloc[i, 1]:
                spacer_thi_list_v3[3] = int(spacer_thi_list_v3[3]) - int(final.iloc[i, 1][5])
            elif 'SP5_+' in final.iloc[i, 1]:
                spacer_thi_list_v3[5] = int(spacer_thi_list_v3[5]) + int(final.iloc[i, 1][5])
            elif 'SP5_-' in final.iloc[i, 1]:
                spacer_thi_list_v3[5] = int(spacer_thi_list_v3[5]) - int(final.iloc[i, 1][5])

            if 'SP1_+' in final.iloc[i,2]:
                spacer_thi_list_v3[0] = int(spacer_thi_list_v3[0]) + int(final.iloc[i, 2][5])
            elif 'SP1_-' in final.iloc[i,2]:
                spacer_thi_list_v3[0] = int(spacer_thi_list_v3[0]) - int(final.iloc[i, 2][5])
            elif 'SP2_+' in final.iloc[i,2]:
                spacer_thi_list_v3[1] = int(spacer_thi_list_v3[1]) + int(final.iloc[i, 2][5])
            elif 'SP2_-' in final.iloc[i,2]:
                spacer_thi_list_v3[1] = int(spacer_thi_list_v3[1]) - int(final.iloc[i, 2][5])
            elif 'SP3_+' in final.iloc[i, 2]:
                spacer_thi_list_v3[2] = int(spacer_thi_list_v3[2]) + int(final.iloc[i, 2][5])
            elif 'SP3_-' in final.iloc[i, 2]:
                spacer_thi_list_v3[2] = int(spacer_thi_list_v3[2]) - int(final.iloc[i, 2][5])
            elif 'SP4_+' in final.iloc[i, 2]:
                spacer_thi_list_v3[3] = int(spacer_thi_list_v3[3]) + int(final.iloc[i, 2][5])
            elif 'SP4_-' in final.iloc[i, 2]:
                spacer_thi_list_v3[3] = int(spacer_thi_list_v3[3]) - int(final.iloc[i, 2][5])
            elif 'SP5_+' in final.iloc[i, 2]:
                spacer_thi_list_v3[5] = int(spacer_thi_list_v3[5]) + int(final.iloc[i, 2][5])
            elif 'SP5_-' in final.iloc[i, 2]:
                spacer_thi_list_v3[5] = int(spacer_thi_list_v3[5]) - int(final.iloc[i, 2][5])
            spacer_change.append(str(spacer_thi_list_v3[0])+'.'+str(spacer_thi_list_v3[1])+'.'+str(spacer_thi_list_v3[2])+'.'+str(spacer_thi_list_v3[3])+'.'+str(spacer_thi_list_v3[4]+'.'+str(spacer_thi_list_v3[5])))

        final['spacer'] = spacer_change
        final['yield'] = DAT_yield
        final['PD_rate'] = str(pd_rate)+'%'


    return final