import models
from matplotlib.pyplot import title
import numpy as np
import pandas as pd
import nltk
import re
import os
import codecs
from sklearn import feature_extraction
from bs4 import BeautifulSoup
import mpld3
import data_analysis


def getKmeansRes(list: list[models.Song, models.Song], k: int):
    Songs = list  # class Song 列表
    texts = []  # 歌词列表
    for song in Songs:
        texts.append(song.getData("lyrics"))
    
    # nltk.download('stopwords')
    # stopwords=nltk.corpus.stopwords.words('english')
    # print(stopwords[:10])
    # from nltk.stem.snowball import SnowballStemmer
    # 如果报错，访问http://www.nltk.org/nltk_data/，下载Punkt Tokenizer Models，粘贴到C:\Users\Administrator\AppData\Roaming\nltk_data\tokenizers，解压
    # not super pythonic, no, not at all.
    # use extend so it's a big flat list of vocab
    totalvocab_stemmed = []
    totalvocab_tokenized = []
    for i in texts:
        allwords_stemmed = tokenize_and_stem(
            i
        )  # for each item in 'synopses', tokenize/stem
        totalvocab_stemmed.extend(
            allwords_stemmed
        )  # extend the 'totalvocab_stemmed' list
        allwords_tokenized = tokenize_only(i)
        totalvocab_tokenized.extend(allwords_tokenized)
    vocab_frame = pd.DataFrame(
        {"words": totalvocab_tokenized}, index=totalvocab_stemmed
    )
    
    from sklearn.feature_extraction.text import TfidfVectorizer

    # define vectorizer parameters
    tfidf_vectorizer = TfidfVectorizer(
        max_df=0.5,
        max_features=200000,
        min_df=0.1,
        stop_words="english",
        use_idf=True,
        tokenizer=tokenize_and_stem,
        ngram_range=(1, 3),
    )
    # 需要根据实际需要修改参数,含义如下!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # 别他吗忘了!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # 忘了我是傻逼!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    """
    max_df: this is the 最大频率 within the documents 
    a given feature can have to be used in the tfi-idf matrix. 
    If the term is in greater than 80% of the documents 
    it probably cares little meanining (in the context 
    of film synopses)

    min_idf: this could be an integer (e.g. 5) and the term 
    至少要在 5 of the documents 才会被考虑. Here I pass 0.2; 
    the term must be in at least 20% of the document. I 
    found that if I allowed a lower min_df I ended up 
    靠着名字进行聚类--for example "Michael" or "Tom" are 
    names found in several of the movies and the synopses 
    use these names frequently, but the names carry no real meaning.

    ngram_range: this just means I'll look at unigrams, bigrams and 
    trigrams (unigram 一元分词，把句子分成一个一个的汉字；bigram 二元分词
    ，把句子从头到尾每两个字组成一个词语；trigram 三元分词，把句子从头到尾
    每三个字组成一个词语). See n-grams
    """
    #%time：Time execution of a Python statement or expression. https://ipython.readthedocs.io/en/stable/interactive/magics.html
    #%time tfidf_matrix = tfidf_vectorizer.fit_transform(synopses) #fit the vectorizer to synopses

    tfidf_matrix = tfidf_vectorizer.fit_transform(
        texts
    )  # fit the vectorizer to synopses
    
    terms = tfidf_vectorizer.get_feature_names()
    from sklearn.metrics.pairwise import cosine_similarity

    dist = 1 - cosine_similarity(tfidf_matrix)
    from sklearn.cluster import KMeans

    num_clusters = k
    km = KMeans(n_clusters=num_clusters)
    #%time km.fit(tfidf_matrix)
    km.fit(tfidf_matrix)
    clusters = km.labels_.tolist()
    import joblib

    # uncomment the below to save your model
    # since I've already run my model I am loading from the pickle
    joblib.dump(
        km, "./data/doc_cluster.pkl"
    )  # 第一次运行时将注释打开，项目中会生成doc_cluster.pkl文件，之后运行的时候再注释掉这行就可以使用之前持久化的模型了
    km = joblib.load("./data/doc_cluster.pkl")
    clusters = km.labels_.tolist()
    songs = []
    albums = []
    whos = []
    artists = []
    for i in list:
        songs.append(i.name)
        albums.append(i.album)
        whos.append(i.wholike)
        artists.append(i.artist)
    import os  # for os.path.basename
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    from sklearn.manifold import MDS

    MDS()
    # convert two components as we're plotting points in a two-dimensional plane
    # "precomputed" because we provide a distance matrix
    # we will also specify `random_state` so the plot is reproducible.
    mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)
    pos = mds.fit_transform(dist)  # shape (n_components, n_samples)
    xs, ys = pos[:, 0], pos[:, 1]
    dic = {
        "song": songs,
        "album": albums,
        "wholikes": whos,
        "artist": artists,
        "lyric": texts,
        "cluster": clusters,
        "x": xs,
        "y": ys,
    }

    print()
    print("songs:" + str(len(songs)))
    print("clusters:" + str(len(clusters)))
    for i in range(len(songs)):
        print("{0}:{1}".format(songs[i], clusters[i]))
        list[i].addData("x", xs[i])
        list[i].addData("y", ys[i])
    # clusternames=['']*num_clusters
    # sort cluster centers by proximity to centroid
    order_centroids = km.cluster_centers_.argsort()[:, ::-1]

    # 到这里为止已经完成了聚类,接下来是一些聚类结果可视化的代码

    base = {"name": "root", "children": []}

    def makedic(name, childrenlist):
        return {"name": name, "children": childrenlist}

    def addchild(dad, son):
        dad["children"].append(son)

    def getchild(dad, sonname):
        for child in dad["children"]:
            if child["name"] == sonname:
                return child
        return {}

    cluset = []
    for ind in range(len(list)):
        list[ind].addData("x", xs[ind])
        list[ind].addData("y", ys[ind])
        clusternum = clusters[ind]
        # clustername=clusternames[clusternum]
        clustername = ""
        for i in order_centroids[clusternum, :6]:  # replace 3 with n words per cluster
            # b'...' is an encoded byte string. the unicode.encode() method outputs a byte string that needs to be converted back to a string with .decode()
            print(
                "%s"
                % vocab_frame.loc[terms[i].split(" ")]
                .values.tolist()[0][0]
                .encode("utf-8", "ignore"),
                end=", ",
            )
            clustername = clustername + str(
                vocab_frame.loc[terms[i].split(" ")]
                .values.tolist()[0][0]
                .encode("utf-8", "ignore")
            )
        print()
        print(clustername)
        print()
        wholike = whos[ind]
        artist = artists[ind]
        album = albums[ind]
        songname = songs[ind]
        leaf = {"name": songname}
        clusternode = {}
        if clusternum not in cluset:
            cluset.append(clusternum)
            clusternode = makedic("cluster" + str(clusternum), [])
            clustername = ""
            for i in order_centroids[
                clusternum, :6
            ]:  # replace 6 with n words per cluster
                # b'...' is an encoded byte string. the unicode.encode() method outputs a byte string that needs to be converted back to a string with .decode()
                print(
                    "%s"
                    % vocab_frame.loc[terms[i].split(" ")]
                    .values.tolist()[0][0]
                    .encode("utf-8", "ignore"),
                    end=", ",
                )
                clustername = clustername + str(
                    vocab_frame.loc[terms[i].split(" ")]
                    .values.tolist()[0][0]
                    .encode("utf-8", "ignore")
                )
            print()
            print(clustername)
            print()
            clusternode["value"] = clustername
            addchild(base, clusternode)
        else:
            clusternode = getchild(base, "cluster" + str(clusternum))
        whonode = getchild(clusternode, wholike)
        if len(whonode) == 0:
            whonode = makedic(wholike, [])
            addchild(clusternode, whonode)
        artistnode = getchild(whonode, artist)
        if len(artistnode) == 0:
            artistnode = makedic(artist, [])
            addchild(whonode, artistnode)
        albumnode = getchild(artistnode, album)
        if len(albumnode) == 0:
            albumnode = makedic(album, [])
            addchild(artistnode, albumnode)
        addchild(albumnode, leaf)
    return base


def main():
    root = models.Root("./data/finaldata.csv")
    res = getKmeansRes(root.getSongs(), 3)
    print()
    print("this is the res")
    print()
    print(res)


def tokenize_and_stem(text):
    return data_analysis.tokenize_and_stem(text)


def tokenize_only(text):
    return data_analysis.tokenize_only(text)


if __name__ == "__main__":
    main()
    pass
