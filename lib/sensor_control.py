from lib.paho_mqtt import PahoMqtt
import csv


class Sensor(PahoMqtt):

    def __init__(self, broker, info, port=1883, raw_msg=False,
                 c_msg='', d_msg=''):
        super().__init__(broker, info, port=port, raw_msg=raw_msg,
                         c_msg=c_msg, d_msg=d_msg)

        # Flags
        self.is_streaming = False

        # Attributes
        self.label = None

    def _on_message(self, client, userdata, message):
        if self.is_streaming:
            msg = message.payload.decode("utf-8", "ignore")
            msg = msg.replace("[", "")
            msg = msg.replace("]", "")
            msg = msg.replace(" ", "")
            # TODO: insert timestamp
            if self.label:
                self._writer.writerow([msg, self.label])
                self.label = None
            else:
                self._writer.writerow([msg, 0])

    def stream_init(self, path):
        self._file = open(f'{path}/sensor_{self.info}.csv', "w+", newline='')
        self._writer = csv.writer(self._file)
        self.is_streaming = True
        self.is_started = True

    def stream_stop(self):
        self.is_streaming = False
        self.is_started = False
