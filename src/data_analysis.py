import re
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


def writeDicToJson(dic, path, filename):
    import json

    json_dict = json.dumps(dic, indent=2, sort_keys=True, ensure_ascii=False)
    with open(path + "/" + filename, "w", encoding="gb18030") as f:
        f.write(json_dict)
    print(path + "/" + filename + "写入成功")


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


def releaseYear(row):
    year = row[YEAR]
    print(year)
    dic = {"year": year}
    path = file_op.getpath(row[WHOLIKES], row[BAND], row[ALBUM], row[SONG])
    writeDicToJson(dic, path, "发行年份.json")


def sentiment(row):
    text = row[LYRICS]
    print("this is text")
    print(text)
    print("-----------------------")
    blob = textblob.TextBlob(text)
    res = blob.sentiment
    print(type(res))
    print(res.polarity)
    dic = {"polarity": res.polarity, "subjectivity": res.subjectivity}
    json_dict = json.dumps(dic, indent=2, sort_keys=True, ensure_ascii=False)
    print(json_dict)
    path = file_op.getpath(row[WHOLIKES], row[BAND], row[ALBUM], row[SONG])
    print(path)
    with open(path + "/sentiment.json", "w", encoding="gb18030") as f:
        f.write(json_dict)
    print(path + "情感分析写入成功")
    del blob


def wordCount(row):
    text = row[LYRICS]
    print("this is text")
    print(text)
    print("-----------------------")
    blob = textblob.TextBlob(text)
    sentences = blob.sentences
    word_list = []
    for sentence in sentences:
        word_list.append(sentence.word_counts)
    print("this is word_list")
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
    print(z)
    json_dict = json.dumps(z, indent=2, sort_keys=True, ensure_ascii=False)
    print(json_dict)
    path = file_op.getpath(row[WHOLIKES], row[BAND], row[ALBUM], row[SONG])
    print(path)
    with open(path + "/wordCount.json", "w", encoding="gb18030") as f:
        f.write(json_dict)
    print(path + "词频统计写入成功")
    del blob


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
    if isinstance(res, Song):
        return res.getData("lyrics")
    return " ".join(map(lambda x: x.getData("lyrics"), res.getSongs()))


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
        [x for x in word_tokenize(text) if not x in stopwords.words("english")]
    )

    def get_wordnet_pos(tag):
        if tag.startswith('J'):
            return wordnet.ADJ
        elif tag.startswith('V'):
            return wordnet.VERB
        elif tag.startswith('N'):
            return wordnet.NOUN
        elif tag.startswith('R'):
            return wordnet.ADV
        else:
            return None

    wnl = WordNetLemmatizer()
    lemmas_sent = []
    for tag in tagged_sent:
        wordnet_pos = get_wordnet_pos(tag[1]) or wordnet.NOUN
        lemmas_sent.append(wnl.lemmatize(tag[0], pos=wordnet_pos))
    return lemmas_sent


def wordCnt(
    root: Root, sel: dict[str, str], n: int
) -> list[dict[str, Union[str, int]]]:
    """
    output:
    [
        {'word': 'cyf', 'count': 1},
        {'word': 'tml', 'count': 5},
    ]
    """
    text = getText(root, sel)
    cnt = Counter(preprocess(text)).most_common(n)
    return list(map(lambda x: {"word": x[0], "count": x[1]}, cnt))


def kMeans(root: Root) -> dict[str, Union[str, str]]:
    """
    output:
    https://fastly.jsdelivr.net/gh/apache/echarts-website@asf-site/examples/data/asset/data/flare.json
    """
    return {}


def emo2(root: Root, sel: dict[str, str]) -> dict[str, float]:
    return {}


def emo5(root: Root, sel: dict[str, str]) -> dict[str, int]:
    ret = te.get_emotion(getText(root, sel))
    if ret is None:
        raise Exception("get_emotion failed")
    return ret


if __name__ == "__main__":
    # create_dir.main()
    # writeData(wordCount)
    # writeData(sentiment)
    # writeData(releaseYear)
    root = Root("./data/finaldata.csv")
    print(wordCnt(root, {"who": "tml"}, 10))
    # print(emo5(root, {"who": "tml"}))
