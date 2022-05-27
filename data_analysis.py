import textblob
import csv

WHOLIKES=4
ALBUM=2
BAND=1
SONG=0
LYRICS=5
def main():
    with open('./data/finalldata.csv','r',encoding='gb18030',newline='') as f:
        rows=csv.reader(f)
        i=0
        for row in rows:
            if(i==0):
                continue
                i+=1
            text=row[LYRICS]
            blob=textblob.TextBlob(text)
            
    