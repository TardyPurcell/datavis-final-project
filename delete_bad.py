import pandas as pd
import csv
df = pd.read_csv("data!.csv",encoding='gb18030')
df.head()
list=[]
with open("data!.csv",'r',encoding='gb18030',newline='') as fp:
    rows=csv.reader(fp)
    i=0
    for row in rows:
        print(row)
        if(row[4].find('cant open html')!=-1):
            list.append(i-1)
        i+=1
print(list)
df_new=df.drop(list)
df_new.to_csv("dataout.csv",index=0)