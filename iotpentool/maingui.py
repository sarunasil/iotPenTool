#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
Main GUI file

By sarunasil
"""

import sys
from os import path
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from vtabwidget import TabWidget

CURRENT_DIR = path.dirname(path.realpath(__file__))
MAIN_GUI_FILEPATH = path.join(CURRENT_DIR, "gui/main_gui.ui")

Ui_MainWindow, QtBaseClass = uic.loadUiType(MAIN_GUI_FILEPATH)

class MainGui(QtWidgets.QMainWindow, Ui_MainWindow):
	'''Main application gui. Deals with:
		- Status bar
		- Tool bar
		- Panels
	'''
	resized = QtCore.pyqtSignal()

	def output(self, data):
		'''STUB OUTPUT FUNCTION
		'''

		textedit = self.central.findChild(QtWidgets.QPlainTextEdit)
		textedit.insertPlainText(data)

	def __init__(self, interfaces, manager):
		'''Init

		Args:
			interfaces (Interface): receives interfaces to be displayed
			manager (Manager): deals with multithreading
		'''
		QtWidgets.QMainWindow.__init__(self)

		#Load gui from ./gui/iot_main.ui (rename file)
		Ui_MainWindow.__init__(self)
		self.setupUi(self)

		self.w = TabWidget()
		self.w.setMaximumWidth(500)
		for name, interface in interfaces.items():
			manager.add_output_func(name, self.output) #adds functions to deal with each separate interface output independantly
			interface.generate_gui(manager) #generates gui for every Interface
			self.w.addTab(interface.gui_controller.modulegui, name) #adds generated guis to TabWidget

			# self.resized.connect(interface.gui.print_general_size)

		self.module_bar.layout().addWidget(self.w)

	# def resizeEvent(self, event):
	# 	self.resized.emit()
	# 	return super(MainGui, self).resizeEvent(event)