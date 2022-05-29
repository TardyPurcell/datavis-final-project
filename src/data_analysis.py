import textblob
import csv
import json
import file_op
import create_dir
WHOLIKES=4
ALBUM=2
BAND=1
SONG=0
YEAR=3
LYRICS=5

def writeDicToJson(dic,path,filename):
    import json
    json_dict=json.dumps(dic,indent=2,sort_keys=True,ensure_ascii=False)
    with open(path+'/'+filename,'w',encoding='gb18030') as f:
        f.write(json_dict)
    print(path+'/'+filename+'写入成功')

def writeData(func):
    with open('./data/finalldata.csv','r',encoding='gb18030',newline='') as f:
        rows=csv.reader(f)
        i=0
        for row in rows:
            print(type(row))
            if(i==0):
                i+=1
                continue
            func(row)
            #break
def releaseYear(row):
    year=row[YEAR]
    print(year)
    dic={'year':year}
    path=file_op.getpath(row[WHOLIKES],row[BAND],row[ALBUM],row[SONG])
    writeDicToJson(dic,path,"发行年份.json")
def sentiment(row):
    text=row[LYRICS]
    print('this is text')
    print(text)
    print('-----------------------')
    blob=textblob.TextBlob(text)
    res=blob.sentiment
    print(type(res))
    print(res.polarity)          
    dic={'polarity':res.polarity,'subjectivity':res.subjectivity}
    json_dict=json.dumps(dic,indent=2,sort_keys=True,ensure_ascii=False)
    print(json_dict)
    path=file_op.getpath(row[WHOLIKES],row[BAND],row[ALBUM],row[SONG])
    print(path)
    with open(path+'/sentiment.json','w',encoding='gb18030') as f:
        f.write(json_dict)
    print(path+'情感分析写入成功')
    del blob
def wordCount(row):
    text=row[LYRICS]
    print('this is text')
    print(text)
    print('-----------------------')
    blob=textblob.TextBlob(text)
    sentences=blob.sentences
    word_list=[]
    for sentence in sentences:
        word_list.append(sentence.word_counts)
    print("this is word_list")
    #for word in word_list:
        #print(len(word_list))
        #print(type({'1':2,'2':3}))
        #print(type(word))
        #print("-----------------------")
    #word_list内元素:defaultdict(<class 'int'>, {'no': 1, 'matter': 1, 'how': 1, 'many': 1, 'characters': 1, 'are': 1, 'available': 1, 'for': 1, 'your': 1, 'password': 1, 'you': 1, 'should': 1, 'be': 1, 'sure': 1, 'to': 1, 'use': 1, 'every': 1, 'one': 1, 'of': 1, 'them': 1})
    def sumDict(x,y):
        temp={}
        for k in x.keys() | y.keys():
            temp[k] = sum(i.get(k,0) for i in (x,y))
        return temp
    from functools import reduce
    z=reduce(sumDict,word_list)
    print(z)
    json_dict=json.dumps(z,indent=2,sort_keys=True,ensure_ascii=False)
    print(json_dict)
    path=file_op.getpath(row[WHOLIKES],row[BAND],row[ALBUM],row[SONG])
    print(path)
    with open(path+'/wordCount.json','w',encoding='gb18030') as f:
        f.write(json_dict)
    print(path+'词频统计写入成功')
    del blob
if __name__ == '__main__':
    create_dir.main()
    writeData(wordCount)
    writeData(sentiment)
    writeData(releaseYear)