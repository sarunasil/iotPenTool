#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Main part of the window and it's content, separate from the QMainWindow
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLCDNumber, QSlider


class Content(QWidget):
    '''Content of the MainWindow

    Arguments:
        QWidget {[type]} -- [description]
    '''

    def __init__(self):
        super().__init__()

        self.init_ui()


    def init_ui(self):
        '''Initialize content
        '''

        ok_btn = QPushButton("OK")
        ok_btn.setToolTip('This is a <b>QPushButton</b> widget')
        ok_btn.resize(ok_btn.sizeHint())

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setToolTip('This is a <b>QPushButton</b> aaaaaaaaaaaaaaaa')
        cancel_btn.resize(cancel_btn.sizeHint())

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(ok_btn)
        hbox.addWidget(cancel_btn)

        vbox = QVBoxLayout()


        lcd = QLCDNumber(self)
        sld = QSlider(Qt.Horizontal, self)
        sld.valueChanged.connect(lcd.display)

        vbox.addWidget(lcd)
        vbox.addWidget(sld)
        # vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
