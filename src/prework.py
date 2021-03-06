import create_dir
import models
import data_analysis as da
import csv
import numpy as np
import os
import shutil

def del_file(filepath):
    """
    删除某一目录下的所有文件或文件夹
    :param filepath: 路径
    :return:
    """
    del_list = os.listdir(filepath)
    for f in del_list:
        file_path = os.path.join(filepath, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

def init():
    create_dir.main()
    root = models.Root("./data/finaldata.csv")
    tree = da.kMeans_tree(root, 3)
    return root, tree


def cleanCsv(path):
    del_file("./data")
    shutil.copyfile("./backupdata/finaldata.csv","./data/finaldata.csv")
    shutil.copyfile("./backupdata/doc_cluster.pkl","./data/doc_cluster.pkl")
    import re
    import pandas as pd
    import numpy as np
    df = pd.read_csv(path, encoding="gb18030",dtype={'ind':np.str})
    hang, lie = df.shape
    for i in range(0, hang):
        df["song"].loc[i] = re.sub(r"[^A-Za-z0-9\s]+", "", df["song"].loc[i])
        df["band"].loc[i] = re.sub(r"[^A-Za-z0-9\s ]+", "", df["band"].loc[i])
        df["album"].loc[i] = re.sub(r"[^A-Za-z0-9\s ]+", "", df["album"].loc[i])
        df["who likes"].loc[i] = re.sub(r"[^A-Za-z0-9\s ]+", "", df["who likes"].loc[i])
    df.to_csv(path, encoding="gb18030", index=False)


def addData(path):  # 用户自行添加的文件中不能包含有不能作为目录的字符(除了歌词部分)
    import pandas as pd
    cleanCsv(path)
    df = pd.read_csv(path, encoding="gb18030",dtype={'ind':np.str})
    #df = df.drop_duplicates(subset=['song','band'],keep='last',inplace=False)
    df1 = pd.read_csv("./data/finaldata.csv", encoding="gb18030",dtype={'ind':np.str})
    df1 = pd.concat([df1,df])
    df1=df1.drop_duplicates(subset=['song','band'],keep='first',inplace=False)
    df1.to_csv(
        "./data/finaldata.csv", encoding="gb18030", index=False, header=True, mode="w"
    )
    return init()


if __name__ == "__main__":
    init()
    addData("newdata.csv")
