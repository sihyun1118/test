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