from numpy import std
import numpy as np
import pandas as pd


def detect(s):
    if s[-1] != 0 and std(s) > 280:
        return 1
    else:
        return 0


def identify(s):
    f = get_features(s)


def get_features(s):
    ss = pd.Series(s)
    features = np.zeros((5, 1))
    features[0] = np.max(s)
    features[1] = np.mean(s)
    features[2] = ss.skew()
    features[3] = ss.kurt()
    features[4] = ss.std()
    return features
