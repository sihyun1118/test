import pandas as pd
from glob import glob
import sys, os
sys.path.append(os.path.abspath('..'))

from tools import dat_convert
from tools.dat_convert import data_titles
import tools.data_generator as generator
import numpy as np
from tools import mingamdo_summarize
import scipy.spatial
from statistics import NormalDist


mingamdo_movement = pd.read_csv('answer_sheet_MP_1sp.csv')
mingamdo_movement

def dat_pd_pv_d0(dat_paths):
    dat_spec = []
    dat_measurement = []
    dat_feature = []
    for i, path in enumerate(dat_paths[:15]):
        print(path)
        dat_content = dat_convert.DatToPan(path)
        temp_measure = dat_content.dat_measurement()

        dat_spec.append(dat_content.dat_spec())

        # clear defoucs 0.002
        temp_measure = generator.get_dat_clear(temp_measure, 0)
        #     temp_measure = generator.get_dat_clear(temp_measure, 1) # EFL clear

        dat_measurement.append(temp_measure)

        dat_feature.append(generator.get_dat_feature(temp_measure))

        del dat_content, temp_measure
        return dat_feature

def remove_outlier(dat_feature):
    for i in range(0, len(dat_feature)):
        # 0F peak >= 60
        dat_feature[i] = dat_feature[i][
            (dat_feature[i]['PV_S1'].astype(float) >= 60) & (dat_feature[i]['PV_T1'].astype(float) >= 60)]

        # min max 제거(20%,8F Tan)
        size = int(dat_feature[i].shape[0] * 0.20)
        head_idx = dat_feature[i]['PD_Tan(6,7,8,9)'].sort_values().head(size).index
        tail_idx = dat_feature[i]['PD_Tan(6,7,8,9)'].sort_values().tail(size).index
        dat_feature[i] = dat_feature[i].drop(head_idx)
        dat_feature[i] = dat_feature[i].drop(tail_idx)

        dat_feature[i] = dat_feature[i].reset_index(drop=True)

        dat_df = dat_feature[0]

        dat_df.dropna(how='any', inplace=True)
        dat_df.reset_index(drop=True, inplace=True)

        result = dat_df['Result']
        dat_df = dat_df.drop(['Result'], axis=1)

        sag = dat_df.iloc[:, ::2]
        sag.reset_index(drop=True, inplace=True)
        sag = sag.astype(float)
        tan = dat_df.iloc[:, 1::2]
        tan.reset_index(drop=True, inplace=True)
        tan = tan.astype(float)

        DAT_PD_SAG = sag.iloc[:, :8:2]
        DAT_PS_SAG = sag.iloc[:, 1:8:2]
        DAT_PD_SAG.columns = ['PD_Sag_0.6F', 'PD_Sag_0.8F', 'PD_Sag_0.2F', 'PD_Sag_0.4F']
        DAT_PD_SAG = DAT_PD_SAG[['PD_Sag_0.2F', 'PD_Sag_0.4F', 'PD_Sag_0.6F', 'PD_Sag_0.8F']]

        DAT_PD_TAN = tan.iloc[:, :8:2]
        DAT_PS_TAN = tan.iloc[:, 1:8:2]
        DAT_PD_TAN.columns = ['PD_Tan_0.6F', 'PD_Tan_0.8F', 'PD_Tan_0.2F', 'PD_Tan_0.4F']
        DAT_PD_TAN = DAT_PD_TAN[['PD_Tan_0.2F', 'PD_Tan_0.4F', 'PD_Tan_0.6F', 'PD_Tan_0.8F']]

        final_dat_df = pd.DataFrame()
        final_dat_df = pd.concat([DAT_PD_SAG, DAT_PD_TAN, result], axis=1)

        # final_dat_df['PV_Sag_0.2F'] = sag.iloc[:,34:38].mean(axis=1)
        # final_dat_df['PV_Sag_0.4F'] = sag.iloc[:,38:42].mean(axis=1)
        # final_dat_df['PV_Sag_0.6F'] = sag.iloc[:,26:30].mean(axis=1)
        # final_dat_df['PV_Sag_0.8F'] = sag.iloc[:,30:34].mean(axis=1)
        #
        # final_dat_df['PV_Tan_0.2F'] = tan.iloc[:,34:38].mean(axis=1)
        # final_dat_df['PV_Tan_0.4F'] = tan.iloc[:,38:42].mean(axis=1)
        # final_dat_df['PV_Tan_0.6F'] = tan.iloc[:,26:30].mean(axis=1)
        # final_dat_df['PV_Tan_0.8F'] = tan.iloc[:,30:34].mean(axis=1)

        final_dat_df['D0_Sag_0.2F'] = sag.iloc[:, 17:21].mean(axis=1)
        final_dat_df['D0_Sag_0.4F'] = sag.iloc[:, 21:25].mean(axis=1)
        final_dat_df['D0_Sag_0.6F'] = sag.iloc[:, 9:13].mean(axis=1)
        final_dat_df['D0_Sag_0.8F'] = sag.iloc[:, 13:17].mean(axis=1)

        final_dat_df['D0_Tan_0.2F'] = tan.iloc[:, 17:21].mean(axis=1)
        final_dat_df['D0_Tan_0.4F'] = tan.iloc[:, 21:25].mean(axis=1)
        final_dat_df['D0_Tan_0.6F'] = tan.iloc[:, 9:13].mean(axis=1)
        final_dat_df['D0_Tan_0.8F'] = tan.iloc[:, 13:17].mean(axis=1)
        final_dat_df = pd.concat([final_dat_df, sag.iloc[:, 9:25], tan.iloc[:, 9:25]], axis=1)

    return final_dat_df

dat_paths = glob('C:/Users/sihyun/Desktop/빅데이터 센터/세코닉스/data/개선 전후 DAT/개선 전후 초판 DAT/SN084JA_21.04.17.D_N4-12.12.12.12.8.12-A2_before(SP5-2 28)_43.3%.dat')
a = dat_pd_pv_d0(dat_paths)
before = remove_outlier(a)
before = before.iloc[:,:8]

dat_paths = glob('C:/Users/sihyun/Desktop/빅데이터 센터/세코닉스/data/개선 전후 DAT/개선 전후 초판 DAT/SN084JA_21.04.17.D_N4-12.12.12.12.8.12. (SP5-2 24) A2_after(SP5-2 24)_96.7%.dat')
a = dat_pd_pv_d0(dat_paths)
after = remove_outlier(a)
after = after.iloc[:,:8]
