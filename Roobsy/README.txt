Purpose 
Scrape a website with a "top 40" list from a danish radio station - http://www.skala.fm/index.php?option=com_jumi&fileid=8&Itemid=75
Use youtube-dl to download flv/mp4 of each song - http://rg3.github.com/youtube-dl/
Use ffmpeg to rip the audio from each video to mp3
Track what songs have been downloaded in a txt file - todo: maybe use an sqlite db instead

Tested on windows, for *nix you will at least need to install ffmpeg but there might be other compatibility issues as well.
