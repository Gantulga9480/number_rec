from tkinter import Label, LabelFrame, Tk
from tkinter.constants import LEFT
from lib.sensor_control import Sensor
from lib.params import *


class GUI(Tk):

    def __init__(self, screenName=None, baseName=None,
                 useTk=1, sync=0, use=None):
        super().__init__(screenName=screenName, baseName=baseName,
                         useTk=useTk, sync=sync, use=use)

        self.clients = list()
        dis = 0
        for i, item in enumerate(SENSORS):
            if item[2]:
                self.clients.append(Sensor(BROKER, f"{item[1]}",
                                           c_msg=item[0]))
                self.clients[i-dis].subscribe(item[0])
                self.clients[i-dis].loop_start()
            else:
                dis += 1

        self.title("Control")
        self.resizable(0, 0)
        self.configure(bg='white')

        self.sensor_frame1 = LabelFrame(self, text="Sensor control",
                                        background='white')
        self.sensor_frame1.pack(side=LEFT, fill="y")

        self.sensor_state = list()
        for item in self.clients:
            self.sensor_state.append(Label(self.sensor_frame1,
                                           text=f"SENSOR {item.info}",
                                           background='white',
                                           font=("default", 15, 'bold')))
            self.sensor_state[-1].grid(row=len(self.sensor_state),
                                       column=0)

        self.mainloop()


GUI()
