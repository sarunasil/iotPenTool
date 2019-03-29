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
from PyQt5.QtWidgets import QApplication

from iotpentool.vtabwidget import TabWidget
from iotpentool.utils import *

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
	extension = ".pickle"

	def output(self, data):
		'''STUB OUTPUT FUNCTION
		'''

		self.main_output_text_box.insertPlainText(data)

	def __init__(self, main, interfaces, manager, threat_model):
		'''Init

		Args:
			main (Main): callback to main
			interfaces (Interface): receives interfaces to be displayed
			manager (Manager): deals with multithreading
			threat_model (ThreatModel): Model part of the MVC
		'''
		QtWidgets.QMainWindow.__init__(self)

		#Load gui from ./gui/iot_main.ui
		Ui_MainWindow.__init__(self)
		self.setupUi(self)

		self.main = main

		self.threat_model = None

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

		#initialise GUI that regards Threat Model
		self.init_threat_model(threat_model)

		self.actionNew_Threat_Model.triggered.connect(self.new_model_button_action)
		self.actionOpen_Threat_Model.triggered.connect(self.open_model_button_action)
		self.actionSave_Threat_Model.triggered.connect(self.save_model_button_action)

		self.actionExit.triggered.connect(self.exit_button_action)

	def init_threat_model(self, threat_model):
		self.threat_model = threat_model

		self.actionClear_Assets_cache.triggered.connect(threat_model.clear_assets_cache)
		self.actionClear_Technologies_cache.triggered.connect(threat_model.clear_technologies_cache)
		self.actionClear_Entry_Points_cache.triggered.connect(threat_model.clear_entry_points_cache)
		self.actionExport_as_yaml.triggered.connect(self.export_yaml_button_action)

		#create right side tool menu
		threat_model.generate_gui()

		#remove previous threat model
		for children in self.metho_bar.findChildren(QtWidgets.QWidget):
			children.setParent(None)

		self.metho_bar.layout().addWidget(threat_model.threat_model_controller.threat_model_gui)
		self.module_bar.setCurrentIndex(4)

	def closeEvent(self, event):
		if not self.threat_model.saved:
			response = QMessageBox.question(self, "Quiting", "Save Threat Model before closing?", QMessageBox.Cancel | QMessageBox.No | QMessageBox.Yes, QMessageBox.No)

			if response == QMessageBox.Cancel:
				event.ignore()
				return
			elif response == QMessageBox.Yes:
				self.save_model_button_action()

		event.accept()


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

	def new_model_button_action(self):
		'''Loads a new ThreatModel instance
		'''

		if not self.threat_model.saved:
			response = QMessageBox.question(self, "Quiting", "Save Threat Model before closing?", QMessageBox.Cancel | QMessageBox.No | QMessageBox.Yes, QMessageBox.No)

			if response == QMessageBox.Cancel:
				return
			elif response == QMessageBox.Yes:
				self.save_model_button_action()

		try:
			threat_model = self.main.create_threat_model()
		except PersistenceException as e:
			Message.print_message(MsgType.ERROR, "Could not create new Threat Model instance. "+ str(e))
			Message.show_message_box(self, MsgType.ERROR, "Could not create new Threat Model instance. "+ str(e))

		self.init_threat_model(threat_model)

	def open_model_button_action(self):
		'''Loads a saved ThreatModel instance from a file
		'''

		filepath, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Save Threat Model", "", filter="Threat Model obj (*" + MainGui.extension + ")")

		if not filepath:
			return

		threat_model = None
		try:
			threat_model = self.main.open_threat_model(filepath)
		except PersistenceException as e:
			Message.print_message(MsgType.ERROR, "Could not open Threat Model " + filepath + ". " + str(e))
			Message.show_message_box(self, MsgType.ERROR, "Could not open Threat Model " + filepath + ". " + str(e))
			return

		self.init_threat_model(threat_model)

	def save_model_button_action(self):
		'''Saves current ThreatModel instance to a file
		'''

		filepath, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Threat Model", "", filter="Threat Model obj (*" + MainGui.extension + ")")

		if not filepath:
			return

		filepath += MainGui.extension if not filepath.endswith(MainGui.extension) else ""

		self.threat_model.saved = True
		try:
			self.main.save_threat_model(filepath, self.threat_model)
		except PersistenceException as e:
			Message.print_message(MsgType.ERROR, "Could not save Threat Model as " + filepath + ". " + str(e))
			Message.show_message_box(self, MsgType.ERROR, "Could not save Threat Model as " + filepath + ". " + str(e))
			self.threat_model.saved = False
			return

		Message.show_message_box(self, MsgType.INFO, "Threat Model saved successfully")

	def exit_button_action(self):
		'''Check is the Threat Model saved and exit
		'''
		self.close()

	def export_yaml_button_action(self):
		'''Exports current threat model as yaml file
		'''

		yml_extension = ".yml"
		yaml_extension = ".yaml"
		filepath, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Export Threat Model", "", filter="*.yml | *.yaml")

		if not filepath:
			return

		filepath += yml_extension if not (filepath.endswith(yml_extension) or filepath.endswith(yaml_extension)) else ""

		try:
			self.main.export_yaml(filepath, self.threat_model)
		except PersistenceException as e:
			Message.print_message(MsgType.ERROR, "Could not export Threat Model as " + filepath + ". " + str(e))
			Message.show_message_box(self, MsgType.ERROR, "Could not export Threat Model as " + filepath + ". " + str(e))
			self.threat_model.saved = False
			return

		Message.show_message_box(self, MsgType.INFO, "Threat Model exported successfully")

