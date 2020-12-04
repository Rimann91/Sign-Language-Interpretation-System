#    Copyright 2020 Braden Bagby, Robert Stonner, Riley Hughes, David Gray, Zachary Langford

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.


import os
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import pandas as pd
import re

print("TensorFlow version: {}".format(tf.__version__))
print("Eager execution: {}".format(tf.executing_eagerly()))

root = "/home/rms/Downloads/Dataset/Output"

df_file = "/home/rms/Downloads/Dataset/output.csv"

header = ""

for i in range(1, 22):
    header += str(i) + "x," + str(i) + "y," + str(i) + "z,"

header += "target\n"

output_file = open(df_file, "w")

output_file.write(header)

index = 0

char_dict = {}

for subdir, dirs, files in os.walk(root):
    for file in files:
        row = ""
        for line in open(os.path.join(subdir, file), 'r').readlines():
            row += line.replace("\n", "") + ","
        output_file.write(row)
        char = (re.findall(r'^[A-Za-z^(csv)]+', file)[0])
        if char not in char_dict:
            char_dict[char] = index
            index += 1
        output_file.write(str(char_dict[char]) + "\n")

output_file.close()

df = pd.read_csv(df_file)

tf.keras.backend.set_floatx('float64')

# Load dataset.
dftrain = df.loc[0:50000]
dfeval = df.loc[50000:51000]
y_train = dftrain.pop("target")
y_eval = dfeval.pop("target")

feature_columns = []
for feature_name in list(dftrain.columns.values):
        feature_columns.append(tf.feature_column.numeric_column(feature_name, dtype=tf.float32))

def make_input_fn(data_df, label_df, num_epochs=10, shuffle=True, batch_size=32):
  def input_function():
    ds = tf.data.Dataset.from_tensor_slices((dict(data_df), label_df))
    if shuffle:
      ds = ds.shuffle(10000)
    ds = ds.batch(batch_size).repeat(num_epochs)
    return ds
  return input_function

train_input_fn = make_input_fn(dftrain, y_train)
eval_input_fn = make_input_fn(dfeval, y_eval, num_epochs=10, shuffle=False)

linear_est = tf.estimator.LinearClassifier(feature_columns=feature_columns,n_classes=len(char_dict))

linear_est.train(train_input_fn) 
result = linear_est.evaluate(eval_input_fn)

print(result['accuracy']) 
