from control import Control
import threading


def sound_main():
    pass


sound = threading.Thread(target=sound_main)
sound.start()
Control()
