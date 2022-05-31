import csv


class Song:
    def __str__(self) -> str:
        return f'{str(self.data)}>'

    def __init__(self, name, lyrics):
        self.name = name
        self.data = {
            'lyrics': lyrics,
        }

    def addData(self, key, value):
        self.data[key] = value

    def getData(self, key):
        return self.data[key]


class Album:
    def __str__(self) -> str:
        return f'{str(self.songs)}'

    def __init__(self, name) -> None:
        self.name = name
        self.songs = {}

    def addSong(self, song: Song) -> None:
        self.songs[song.name] = song

    def getSong(self, name: str) -> Song:
        return self.songs[name]


class Artist:
    def __str__(self) -> str:
        return f'{self.albums}'

    def __init__(self, name: str):
        self.name = name
        self.albums = {}

    def addAlbum(self, album: Album):
        self.albums[album.name] = album

    def getAlbum(self, album: str) -> Album:
        return self.albums[album]


class Who:
    def __str__(self) -> str:
        return f'{str(self.artists)}'

    def __init__(self, name):
        self.name = name
        self.artists = {}

    def addArtist(self, artist: Artist):
        self.artists[artist.name] = artist

    def getArtist(self, artist: str) -> Artist:
        return self.artists[artist]


class Root:
    def __str__(self) -> str:
        return f'{str(self.root)}'

    def __init__(self, path):
        self.root = {}
        WHOLIKES = 4
        ALBUM = 2
        BAND = 1
        SONG = 0
        LYRICS = 5
        # dirs = {}
        # whoset = []
        # bandset = []
        # albumset = []
        with open(path, 'r', encoding='gb18030') as fp:
            rows = csv.reader(fp)
            flag = True
            for row in rows:
                if flag:
                    flag = False
                    continue
                if row[WHOLIKES] not in self.root:
                    self.root[row[WHOLIKES]] = Who(row[WHOLIKES])
                    # whoset.append(row[WHOLIKES])
                    # dirs.update({row[WHOLIKES]: {}})  # 建立第一级目录
                if row[BAND] not in self.root[row[WHOLIKES]].artists:
                    self.root[row[WHOLIKES]].artists[row[BAND]
                                                     ] = Artist(row[BAND])
                    # bandset.append(row[BAND])
                    # dirs[row[WHOLIKES]].update({row[BAND]: {}})  # 添加第二级目录
                if row[ALBUM] not in self.root[row[WHOLIKES]].artists[row[BAND]].albums:
                    self.root[row[WHOLIKES]].artists[row[BAND]
                                                     ].albums[row[ALBUM]] = Album(row[ALBUM])
                    # albumset.append(row[ALBUM])
                    # dirs[row[WHOLIKES]][row[BAND]].update(
                    #     {row[ALBUM]: {}})               # 添加第三级目录
                if row[SONG] not in self.root[row[WHOLIKES]].artists[row[BAND]].albums[row[ALBUM]].songs:
                    self.root[row[WHOLIKES]].artists[row[BAND]].albums[row[ALBUM]].songs[row[SONG]] = Song(
                        row[SONG], row[LYRICS])
                # dirs[row[WHOLIKES]][row[BAND]][row[ALBUM]].update(
                #     {row[SONG]: {}})
                # dirs[row[WHOLIKES]][row[BAND]][row[ALBUM]
                #     ][row[SONG]].update({'lyrics': row[LYRICS]})
        # self.root = dirs

    def getWho(self, who: str) -> Who:
        return self.root[who]


if __name__ == '__main__':
    root = Root('./data/finaldata.csv')
    for name, who in root.root.items():
      for name, artist in who.artists.items():
        for name, album in artist.albums.items():
          for name, song in album.songs.items():
            print(name)