# NN training and testing with scikit learn

import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

train_folder_fp = "C:\\Users\\david\\Documents\\David\\MSU\\CSC450\\ASL_landmarks\\train"
test_folder_fp = "C:\\Users\\david\\Documents\\David\\MSU\\CSC450\\ASL_landmarks\\test"
model_fp = "C:\\Users\\david\\Documents\\David\\MSU\\CSC450\\landmark_model_v7.h5"
test_fp = "C:\\Users\\david\\Documents\\David\\MSU\\CSC450\\new_test_dataset.csv"
train_fp = "C:\\Users\\david\\Documents\\David\\MSU\\CSC450\\new_train_dataset.csv"

train_df = pd.read_csv(train_fp)
print(train_df.iloc[:,1:])
print(train_df.iloc[:,0])

clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(64, 64), random_state=1)
clf.fit(train_df.iloc[:,1:], train_df.iloc[:,0])