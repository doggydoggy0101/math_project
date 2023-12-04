import numpy as np
import pandas as pd
from parameter import Paras

import os
os.system("python dataProcess.py")
os.system("python dataTrainTest.py")

train = pd.read_csv('data/math_score_train.csv')
train2 = pd.read_csv('data/math_score_train2.csv')
train = pd.concat([train, train2], axis=1)
train = train.iloc[:,:-1]

test = pd.read_csv('data/math_score_test.csv')
test2 = pd.read_csv('data/math_score_test2.csv')
test = pd.concat([test, test2], axis=1)
test = test.iloc[:,:-1]

paras = Paras()

output = paras.model(train)
paras.fit(output)

predict = paras.model(test)
paras.loss(predict)