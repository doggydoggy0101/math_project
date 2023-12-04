import numpy as np
import pandas as pd

class Paras:
    def __init__(self):

        ### parameters from SAS
        self.label = ["interest", "favor", "extras"]
        self.betas = [8.70888, -3.45130, 3.10016]
        self.beta0 = 57.32719

        self.num = len(self.label)

    def model(self, data):

        df = pd.DataFrame()
        df["label"] = data["score"]
        df["y_hat"] = data["score"]*0 + self.beta0

        for i in range(self.num):
            df["y_hat"] += self.betas[i]*data[self.label[i]]

        return df

    def fit(self, df):
        print("fitting...")

        dof = df.shape[0] - self.num - 1
        print("    DoF:", dof)

        sse_df = (df["label"] - df["y_hat"])**2
        sse = sse_df.sum()
        print("    sum of square error:", np.round(sse,3))

        mse = sse/dof
        print("    mean square error:",np.round(mse,5), "\n")

    def loss(self, df):
        print("evaluating...")

        sse_df = (df["label"] - df["y_hat"])**2
        sse = sse_df.sum()

        mse = sse/df.shape[0]
        print("    mean square loss:",np.round(mse,5), "\n")