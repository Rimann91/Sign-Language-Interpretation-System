import pandas as pd
import glob
import csv

path_to_data = "C:\\Users\\david\\Documents\\David\\MSU\\CSC450"
ANNOTATIONS = "ASL_annotations"
image_dir = "ASL_library\\asl_alphabet_train\\asl_alphabet_train"
landmark_dir = "ASL_landmarks"
CLASSES = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "del", "nothing", "space"]

annotation_file_path = path_to_data+"\\"+ANNOTATIONS+".csv"
print("annotation_file_path: %s", annotation_file_path)
annotation_list = []
image_list = glob.glob(path_to_data+"\\"+image_dir+"\\*\\*")
for image in image_list:
  id = image.split("\\")[-1].split(".")[0]
  classification = image.split("\\")[-2]
  for c in range(len(CLASSES)):
    if CLASSES[c] == classification:
      index = c
  annotation = {"id":id, "index":index, "class":classification}
  annotation_list.append(annotation)

landmark_list = glob.glob(path_to_data+"\\"+landmark_dir+"\\*.csv")
node_list = []
for landmark in landmark_list:
  print(landmark)
  id = landmark.split("\\")[-1].split(".")[0]
  landmark_dict = {"id":id}
  landmark_df = pd.read_csv(landmark, header=None)
  landmark_df.columns = ["x","y","z"]
  for column in landmark_df:
    for i in range(0,21):
      landmark_dict["landmark_"+str(column)+str(i)] = landmark_df.loc[i,column]
  node_list.append(landmark_dict)
node_df = pd.DataFrame(node_list)
annotation_df = pd.DataFrame(annotation_list)
annotation_df = pd.merge(annotation_df, node_df, on=["id"])
annotation_df.to_csv(annotation_file_path, index=False)
print(annotation_file_path)