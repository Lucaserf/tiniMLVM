# given multiple models of the same type this funcion will compare them on:
# - type1: data distribution difference (can be done without labels)
# - type2: accuracy difference (needs labels)
from scipy.stats import ks_2samp
import numpy as np


def model_selection_data(new_data, reference_data):

    min_distance = (0, 1)

    for i, data in enumerate(reference_data):
        ks_stat = ks_2samp(new_data, data)
        ks_p_value = np.mean(ks_stat.pvalue)
        if ks_p_value < min_distance:
            min_distance = i, ks_p_value

    return min_distance[0]
