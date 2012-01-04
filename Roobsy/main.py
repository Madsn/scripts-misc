# -*- coding: utf-8 -*-
import urllib
import sys
import os
import re
import time
import codecs

class Collection:

	def __init__(self):
		self.collection = {}
		try:
			f = codecs.open("collection.txt", "r", encoding="utf-8")
			lines = f.readlines()
			for line in lines:
				artist, song = line.split("#-#")
				self.add_to_collection(artist, song)
		except:
			print "error parsing file, creating new file"
			f = codecs.open("collection.txt", "w", encoding="utf-8")
		f.close()

	def add(self, artist, song):
		# write to file
		f = codecs.open("collection.txt", "a", encoding="utf-8")
		f.write(artist.encode("utf-8") +"#-#"+song.encode("utf-8")+"\r\n")
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
				print song+" by "+artist+" is in collection"
				return True
		print song+" by "+artist+" is not collection"
		return False


if __name__ == "__main__":
	page = urllib.urlopen("http://www.skala.fm/index.php?option=com_jumi&fileid=8&Itemid=75")
	lines = page.readlines()
	page.close()
	songs = [] 
	collection = Collection()
	old = 0
	match = "[\w| |æ|ø|å|\.]+"
	for i in range(0, len(lines)):
		item = re.findall("\d+\. "+match+" - "+match, lines[i])
		if item:
			temp = item[0].split(".")[1:] #strip away the number at the beginning
			number =temp[0]
			if len(temp)>1:
				for i in range(1, len(temp)):
					number += "." + temp[i]
			number = number.split(" - ")
			artist = number[0].strip().decode('utf-8')
			song = number[1].strip().decode('utf-8')
			# get youtube ID from 10 lines above
			temp = re.findall("&kl=\w+", lines[i-10])
			if temp:
				vid_id = temp[0].split("=")[1].split("\"")[0]
				if not collection.contains(artist, song):
					songs.append([artist, song, vid_id])
				else:
					print "Already in collection: "+song+" - "+artist
					old += 1

	for entry in songs:
			artist, song, vid_id = entry
			if not os.path.isfile(song+" - "+artist+".mp3"):
				print "------------\n\nDownloading song: "+song+" - "+artist+"\n"
				os.system("python youtube_dl.py http://youtube.com/watch?v={0}".format(vid_id))
				print "------------\n\nConverting song: "+song+" - "+artist+"\n"
				charset = sys.getdefaultencoding()
				os.system("ffmpeg -i "+vid_id+".* -ar 44100 -ab 160k -ac 2 \""+song.encode(charset, "replace")+" - "+
				          artist.encode(charset, "replace")+".mp3\"")
				os.system("del {0}.*".format(vid_id))
				if os.path.isfile(song+" - "+artist+".mp3"):
					# only add to collection if the file was downloaded and converted successfully
					collection.add(artist, song)
			else:
				print ("-----------------------\n------------------------\n" +
						"SONG "+song+" by "+artist+" ALREADY EXISTS BUT NOT IN COLLECTION!!!\n" +
						"-----------------------\n------------------------\n")
				#time.sleep(5)
				collection.add(artist, song)


	print "---------\n{0} new songs downloaded, {1} songs already in collection".format(len(songs), old)


