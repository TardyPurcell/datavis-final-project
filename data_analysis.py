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
                i+=1
                continue
            text=row[LYRICS]
            blob=textblob.TextBlob(text)
            sentences=blob.sentences
            word_list=[]
            for sentence in sentences:
                word_list.append(sentence.word_counts)
            print(word_list)
            #word_list内元素:defaultdict(<class 'int'>, {'no': 1, 'matter': 1, 'how': 1, 'many': 1, 'characters': 1, 'are': 1, 'available': 1, 'for': 1, 'your': 1, 'password': 1, 'you': 1, 'should': 1, 'be': 1, 'sure': 1, 'to': 1, 'use': 1, 'every': 1, 'one': 1, 'of': 1, 'them': 1})
            from collections import Counter
            x=word_list[0]
            z={}
            for i in range (1,len(word_list)):
                y=word_list[i]
                X,Y=Counter(x),Counter(y)
                z=dict(X+Y)
            print(z)