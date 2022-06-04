from ntpath import join
import file_op
import csv
WHOLIKES=4
ALBUM=2
BAND=1
SONG=0
LYRICS=5
def getdirs():
    dirs={}
    whoset=[]
    bandset=[]
    albumset=[]
    with open("./data/finaldata.csv",'r',encoding='gb18030') as fp:
        rows=csv.reader(fp)
        i=0
        for row in rows:
            if(i==0):
                i+=1
                continue
            if(row[WHOLIKES] not in whoset):
                whoset.append(row[WHOLIKES])
                dirs.update({row[WHOLIKES]:{}})#建立第一级目录
            if(row[BAND] not in bandset):
                bandset.append(row[BAND])
                dirs[row[WHOLIKES]].update({row[BAND]:{}})#添加第二级目录
            if(row[ALBUM] not in albumset):
                albumset.append(row[ALBUM])
                dirs[row[WHOLIKES]][row[BAND]].update({row[ALBUM]:[]}) #添加第三级目录
            dirs[row[WHOLIKES]][row[BAND]][row[ALBUM]].append(row[SONG])
    return dirs

def becomeCorrectDircName(s):
    s=[i for i in s if i.isalpha() or i.isnumeric() or i==' ']
    s=''.join(s)

def main():
    dirs=getdirs()
    print(dirs)
    for who in dirs:
        bands=dirs[who]
        for band in bands:
            albums=bands[band]
            for album in albums:
                songs=albums[album]
                #path="./data/"+who+'/'+band+'/'+album
                for song in songs:
                    song=''.join(filter(str.isalnum,song))
                    path="./data/"+who+'/'+band+'/'+album+'/'+song
                    file_op.mkdir(path)

if __name__=='__main__':
    main()