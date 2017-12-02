#! /usr/bin/env python
from subprocess import Popen, PIPE
import sys
from random import randint
import vlc
import time
import termios, fcntl, os

DEBUG = False

ENGINE = "mplayer"

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

#pipes = dict(stdin=PIPE, stdout=PIPE, stderr=PIPE)

paused = False

try:
    while True:
        song = dirlisting[randint(0, len(dirlisting)-1)]
        print(song.rstrip())
        #mplayer = Popen(["mplayer", song.rstrip()], **pipes)
        #mplayer.communicate(input=b">")

        mplayer = True              # does not mean mplayer is running
                                    # means that we won't sleep a few lines down
                                    # if we don't use it
        player = vlc.MediaPlayer(song.rstrip())
        current_len = 0
        if ENGINE != "mplayer":
            time.sleep(1)
            player.play()
            time.sleep(2)
            current_len = player.get_length()
            print(player.get_length())
        if current_len == 0 or ENGINE == "mplayer":
            print("reverting to mplayer")
            mplayer = Popen(["mplayer", song.rstrip()])
            mplayer.communicate(input=b">")

        while(not mplayer): sleep(1)

        while player.is_playing() or paused:
            try:
                c = sys.stdin.read(1)
                if DEBUG: print("Got character", repr(c))
                if c == 'q':
                    print("Exiting")
                    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
                    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
                    sys.exit()
                elif c == 'C':
                    player.stop()
                elif c == ' ':
                    player.pause()
                    paused = not paused
                    if paused: print("PAUSED")
                    time.sleep(1)
                elif c == 'A':
                    newvol = player.audio_get_volume() + 2
                    print("Volume: {}%".format(newvol))
                    if newvol <= 98: player.audio_set_volume(newvol)
                elif c == 'B':
                    newvol = player.audio_get_volume() - 2
                    print("Volume: {}%".format(newvol))
                    if newvol >= 2: player.audio_set_volume(newvol)

            except IOError: pass
except:         # this masks exceptions but will restore our terminal :\
    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
