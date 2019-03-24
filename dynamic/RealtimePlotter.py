# -*- coding: utf-8 -*-
import datetime
import os
import pickle
import subprocess
import threading
from random import randint
from time import sleep

from PyQt5.QtGui import QPixmap
from numpy import std
import matplotlib.animation as animation
import numpy as np
from matplotlib.figure import Figure
from dynamic import load_csi_real_time_data
from dynamic.data_process import detect, get_features

s = np.zeros((64, 1))
pin = 0
segments = []


class RealtimePlotter(object):
    ani = None

    def __init__(self, ui):
        self.d_flag = 0
        self.ui = ui
        self.interval_msec = 10
        self.tx = 0
        self.rx = 0
        self.subcarrier_no = 0
        self.mode = 'subcarrier'
        self.data = 'amplitude'
        self.offset = 0
        self.last_value = None
        self.last_plot_data = None
        self.filename = "/home/luxiang/linux-80211n-csitool-supplementary/csi_data/1.dat"
        self.start_flag = False

    def start(self):
        log = threading.Thread(target=self.log)
        if os.path.exists("/home/luxiang/linux-80211n-csitool-supplementary/csi_data/sample/model.pickle"):
            det = threading.Thread(target=self.detect, daemon=True)
            print(1)
        else:
            det = threading.Thread(target=self.sample, daemon=True)
            print(2)
        log.start()
        det.start()

    def get_values(self):
        if self.start_flag:
            r = self.get_csi_values()
            return r
        return None

    def get_csi_values(self):
        self.last_plot_data = self.get_single_subcarrier_amplitude_value()
        return self.last_plot_data

    def animate_subcarrier(self, _):
        values = self.get_values()
        RealtimePlotter.roll_y_value(self.lines[0], values)
        self.last_plot_data = self.lines
        return self.lines

    def log(self):
        subprocess.call(
            "cd " + self.filename[:self.filename.find(self.filename.split("/")[-1])] +
            "; sudo /home/luxiang/linux-80211n-csitool-supplementary/netlink/log_to_file " +
            self.filename.split("/")[-1] + "&", shell=True)

    def detect(self):
        global s
        global segments
        with open('/home/luxiang/linux-80211n-csitool-supplementary/csi_data/sample/scale.pickle', 'rb') as fr:
            min_max_scaler = pickle.load(fr)

        with open('/home/luxiang/linux-80211n-csitool-supplementary/csi_data/sample/model.pickle', 'rb') as fr:
            clf = pickle.load(fr)

        while 1:
            t_flag = detect(s)
            if t_flag == 1:
                v = std(s)
                if v < 400:
                    self.ui.set_p2()
                elif v < 450:
                    self.ui.set_p3()
                elif v < 500:
                    self.ui.set_p4()
                elif v < 550:
                    self.ui.set_p5()
                elif v < 600:
                    self.ui.set_p6()
                elif v < 650:
                    self.ui.set_p7()
                else:
                    self.ui.set_p8()
                if t_flag != self.d_flag:
                    self.ui.msg_text.append(self.get_time() + "<font color = 'red'>--> Warning! Someone coming!!")
                    self.ui.auto_scroll()
                segments.append(s[-1])
            else:
                if t_flag != self.d_flag:
                    f = get_features(segments)
                    f = np.reshape(f, (1, 5))
                    f = min_max_scaler.transform(f)
                    res = clf.predict(f)
                    if res < 0:
                        self.ui.msg_text.append(
                            self.get_time() + "<font color = 'black'>--> Security! Legal person passed!!")
                        self.ui.set_p1()
                    else:
                        self.ui.msg_text.append(
                            self.get_time() + "<font color = 'red'>--> Dangerous! Someone invaded!!")
                        self.ui.set_p9()
                    self.ui.auto_scroll()
            self.d_flag = t_flag
            sleep(0.01)

    def sample(self):
        global pin
        global s
        global segments
        while 1:
            t_flag = detect(s)
            if t_flag == 1:
                if t_flag != self.d_flag:
                    self.ui.set_p5()
                    self.ui.msg_text.append(self.get_time() + "<font color = 'red'>--> Sample start!!")
                    self.ui.auto_scroll()
                    pin = pin % 64
                    segments.append([s[pin]])
                else:
                    pin = pin % 64
                    segments[-1].append(s[pin])
            else:
                if t_flag != self.d_flag:
                    self.ui.set_p1()
                    self.ui.msg_text.append(self.get_time() + "<font color = 'black'>--> Sample end!!")
                    self.ui.auto_scroll()
            self.d_flag = t_flag
            sleep(0.01)

    def get_single_subcarrier_amplitude_value(self):
        global s
        global pin
        file_data, self.offset = load_csi_real_time_data.read_bf_file(self.filename, self.offset)
        if len(file_data) > 0:
            csi_entry = file_data.loc[len(file_data) - 1]
            csi = load_csi_real_time_data.get_scale_csi(csi_entry)
            self.last_value = abs(np.squeeze(csi[self.tx][self.rx][self.subcarrier_no]))
            pin = pin % 64
            s[pin] = sum(sum(sum(abs(csi))))
            pin += 1
        return self.last_value

    @classmethod
    def roll_y_value(cls, line, newval):
        data = line.get_ydata(line)
        data = np.roll(data, -1)
        data[-1] = newval
        line.set_ydata(data)

    @staticmethod
    def pause():
        RealtimePlotter.ani.event_source.stop()
        if not os.path.exists("/home/luxiang/linux-80211n-csitool-supplementary/csi_data/sample/model.txt"):
            path = r"/home/luxiang/linux-80211n-csitool-supplementary/csi_data/sample/"
            for i in range(len(segments)):
                np.savetxt(path + str(i) + ".txt", segments[i])

    @staticmethod
    def get_time():
        time = datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')
        return time
