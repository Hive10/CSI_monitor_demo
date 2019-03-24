# -*- coding: utf-8 -*-

import os
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor, QPalette, QColor, QPixmap
from PyQt5.QtWidgets import QSizePolicy, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from dynamic.RealtimePlotter import RealtimePlotter, segments


class UiMainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(UiMainWindow, self).__init__()

        # define the object variable
        self.vertical_top_layout, self.vertical_main_layout = None, None
        self.horizontal_second_layout, self.vertical_tips_layout = None, None
        self.central_widget, self.plotter, self.widget_canvas = None, None, None

        self.p0, self.p1, self.p2, self.p3 = None, None, None, None
        self.safe_label1, self.safe_label2, self.safe_label3 = None, None, None
        self.warning_label1, self.warning_label2, self.warning_label3 = None, None, None
        self.danger_label1, self.danger_label2, self.danger_label3 = None, None, None
        self.data_select_button, self.file_name = None, None
        self.start_button, self.pause_button, self.quit_button = None, None, None


        self.msg_text = None
        self.shown_speed = 1
        self.setup_ui(self)
        self.retranslate_ui(self)

    def setup_ui(self, main_window):
        main_window.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.central_widget = QtWidgets.QWidget(main_window)
        font_12 = QtGui.QFont()
        font_12.setPointSize(12)
        font_13 = QtGui.QFont()
        font_13.setPointSize(13)
        font_14 = QtGui.QFont()
        font_14.setPointSize(14)
        font_15 = QtGui.QFont()
        font_15.setPointSize(15)

        # define layout
        self.vertical_top_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.vertical_top_layout.setContentsMargins(10, 10, 10, 10)

        self.vertical_main_layout = QtWidgets.QVBoxLayout()
        self.vertical_top_layout.addLayout(self.vertical_main_layout)
        self.vertical_main_layout.setContentsMargins(10, 10, 10, 10)

        self.vertical_second_layout = QtWidgets.QVBoxLayout()
        self.vertical_second_layout.setContentsMargins(0, 10, 0, 10)

        self.horizontal_second_layout = QtWidgets.QHBoxLayout()
        self.horizontal_second_layout.setContentsMargins(0, 10, 0, 10)

        self.vertical_tips_layout = QtWidgets.QVBoxLayout()
        self.vertical_tips_layout.setContentsMargins(0, 0, 0, 0)

        # add widget into layouts
        self.plotter = RealtimePlotter(self)

        pic_map = QPixmap('t1.png')
        self.label_map = QLabel()
        self.label_map.setScaledContents(True)
        self.label_map.setPixmap(pic_map.scaled(self.label_map.size(), Qt.KeepAspectRatioByExpanding))
        pic_man = QPixmap('t2.png')
        self.label_man = QLabel()
        self.label_man.setPixmap(pic_man)
        pic_intruder = QPixmap('p3.png')
        label_intruder = QLabel()
        label_intruder.setPixmap(pic_intruder)

        self.vertical_second_layout.addWidget(self.label_map)
        self.vertical_main_layout.addLayout(self.vertical_second_layout)
        self.vertical_main_layout.addLayout(self.horizontal_second_layout)

        self.start_button = QtWidgets.QPushButton()
        self.start_button.setFont(font_15)

        self.pause_button = QtWidgets.QPushButton()
        self.pause_button.setFont(font_15)

        self.quit_button = QtWidgets.QPushButton()
        self.quit_button.setFont(font_15)

        self.p0 = QPalette()
        self.p0.setColor(QPalette.Background, Qt.white)

        self.p1 = QPalette()
        self.p1.setColor(QPalette.Background, QColor(0x76EE00))

        self.p2 = QPalette()
        self.p2.setColor(QPalette.Background, QColor(0x99ff00))

        self.p3 = QPalette()
        self.p3.setColor(QPalette.Background, QColor(0xccff00))

        self.p4 = QPalette()
        self.p4.setColor(QPalette.Background, QColor(0xffff00))

        self.p5 = QPalette()
        self.p5.setColor(QPalette.Background, QColor(0xEEEE00))

        self.p6 = QPalette()
        self.p6.setColor(QPalette.Background, QColor(0xFFB90F))

        self.p7 = QPalette()
        self.p7.setColor(QPalette.Background, QColor(0xFF8C00))

        self.p8 = QPalette()
        self.p8.setColor(QPalette.Background, QColor(0xFF4500))

        self.p9 = QPalette()
        self.p9.setColor(QPalette.Background, QColor(0xCD0000))

        self.safe_label1 = QtWidgets.QLabel()
        self.safe_label1.setAlignment(Qt.AlignCenter)
        self.safe_label1.setAutoFillBackground(True)
        self.safe_label1.setPalette(self.p0)

        self.safe_label2 = QtWidgets.QLabel()
        self.safe_label2.setAlignment(Qt.AlignCenter)
        self.safe_label2.setAutoFillBackground(True)
        self.safe_label2.setPalette(self.p0)

        self.safe_label3 = QtWidgets.QLabel()
        self.safe_label3.setAlignment(Qt.AlignCenter)
        self.safe_label3.setAutoFillBackground(True)
        self.safe_label3.setPalette(self.p0)

        self.warning_label1 = QtWidgets.QLabel()
        self.warning_label1.setAlignment(Qt.AlignCenter)
        self.warning_label1.setAutoFillBackground(True)
        self.warning_label1.setPalette(self.p0)

        self.warning_label2 = QtWidgets.QLabel()
        self.warning_label2.setAlignment(Qt.AlignCenter)
        self.warning_label2.setAutoFillBackground(True)
        self.warning_label2.setPalette(self.p0)

        self.warning_label3 = QtWidgets.QLabel()
        self.warning_label3.setAlignment(Qt.AlignCenter)
        self.warning_label3.setAutoFillBackground(True)
        self.warning_label3.setPalette(self.p0)

        self.danger_label1 = QtWidgets.QLabel()
        self.danger_label1.setAlignment(Qt.AlignCenter)
        self.danger_label1.setAutoFillBackground(True)
        self.danger_label1.setPalette(self.p0)

        self.danger_label2 = QtWidgets.QLabel()
        self.danger_label2.setAlignment(Qt.AlignCenter)
        self.danger_label2.setAutoFillBackground(True)
        self.danger_label2.setPalette(self.p0)

        self.danger_label3 = QtWidgets.QLabel()
        self.danger_label3.setAlignment(Qt.AlignCenter)
        self.danger_label3.setAutoFillBackground(True)
        self.danger_label3.setPalette(self.p0)

        self.vertical_tips_layout.addWidget(self.danger_label3)
        self.vertical_tips_layout.addWidget(self.danger_label2)
        self.vertical_tips_layout.addWidget(self.danger_label1)
        self.vertical_tips_layout.addWidget(self.warning_label3)
        self.vertical_tips_layout.addWidget(self.warning_label2)
        self.vertical_tips_layout.addWidget(self.warning_label1)
        self.vertical_tips_layout.addWidget(self.safe_label3)
        self.vertical_tips_layout.addWidget(self.safe_label2)
        self.vertical_tips_layout.addWidget(self.safe_label1)

        self.msg_text = QtWidgets.QTextBrowser()
        self.msg_text.setFont(font_12)
        self.msg_text.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.msg_text.setObjectName("message")

        self.main_splitter = QtWidgets.QSplitter(Qt.Horizontal)
        self.sub_splitter = QtWidgets.QSplitter(Qt.Vertical)
        self.sub_splitter.addWidget(self.start_button)
        self.sub_splitter.addWidget(self.pause_button)
        self.sub_splitter.addWidget(self.quit_button)
        self.sub_splitter.setHandleWidth(8)
        self.main_splitter.addWidget(self.sub_splitter)
        self.main_splitter.addWidget(self.msg_text)
        self.main_splitter.setStretchFactor(0, 1)
        self.main_splitter.setStretchFactor(1, 100)
        self.vertical_main_layout.addWidget(self.main_splitter)

        self.horizontal_second_layout.addWidget(self.main_splitter)
        self.horizontal_second_layout.addLayout(self.vertical_tips_layout)
        main_window.setCentralWidget(self.central_widget)
        self.retranslate_ui(main_window)

    def retranslate_ui(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle("CSI Guard")
        self.start_button.setText("start")
        self.start_button.clicked.connect(self.start)
        self.pause_button.setText("pause")
        self.pause_button.clicked.connect(self.pause)
        self.quit_button.setText("quit")
        self.quit_button.clicked.connect(self.quit)

    def start(self):
        if self.plotter.start_flag is True:
            return
        self.plotter.start_flag = True
        # self.plotter.filename = self.plotter.filepath + str(randint(0, 100000)) + '.dat'
        self.plotter.start()
        self.msg_text.append(self.plotter.get_time() + "<font color = 'black'>--> Showing...")
        self.auto_scroll()

    def pause(self):
        if self.plotter.start_flag is False:
            return
        os.system("sudo kill -s 9 `ps -ef|grep '../netlink/log_to_file'|grep -v sudo|grep -v grep|awk '{print $2}'`")
        self.msg_text.append(
            "<font color = 'black'>" + self.plotter.get_time() + "<font color = 'red'>--> Stop showing!")
        self.auto_scroll()
        self.plotter.pause()
        self.plotter.start_flag = False

    def add_msg(self, msg):
        self.msg_text.append(msg)

    def auto_scroll(self):
        self.msg_text.moveCursor(QTextCursor.End)

    def set_p0(self):
        self.safe_label1.setPalette(self.p0)
        self.safe_label2.setPalette(self.p0)
        self.safe_label3.setPalette(self.p0)
        self.warning_label1.setPalette(self.p0)
        self.warning_label2.setPalette(self.p0)
        self.warning_label3.setPalette(self.p0)
        self.danger_label1.setPalette(self.p0)
        self.danger_label2.setPalette(self.p0)
        self.danger_label1.setPalette(self.p0)

    def set_p1(self):
        self.safe_label1.setPalette(self.p1)
        self.safe_label2.setPalette(self.p0)
        self.safe_label3.setPalette(self.p0)
        self.warning_label1.setPalette(self.p0)
        self.warning_label2.setPalette(self.p0)
        self.warning_label3.setPalette(self.p0)
        self.danger_label1.setPalette(self.p0)
        self.danger_label2.setPalette(self.p0)
        self.danger_label1.setPalette(self.p0)

    def set_p2(self):
        self.safe_label1.setPalette(self.p1)
        self.safe_label2.setPalette(self.p2)
        self.safe_label3.setPalette(self.p0)
        self.warning_label1.setPalette(self.p0)
        self.warning_label2.setPalette(self.p0)
        self.warning_label3.setPalette(self.p0)
        self.danger_label1.setPalette(self.p0)
        self.danger_label2.setPalette(self.p0)
        self.danger_label1.setPalette(self.p0)

    def set_p3(self):
        self.safe_label1.setPalette(self.p1)
        self.safe_label2.setPalette(self.p2)
        self.safe_label3.setPalette(self.p3)
        self.warning_label1.setPalette(self.p0)
        self.warning_label2.setPalette(self.p0)
        self.warning_label3.setPalette(self.p0)
        self.danger_label1.setPalette(self.p0)
        self.danger_label2.setPalette(self.p0)
        self.danger_label1.setPalette(self.p0)

    def set_p4(self):
        self.safe_label1.setPalette(self.p1)
        self.safe_label2.setPalette(self.p2)
        self.safe_label3.setPalette(self.p3)
        self.warning_label1.setPalette(self.p4)
        self.warning_label2.setPalette(self.p0)
        self.warning_label3.setPalette(self.p0)
        self.danger_label1.setPalette(self.p0)
        self.danger_label2.setPalette(self.p0)
        self.danger_label1.setPalette(self.p0)

    def set_p5(self):
        self.safe_label1.setPalette(self.p1)
        self.safe_label2.setPalette(self.p2)
        self.safe_label3.setPalette(self.p3)
        self.warning_label1.setPalette(self.p4)
        self.warning_label2.setPalette(self.p5)
        self.warning_label3.setPalette(self.p0)
        self.danger_label1.setPalette(self.p0)
        self.danger_label2.setPalette(self.p0)
        self.danger_label1.setPalette(self.p0)

    def set_p6(self):
        self.safe_label1.setPalette(self.p1)
        self.safe_label2.setPalette(self.p2)
        self.safe_label3.setPalette(self.p3)
        self.warning_label1.setPalette(self.p4)
        self.warning_label2.setPalette(self.p5)
        self.warning_label3.setPalette(self.p6)
        self.danger_label1.setPalette(self.p0)
        self.danger_label2.setPalette(self.p0)
        self.danger_label1.setPalette(self.p0)

    def set_p7(self):
        self.safe_label1.setPalette(self.p1)
        self.safe_label2.setPalette(self.p2)
        self.safe_label3.setPalette(self.p3)
        self.warning_label1.setPalette(self.p4)
        self.warning_label2.setPalette(self.p5)
        self.warning_label3.setPalette(self.p6)
        self.danger_label1.setPalette(self.p7)
        self.danger_label2.setPalette(self.p0)
        self.danger_label3.setPalette(self.p0)

    def set_p8(self):
        self.safe_label1.setPalette(self.p1)
        self.safe_label2.setPalette(self.p2)
        self.safe_label3.setPalette(self.p3)
        self.warning_label1.setPalette(self.p4)
        self.warning_label2.setPalette(self.p5)
        self.warning_label3.setPalette(self.p6)
        self.danger_label1.setPalette(self.p7)
        self.danger_label2.setPalette(self.p8)
        self.danger_label3.setPalette(self.p0)

    def set_p9(self):
        self.safe_label1.setPalette(self.p1)
        self.safe_label2.setPalette(self.p2)
        self.safe_label3.setPalette(self.p3)
        self.warning_label1.setPalette(self.p4)
        self.warning_label2.setPalette(self.p5)
        self.warning_label3.setPalette(self.p6)
        self.danger_label1.setPalette(self.p7)
        self.danger_label2.setPalette(self.p8)
        self.danger_label3.setPalette(self.p9)

    @staticmethod
    def quit():
        # print(segments)
        # for item in segments:
        #     print(len(item))
        os.system("sudo kill -s 9 `ps -ef|grep '../netlink/log_to_file'|grep -v sudo|grep -v grep|awk '{print $2}'`")
        sys.exit(0)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UiMainWindow()
    ui.setup_ui(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
