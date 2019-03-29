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

from iotpentool.vtabwidget import TabWidget

CURRENT_DIR = path.dirname(path.realpath(__file__))
MAIN_GUI_FILEPATH = path.join(CURRENT_DIR, "gui/main_gui.ui")

Ui_MainWindow, QtBaseClass = uic.loadUiType(MAIN_GUI_FILEPATH)

class MainGui(QtWidgets.QMainWindow, Ui_MainWindow):
	'''Main application gui. Deals with:
		- Status bar
		- Tool bar
		- Panels
	'''
	# resized = QtCore.pyqtSignal()
	interfaces_categories = ["Firmware", "Web App", "Mobile App", "Hardware", "Wireless"]

	def output(self, data):
		'''STUB OUTPUT FUNCTION
		'''

		self.main_output_text_box.insertPlainText(data)

	def __init__(self, interfaces, manager, threat_model):
		'''Init

		Args:
			interfaces (Interface): receives interfaces to be displayed
			manager (Manager): deals with multithreading
		'''
		QtWidgets.QMainWindow.__init__(self)

		#Load gui from ./gui/iot_main.ui
		Ui_MainWindow.__init__(self)
		self.setupUi(self)

		self.actionClear_Assets_cache.triggered.connect(threat_model.clear_assets_cache)
		self.actionClear_Technologies_cache.triggered.connect(threat_model.clear_technologies_cache)
		self.actionClear_Entry_Points_cache.triggered.connect(threat_model.clear_entry_points_cache)

		#create left side tool menu
		self.firmware_tabs = TabWidget()
		self.web_app_tabs = TabWidget()
		self.mobile_app_tabs = TabWidget()
		self.remote_access_tabs = TabWidget()
		self.wireless_tabs = TabWidget()

		self.firmware_tabs.setMaximumWidth(500)
		for name, interface in interfaces.items():
			manager.add_output_func(name, self.output) #adds functions to deal with each separate interface output independantly
			interface.generate_gui(manager) #generates gui for every Interface


			self.get_tab(interface.category).addTab(interface.gui_controller.interfacegui, name) #adds generated guis to TabWidget

			# self.resized.connect(interface.gui.print_general_size)
		self.firmware_tab.layout().addWidget(self.firmware_tabs)
		self.web_app_tab.layout().addWidget(self.web_app_tabs)
		self.mobile_app_tab.layout().addWidget(self.mobile_app_tabs)
		self.remote_access_tab.layout().addWidget(self.remote_access_tabs)
		self.wireless_tab.layout().addWidget(self.wireless_tabs)


		#create right side tool menu
		threat_model.generate_gui()
		self.metho_bar.layout().addWidget(threat_model.threat_model_controller.threat_model_gui)

		self.module_bar.setCurrentIndex(4)

	# def resizeEvent(self, event):
	# 	self.resized.emit()
	# 	return super(MainGui, self).resizeEvent(event)

	def get_tab(self, category):
		'''Returns the qtabwidget tab to which particular interface has to be added

		Args:
			category (String): interface category

		Returns:
			QWidget: tab to add interface to
		'''

		if category == "FIRMWARE":
			return self.firmware_tabs
		elif category == "WEB APP":
			return self.web_app_tabs
		elif category == "MOBILE APP":
			return self.mobile_app_tabs
		elif category == "REMOTE ACCESS":
			return self.remote_access_tabs
		elif category == "WIRELESS":
			return self.wireless_tabs

		return self.wireless_tabs

