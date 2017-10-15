#! /usr/bin/env python
from subprocess import Popen, PIPE
import sys
from random import randint
import vlc
import time
import termios, fcntl, os

# set up keyboard input
fd = sys.stdin.fileno()

oldterm = termios.tcgetattr(fd)
newattr = termios.tcgetattr(fd)
newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
termios.tcsetattr(fd, termios.TCSANOW, newattr)

oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

# get all mp3s in our current directory

dirlisting = []

proc = Popen(['ls *.mp3'], shell=True, stdout=PIPE)         # *nix only, if you don't like it, change it ;)
for line in proc.stdout.readlines():
    if line != '':
        #print(line)
        dirlisting.append(line)


#print(dirlisting[0])

pipes = dict(stdin=PIPE, stdout=PIPE, stderr=PIPE)

paused = False

try:
    while True:
        song = dirlisting[randint(0, len(dirlisting)-1)]
        print(song)
        #mplayer = Popen(["mplayer", song.rstrip()], **pipes)
        #mplayer.communicate(input=b">")
        player = vlc.MediaPlayer(song.rstrip())
        player.play()
        time.sleep(2)
        while player.is_playing() or paused:
            try:
                c = sys.stdin.read(1)
                print "Got character", repr(c)
                if c == 'q':
                    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
                    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
                    sys.exit()
                elif c == 'C':
                    player.stop()
                elif c == ' ':
                    player.pause()
                    paused = not paused
                    time.sleep(1)

            except IOError: pass
except KeyboardInterrupt:
    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

