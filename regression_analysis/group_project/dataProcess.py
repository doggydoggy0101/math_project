import numpy as np
import pandas as pd

class dataProcess:
    def __init__(self):
      
        self.label = {"old":["目前幾年級", "生理性別", "對數學的喜好程度", "對數學老師的喜好程度", 
                             "自認國文「閱讀理解」程度", "有無耐心閱讀數學題目", "平均每週額外補數學的時間（家教或去補習班）",
                             "平均每週花多少時間做以下事項\n（e.g.剛好2小時請選「2~3 小時」） [讀數學（含練習題目、整理筆記）]",
                             "平均每週花多少時間做以下事項\n（e.g.剛好2小時請選「2~3 小時」） [練習課外數學題（補習、家教作業皆算）]",
                             "平均每週花多少時間做以下事項\n（e.g.剛好2小時請選「2~3 小時」） [社團活動（處理社團相關事務）]",
                             "平均每日睡眠時間\n（e.g.剛好3小時請選「3~5小時」）", "平均每日通勤時長：上學＋放學\n（若有補習也要加上補習的通勤）",
                             "數學成績"],
                      "new":["grade", "gender", "interest", "favor",
                             "chinese", "patience", "extras",
                             "study_hours", "work_hours", "club_hours", "sleep_hours", "commute_hours",
                             "score"]}
        self.len = len(self.label["old"])

    def check(self, x):
        if x is None: 
            return False
        try:
            float(x)
            return True
        except:
            return False

    def grade(self, x): # 高一=0, 高二 / 高三=1
       return 0 if x == "高一（請以高一上學期第一次段考的成績及狀況回答表單）" else 1 

    def gender(self, x): # 生理女=0, 生理男=1
       return 0 if x == "生理女" else 1 

    def extras(self, x):
        if self.check(x[:3]):
            return np.float64(x[:3])
        elif self.check(x[0]):
            return np.float64(x[0])
        else: 
            raise ValueError('error')

    def hours(self, x):
        if self.check(x[2]):
            return (np.float64(x[0])+np.float64(x[2]))/2
        elif self.check(x[0]):
            return np.float64(x[0]) 
        else: 
            raise ValueError('error')    

    def hours_interval(self, x):
        if self.check(x[2]):
            return x[:3]
        elif self.check(x[0]):
            return x[0] 
        else: 
            raise ValueError('error')    


raw_df = pd.read_csv('data/math_score_raw.csv')

### seperate line 27
raw_df = raw_df.drop(27)


df = pd.DataFrame()
process = dataProcess()

for i in range(process.len):
    df[process.label["new"][i]] = raw_df[process.label["old"][i]]
df["grade"] = df["grade"].apply(lambda x: process.grade(x))
df["gender"] = df["gender"].apply(lambda x: process.gender(x))
df["extras"] = df["extras"].apply(lambda x: process.extras(x))
for labels in process.label["new"][7:12]:
    df[labels] = df[labels].apply(lambda x: process.hours_interval(x))

df.to_csv("data/math_score_plot.csv", encoding='utf-8', index=False)


df = pd.DataFrame()
process = dataProcess()

for i in range(process.len):
    df[process.label["new"][i]] = raw_df[process.label["old"][i]]
df["grade"] = df["grade"].apply(lambda x: process.grade(x))
df["gender"] = df["gender"].apply(lambda x: process.gender(x))
df["extras"] = df["extras"].apply(lambda x: process.extras(x))
for labels in process.label["new"][7:12]:
    df[labels] = df[labels].apply(lambda x: process.hours(x))

# df.head(10)

df.to_csv("data/math_score.csv", encoding='utf-8', index=False)