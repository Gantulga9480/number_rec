import sounddevice as sd
import numpy as np
import os

from lib.paho_mqtt import PahoMqtt
from lib.params import SOUND_BUFFER_MAX_CAPACITY


class Sound(PahoMqtt):

    def __init__(self, broker, info, port=1883, raw_msg=False,
                 c_msg='', d_msg=''):
        super().__init__(broker, info, port=port, raw_msg=raw_msg,
                         c_msg=c_msg, d_msg=d_msg)

        # TODO

    def _on_message(self, client, userdata, message):
        pass

    def _on_connect(self, client, userdata, level, buf):
        self.reset()
        self.publish(topic='sound', msg=f'{self.info}, connected')
        self.subscribe(topic='sound', qos=0)
        print(f"{self.info} connected")
