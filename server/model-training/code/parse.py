import pandas as pd
import glob

class_names = ["A","B","C","D","E","F","G","H","I",
                "J","K","L","O","P","Q","R","T","V","W","Y"]

def parseCSVs(path, files, column_names, name):
    final_path = path+"\\parsed_"+name+"_dataset.csv"
    complete_list = []
    for f in files:
        print("file:", f)
        unique_id = f.split("\\")[-1].split(".")[0]
        print("unique_id:", unique_id)


        if name == "test":
            # Use this for test data
            label = unique_id.split("_")[0]
        else:
            # Use this for train data
            label = unique_id[0]

        for x in unique_id:
            try:
                int(x)
                label = unique_id.split(x)[0]
                break
            except:
                str(x)
        print("label:", label)
        feature_dict = {"label":class_names.index(label)}
        data_df = pd.read_csv(f, header=None)
        data_df.columns = ["x","y","z"]
        for column in data_df:
            for row in range(0,21):
                feature = data_df.loc[row,column]
                feature_dict[str(column)+str(row)] = feature
        complete_list.append(feature_dict)
        print("--------------------------------------")
    df = pd.DataFrame(complete_list)
    df.to_csv(final_path, index=False)
    return final_path

column_names = ["label","x0","x1","x2","x3","x4","x5","x6","x7","x8","x9","x10","x11","x12","x13","x14","x15","x16","x17","x18","x19","x20","y0","y1","y2","y3","y4","y5","y6","y7","y8","y9","y10","y11","y12","y13","y14","y15","y16","y17","y18","y19","y20","z0","z1","z2","z3","z4","z5","z6","z7","z8","z9","z10","z11","z12","z13","z14","z15","z16","z17","z18","z19","z20"]
folder_fp = "C:\\Users\\david\\Documents\\David\\MSU\\CSC450\\modified_dataset"
dataset_fp = parseCSVs("C:\\Users\\david\\Documents\\David\\MSU\\CSC450", glob.glob(folder_fp+"\\*.csv"), column_names, "mod")