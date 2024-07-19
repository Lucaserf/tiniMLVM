# distance calculation between two datasets with gzip compression

import numpy as np
import pandas as pd
import gzip


def calculate_distance(data1, data2):
    return np.linalg.norm(data1 - data2)


df_ref = pd.read_csv("regression_test/reference.csv")
df_data = pd.read_csv("regression_test/reference.csv")

# take out label
df_ref = df_ref.drop(columns=["label"])
df_data = df_data.drop(columns=["label"])

print("compressing reference")
ref_len = len(gzip.compress(df_ref.to_csv(index=False).encode()))

print("compressing data")
data_len = len(gzip.compress(df_data.to_csv(index=False).encode()))

print("compressing joint data")
joint_data_len = len(
    gzip.compress(pd.concat([df_ref, df_data]).to_csv(index=False).encode())
)

ncd = (joint_data_len - min(ref_len, data_len)) / max(ref_len, data_len)


print("NCD: ", ncd)
