import pandas as pd
import numpy as np

sensivity = pd.read_csv('sensivity.csv', header=None)
# 0F, 0.2F, 0.4F, 0.6F, 0.8F
sensivity = sensivity.iloc[np.arange(0, 10, 2)]

# sag, tan 분리
sag = []
tan = []
for i in range(len(sensivity.columns)):
    if i % 2 == 0:
        sag.append(i)
    else:
        tan.append(i)
sensivity_sag = sensivity.iloc[:, sag]
sensivity_tan = sensivity.iloc[:, tan]
sensivity_sag.columns = list(np.round(np.linspace(-0.04, 0.04, num=81, endpoint=True), 3))
sensivity_tan.columns = list(np.round(np.arange(-0.04, 0.041, 0.001), 3))

PV_Sag = []
PV_Tan = []
for i in range(len(sensivity_sag)):
    PV_Sag.append(max(sensivity_sag.iloc[i]))
    PV_Tan.append(max(sensivity_tan.iloc[i]))


PD_Sag = pd.DataFrame(sensivity_sag.idxmax(axis=1))
PD_Tan = pd.DataFrame(sensivity_tan.idxmax(axis=1))
PV_Sag = pd.DataFrame(PV_Sag)
PV_Tan = pd.DataFrame(PV_Tan)
D0_Sag = sensivity_sag.iloc[:][0]
D0_Tan = sensivity_tan.iloc[:][0]

##################################################################

data = pd.read_csv('C:/Users/sihyun/Desktop/빅데이터 센터/세코닉스/data/세코닉스 _렌즈 설계 민감도 DATA_V2/민감도_V2/Text/Decenter/DEC_L1_peak_p0010_m.txt',sep='\t',header=None)
df = data[0:11]
df = df.iloc[np.arange(0, 10, 2)]
