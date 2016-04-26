import music_generator as generator
import music_player as player

import time

import threading

musicList = []

def musicator(i):
    print "thread %d generating" % i
    generator.generate(id=i, type=0, harmony=0)
    musicList.append(i)
    print "thread %d done" % i

for i in range(4):
    try:
        t = threading.Thread(target=musicator, args=(i,))
        t.start()
    except:
        print "Error: unable to start thread"

while (threading.activeCount() != 1) or (len(musicList) != 0):
    if len(musicList) != 0:
        id = musicList.pop(0)
        print("playing id:"+str(id))
        player.play(id)
        print("end playing")