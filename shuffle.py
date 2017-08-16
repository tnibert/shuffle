#! /usr/bin/env python
from subprocess import Popen, PIPE
import sys

dirlisting = []

proc = Popen(['ls *.mp3'], shell=True, stdout=PIPE)
for line in proc.stdout.readlines():
    if line != '':
        print line
        dirlisting.append(line)


print dirlisting[0]

pipes = dict(stdin=PIPE, stdout=PIPE, stderr=PIPE)
for song in dirlisting:
    mplayer = Popen(["mplayer", song.rstrip()], **pipes)
    mplayer.communicate(input=b">")
