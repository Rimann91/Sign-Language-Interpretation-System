from sklearn.model_selection import train_test_split
import pandas as pd

def splitTrainTest(dataset_fp):
    test_fp = "C:\\Users\\david\\Documents\\David\\MSU\\CSC450\\new_test_dataset.csv"
    train_fp = "C:\\Users\\david\\Documents\\David\\MSU\\CSC450\\new_train_dataset.csv"
    df = pd.read_csv(dataset_fp)
    df = df[:][df.label != 28]
    df = df[:][df.label != 27]
    df = df[:][df.label != 26]
    train, test = train_test_split(df)
    print("train",train)
    print("-------", len(train))
    print(train['label'].unique())
    print("test",test)
    print("-------", len(test))
    print(test['label'].unique())
    train.to_csv(test_fp, index=None)
    test.to_csv(train_fp, index=None)

dataset_fp = "C:\\Users\\david\\Documents\\David\\MSU\\CSC450\\parsed_train_dataset.csv"
splitTrainTest(dataset_fp)