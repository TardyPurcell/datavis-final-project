### Issues

- [ ] kMeans_tree的k无效
- [ ] kMeans_map有问题
- [ ] 不支持多个session

----
### 今天做的
- [x] 修改了文件的目录,单个歌曲也有一个文件夹,把不同数据写到里面,先不同数据分别作为单个json文件,或许后期可以用程序将这些json拼到一个里面
- [x] 完成函数writeData(func) 根据finalldata将数据处理写到文件中,func是处理数据并写数据的函数,参数为读取csv的row列表
- [x] 完成词频统计wordCount(),可以写入歌曲文件夹下的json文件
- [x] 完成情感分析sentiment(),可以写入歌曲文件夹下的json文件
- [x] .............releaseYear()...................
- [ ] 所有数据处理都完成了
- [ ] 其中新的是kmeans_map 这个返回的字典dic里面 dic['data']是点坐标列表 dic['names']是对应歌名列表

外面文件夹表示内部内容如wordcount

内部层级为:band->album->song

song为数据的文件

前面是文件夹

~~song为csv文件~~
song为文件夹,各种数据作为单个文件放在里面(词频统计是字典所以适合放在json内)
歌名文件夹名需要使用song=''.join(filter(str.isalnum,song))去除不合法字符

路径调用fileop.getpath(who,band,album,song)

歌曲文件中数据格式:

数据属性1,数据1

数据属性2,数据2