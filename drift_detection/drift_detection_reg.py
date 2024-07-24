# distance calculation between two datasets with gzip compression

import numpy as np
import pandas as pd
import gzip
from scipy.stats import ks_2samp


df_ref = pd.read_csv("regression_test/reference.csv")
df_data = pd.read_csv("regression_test/data.csv")


# take out label
df_ref = df_ref.drop(columns=["y"]).values
df_data = df_data.drop(columns=["y"]).values

# print("compressing reference")
# ref_len = len(gzip.compress(df_ref.to_csv(index=False).encode()))

# print("compressing data")
# data_len = len(gzip.compress(df_data.to_csv(index=False).encode()))

# print("compressing joint data")
# joint_data_len = len(
#     gzip.compress(pd.concat([df_ref, df_data]).to_csv(index=False).encode())
# )

# ncd = (joint_data_len - min(ref_len, data_len)) / max(ref_len, data_len)


# print("NCD: ", ncd)


# calculate Kolmogorov-Smirnov distance
ks = ks_2samp(df_ref, df_ref)
print("KS: ", ks)
