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

        Args:
            interfaces (Interface): receives interfaces to be displayed
        '''

        QMainWindow.__init__(self)

        #Load gui from ./gui/iot_main.ui (rename file)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)


        self.w = TabWidget()
        self.w.setMaximumWidth(400)
        for name, interface in interfaces.items():
            interface.generate_gui()
            self.w.addTab(interface.gui, name)


        self.module_bar.layout().addWidget(self.w)