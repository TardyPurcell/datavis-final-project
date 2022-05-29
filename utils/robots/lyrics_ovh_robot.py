from urllib import request
from urllib.error import HTTPError
import json
import csv

base_url = 'https://api.lyrics.ovh/v1/'
csvfile_url = 'qwq.csv'

def main():
  cnt_total = 0
  cnt_success = 0
  with open(csvfile_url, encoding='utf8') as csvfile, open('log.txt', 'w') as logfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
      artist = row[1]
      song = row[0]
      url = base_url + artist.replace(
        ' ', '%20').replace('/', '%20') + '/' + song.replace(
          ' ', '%20').replace('/', '%20')
      cnt_total += 1
      try:
        resp = request.urlopen(url).read()
        obj = json.loads(resp)
        f = open('lyrics/' + artist.replace(
          '/', '%2f') + '-' + song.replace(
            '?', '%3f').replace('/', '%2f') + '.txt', 'w', encoding='utf8')
        f.write(obj['lyrics'])
        cnt_success += 1
      except HTTPError:
        msg = '404    ' + artist + '-' + song
        print(msg)
        logfile.write(msg + '\n')
      except IOError:
        msg = 'io     ' + artist + '-' + song
        print(msg)
        logfile.write(msg + '\n')
      print(cnt_success, '/', cnt_total)

if __name__ == '__main__':
  main()