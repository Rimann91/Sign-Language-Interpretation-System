import contextlib
import csv
import os
import random
import subprocess
import sys
import tempfile
import zipfile
# added
import glob
import pandas as pd
#import requests
#import io
# end of add

from absl import app
from absl import flags
from absl import logging
from six.moves import range
from six.moves import urllib
import tensorflow.compat.v1 as tf

# DATA_URL_IMAGES = "https://storage.googleapis.com/kaggle-data-sets/23079/29550/bundle/archive.zip?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcp-kaggle-com%40kaggle-161607.iam.gserviceaccount.com%2F20201002%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20201002T235941Z&X-Goog-Expires=259199&X-Goog-SignedHeaders=host&X-Goog-Signature=17412106bd932a59135c442a13cb282005eafa2d81ea0feb736dd5ad2ace0cd155ded4c6b24e197fb7aa90431cf39b4c92d466471dc9648a5e36bf8ca03534ff42cedec9efabcac88d70532b05b6a957b8de0c694bd7514b488bd5a34097b14fd01a67cd6673670d1b202b8284f43c6988d89b1a61be0bec394af9a3570c46b9b849d0b9931c90988676b5fa76a0f017e713912469baa843a4b402d867d37efd3bfef1c03235baf3acf2f0fb044e897b801e1db5bfaf45480dfbf6de9c10c636ac517fc2e6c919f490e3ff3d509099f5315ed6ed733687009ff1cf576c51a04bc1af22d58ec8dfc3ae3a03736d0c6a8addd9dd995ed393e7e359196d9e1f4056"
DATA_URL_IMAGES = "https://www.kaggle.com/grassknoted/asl-alphabet?resource=download&downloadHash=4c26ddd48724c3efad045f3bd85017fce744ffa99cd55366273a939e3ac82790"
DATA_FOLDER_IMAGES = "ASL_library.zip"
path_to_data = 'C:\\Users\\david\\Documents\\David\\MSU\\CSC450\\test'

def progress_hook(blocks, block_size, total_size):
    print("Downloaded %d%% of %d bytes   (%d blocks)\r" % (
    blocks * block_size / total_size * 100, total_size, blocks), end="")

urlretrieve = urllib.request.urlretrieve
print("Creating data directory.")
tf.io.gfile.makedirs(path_to_data)
print("Downloading images.")
local_images_path = os.path.join(
    path_to_data, DATA_FOLDER_IMAGES)
if not tf.io.gfile.exists(local_images_path):
      urlretrieve(DATA_URL_IMAGES, local_images_path, progress_hook)
# if not tf.io.gfile.exists(local_images_path):
#     r = requests.get(DATA_URL_IMAGES, stream=True)
#     with open(local_images_path, 'wb') as fd:
#         for chunk in r.iter_content(chunk_size=128):
#             fd.write(chunk)
print("Extracting images.")
image_dir = local_images_path[:-4]
if not tf.io.gfile.exists(image_dir):
    with zipfile.ZipFile(local_images_path) as images_zip:
        images_zip.extractall(path_to_data)
print(image_dir)
print("done")