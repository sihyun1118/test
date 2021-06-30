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

paths = glob('C:/Users/sihyun/Desktop/빅데이터 센터/세코닉스/data/세코닉스 _렌즈 설계 민감도 DATA_V2/민감도_V2/Text/**/*.txt')
M = mingamdo_summarize.summarize_mingamdo(paths)
DEC = M[0]
THI = M[1]

dat_paths = glob('C:/Users/sihyun/Desktop/빅데이터 센터/세코닉스/data/개선 전후 초판 DAT/SN084JA_21.04.17.D_N4-12.12.12.12.8.12-A2_before(SP5-2 28)_43.3%.dat')
# dat_title = data_titles(dat_paths)
dat_spec = []
dat_measurement = []
dat_feature = []
for i, path in enumerate(dat_paths) :
    dat_content = dat_convert.DatToPan(path)
    temp_mesure = dat_content.dat_measurement()

    dat_spec.append(dat_content.dat_spec())
    dat_measurement.append(temp_mesure)
    dat_feature.append(generator.get_dat_feature(temp_mesure))

    del dat_content, temp_mesure

dat = dat_feature[0]
dat = dat.drop('Result',axis=1)

dat.columns = ['S_PD_6','T_PD_6','S_PS_6','T_PS_6','S_PD_8','T_PD_8','S_PS_8','T_PS_8','S_PD_2','T_PD_2','S_PS_2','T_PS_2','S_PD_4','T_PD_4','S_PS_4','T_PS_4']

pd_cols = [col for col in dat.columns if 'PD' in col]
ps_cols = [col for col in dat.columns if 'PS' in col]

dat = dat.dropna().reset_index(drop=True)
dat_pd = dat[pd_cols]
dat_pd = dat_pd[THI.columns[4:]] #column 순서 변경
design_pd = mingamdo_summarize.cal_design_pd(dat_pd.shape[0])
design_pd.columns = dat_pd.columns
dat_pd_r = dat_pd.subtract(design_pd,axis=1)
THI

solution_idx = []
for idx, row in dat_pd_r.iterrows():
    print(row)

    tmp1 = pd.DataFrame([row] * THI.shape[0], columns=dat_pd_r.columns).reset_index(drop=True)
    tmp2 = THI.iloc[:, 4:]

    arr = np.where(tmp1.multiply(tmp2) > 0, 1, 0)
    arr = [sum(l) for l in arr]
    tmp2['score_sign'] = arr
    print(tmp2.tail(10))

    tmp3 = tmp2[tmp2['score_sign'] == tmp2['score_sign'].max()]
    #     print(tmp3)
    ary = scipy.spatial.distance.cdist(tmp3.iloc[:, :-1], dat_pd_r.loc[[idx]], metric='euclidean')
    solution_idx.append(tmp3[ary == ary.min()].index[0])

solution_idx

sol = max(set(solution_idx), key=solution_idx.count)

THI.loc[[sol]]