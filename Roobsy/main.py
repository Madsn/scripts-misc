import urllib
import os
import re

page = urllib.urlopen("http://www.skala.fm/index.php?option=com_jumi&fileid=8&Itemid=75")
lines = page.readlines()
page.close()
songs = [] 
for i in range(0, len(lines)):
    item = re.findall("\d+\. [\w| ]+ - [\w| ]+", lines[i])
    if item:
        number = item[0].split(".")[1].split("-")
        artist = number[0].strip()
        song = number[1].strip()
        # get youtube ID from 10 lines above
        temp = re.findall("&kl=\w+", lines[i-10])
        if temp:
            vid_id = temp[0].split("=")[1].split("\"")[0]
            songs.append([song, artist, vid_id])

for entry in songs:
    song, artist, vid_id = entry
    print "Downloading song: {0} - {1}".format(song, artist)
    os.system("python youtube_dl.py http://youtube.com/watch?v={0}".format(vid_id))
    os.system("ffmpeg -i {0}.flv -ar 44100 -ab 160k -ac 2 \"{1} - {2}.mp3\"".format(vid_id, song, artist))
    os.system("del {0}.flv".format(vid_id))
