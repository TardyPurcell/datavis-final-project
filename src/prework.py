import create_dir
import models
import data_analysis as da
import csv
def init():
    create_dir.main()
    root = models.Root("./data/finaldata.csv")
    tree=da.kMeans_tree(root,3)
    return root,tree
def addData(path):  #用户自行添加的文件中不能包含有不能作为目录的字符(除了歌词部分)
    import pandas as pd
    df=pd.read_csv(path,encoding='gb18030')
    df.to_csv('./data/finaldata.csv',encoding="gb18030",index=False, header=False, mode='a+')
    init()

if __name__=='__main__':
    init()
    addData("newdata.csv")
