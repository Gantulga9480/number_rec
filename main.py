from tkinter import Label, LabelFrame, Tk, messagebox, ttk
from tkinter.constants import DISABLED, LEFT, NORMAL
from lib.sensor_control import Sensor
from lib.params import *
import os


class GUI(Tk):

    def __init__(self, screenName=None, baseName=None,
                 useTk=1, sync=0, use=None):
        super().__init__(screenName=screenName, baseName=baseName,
                         useTk=useTk, sync=sync, use=use)

        self.__init()
        self.__disp()
        self.set_state()
        self.mainloop()

    def stream_init(self):
        sen_count = 0
        for i in range(len(self.clients)):
            if self.clients[i].sensor_ready:
                sen_count += 1
            else:
                if self.sensor_ignore.get():
                    sen_count += 1
                else:
                    messagebox.showwarning("Sensor Error",
                                           f"{SENSOR_ERROR}-{i+1}")
        if sen_count == len(self.clients):
            self.start_btn['state'] = NORMAL

    def stream_start(self):
        if self.label_index < 4:
            for client in self.clients:
                if not client.is_started:
                    path = f'{CACHE_PATH}/{self.location[self.location_index]}'
                    client.init(path)
                client.label = self.label[self.label_index]
            self.label_index += 1
        else:
            for client in self.clients:
                client.stop()
            self.stream_save()
        self.update_label()

    def stream_reset(self):
        self.label_index = 0
        for client in self.clients:
            client.stop()
            client.reset()
        self.update_label()

    def stream_save(self):
        for client in self.clients:
            client.save()
        self.location_index += 1

    def result(self):
        pass

    def update_label(self):
        self.current_location['text'] = f'{self.location[self.location_index]}' + f' - {self.label[self.label_index]}'
        if self.label_index < 4:
            self.start_btn['text'] = f'{self.label[self.label_index]}'
        else:
            self.start_btn['text'] = 'SAVE'

    def set_state(self):
        for index, client in enumerate(self.clients):
            if client.counter != client.counter_temp:
                client.counter_temp = client.counter
                client.death_counter = 0
                client.sensor_ready = True
                self.sensor_state[index]["foreground"] = 'green'
            else:
                print(f'[WARNING] SENSOR-{client.info} is not responding')
                client.death_counter += 1
                client.sensor_ready = False
                self.sensor_state[index]["foreground"] = 'red'
            if client.death_counter > 8:
                messagebox.showerror('ERROR', f'SENSOR {client.info} DEAD')
        self.after(1000, self.set_state)

    def __init(self):
        try:
            os.mkdir(f'{CACHE_PATH}')
        except FileExistsError:
            pass
        try:
            os.mkdir(f'{SAVE_PATH}')
        except FileExistsError:
            pass
        for item in LOCATION_LIST:
            try:
                os.mkdir(f'{CACHE_PATH}/{item}')
            except FileExistsError:
                pass
            try:
                os.mkdir(f'{SAVE_PATH}/{item}')
            except FileExistsError:
                pass

        self.location = LOCATION_LIST
        self.location_index = 0
        self.label = LABEL_LIST
        self.label_index = 0
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

    def __disp(self):
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
        self.sensor_frame2 = LabelFrame(self, text="Data control",
                                        background='white')
        self.sensor_frame2.pack(side=LEFT, fill="y")
        self.current_location = Label(self.sensor_frame2,
                                      text=f'{self.location[self.location_index]}'
                                      + f' - {self.label[self.label_index]}',
                                      background='white',
                                      font=("default", 10, 'bold'))
        self.current_location.grid(row=0, column=0, padx=2, pady=2)
        self.init_btn = ttk.Button(self.sensor_frame2, text="Stream init",
                                   command=self.stream_init,
                                   width=11)
        self.init_btn.grid(row=1, column=0, padx=2, pady=2)
        self.start_btn = ttk.Button(self.sensor_frame2,
                                    text=f"{self.label[self.label_index]}",
                                    command=self.stream_start,
                                    width=11)
        self.start_btn['state'] = DISABLED
        self.start_btn.grid(row=2, column=0, padx=2, pady=2)
        self.reset_btn = ttk.Button(self.sensor_frame2,
                                    text=f"{self.label[self.label_index]}",
                                    command=self.stream_reset,
                                    width=11)
        self.reset_btn['state'] = DISABLED
        self.reset_btn.grid(row=2, column=1, padx=2, pady=2)


GUI()
