import csv
class Root:
    def __init__(self,path):
        WHOLIKES=4
        ALBUM=2
        BAND=1
        SONG=0
        LYRICS=5
        dirs={}
        whoset=[]
        bandset=[]
        albumset=[]
        with open(path,'r',encoding='gb18030') as fp:
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
                    dirs[row[WHOLIKES]][row[BAND]].update({row[ALBUM]:{}}) #添加第三级目录
                dirs[row[WHOLIKES]][row[BAND]][row[ALBUM]].update({row[SONG]:{}})
                dirs[row[WHOLIKES]][row[BAND]][row[ALBUM]][row[SONG]].update({'lyrics':row[LYRICS]})
        self.root=dirs
    def getWhos(self,who):
        return self.root[who]
class Who:
    def __init__(self,Root,who):
        self.name=who
        self.root=Root.getWhos(who)
    def getArtist(self,band):
        return self.root[band]
