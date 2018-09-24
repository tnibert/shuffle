#! /usr/bin/env python
# usage: ./downloadone.py <videourl>
# downloads audio for one youtube video specified at command line

import youtube_dl
import sys

options = {
  'format': 'bestaudio/best',
  'extractaudio' : True,  # only keep the audio
  'audioformat' : "mp3",  # convert to mp3
  'outtmpl': '%(title)s.mp3',    # name the file the ID of the video
  'noplaylist' : True,    # download single video
}

downloader = youtube_dl.YoutubeDL(options)

downloader.download([sys.argv[1]])

