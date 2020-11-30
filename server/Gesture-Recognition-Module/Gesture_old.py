import sys
import socket
import select

import tensorflow as tf
from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt
import os
import glob
import pandas as pd
import numpy as np
import pathlib
from io import StringIO

TCP_IP = '127.0.0.1'
TCP_PORT = 6009
BUFFER_SIZE = 1024
param = []

class_names = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]


def createDataset(fp):
    print("start: --------------------------------------\n\n")
   # df = pd.read_csv(StringIO(fp))#pd.read_csv(fp)
   # print(df.head())
    lm_dataset = []
    label_dataset = []
    df = fp.split(",")

    #for i in range(len(df)):
        #df[i] = float(df[i])

    label = df[0]

    print("label: " + label)
    lm_list = []
    lm_group=[]
    for j in range(1,17):
        print("x: " + str(df[j]))
        print("y: " + str(df[j+21]))
        print("z: " + str(df[j+42]))
        landmark = [float(df[j]), float(df[j+21]), float(df[j+42])]
        lm_group.append(landmark)
        if (j)%4==0:
            lm_list.append(lm_group)
            lm_group=[]
    for j in range(17,22):
        landmark = [float(df[j]), float(df[j+21]), float(df[j+42])]
        lm_group.append(landmark)
    lm_list.append(lm_group)
    lm_dataset.append(lm_list)
    label_dataset.append(9)





    features = tf.ragged.constant(lm_dataset)
    labels = tf.constant(label_dataset)
    dataset = tf.data.Dataset.from_tensor_slices((features.to_tensor(), labels))
    dataset = dataset.batch(batch_size=32)
    print("features:",features.shape)
    print("labels:",labels.shape)
    print("dataset:",dataset)
    return dataset

print("--------")
print("TensorFlow version: {}".format(tf.__version__)) 

print("--------")
testString = "J,0.536133,0.655762,0.713379,0.665039,0.552734,0.587891,0.558594,0.585938,0.606445,0.492188,0.471191,0.523438,0.561035,0.408691,0.401367,0.462402,0.497803,0.338867,0.267578,0.2323,0.204834,0.873047,0.760742,0.608887,0.493896,0.462646,0.507812,0.386963,0.463867,0.538086,0.527344,0.426514,0.530273,0.606934,0.557617,0.480225,0.571289,0.640137,0.594727,0.483398,0.390137,0.296143,0.000100657,-0.0635147,-0.0962067,-0.154037,-0.200653,0.0497055,-0.0992584,-0.16098,-0.140533,0.0265312,-0.1474,-0.193176,-0.144958,-0.0245667,-0.182953,-0.20401,-0.153732,-0.0862885,-0.111542,-0.116653,-0.0995636"
newSet = createDataset(testString)

model = tf.keras.models.load_model("./landmark_cnn_v1.h5", )

# Check its architecture
model.summary()

print("------------------------------------------")
print(newSet)
print("------------------------------------------")

#test_loss, test_acc = model.evaluate(newSet, verbose=2)
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#print(test_acc)

#pred = model.predict(newSet)
#print(pred)
#print("===")
#res = np.argmax(pred[0])
#print(res)



def classify(s):
    newSet = createDataset(s)
    pred = model.predict(newSet)
    print("===")
    res = np.argmax(pred[0])
    print(res)
    print(class_names[res])
    print()
    print()

classify(testString)

def reformat(start):
    start = start.replace("\n", "")
    start = start.replace("\r", "")
    ar = start.split(",")


    xs = []
    ys = []
    zs = []

    index = 0
    for val in ar:
        if index % 3 == 0:
            xs.append(val)
        elif (index + 2) % 3 == 0:
            ys.append(val)
        elif (index + 1) % 3 == 0:
            zs.append(val)

        index += 1
    delimeter = ","
    finalS = delimeter.join(xs) + "," + delimeter.join(ys) + "," + delimeter.join(zs)
    return finalS


print( 'Listening for client...')
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((TCP_IP,TCP_PORT))
server.listen(1)
rxset = [server]
txset = []

times = 0

while 1:
    rxfds, txfds, exfds = select.select(rxset, txset, rxset)
    for sock in rxfds:
        if sock is server:
            conn, addr = server.accept()
            conn.setblocking(0)
            rxset.append(conn)
           # print( 'Connection from address:' + str(addr))
        else:
            try:
                data = sock.recv(BUFFER_SIZE).decode("utf-8")
                if ";" in data:
                    #print ("Received all the data")
                    param.append(data)
                    finalString = ""
                    for x in param:
                        finalString = finalString + x

                    param = []
                    rxset.remove(sock)

                    times = times + 1
                    if times < 25:
                        continue
                    times = 0
                    finalString = finalString.replace(";","")
                    finalString = finalString.replace("value_","")
                    reformatString = "F," + reformat(finalString) #add f because the format looks for a class in beginning right now
                    reformatString = reformatString.rstrip('\x00')
                    print()
                    print("'" + reformatString + "'")
                    print()
                    classify(reformatString)

                    sock.close()
                else:
                    if data != "":
                        print(data)
                  #  print ('"' + str(data) + '"')
                    param.append(data)
            except:
                print ("Connection closed by remote end")
                param = []
                rxset.remove(sock)
                sock.close()