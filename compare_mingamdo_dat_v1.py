import pandas as pd
import glob
import numpy as np
from tools.mingamdo_info import mingamdo_parser, make_PD_PV_D0
from tools.mingamdo_preprocessing import mingamdo_design
from tools.dat_info import dat_pd_pv_d0
import scipy.spatial
#################################    Design    ##############################################

design = pd.read_csv('C:/Users/sihyun/Desktop/빅데이터 센터/세코닉스/data/세코닉스 _렌즈 설계 민감도 DATA_V2/민감도_V2/Text/Design_peak_000.txt', sep='\t', header=None)

design = design.iloc[:11, :]
# 0F, 0.2F, 0.4F, 0.6F, 0.8F
design = design.iloc[np.arange(2, 10, 2)]
# sag, tan 분리
sag = []
tan = []
for i in range(len(design.columns)):
    if i % 2 == 0:
        sag.append(i)
    else:
        tan.append(i)
design_sag = design.iloc[:, sag]
design_tan = design.iloc[:, tan]
design_sag.columns = list(np.round(np.linspace(-0.04, 0.04, num=81, endpoint=True), 3))
design_tan.columns = list(np.round(np.arange(-0.04, 0.041, 0.001), 3))
design_sag = design_sag.astype(float)
design_tan = design_tan.astype(float)

PV_Sag = []
PV_Tan = []
for i in range(len(design_sag)):
    PV_Sag.append(max(design_sag.iloc[i]))
    PV_Tan.append(max(design_tan.iloc[i]))

PD_Sag = pd.DataFrame(design_sag.idxmax(axis=1)*1000)
PD_Sag.reset_index(drop=True, inplace=True)
PD_Tan = pd.DataFrame(design_tan.idxmax(axis=1)*1000)
PD_Tan.reset_index(drop=True, inplace=True)
PV_Sag = pd.DataFrame(PV_Sag)
PV_Sag = PV_Sag * 100
PV_Tan = pd.DataFrame(PV_Tan)
PV_Tan = PV_Tan * 100
D0_Sag = design_sag.iloc[:][0]
D0_Sag.reset_index(drop=True, inplace=True)
D0_Sag = D0_Sag * 100
D0_Tan = design_tan.iloc[:][0]
D0_Tan.reset_index(drop=True, inplace=True)
D0_Tan = D0_Tan * 100

df = pd.concat([PD_Sag, PD_Tan])
df = df.T
x = ['PD_Sag', 'PD_Tan']
y = ['0.2F','0.4F','0.6F','0.8F']
col_list = []

for i in x:
    for j in y:
        col_list.append(i+'_'+j)
df.columns = col_list
df

####################################### 민감도 설계 data 전처리 ############################################

file_path = glob.glob(r'C:/Users/sihyun/Desktop/빅데이터 센터/세코닉스/data/세코닉스 _렌즈 설계 민감도 DATA_V2/민감도_V2/Text/Thickness/*')

file_list = []
df_final = pd.DataFrame()
for i in file_path:
    data_sag, data_tan = mingamdo_parser(i)
    file_list.append(i.split('\\')[-1].split('_')[1] + '_' + i.split('\\')[-1].split('_')[3])
    df_final = pd.concat([df_final, make_PD_PV_D0(data_sag, data_tan)])
    # globals()[i.split('\\')[-1].split('.')[0]] = make_PD_PV_D0(data_sag, data_tan)
df_final.reset_index(drop=True, inplace=True)
df_final['change_value'] = file_list

value_list = []
for i in list(df_final['change_value']):
    if 'p' in i:
        value_list.append(i[-2])
    else:
        value_list.append('-' + i[-2])
value_list
df_final['value'] = value_list
df_final['value'] = df_final['value'].astype(int)

temp = df_final.iloc[:,0:8]
el = df_final.iloc[:,16:]
minus_df = pd.DataFrame()

for i in range(len(temp)):
    minus_df = pd.concat([minus_df, temp.iloc[i,:] - df])
minus_df.reset_index(drop=True, inplace=True)
mingamdo_df = pd.concat([minus_df, el], axis=1)

test_seconics = mingamdo_df.iloc[36:,:]
test_seconics.reset_index(drop=True, inplace=True)
test_seconics_num = test_seconics.iloc[:, :-2]
# 상관관계
# correlation_df = mingamdo_df.corr()
# Euclidean Distance 가중치를 위한 indexing
mingamdo_df_num = mingamdo_df.iloc[:, :-2]

################################################################### Start

# DAT 파일 전처리

dat_paths = glob.glob('C:/Users/sihyun/Desktop/빅데이터 센터/세코닉스/data/DAT_v1/**/*.dat')

output = pd.DataFrame()
for k in range(len(dat_paths)):
    dat_file = [dat_paths[k]]
    DAT = dat_pd_pv_d0(dat_file)
    DAT.drop(['Result'],axis=1, inplace=True)
    DAT_f = DAT.iloc[:,0:16]
# 유클리디안 거리비교
    rank_list = []
    # 10위까지의 거리 순위 출력
    for j in range(10):
        for i in range(len(DAT_f)):
            ary = scipy.spatial.distance.cdist(mingamdo_df.iloc[:, :-2], pd.DataFrame(DAT_f.iloc[i,:]).T, metric='euclidean')
            change_val = []
            result = mingamdo_df.loc[mingamdo_df_num[ary == np.sort(ary.reshape(1, -1))[0][j]].index]
            change_val.extend(list(result['change_value']))
        rank_list.append(max(set(change_val), key=change_val.count))
    rank_list = pd.DataFrame(rank_list)
    file_name = pd.DataFrame(dat_file)
    b = pd.concat([file_name, rank_list], axis=1)
    output = pd.concat([output, b])

output.to_csv('PD_D0_output.csv')
########################################################################################################################################################################################################






################################### Scaling ########################################


from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
mingamdo_df_s_num = scaler.fit_transform(mingamdo_df_num)
mingamdo_df_s_num = pd.DataFrame(mingamdo_df_s_num)
mingamdo_df_s_num.columns = mingamdo_df_num.columns
mingamdo_df_s = pd.concat([mingamdo_df_s_num, mingamdo_df['change_value']],axis=1)

DAT_f_s = scaler.fit_transform(DAT_f)
DAT_f_s = pd.DataFrame(DAT_f_s)
DAT_f_s.columns = DAT_f.columns

a = []
b = []
c = []

for i in range(len(DAT_f)):
    ary = scipy.spatial.distance.cdist(mingamdo_df_s.iloc[:, :-1], pd.DataFrame(DAT_f_s.iloc[i,:]).T, metric='euclidean')

    result_1 = mingamdo_df_s.loc[mingamdo_df_s[ary == ary.min()].index]
    result_2 = mingamdo_df_s.loc[mingamdo_df_s_num[ary == np.sort(ary.reshape(1, -1))[0][1]].index]
    result_3 = mingamdo_df_s.loc[mingamdo_df_s_num[ary == np.sort(ary.reshape(1, -1))[0][2]].index]
    a.extend(list(result_1['change_value']))
    b.extend(list(result_2['change_value']))
    c.extend(list(result_3['change_value']))

max(set(a), key=a.count)
max(set(b), key=b.count)
max(set(c), key=c.count)
# df_final.loc[df_final_num[ary==np.sort(ary.reshape(1,-1))[0][0]].index]
dict((i, a.count(i)) for i in a)
dict((i, b.count(i)) for i in b)
dict((i, c.count(i)) for i in c)







######################################## std 가중치 ################################################
# 표준편차
r=[]
for i in range(len(mingamdo_df.columns)-2):
    r.append(mingamdo_df.iloc[:, i].std())
r
# 수식 유클리디안 거리 가중치
# distance = []
# 가중치 설정
# w = [1]*16
# for i in range(len(r)):
#     r[i] = r[i]/10
w = r


a = []
b = []
c = []
arr = []
for j in range(len(DAT_f)):
    distance = []
    for i in range(len(mingamdo_df_s_num)):
        distance.extend(np.sqrt(np.power(np.subtract(pd.DataFrame(mingamdo_df_num.iloc[i, :]).T, pd.DataFrame(DAT_f.iloc[j, :]).T), 2).multiply(w).sum(axis=1)))
        dist = pd.DataFrame(distance)
    arr.append(dist.min())

arr = pd.DataFrame(arr)
arr == arr.min()
result_1 = mingamdo_df.loc[mingamdo_df[arr == arr.min()].index]
result_2 = mingamdo_df.loc[mingamdo_df_num[arr == np.sort(arr)[1]].index]
result_3 = mingamdo_df.loc[mingamdo_df_num[arr == np.sort(arr)[2]].index]
a.extend(list(result_1['change_value']))
b.extend(list(result_2['change_value']))
c.extend(list(result_3['change_value']))

max(set(a), key=a.count)
max(set(b), key=b.count)
max(set(c), key=c.count)



######################################## Feature Selection ################################################

mingamdo_df.columns
test_final = mingamdo_df_num[['PD_Sag_0.6F', 'PD_Sag_0.8F','PD_Tan_0.6F', 'PD_Tan_0.8F','D0_Sag_0.6F', 'D0_Sag_0.8F','D0_Tan_0.6F', 'D0_Tan_0.8F']]
test_dat = DAT_f[['PD_Sag_0.6F', 'PD_Sag_0.8F','PD_Tan_0.6F', 'PD_Tan_0.8F','D0_Sag_0.6F', 'D0_Sag_0.8F','D0_Tan_0.6F', 'D0_Tan_0.8F']]

a = []
b = []
c = []

for i in range(len(DAT_f)):
    ary = scipy.spatial.distance.cdist(test_final.iloc[:, :], pd.DataFrame(test_dat.iloc[i,:]).T, metric='euclidean')

    result_1 = mingamdo_df.loc[test_final[ary == ary.min()].index]
    result_2 = mingamdo_df.loc[test_final[ary == np.sort(ary.reshape(1, -1))[0][1]].index]
    result_3 = mingamdo_df.loc[test_final[ary == np.sort(ary.reshape(1, -1))[0][2]].index]
    a.extend(list(result_1['change_value']))
    b.extend(list(result_2['change_value']))
    c.extend(list(result_3['change_value']))

max(set(a), key=a.count)
max(set(b), key=b.count)
max(set(c), key=c.count)
# df_final.loc[df_final_num[ary==np.sort(ary.reshape(1,-1))[0][0]].index]
dict((i, a.count(i)) for i in a)
dict((i, b.count(i)) for i in b)
dict((i, c.count(i)) for i in c)






####################################### D0 SPEC 고려 ################################################
dat_paths = glob.glob('C:/Users/sihyun/Desktop/빅데이터 센터/세코닉스/data/DAT_v1/0526/SN084JA_SEKO_TH_210526_N12_3#2 1_6.6.6.6.10.10_3.3.3.3.2.3_28.28.26.24.#6 466.32_90.270.0.270.180.0.dat')
dat = dat_pd_pv_d0(dat_paths)
def get_fail_field(dat):
    D0_col = ['Result', 'S2', 'T2', 'S3', 'T3',
              'S4', 'T4', 'S5', 'T5', 'S6', 'T6', 'S7', 'T7', 'S8', 'T8', 'S9', 'T9',
              'S10', 'T10', 'S11', 'T11', 'S12', 'T12', 'S13', 'T13', 'S14', 'T14',
              'S15', 'T15', 'S16', 'T16', 'S17', 'T17']
    field_cam = {
        '2': ['10', '11', '12', '13'],
        '4': ['14', '15', '16', '17'],
        '6': ['2', '3', '4', '5'],
        '8': ['6', '7', '8', '9']
    }
    spec = [44] * 8 + [34] * 16 + [49] * 8

    dat_D0 = dat[D0_col]
    spec_fail = dat_D0[dat_D0['Result'] == 0].drop(['Result'], axis=1)

    fail_cam = []
    # spec_fail

    for i, value in spec_fail.iterrows():
        fail = np.less(value, spec)
        idx = [i for i, x in enumerate(fail) if x]
        print(i, idx)
        fail_cam.append(spec_fail.columns[idx][0])
    fail_cam = list(dict.fromkeys(fail_cam))  # 중복제거

    fail_field = []
    for i in range(0, len(fail_cam)):
        for key, val in field_cam.items():
            if any(x in fail_cam[i] for x in val):
                fail_field.append(fail_cam[i][0] + key)
                break
    fail_field = list(dict.fromkeys(fail_field))  # 중복제거

    return fail_field


def get_compare_col(fail_list):
    compare_col = []
    if 'S10' in fail_list or 'S11' in fail_list or 'S12' in fail_list or 'S13' in fail_list:
        compare_col.extend(['PD_Sag_0.2F', 'D0_Sag_0.2F'])
    elif 'S14' in fail_list or 'S15' in fail_list or 'S16' in fail_list or 'S17' in fail_list:
        compare_col.extend(['PD_Sag_0.4F', 'D0_Sag_0.4F'])
    elif 'S2' in fail_list or 'S3' in fail_list or 'S4' in fail_list or 'S5' in fail_list:
        compare_col.extend(['PD_Sag_0.6F', 'D0_Sag_0.6F'])
    elif 'S6' in fail_list or 'S7' in fail_list or 'S8' in fail_list or 'S9' in fail_list:
        compare_col.extend(['PD_Sag_0.8F', 'D0_Sag_0.8F'])

    if 'T10' in fail_list or 'T11' in fail_list or 'T12' in fail_list or 'T13' in fail_list:
        compare_col.extend(['PD_Tan_0.2F', 'D0_Tan_0.2F'])
    elif 'T14' in fail_list or 'T15' in fail_list or 'T16' in fail_list or 'T17' in fail_list:
        compare_col.extend(['PD_Tan_0.4F', 'D0_Tan_0.4F'])
    elif 'T2' in fail_list or 'T3' in fail_list or 'T4' in fail_list or 'T5' in fail_list:
        compare_col.extend(['PD_Tan_0.6F', 'D0_Tan_0.6F'])
    elif 'T6' in fail_list or 'T7' in fail_list or 'T8' in fail_list or 'T9' in fail_list:
        compare_col.extend(['PD_Tan_0.8F', 'D0_Tan_0.8F'])
    return compare_col


dat_paths = glob.glob('C:/Users/sihyun/Desktop/빅데이터 센터/세코닉스/data/DAT_v1/**/*.dat')
DAT = dat_pd_pv_d0(dat_paths)

output_v1 = pd.DataFrame()
for k in range(12):
    dat_file = [dat_paths[k]]
    DAT = dat_pd_pv_d0(dat_file)
    fail_list = get_fail_field(DAT)
    compare_col_list = get_compare_col(fail_list)

    mingamdo_df_ss_num = mingamdo_df[compare_col_list]
    mingamdo_df_ss = pd.concat([mingamdo_df_ss_num, mingamdo_df['change_value']], axis=1)
    DAT_f_ss = DAT[compare_col_list]

# 유클리디안 거리비교
    rank_list = []
    # 10위까지의 거리 순위 출력
    for j in range(10):
        for i in range(len(DAT_f_ss)):
            ary = scipy.spatial.distance.cdist(mingamdo_df_ss_num.iloc[:, :], pd.DataFrame(DAT_f_ss.iloc[i,:]).T, metric='euclidean')
            change_val = []
            result = mingamdo_df.loc[mingamdo_df_ss_num[ary == np.sort(ary.reshape(1, -1))[0][j]].index]
            change_val.extend(list(result['change_value']))
        rank_list.append(max(set(change_val), key=change_val.count))
    rank_list = pd.DataFrame(rank_list)
    file_name = pd.DataFrame(dat_file)
    b = pd.concat([file_name, rank_list], axis=1)
    output_v1 = pd.concat([output_v1, b])

output_v1.to_csv('D0_spec_output.csv')


############################test##################################

############################spacer만 고려##################################
output_v1 = pd.DataFrame()
for k in range(len(dat_paths)):
    dat_file = [dat_paths[k]]
    DAT = dat_pd_pv_d0(dat_file)
    fail_list = get_fail_field(DAT)
    compare_col_list = get_compare_col(fail_list)

    mingamdo_df_ss_num = test_seconics_num[compare_col_list]
    mingamdo_df_ss = pd.concat([mingamdo_df_ss_num, test_seconics['change_value']], axis=1)
    DAT_f_ss = DAT[compare_col_list]

    # 유클리디안 거리비교
    rank_list = []
    # 10위까지의 거리 순위 출력
    for j in range(10):
        for i in range(len(DAT_f_ss)):
            ary = scipy.spatial.distance.cdist(mingamdo_df_ss_num.iloc[:, :], pd.DataFrame(DAT_f_ss.iloc[i, :]).T,
                                               metric='euclidean')
            change_val = []
            result = mingamdo_df.loc[mingamdo_df_ss_num[ary == np.sort(ary.reshape(1, -1))[0][j]].index]
            change_val.extend(list(result['change_value']))
        rank_list.append(max(set(change_val), key=change_val.count))
    rank_list = pd.DataFrame(rank_list)
    file_name = pd.DataFrame(dat_file)
    b = pd.concat([file_name, rank_list], axis=1)
    output_v1 = pd.concat([output_v1, b])

output_v1.to_csv('D0_spec_output.csv')
############################test##################################
mingamdo_df_ss_num = test_seconics_num[compare_col_list]
mingamdo_df_ss = pd.concat([mingamdo_df_ss_num, test_seconics['change_value']], axis=1)
############################test##################################


# 유클리디안 거리비교
a = []
b = []
c = []

import scipy.spatial
for i in range(len(DAT_f_ss)):
    ary = scipy.spatial.distance.cdist(mingamdo_df_ss.iloc[:, :-1], pd.DataFrame(DAT_f_ss.iloc[i,:]).T, metric='euclidean')

    result_1 = mingamdo_df_ss.loc[mingamdo_df_ss[ary == ary.min()].index]
    result_2 = mingamdo_df_ss.loc[mingamdo_df_ss_num[ary == np.sort(ary.reshape(1, -1))[0][1]].index]
    result_3 = mingamdo_df_ss.loc[mingamdo_df_ss_num[ary == np.sort(ary.reshape(1, -1))[0][2]].index]
    a.extend(list(result_1['change_value']))
    b.extend(list(result_2['change_value']))
    c.extend(list(result_3['change_value']))

max(set(a), key=a.count)
max(set(b), key=b.count)
max(set(c), key=c.count)
# df_final.loc[df_final_num[ary==np.sort(ary.reshape(1,-1))[0][0]].index]
dict((i, a.count(i)) for i in a)
dict((i, b.count(i)) for i in b)
dict((i, c.count(i)) for i in c)

