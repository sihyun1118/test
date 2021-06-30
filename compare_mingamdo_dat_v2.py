import pandas as pd
import glob
import numpy as np
from tools.mingamdo_info import mingamdo_parser, make_PD_PV_D0
from tools.mingamdo_preprocessing import mingamdo_design
from tools.dat_info import dat_pd_pv_d0
import scipy.spatial
from collections import Counter

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
df.to_csv('df.csv',index=False)

####################################### 민감도 설계 data 전처리 ############################################

file_path = glob.glob(r'C:/Users/sihyun/Desktop/빅데이터 센터/세코닉스/data/세코닉스 _렌즈 설계 민감도 DATA_V2/민감도_V2/Text/Thickness/*')

file_list = []
df_final = pd.DataFrame()
for i in file_path:
    data_sag, data_tan = mingamdo_parser(i)
    file_list.append(i.split('\\')[-1].split('_')[1] + '_' + i.split('\\')[-1].split('_')[3])
    df_final = pd.concat([df_final, make_PD_PV_D0(data_sag, data_tan)])
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
# Spacer만 가져오기
mingam_sp = df_final.iloc[36:,:]
mingam_sp.reset_index(drop=True, inplace=True)

mingam_pd = mingam_sp.iloc[:,0:8]
el = mingam_sp.iloc[:,16:]

minus_df = pd.DataFrame()
for i in range(len(mingam_pd)):
    minus_df = pd.concat([minus_df, mingam_pd.iloc[i,:] - df])
minus_df.reset_index(drop=True, inplace=True)

spacer_list = ['SP1','SP2','SP3','SP4','SP5']
spacervalue_list = ['-2','-4','-6','+2','+4','+6']
change_list = []
for i in spacer_list:
    for j in spacervalue_list:
        change_list.append(i+'_'+j)

caculated_df = pd.concat([minus_df, pd.DataFrame(change_list)], axis=1)
caculated_df.rename(columns={0:'change_value'},inplace=True)

# 답안지 만들기
answer_sheet = pd.DataFrame()
d = 6
c = 0
for i in range(len(caculated_df)):
    c+=1
    if c == 7:
        d += 6
        c = 1
    for j in range(d, len(caculated_df)):
        answer_sheet = pd.concat([answer_sheet, pd.DataFrame(caculated_df.iloc[i,:] + caculated_df.iloc[j,:]).T])
answer_sheet = pd.concat([answer_sheet, caculated_df])
answer_sheet.reset_index(drop=True, inplace=True)
answer_sheet.to_csv('answer_sheet_MP.csv',index=False)
#####################################################################################################################
answer_sheet = answer_sheet.iloc[360:,:]
answer_sheet.to_csv('answer_sheet_MP_1sp.csv' ,index=False)
#####################################################################################################################


dat_file = glob.glob('C:/Users/sihyun/Desktop/빅데이터 센터/세코닉스/data/DAT/SN084JA_SEKO_0609_0610_DAT/SN084JA_SEKO_TH_210610_N2_13#4 _8.8.8.8.8.8_8.1.8.8.8.12_24(4).26(6).26.26.465#6.36_315.180.315.180.270.315.dat')
dat_file = glob.glob('C:/Users/sihyun/Desktop/빅데이터 센터/세코닉스/data/DAT/SN084JA_21.06.17D_AI TEST 1.dat')


def solution(dat_file):
    # DAT 전처리
    DAT = dat_pd_pv_d0(dat_file)

    DAT.drop(['Result'],axis=1, inplace=True)
    # PD만 가져오기
    DAT_f = DAT.iloc[:,0:8]

    # 단위 맞추기
    # DAT_f = DAT_f.mul(1000)

    measurement_cal = pd.DataFrame()
    change_val = []

    for i in range(len(DAT_f)):
        # exe 2) Measurement i 별 차이를 볼 수 있음.

        for j in range(len(answer_sheet)):
            measurement_cal = pd.concat([measurement_cal, pd.DataFrame(DAT_f.iloc[i,:]).T - answer_sheet.iloc[j,:-1]])
        measurement_cal.reset_index(drop=True, inplace=True)
        # 각 measurement 별 0과의 거리
        ary = scipy.spatial.distance.cdist(measurement_cal, pd.DataFrame([0] * 8).T, metric='euclidean')
        ######
        result = answer_sheet.loc[answer_sheet.iloc[:, :-1][ary == np.sort(ary.reshape(1, -1))[0][0]].index]
        change_val.extend(list(result['change_value']))
        # exe 1)
        measurement_cal = pd.DataFrame()
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
    final['file_name'] = dat_file[0].split('\\')[-1]
    final = pd.concat([final, pd.DataFrame(change_list)], axis=1)
    final['file_name'] = dat_file[0].split('\\')[-1]
    final.columns = ['file_name','change_value']
    if len(final) == 3:
        final.index = [1,2,3]
    elif len(final) == 2:
        final.index = [1,2]
    else:
        final.index = [1]
    return final

# 검증 exe 1,2번 실행
# z = pd.concat([measurement_cal, answer_sheet['change_value'],pd.DataFrame(ary)], axis=1).sort_values(by=[0], axis=0)



dat_paths = glob.glob('C:/Users/sihyun/Desktop/빅데이터 센터/세코닉스/data/DAT/test/*.dat')
solution_df = pd.DataFrame()
for i in range(len(dat_paths)):
    dat_file = [dat_paths[i]]
    solution_df = pd.concat([solution_df, solution(dat_file)])

a = list(solution_df['change_value'])
first=[]
second=[]
for i in range(len(solution_df)):
    first.append(a[i][0:6])
    second.append(a[i][6:])
solution_df['First_change'] = first
solution_df['Second_change'] = second
solution_df.drop('change_value', axis=1, inplace=True)

solution_df.to_csv('solution_test_.csv')

########################################################## D0 spec fail ################################################

dat_paths = glob.glob('C:/Users/sihyun/Desktop/빅데이터 센터/세코닉스/data/DAT/SN084JA_SEKO_0611_DAT/SN084JA_SEKO_TH_210611_N2_13#4 _8.8.8.8.8.8_8.1.8.8.8.12_24(4).26(6).26.26.#6 465.36_315.180.315.180.270.315.dat')
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

fail_field = get_fail_field(dat)
compare_col = get_compare_col(fail_field)













####검증####검증####검증####검증####검증####검증####검증####검증####검증####검증####검증####검증####검증####검증####검증####검증####검증####검증####검증####검증####검증####검증
test = DAT_f
test_r = pd.DataFrame([2,3,4,4,4,5,3,-2])

sp2_m2sp5_p6 = test.add([2,3,4,4,4,5,3,-2])
sp3_p2 = test.add([-1,-1,0,0,0,0,1,-1])
sp3_m2 = test.add([1,0,0,-1,1,-1,-1,1])
sp3_m6 = test.add([3,2,1,-1,3,-1,-3,3])
a =sp2_m2sp5_p6.describe()

############################################## 거리 순위 & 거리 #######################################################################

dat_file = glob.glob('C:/Users/sihyun/Desktop/빅데이터 센터/세코닉스/data/DAT/SN084JA_SEKO_0612_DAT/SN084JA_SEKO_TH_210612_N2_13#2 _8.8.8.8.8.8_13.3.16.6.16.3_28(8).28(8).32.32.#5 465.26_315.180.90.180.180.270.dat')

test_answer_sheet = answer_sheet.iloc[360:,:]
measurement_cal = pd.DataFrame()
for j in range(len(test_answer_sheet)):
    measurement_cal = pd.concat([measurement_cal, pd.DataFrame(DAT_f.iloc[6, :]).T - test_answer_sheet.iloc[j, :-1]])
ary = scipy.spatial.distance.cdist(measurement_cal, pd.DataFrame([0] * 8).T, metric='euclidean')

a = pd.concat([pd.DataFrame(ary), test_answer_sheet['change_value']], axis=1)
b = a.sort_values(0)
b.reset_index(drop=True, inplace=True)
b[b['change_value'] == 'SP5_P2']

len(DAT_f)