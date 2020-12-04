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


import tensorflow as tf 
import os
import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

#create tensors
#Get all filenames from root to run in train 

#root folder of CSV files
root = "/Users/bradenbagby/Downloads/Final/"

#final folder to place new dataset CSV files in
finalFolder = "/Users/bradenbagby/Downloads/CleanDataset/"

#asl root image folder
aslRoot= "/Users/bradenbagby/Downloads/asl"

#skip these letters
skip = []#['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W']

#number of each letter to get. so get 150 of As, 150 of B's, etc
NUMBER_OF_EACH_LETTER = 150


columns = []
xOry = 0
for c in range(21):
    columns.append(('x') + str(c))
    columns.append(('y') + str(c))


print(columns)



count = 0
counter = 10
files = []
counts = {}
for (dirpath, dirnames, filenames) in os.walk(root):
    #if counter > count:
       # break
    for f in filenames:
        if ".DS" in f:
            continue
        counter += 1
        letter = f[0]
        if not letter in counts:
            counts[letter] = 0
        counts[letter] = counts[letter] + 1
        
        if counts[letter] > NUMBER_OF_EACH_LETTER:
            continue

        skipperoo = False
        for c in skip:
            if c in f:
                skipperoo = True
        if skipperoo:
            continue

        files.append(dirpath + "/" + f)
       # if counter > count:
          #  break

count = len(files)

print("" + str(len(files)) + " files found")

files.sort()

fullArray = []

for f in files:
    print(f)
    df = pd.read_csv(f,header=None)
    count_row = df.shape[0]
    d = {}

    index = 0
    for r in range(count_row):
        d[columns[index]] = df.iloc[r,0]#tf.constant(df.iloc[r,0])
        index += 1
        d[columns[index]] = df.iloc[r,1]#tf.constant(df.iloc[r,1])
        index +=1

    className =  f[f.rfind("/") + 1:].replace(".csv","")[0]
    d['class'] = f[f.rfind("/") + 1:]#className
    d['file'] = f
    fullArray.append(d)


df = pd.DataFrame(fullArray) 



def get_image_path(csv_name):
    ending = csv_name.replace(".csv","")
    letter = ending[0]
    folder = aslRoot + "/" + letter
    number = ending[1:]
    f = folder + "/" + ending + ".jpg"
    return f


def close_event():
    plt.close() #timer calls this function after 3 seconds and closes the window 



#for plotting
#get all x's 
#get all ys
print(df.head(2))
print("---------------VISUALIZE---------------")
for i in range(0,count):
    xs = []
    ys = []
    series = df.iloc[i]

    for i in range(0,21):
        xs.append(series[i * 2])
        ys.append(series[(i * 2) + 1])

    print("-----------------------")
    fig, ax = plt.subplots()
    title = series['class']
    fileName = series['file']
    imagePath = get_image_path(title)
    print(title)
    print(imagePath)
    img = plt.imread(imagePath)
    ax.imshow(img, extent=[0, 1, 0, 1])
    colors = cm.rainbow(np.linspace(0, 1, len(ys)))
    for i in range(0,len(ys)):
        print("(" + str(xs[i]) + "," + str(ys[i]) + ") : " + str(colors[i]))
        ax.plot(xs[i],ys[i],'o',color=colors[i])
    #or y, c in zip(ys, colors):
     #   ax.plot(xs, ys, 'o', color=c)
    
    plt.title(title)
    plt.draw()
    plt.pause(0.1)
    val = input("Keep?: ").lower()
    if "k" in val or "y" in val:
        command = "cp " + fileName + " " + finalFolder
        os.system(command)
        print(command)


    plt.clf()
    plt.close()

