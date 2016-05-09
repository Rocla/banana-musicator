import music_generator as generator
import music_player as player
import time
import threading

musicList = []


def musicator(id, type):
    time.sleep(id)
    generator.generate(id=id, type=type)
    musicList.append(id)


def play_music(periods, sentiment):
    for i in range(periods):
        try:
            t = threading.Thread(target=musicator, args=(i, sentiment))
            t.start()
        except:
            print "Error: unable to start thread"

    while (threading.activeCount() > 1) or (len(musicList) > 0):
        if len(musicList) > 0:
            player.play(musicList.pop(0))


if __name__ == "__main__":
    play_music(40, 2)
