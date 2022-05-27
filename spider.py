from urllib.request import urlopen
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import ssl
import csv
import time
import re

songs=[]
bands=[]
#这里进行文件操作,把歌手歌名经过处理弄到list内
with open("newdata.csv",'r',newline='') as fp:
    rows=csv.reader(fp)
    i=0
    for row in rows:  
        if(i!=0):
            songs.append(''.join(filter(str.isalnum,row[0])).lower()) 
            bands.append(''.join(filter(str.isalnum,row[1])).lower())
        i+=1
print("文件读取完毕,一共%d项\n",len(songs))
#print(songs,bands)
#这里爬虫

print("开始爬虫")
ips=['115.28.150.197:16817',
'120.24.171.107:16817',
'123.56.246.33:16817',
'121.41.11.179:16817',
'116.198.207.82:16817',
'42.51.40.10:16817',
'121.41.8.23:16816',
'121.204.168.137:16818',
'36.26.77.55:16818',
'106.52.125.100:16818',
'139.186.175.184:16818',
'218.241.17.128:16818',
'116.198.207.57:16818',
'120.24.216.121:16818',
'139.9.250.230:16818',
'122.114.99.229:16818',
'47.97.37.74:16818',
'182.151.43.89:16818',
'113.219.242.53:16818',
'117.81.232.88:16819',
'112.74.114.105:16819',
'222.84.252.38:16819',
'116.198.207.79:16819',
'47.92.127.154:16819',
'122.114.112.242:16819',
'61.171.49.61:16819',
'116.63.187.80:16819',
'8.134.13.249:16819',
'27.150.170.3:16819',
'139.155.5.184:16819',
'123.56.136.130:16819',
'42.81.136.193:16819',
'43.226.67.198:16819',
'106.58.210.91:16819',
'116.8.109.251:16819',
'27.50.175.58:16819',
'124.225.201.183:16819',
'129.28.158.139:16819',
'115.220.1.49:16819',
'223.247.138.63:16819',
'119.96.234.190:16819',
'125.77.162.79:16819',
'1.13.192.116:16819',
'121.199.6.124:16819',
'36.103.242.231:16819',
'150.223.57.44:16819',
'59.63.210.10:16819',
'1.13.9.110:16819',
'175.6.140.197:16819',
]
ipcot=9
rescount=0
try:
    ind=0
    f=open("res5271106.csv",'w',encoding='utf-8',newline='')
    writer=csv.writer(f)
    while(ind<len(songs)):
        ssl._create_default_https_context = ssl._create_unverified_context
        link="https://www.azlyrics.com/lyrics/"+bands[ind]+'/'+songs[ind]+'.html'
        proxies = {
            'https':ips[ipcot],
        }
        headers={'User-Agent':UserAgent().chrome}
        print("尝试打开第"+str((ind+1))+"个链接\n"+link)
        print("使用"+str(ipcot)+"号ip")
        try:
            html = requests.get(url=link,proxies=proxies,headers=headers)
        except:
            print("使用下一个ip")
            ipcot=ipcot+1
            continue
        else:
            print("打开成功")
            try:
                bsObj = BeautifulSoup(html.text, "html.parser")
                #print(table)
                a=bsObj.find_all("div",class_="col-xs-12 col-lg-8 text-center",limit=1);
                l=a[0].find_all("div")
                #print(l[5].text)  #这个就是我们要的歌词 l[5].text
            except :
                if(len(a)==0 and False):
                    print("此ip被封禁,使用下一个ip")
                    ipcot=ipcot+1
                else:
                    print("不知道为什么,先写入空内容")
                    writer.writerow(['cant open html:'+link])
                    ind+=1
                continue
            else:    
                if(rescount==0):
                    writer.writerow(['lyrics'])
                
                #''.join(re.findall('[^\n\t\d:.,]+',l[5].text))
                writer.writerow([re.sub(' +', " ",re.sub('\s', ' ', l[5].text).replace("  ",' ') )]) #str=re.sub(' +', " ",re.sub(r'[^A-Za-z0-9 ]+', '', str).replace("  ",' ') )
                rescount+=1
                print("歌词写入成功!,睡眠一会,已写入"+str(rescount))
                ind+=1
                time.sleep(5)
                #if(ind%5==0):
                 #   time.sleep(60)
    #这里处理歌词,把歌词写入csv新一列
except:
    print("出问题了,没写完")
finally:
    f.close()
    print('qwq')
    