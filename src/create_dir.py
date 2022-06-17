from ntpath import join
import file_op
import csv
from urllib import parse

WHOLIKES = 4
ALBUM = 2
BAND = 1
SONG = 0
LYRICS = 5


def getdirs():
    dirs = {}
    whoset = []
    bandset = []
    albumset = []
    with open("./data/finaldata.csv", "r", encoding="gb18030") as fp:
        rows = csv.reader(fp)
        i = 0
        for row in rows:
            try:
                if i == 0:
                    i += 1
                    continue
                if row[WHOLIKES] not in whoset:
                    whoset.append(row[WHOLIKES])
                    dirs.update({row[WHOLIKES]: {}})  # 建立第一级目录
                if row[BAND] not in bandset:
                    bandset.append(row[BAND])
                    dirs[row[WHOLIKES]].update({row[BAND]: {}})  # 添加第二级目录
                if row[ALBUM] not in albumset:
                    albumset.append(row[ALBUM])
                    dirs[row[WHOLIKES]][row[BAND]].update({row[ALBUM]: []})  # 添加第三级目录
                dirs[row[WHOLIKES]][row[BAND]][row[ALBUM]].append(row[SONG])
            except KeyError as e:
                print("我们已经有这首歌了你还要加,很有品味,但是希望你不要不识抬举")
                continue
    return dirs


def becomeCorrectDircName(s):
    s = [i for i in s if i.isalpha() or i.isnumeric() or i == " "]
    s = "".join(s)


def main():
    dirs = getdirs()
    print(dirs)
    for who in dirs:
        bands = dirs[who]
        for band in bands:
            albums = bands[band]
            for album in albums:
                songs = albums[album]
                # path="./data/"+who+'/'+band+'/'+album
                for song in songs:
                    # import re
                    # song = re.sub(r"[^A-Za-z0-9\s]+", "",song)
                    who_quoted, band_quoted, album_quoted, song_quoted = map(
                        parse.quote, [who, band, album, song]
                    )
                    path = (
                        "./data/"
                        + who_quoted
                        + "/"
                        + band_quoted
                        + "/"
                        + album_quoted
                        + "/"
                        + song_quoted
                    )
                    file_op.mkdir(path)


if __name__ == "__main__":
    main()
