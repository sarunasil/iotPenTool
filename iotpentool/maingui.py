#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
Main GUI file

By sarunasil
"""

import sys
from os import path
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QWidget
from PyQt5 import uic

from vtabwidget import TabWidget

CURRENT_DIR = path.dirname(path.realpath(__file__))
MAIN_GUI_FILEPATH = path.join(CURRENT_DIR, "gui/main_gui.ui")

Ui_MainWindow, QtBaseClass = uic.loadUiType(MAIN_GUI_FILEPATH)

class MainGui(QMainWindow, Ui_MainWindow):
    '''Main application gui. Deals with:
        - Status bar
        - Tool bar
        - Panels
    '''

    def __init__(self, interfaces):
        '''Init
        '''
        QMainWindow.__init__(self)

        #Load gui from ./gui/iot_main.ui (rename file)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)


        self.w = TabWidget()
        for iname in interfaces:
            a = interfaces[iname]
            self.w.addTab(a.gui, iname)

        # self.w.addTab(QWidget(), "tab1")
        # self.w.addTab(QWidget(), "tab2")
        # self.w.addTab(QWidget(), "tab3")

        self.module_bar.layout().addWidget(self.w)