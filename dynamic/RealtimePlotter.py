# -*- coding: utf-8 -*-
import datetime
import os
import pickle
import subprocess
import threading
from time import sleep

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from numpy import std
import numpy as np
from dynamic import load_csi_real_time_data
from dynamic.data_process import get_features

d_len = 64
s = np.zeros((d_len, 1))
pin = 0
segments = []


class RealtimePlotter(object):
    ani = None

    def __init__(self, ui):
        self.d_flag = 0
        self.ui = ui
        self.tx = 0
        self.rx = 0
        self.subcarrier_no = 0
        self.offset = 0
        self.last_value = None
        self.filename = "/home/luxiang/linux-80211n-csitool-supplementary/csi_data/1.dat"
        self.start_flag = False
        self.sample_count = 0
        self.det = None

    def start(self):
        self.start_flag = True
        log = threading.Thread(target=self.log, daemon=True)
        log.start()
        sleep(0.5)
        read = threading.Thread(target=self.get_single_subcarrier_amplitude_value, daemon=True)
        read.start()
        if os.path.exists("/home/luxiang/linux-80211n-csitool-supplementary/csi_data/sample/model.pickle"):
            self.det = threading.Thread(target=self.detect, daemon=True)
            self.det.start()
        else:
            self.ui.set_p5()
            self.ui.msg_text.append(self.get_time() + "<font color = 'black'>--> Sample start!!")
            self.ui.auto_scroll()

    def log(self):
        subprocess.call(
            "cd " + self.filename[:self.filename.find(self.filename.split("/")[-1])] +
            "; sudo /home/luxiang/linux-80211n-csitool-supplementary/netlink/log_to_file " +
            self.filename.split("/")[-1] + "&", shell=True)

    def detect(self):
        global s
        self.ui.msg_text.append(self.get_time() + "<font color = 'blue'>--> Warning! Someone coming!!")
        self.ui.auto_scroll()
        ani = threading.Thread(target=self.move, daemon=True)
        ani.start()
        while self.start_flag:
            v = std(s)
            # print(v)
            if v < 200:
                self.ui.set_p2()
            elif v < 300:
                self.ui.set_p3()
            elif v < 400:
                self.ui.set_p4()
            elif v < 500:
                self.ui.set_p5()
            elif v < 600:
                self.ui.set_p6()
            elif v < 700:
                self.ui.set_p7()
            else:
                self.ui.set_p8()
            sleep(0.2)

    def get_single_subcarrier_amplitude_value(self):
        global s
        global pin
        while self.start_flag:
            file_data, self.offset = load_csi_real_time_data.read_bf_file(self.filename, self.offset)
            if len(file_data) > 0:
                csi_entry = file_data.loc[len(file_data) - 1]
                csi = load_csi_real_time_data.get_scale_csi(csi_entry)
                self.last_value = abs(np.squeeze(csi[self.tx][self.rx][self.subcarrier_no]))
                pin = pin % d_len
                s[pin] = sum(sum(sum(abs(csi))))
                segments.append(s[pin])
                pin += 1
            print(pin)
            sleep(0.002)

    def move(self):
        for i in range(15):
            filename = './dynamic/img/loc' + str(i + 1) + '.png'
            self.ui.pic = QPixmap(filename)
            self.ui.label_map.setPixmap(self.ui.pic.scaled(self.ui.label_map.size(), Qt.IgnoreAspectRatio))
            sleep(0.33)

    def pause(self):
        self.start_flag = False
        global s
        global pin
        global d_len
        self.offset = 0
        s = np.zeros((d_len, 1))
        pin = 0
        if not os.path.exists("/home/luxiang/linux-80211n-csitool-supplementary/csi_data/sample/model.pickle"):
            self.ui.set_p0()
            self.ui.msg_text.append(self.get_time() + "<font color = 'black'>--> Sample end!!")
            self.ui.auto_scroll()
            path = r"/home/luxiang/linux-80211n-csitool-supplementary/csi_data/sample/"
            temp = self.sample_count // 10
            if temp == 0:
                np.savetxt(path + 'a-' + str(self.sample_count) + ".txt", segments)
            elif temp == 1:
                np.savetxt(path + 'b-' + str(self.sample_count - 10) + ".txt", segments)
            elif temp == 2:
                np.savetxt(path + 'c-' + str(self.sample_count - 20) + ".txt", segments)
            elif temp == 3:
                np.savetxt(path + 'd-' + str(self.sample_count - 30) + ".txt", segments)
            else:
                np.savetxt(path + 'e-' + str(self.sample_count - 40) + ".txt", segments)
            print(temp)
            self.sample_count += 1
        else:
            with open('/home/luxiang/linux-80211n-csitool-supplementary/csi_data/sample/scale.pickle', 'rb') as fr:
                min_max_scaler = pickle.load(fr)

            with open('/home/luxiang/linux-80211n-csitool-supplementary/csi_data/sample/model.pickle', 'rb') as fr:
                clf = pickle.load(fr)
            f = get_features(segments)
            f = np.reshape(f, (1, 5))
            f = min_max_scaler.transform(f)
            res = clf.predict(f)
            if res == 0:
                self.ui.msg_text.append(
                    self.get_time() + "<font color = 'black'>--> Security! Legal person A passed!!")
                self.ui.set_p1()
                self.ui.pic = QPixmap('./dynamic/img/one.png')
                self.ui.label_map.setPixmap(self.ui.pic.scaled(self.ui.label_map.size(), Qt.IgnoreAspectRatio))
            elif res == 1:
                self.ui.msg_text.append(
                    self.get_time() + "<font color = 'black'>--> Security! Legal person B passed!!")
                self.ui.set_p1()
                self.ui.pic = QPixmap('./dynamic/img/one.png')
                self.ui.label_map.setPixmap(self.ui.pic.scaled(self.ui.label_map.size(), Qt.IgnoreAspectRatio))
            elif res == 4:
                self.ui.msg_text.append(
                    self.get_time() + "<font color = 'black'>--> Two persons passed!!")
                self.ui.set_p1()
                self.ui.pic = QPixmap('./dynamic/img/two.png')
                self.ui.label_map.setPixmap(self.ui.pic.scaled(self.ui.label_map.size(), Qt.IgnoreAspectRatio))
            else:
                self.ui.msg_text.append(
                    self.get_time() + "<font color = 'red'>--> Dangerous! Someone invaded!!")
                self.ui.pic = QPixmap('./dynamic/img/intrude.png')
                self.ui.label_map.setPixmap(self.ui.pic.scaled(self.ui.label_map.size(), Qt.IgnoreAspectRatio))
                self.ui.set_p9()
            self.ui.auto_scroll()

    @staticmethod
    def get_time():
        time = datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')
        return time
