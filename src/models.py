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

class SongTree:
  def __init__(self):
    self.whos = {}

  def add(self, who: Who):
    self.whos[who.name] = who