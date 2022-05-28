### TODO

- [ ] appendData(path,name,data) 将新属性的数据加入文件
- [ ] 把歌词等属性写到正确的文件里
- [ ] 把dataanalysis的词频统计,情感分析写完然后写到文件里
----

外面文件夹表示内部内容如wordcount

内部层级为:band->album->song

song为数据的文件

前面是文件夹

song为csv文件

路径调用fileop.getpath(who,band,album,song)

歌曲文件中数据格式:

数据属性1,数据1

数据属性2,数据2