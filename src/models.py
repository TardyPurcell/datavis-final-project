import csv
from typing import Union


class Song:
    def __str__(self) -> str:
        return f"{str(self.data)}>"

    def __init__(self,who,artist,album, name, lyrics): #添加这些数据成员方便在建立树型图的时候直接用Song往上确定父节点
        self.wholike=who
        self.artist=artist
        self.album=album
        self.name: str = name
        self.data = {
            "lyrics": lyrics,
        }

    def addData(self, key, value):
        self.data[key] = value

    def getData(self, key):
        return self.data[key]


class Album:
    def __str__(self) -> str:
        return f"{str(self.songs)}"

    def __init__(self, name) -> None:
        self.name = name
        self.songs: dict[str, Song] = {}

    def addSong(self, song: Song) -> None:
        self.songs[song.name] = song

    def getSong(self, name: str) -> Song:
        return self.songs[name]

    def getSongs(self) -> list[Song]:
        return list(self.songs.values())

    def toOption(self) -> dict[str, None]:
        return {song.name: None for song in self.songs.values()}


class Artist:
    def __str__(self) -> str:
        return f"{self.albums}"

    def __init__(self, name: str):
        self.name = name
        self.albums: dict[str, Album] = {}

    def addAlbum(self, album: Album):
        self.albums[album.name] = album

    def getAlbum(self, album: str) -> Album:
        return self.albums[album]

    def getSongs(self) -> list[Song]:
        songs = []
        for album in self.albums.values():
            songs += album.getSongs()
        return songs

    def toOption(self) -> dict[str, Union[str, dict]]:
        return {album.name: album.toOption() for album in self.albums.values()}


class Who:
    def __str__(self) -> str:
        return f"{str(self.artists)}"

    def __init__(self, name):
        self.name = name
        self.artists: dict[str, Artist] = {}

    def addArtist(self, artist: Artist):
        self.artists[artist.name] = artist

    def getArtist(self, artist: str) -> Artist:
        return self.artists[artist]

    def getSongs(self) -> list[Song]:
        songs = []
        for artist in self.artists.values():
            songs += artist.getSongs()
        return songs

    def toOption(self) -> dict[str, Union[str, dict]]:
        return {artist.name: artist.toOption() for artist in self.artists.values()}


class Root:
    def __str__(self) -> str:
        return f"{str(self.root)}"

    def addWho(self, who: Who):
        self.root[who.name] = who

    def __init__(self, path):
        self.root: dict[str, Who] = {}
        WHOLIKES = 4
        ALBUM = 2
        BAND = 1
        SONG = 0
        LYRICS = 5
        with open(path, "r", encoding="gb18030") as fp:
            rows = csv.reader(fp)
            flag = True
            for row in rows:
                if flag:
                    flag = False
                    continue
                who, artist, album, song, lyrics = (
                    row[WHOLIKES],
                    row[BAND],
                    row[ALBUM],
                    row[SONG],
                    row[LYRICS],
                )
                if who not in self.root:
                    self.addWho(Who(who))
                if artist not in self.root[who].artists:
                    self.root[who].addArtist(Artist(artist))
                if album not in self.root[who].artists[artist].albums:
                    self.root[who].artists[artist].addAlbum(Album(album))
                if song not in self.root[who].artists[artist].albums[album].songs:
                    self.root[who].artists[artist].albums[album].addSong(
                        Song(row[WHOLIKES],row[BAND],row[ALBUM],row[SONG], row[LYRICS]) #def __init__(self,who,artist,album, name, lyrics):
                    )

    def getWho(self, who: str) -> Who:
        return self.root[who]

    def getSongs(self) -> list[Song]:
        songs = []
        for who in self.root.values():
            songs += who.getSongs()
        return songs

    def toOption(self) -> dict[str, Union[str, dict]]:
        return {who.name: who.toOption() for who in self.root.values()}


if __name__ == "__main__":
    root = Root("./data/finaldata.csv")
    for name, who in root.root.items():
        for name, artist in who.artists.items():
            for name, album in artist.albums.items():
                for name, song in album.songs.items():
                    print(name)
