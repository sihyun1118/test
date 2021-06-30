import pandas as pd
import numpy as np

import datetime
f = open('log_test.txt', 'a')
now = datetime.datetime.now()
nowDate = now.strftime('%Y-%m-%d')
nowTime = now.strftime('%H:%M:%S')
nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
print(nowDatetime)  # 2021-04-19 12:11:32

f.write('Date : ' + nowDatetime)
f.close()