import re
import os
from typing import Union
from collections import Counter
import textblob
import csv
import json
import file_op
import create_dir
from models import *
import text2emotion as te
from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer

WHOLIKES = 4
ALBUM = 2
BAND = 1
SONG = 0
YEAR = 3
LYRICS = 5


def getListFromJson(path):
    import json

    with open(path, "r", encoding="gb18030") as f:
        l = json.load(f)
        return l


def getDicFromJson(path):
    import json

    with open(path, "r", encoding="gb18030") as f:
        data = json.load(f)
        return data


def writeDicToJson(dic, path):
    import json

    json_dict = json.dumps(dic, indent=2, sort_keys=True, ensure_ascii=False)
    with open(path, "w", encoding="gb18030") as f:
        f.write(json_dict)
    print(path + "写入成功")


def writeListToJson(list, path):
    import json

    with open(path, "w", encoding="gb18030") as f:
        json.dump(list, f, indent=4)
    print(path + "写入成功")


def writeData(func):
    with open("./data/finalldata.csv", "r", encoding="gb18030", newline="") as f:
        rows = csv.reader(f)
        i = 0
        for row in rows:
            print(type(row))
            if i == 0:
                i += 1
                continue
            func(row)
            # break


def getSongs(root: Root, sel: dict[str, str]) -> list[Song]:
    res = root
    if "who" in sel:
        res = res.getWho(sel["who"])
        if "artist" in sel:
            res = res.getArtist(sel["artist"])
            if "album" in sel:
                res = res.getAlbum(sel["album"])
                if "song" in sel:
                    res = res.getSong(sel["song"])
    return res.getSongs() if not isinstance(res, Song) else [res]


def getText(root: Root, sel: dict[str, str]) -> str:
    res = root
    if "who" in sel:
        res = res.getWho(sel["who"])
        if "artist" in sel:
            res = res.getArtist(sel["artist"])
            if "album" in sel:
                res = res.getAlbum(sel["album"])
                if "song" in sel:
                    res = res.getSong(sel["song"])
    # for song in res.getSongs():
    # print(song.name+'\n')
    if isinstance(res, Song):
        return res.getData("lyrics")
    return " ".join(map(lambda x: x.getData("lyrics"), res.getSongs()))


def getPath(sel: dict[str, str], datafilename: str) -> str:
    path = "./data"
    for key in sel.keys():
        path = path + "/" + sel[key]
    path = path + "/" + datafilename
    print(path)
    return path


def preprocess(text: str) -> list[str]:
    pat_letter = re.compile(r"[^a-zA-Z \']+")
    text = pat_letter.sub(" ", text).strip().lower()
    # to find the 's following the pronouns. re.I is refers to ignore case
    pat_is = re.compile("(it|he|she|that|this|there|here)('s)", re.I)
    # to find the 's following the letters
    pat_s = re.compile("(?<=[a-zA-Z])'s")
    # to find the ' following the words ending by s
    pat_s2 = re.compile("(?<=s)'s?")
    # to find the abbreviation of not
    pat_not = re.compile("(?<=[a-zA-Z])n't")
    # to find the abbreviation of would
    pat_would = re.compile("(?<=[a-zA-Z])'d")
    # to find the abbreviation of will
    pat_will = re.compile("(?<=[a-zA-Z])'ll")
    # to find the abbreviation of am
    pat_am = re.compile("(?<=[I|i])'m")
    # to find the abbreviation of are
    pat_are = re.compile("(?<=[a-zA-Z])'re")
    # to find the abbreviation of have
    pat_ve = re.compile("(?<=[a-zA-Z])'ve")

    text = pat_is.sub(r"\1 is", text)
    text = pat_s.sub("", text)
    text = pat_s2.sub("", text)
    text = pat_not.sub(" not", text)
    text = pat_would.sub(" would", text)
    text = pat_will.sub(" will", text)
    text = pat_am.sub(" am", text)
    text = pat_are.sub(" are", text)
    text = pat_ve.sub(" have", text)

    text = text.replace("'", " ")

    tagged_sent = pos_tag(
        [
            x for x in word_tokenize(text) if not x in stopwords.words("english")
        ]  # 这里是分词和去停止词
    )

    def get_wordnet_pos(tag):
        if tag.startswith("J"):
            return wordnet.ADJ
        elif tag.startswith("V"):
            return wordnet.VERB
        elif tag.startswith("N"):
            return wordnet.NOUN
        elif tag.startswith("R"):
            return wordnet.ADV
        else:
            return None

    wnl = WordNetLemmatizer()
    lemmas_sent = []
    for tag in tagged_sent:
        wordnet_pos = get_wordnet_pos(tag[1]) or wordnet.NOUN
        lemmas_sent.append(wnl.lemmatize(tag[0], pos=wordnet_pos))
    return lemmas_sent  # 这里是去了打回了原形的


def tokenize_and_stem(text: str):
    return preprocess(text)


def tokenize_only(text: str):
    pat_letter = re.compile(r"[^a-zA-Z \']+")
    text = pat_letter.sub(" ", text).strip().lower()
    # to find the 's following the pronouns. re.I is refers to ignore case
    pat_is = re.compile("(it|he|she|that|this|there|here)('s)", re.I)
    # to find the 's following the letters
    pat_s = re.compile("(?<=[a-zA-Z])'s")
    # to find the ' following the words ending by s
    pat_s2 = re.compile("(?<=s)'s?")
    # to find the abbreviation of not
    pat_not = re.compile("(?<=[a-zA-Z])n't")
    # to find the abbreviation of would
    pat_would = re.compile("(?<=[a-zA-Z])'d")
    # to find the abbreviation of will
    pat_will = re.compile("(?<=[a-zA-Z])'ll")
    # to find the abbreviation of am
    pat_am = re.compile("(?<=[I|i])'m")
    # to find the abbreviation of are
    pat_are = re.compile("(?<=[a-zA-Z])'re")
    # to find the abbreviation of have
    pat_ve = re.compile("(?<=[a-zA-Z])'ve")

    text = pat_is.sub(r"\1 is", text)
    text = pat_s.sub("", text)
    text = pat_s2.sub("", text)
    text = pat_not.sub(" not", text)
    text = pat_would.sub(" would", text)
    text = pat_will.sub(" will", text)
    text = pat_am.sub(" am", text)
    text = pat_are.sub(" are", text)
    text = pat_ve.sub(" have", text)
    text = text.replace("'", " ")

    return [x for x in word_tokenize(text) if not x in stopwords.words("english")]


def wordCnt(root: Root, sel: dict[str, str]) -> dict[str, list[dict[str, Union[str, int]]]]:
    """
    output:
    [
        {'word': 'cyf', 'count': 1},
        {'word': 'tml', 'count': 5},
    ]
    """
    path = "./data"
    for key in sel.keys():
        path = path + "/" + sel[key]
    path += "/wordCnt.json"
    print(path)
    if not os.path.exists(path):
        text = getText(root, sel)
        text = " ".join(preprocess(text))
        print(text)
        blob = textblob.TextBlob(text)
        sentences = blob.sentences
        word_list = []
        for sentence in sentences:
            word_list.append(sentence.word_counts)
        # print("this is len word_list")
        # for word in word_list:
        # print(len(word_list))
        # print(type({'1':2,'2':3}))
        # print(type(word))
        # print("-----------------------")
        # word_list内元素:defaultdict(<class 'int'>, {'no': 1, 'matter': 1, 'how': 1, 'many': 1, 'characters': 1, 'are': 1, 'available': 1, 'for': 1, 'your': 1, 'password': 1, 'you': 1, 'should': 1, 'be': 1, 'sure': 1, 'to': 1, 'use': 1, 'every': 1, 'one': 1, 'of': 1, 'them': 1})
        def sumDict(x, y):
            temp = {}
            for k in x.keys() | y.keys():
                temp[k] = sum(i.get(k, 0) for i in (x, y))
            return temp

        from functools import reduce

        z = reduce(sumDict, word_list)
        # print(z)
        res = []
        for word, count in z.items():
            res.append({"word": word, "count": count})
        writeListToJson(res, path)
        return {"cnt": res}
    else:
        return {"cnt": getListFromJson(path)}


def kMeans_tree(root: Root, k: int) -> dict[str, Union[str, str]]:
    """
    output:
    https://fastly.jsdelivr.net/gh/apache/echarts-website@asf-site/examples/data/asset/data/flare.json
    """
    import kmeans

    path = "./data/kMeanstree"+ str(k) + ".json"
    if not os.path.exists(path):
        dic = kmeans.getKmeansRes(root.getSongs(), k)
        print(dic)
        writeDicToJson(dic, path)
        return dic
    else:
        return getDicFromJson(path)


def kMeans_map(root: Root, sel: dict[str, str]):  # 需要已经运行过kMeans_tree并且传进去的参数root必须一样
    path = getPath(sel, "map.json")
    if not os.path.exists(path):
        if('x' not in getSongs(root, sel)[0].data.keys()):
            import kmeans
            kmeans.getKmeansRes(root.getSongs(),1)
        ret = {}
        temp = []
        name = {}
        for song in getSongs(root, sel):
            temp.append([song.getData("x"), song.getData("y")])
            name[str(song.getData("x")) + "," + str(song.getData("y"))] = song.name
        ret["data"] = temp
        ret["names"] = name
        writeDicToJson(ret, path)
        return ret
    else:
        return getDicFromJson(path)


def emo2(root: Root, sel: dict[str, str]) -> dict[str, float]:
    path = getPath(sel, "emo2.json")
    if not os.path.exists(path):
        ret = {}
        text = getText(root, sel)
        text = " ".join(preprocess(text))
        blob = textblob.TextBlob(text)
        res = blob.sentiment
        # print(type(res))
        # print(res.polarity)
        ret = {"polarity": res.polarity, "subjectivity": res.subjectivity}
        writeDicToJson(ret, path)
        return ret
    else:
        return getDicFromJson(path)


def emo5(root: Root, sel: dict[str, str]) -> dict[str, int]:
    path = getPath(sel, "emo5.json")
    if not os.path.exists(path):
        text = getText(root, sel)
        text = " ".join(preprocess(text))
        ret = te.get_emotion(text)
        if ret is None:
            raise Exception("get_emotion failed")
        writeDicToJson(ret, path)
        return ret
    else:
        return getDicFromJson(path)


if __name__ == "__main__":
    import prework

    # create_dir.main()
    # writeData(wordCount)
    # writeData(sentiment)
    # writeData(releaseYear)
    root,tree = prework.init()
    root,tree=prework.addData('newdata.csv')
    print(kMeans_map(root, {"who": "tml"}))
