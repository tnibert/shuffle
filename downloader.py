#! /usr/bin/env python3

# usage: ./downloadone.py <videourl>
# Downloads an playlist or video from youtube as mp3s
# Depends on youtube_dl, install with pip install youtube-dl
# This script is MIT licensed
# This script is not to be used for any illegal shenanigans

import sys
import youtube_dl


listurl = sys.argv[1]                   # replace this with the url of the playlist to download
nop = not ('playlist' in listurl)       # specify whether downloading playlist or not, will be False if single video

options = {
  'format': 'bestaudio/best',
  'extractaudio' : True,  # only keep the audio
  'audioformat' : "mp3",  # convert to mp3
  'outtmpl': '%(title)s.mp3',    # name the file the ID of the video
  'noplaylist' : nop,
}

downloader = youtube_dl.YoutubeDL(options)

downloader.download([listurl])
