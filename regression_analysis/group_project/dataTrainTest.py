import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

rng = 42

data = pd.read_csv('data/math_score.csv')

train, test = train_test_split(data, test_size=0.2, random_state=rng)

print("num of train:", train.shape[0])
print("num of test:", test.shape[0])

train.to_csv("data/math_score_train.csv", encoding='utf-8', index=False)
test.to_csv("data/math_score_test.csv", encoding='utf-8', index=False)