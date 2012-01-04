import urllib
import os
import re

class Collection:

    def __init__(self):
        self.collection = {}
        try:
            f = open("collection.txt", "r")
            lines = f.readlines()
            for line in lines:
                artist, song = line.split("#-#")
                self.add_to_collection(artist, song)
        except:
            f = open("collection.txt", "w")
        f.close()

    def add(self, artist, song):
        # write to file
        f = open("collection.txt", "a")
        f.write("{0}#-#{1}\n".format(artist, song))
        f.close()
        # add to collection
        self.add_to_collection(artist, song)
        
    def add_to_collection(self, artist, song):
        artist = artist.replace("\n", "")
        song = song.replace("\n","")
        if artist in self.collection:
            self.collection[artist].append(song)
        else:
            self.collection[artist] = [song]

    def contains(self, artist, song):
        if artist in self.collection:
            if song in self.collection[artist]:
                return True
        return False


page = urllib.urlopen("http://www.skala.fm/index.php?option=com_jumi&fileid=8&Itemid=75")
lines = page.readlines()
page.close()
songs = [] 
collection = Collection()
old = 0
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
            if not collection.contains(artist, song):
                songs.append([artist, song, vid_id])
            else:
                print "Already in collection: {0} - {1}".format(song, artist)
                old += 1

for entry in songs:
    artist, song, vid_id = entry
    print "Downloading song: {0} - {1}".format(song, artist)
    os.system("python youtube_dl.py http://youtube.com/watch?v={0}".format(vid_id))
    os.system("ffmpeg -i {0}.flv -ar 44100 -ab 160k -ac 2 \"{1} - {2}.mp3\"".format(vid_id, song, artist))
    os.system("del {0}.flv".format(vid_id))
    collection.add(artist, song)

print "---------\n{0} new songs downloaded, {1} songs already in collection".format(len(songs), old)

