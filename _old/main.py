#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
Main file

By sarunasil
"""

import sys
# from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QMainWindow, QMenu, QAction, qApp, QToolTip, QPushButton, QApplication, QDesktopWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QFont, QIcon
from content import Content

class Main(QMainWindow):
    '''Main application class

    Arguments:
        QMainWindow {} -- QT main window
    '''


    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        '''Main GUI initializer
        '''

        self.statusBar().showMessage('Loading...')

        QToolTip.setFont(QFont('SansSerif', 10))

        self.load_menu_bar()
        self.load_tool_bar()
        self.setCentralWidget(Content())

        self.resize(640, 480)
        self.center()

        self.setWindowTitle('IoT Penetration testing')
        self.show()

        self.statusBar().showMessage('Done')

    def load_menu_bar(self):
        '''Load menu bar content (File, Edit, Selection, etc...)
        '''

        exitAct = QAction(QIcon('exit.png'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)

    def load_tool_bar(self):
        '''Load application toolbar for frequently used actions
        '''

        exitAct = QAction(QIcon('exit.png'), 'Exit', self)
        exitAct.triggered.connect(qApp.quit)

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAct)

    #EVENTS

    def contextMenuEvent(self, event):
        '''Overwrite context menu event (right click event)

        Arguments:
            event {[type]} -- [description]
        '''

        cmenu = QMenu(self)

        newAct = cmenu.addAction("New")
        opnAct = cmenu.addAction("Open")
        quitAct = cmenu.addAction("Quit")
        action = cmenu.exec_(self.mapToGlobal(event.pos()))

        if action == quitAct:
            qApp.quit()


    #HELPERS

    def center(self):
        '''Load window in the center of the screen
        '''

        window_geo = self.frameGeometry()
        screen_size = QDesktopWidget().availableGeometry().center()
        window_geo.moveCenter(screen_size)
        self.move(window_geo.topLeft())


if __name__ == '__main__':

    APP = QApplication(sys.argv)
    ex = Main()
    sys.exit(APP.exec_())
