import os
import pickle

import numpy as np
from sklearn import preprocessing
from sklearn.ensemble import IsolationForest

from dynamic.data_process import get_features

file_path_train = r"/home/luxiang/linux-80211n-csitool-supplementary/csi_data/sample/"
train_file_name = os.listdir(file_path_train)
data_train = []
for name in train_file_name:
    file_name = file_path_train + name
    data = np.loadtxt(file_name)
    temp = get_features(data)
    data_train.extend(temp)
data_train = np.reshape(data_train, (-1, 5))
data_train = np.array(data_train)
min_max_scale = preprocessing.MinMaxScaler()
data_train_minmax = min_max_scale.fit_transform(data_train)
n_train = len(data_train_minmax)
rng = np.random.RandomState(42)
clf = IsolationForest(n_estimators=1000, max_samples=n_train, random_state=rng, contamination=0.2).fit(
    data_train_minmax)

with open('/home/luxiang/linux-80211n-csitool-supplementary/csi_data/sample/model.pickle', 'wb') as fw:
    pickle.dump(clf, fw)

with open('/home/luxiang/linux-80211n-csitool-supplementary/csi_data/sample/scale.pickle', 'wb') as fw:
    pickle.dump(min_max_scale, fw)
