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

output_file = open(df_file, "r+")

output_file.write(header)

char_dict = {}

index = 0

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

target = df.pop("target")

dataset = tf.data.Dataset.from_tensor_slices((df.values, target.values))

train_dataset = dataset.shuffle(1000).batch(1)

test_dataset = dataset.shuffle(3).batch(1)

tf.keras.backend.set_floatx('float64')

model = tf.keras.Sequential([
    tf.keras.layers.Dense(10, activation='relu'),
    tf.keras.layers.Dense(10, activation='relu'),
    tf.keras.layers.Dense(1)
])

model.compile(optimizer='adam',
    loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
    metrics=['accuracy'])

model.fit(train_dataset, epochs=15)
