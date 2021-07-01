from tools.mingamdo_info import mingamdo_parser, make_PD_PV_D0
import pandas as pd

def mingamdo_design(design):
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

    PD_Sag = pd.DataFrame(design_sag.idxmax(axis=1) * 1000)
    PD_Sag.reset_index(drop=True, inplace=True)
    PD_Tan = pd.DataFrame(design_tan.idxmax(axis=1) * 1000)
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
    y = ['0.2F', '0.4F', '0.6F', '0.8F']
    col_list = []

    for i in x:
        for j in y:
            col_list.append(i + '_' + j)
    df.columns = col_list
    return df

# def mingamdo(file_path):
#     # 민감도 data 전처리 후 병합
#
#     file_list = []
#     df_final = pd.DataFrame()
#     for i in file_path:
#         data_sag, data_tan = mingamdo_parser(i)
#         file_list.append(i.split('\\')[-1].split('_')[1] + '_' + i.split('\\')[-1].split('_')[3])
#         df_final = pd.concat([df_final, make_PD_PV_D0(data_sag, data_tan)])
#         # globals()[i.split('\\')[-1].split('.')[0]] = make_PD_PV_D0(data_sag, data_tan)
#     df_final.reset_index(drop=True, inplace=True)
#     df_final['change_value'] = file_list
#
#     value_list = []
#     for i in list(df_final['change_value']):
#         if 'p' in i:
#             value_list.append(i[-2])
#         else:
#             value_list.append('-' + i[-2])
#     value_list
#     df_final['value'] = value_list
#     df_final['value'] = df_final['value'].astype(int)
#     # correlation_df = df_final.corr()
#     # Euclidean Distance 가중치를 위한 indexing
#     df_final_num = df_final.iloc[:, :-2]
#
#     return df_final, df_final_num


dat_file = glob.glob('C:/Users/sihyun/Desktop/빅데이터 센터/세코닉스/data/DAT/SN084JA_SEKO_0601_DAT/SN084JA_SEKO_TH_210601_N2_13#2 _8.8.8.8.8.8_10.5.5.5.5.11_26(6).24(5).30.30.#5 465.30_0.180.180.90.0.90.dat')
def make_answer_sheet(dat_file):

    stock = pd.read_csv('spacer_stock.csv', index_col=0)
    spacer_list = ['SP1', 'SP2', 'SP3', 'SP4', 'SP5']
    spacervalue_list_int = [-2, -4, -6, 2, 4, 6]

    # stock.index[0]
    # DAT 파일명에서 괄호 없애기
    spacer_thi_list_v1 = dat_file[0].split(os.sep)[-1].split('_')[-2].split('.')
    spacer_thi_list_v2 = []
    for i in range(len(spacer_thi_list_v1)):
        if '(' in spacer_thi_list_v1[i]:
            temp = spacer_thi_list_v1[i].replace(spacer_thi_list_v1[i], spacer_thi_list_v1[i][:2])
            spacer_thi_list_v2.append(temp)
        else:
            spacer_thi_list_v2.append(spacer_thi_list_v1[i])
    sp_list = spacer_thi_list_v2.copy()
    del sp_list[4]
    # Spacer int로 type 변경
    for i in range(5):
        sp_list[i] = int(sp_list[i])

    true_sp_list_all =[]
    for i in range(len(sp_list)):
        check_stock = []
        # 각 Spacer에 조정값 더하고 빼기
        for j in range(len(spacervalue_list_int)):
            check_stock.append(sp_list[i] + spacervalue_list_int[j])
        # 각 조정값이 반영된 Spacer의 재고 확인
        true_sp_list = []
        for k in range(len(check_stock)):
            try:
                if stock.loc[spacer_list[i], str(check_stock[k])] != 0:
                    true_sp_list.append(spacervalue_list_int[k])
                else:
                    pass
            except:
                pass
        true_sp_list_all.append(true_sp_list)




########################################################################################################################


    sp1_list = []
    for i in range(len(check_stock)):
        try:
            if stock.loc[spacer_list[i], str(check_stock[i])] != 0:
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
check_stock
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

stock.loc['sp2', str(check_stock[1])] != 0