import csv


class Song:
    def __init__(self, name, lyrics):
        self.name = name
        self.lyrics = lyrics


class Album:
    def __init__(self, name) -> None:
        self.name = name
        self.songs = {}

    def add(self, song: Song) -> None:
        self.songs[song.name] = song


class Artist:
    def __init__(self, name: str):
        self.name = name
        self.albums = {}

    def add(self, album: Album):
        self.albums[album.name] = album


class Who:
    def __init__(self, name):
        self.name = name
        self.artists = {}

    def add(self, artist: Artist):
        self.artists[artist.name] = artist


class Root:
    def __init__(self, path):
        self.root={}
        WHOLIKES = 4
        ALBUM = 2
        BAND = 1
        SONG = 0
        LYRICS = 5
        dirs = {}
        whoset = []
        bandset = []
        albumset = []
        with open(path, 'r', encoding='gb18030') as fp:
            rows = csv.reader(fp)
            i = 0
            for row in rows:
                if(i == 0):
                    i += 1
                    continue
                if(row[WHOLIKES] not in whoset):
                    whoset.append(row[WHOLIKES])
                    dirs.update({row[WHOLIKES]: {}})  # 建立第一级目录
                if(row[BAND] not in bandset):
                    bandset.append(row[BAND])
                    dirs[row[WHOLIKES]].update({row[BAND]: {}})  # 添加第二级目录
                if(row[ALBUM] not in albumset):
                    albumset.append(row[ALBUM])
                    dirs[row[WHOLIKES]][row[BAND]].update(
                        {row[ALBUM]: {}})               # 添加第三级目录
                dirs[row[WHOLIKES]][row[BAND]][row[ALBUM]].update(
                    {row[SONG]: {}})
                dirs[row[WHOLIKES]][row[BAND]][row[ALBUM]
                    ][row[SONG]].update({'lyrics': row[LYRICS]})
        self.root = dirs

    def getWhos(self, who):
        return self.root[who]
