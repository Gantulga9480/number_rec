from control import Control
import threading
import time


def sound_main():
    while True:
        print('sound')
        time.sleep(1)


sound = threading.Thread(target=sound_main)
sound.start()
Control()
print('END')
