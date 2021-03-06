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

	def __init__(self, main, interfaces, manager, completer, threat_model):
		'''Init

		Args:
			main (Main): callback to main
			interfaces (Interface): receives interfaces to be displayed
			manager (Manager): deals with multithreading
			completer (Completer): generates input suggestions from threat model
			threat_model (ThreatModel): Model part of the MVC
		'''
		QtWidgets.QMainWindow.__init__(self)

		#Load gui from ./gui/iot_main.ui
		Ui_MainWindow.__init__(self)
		self.setupUi(self)

		self.main = main
		self.threat_model = None
		self.module_bar.currentChanged.connect(self.module_bar_switch_action)

		#create left side tool menu
		self.firmware_tabs = TabWidget()
		self.firmware_tabs.setObjectName("FIRMWARE")
		self.firmware_tabs.currentChanged.connect(self.nested_tab_switch_action)

		self.web_app_tabs = TabWidget()
		self.web_app_tabs.setObjectName("WEB APP")
		self.web_app_tabs.currentChanged.connect(self.nested_tab_switch_action)

		self.mobile_app_tabs = TabWidget()
		self.mobile_app_tabs.setObjectName("MOBILE APP")
		self.mobile_app_tabs.currentChanged.connect(self.nested_tab_switch_action)

		self.remote_access_tabs = TabWidget()
		self.remote_access_tabs.setObjectName("REMOTE")
		self.remote_access_tabs.currentChanged.connect(self.nested_tab_switch_action)

		self.wireless_tabs = TabWidget()
		self.wireless_tabs.setObjectName("WIRELESS")
		self.wireless_tabs.currentChanged.connect(self.nested_tab_switch_action)

		self.show_terminal_func = [[], [], [], [], []]
		# manager.add_cleaner(self.hide_all_terminal) no cleaner required - maingui cleans instead of manager
		self.firmware_tabs.setMaximumWidth(500)
		for name, interface in interfaces.items():

			position = -1
			if interface.category == "FIRMWARE":
				position = 0
			elif interface.category == "WEB APP":
				position = 1
			elif interface.category == "MOBILE APP":
				position = 2
			elif interface.category == "REMOTE ACCESS":
				position = 3
			elif interface.category == "WIRELESS":
				position = 4

			output_func, show_func = self.output(name)
			self.show_terminal_func[position].append(show_func)
			manager.add_output_func(name, output_func) #adds functions to deal with each separate interface output independantly
			interface.generate_gui(manager) #generates gui for every Interface

			self.get_tab(interface.category).addTab(interface.gui_controller.interfacegui, name) #adds generated guis to TabWidget

		#add QTabWidgets to module_bar tabs
		self.firmware_tab.layout().addWidget(self.firmware_tabs)
		self.web_app_tab.layout().addWidget(self.web_app_tabs)
		self.mobile_app_tab.layout().addWidget(self.mobile_app_tabs)
		self.remote_access_tab.layout().addWidget(self.remote_access_tabs)
		self.wireless_tab.layout().addWidget(self.wireless_tabs)

		#initialise GUI that regards Threat Model
		self.init_threat_model(threat_model, completer)
		self.actionNew.triggered.connect(self.new_model_button_action)
		self.actionOpen.triggered.connect(self.open_model_button_action)
		self.actionSave.triggered.connect(self.save_model_button_action)
		self.actionSave_as.triggered.connect(self.save_as_model_button_action)
		self.actionExport_as_json.triggered.connect(self.export_json_button_action)
		self.actionExit.setShortcut('Ctrl+Q')
		self.actionExit.triggered.connect(self.exit_button_action)
		self.actionAbout.triggered.connect(self.about_button_action)

		self.statusbar.showMessage("Ready!")

	def init_threat_model(self, threat_model, completer):
		self.threat_model = threat_model

		self.actionClear_Assets_cache.triggered.connect(self.clear_assets_cache_button_action)
		self.actionClear_Technologies_cache.triggered.connect(self.clear_technologies_cache_button_action)
		self.actionClear_Entry_Points_cache.triggered.connect(self.clear_entry_points_cache_button_action)

		#create right side tool menu
		threat_model.generate_gui(completer)

		#remove previous threat model
		for children in self.metho_bar.findChildren(QtWidgets.QWidget):
			children.setParent(None)

		self.metho_bar.layout().addWidget(threat_model.threat_model_controller.threat_model_gui)
		self.module_bar.setCurrentIndex(4)

	def clear_assets_cache_button_action(self):
		self.threat_model.clear_assets_cache()
		self.statusbar.showMessage("Assets cache cleared.")

	def clear_technologies_cache_button_action(self):
		self.threat_model.clear_technologies_cache()
		self.statusbar.showMessage("Technologies cache cleared.")

	def clear_entry_points_cache_button_action(self):
		self.threat_model.clear_entry_points_cache()
		self.statusbar.showMessage("Entry points cache cleared.")

	def closeEvent(self, event):
		if not self.threat_model.saved:
			response = QMessageBox.question(self, "Quiting", "Save Threat Model before closing?", QMessageBox.Cancel | QMessageBox.No | QMessageBox.Yes, QMessageBox.No)

			if response == QMessageBox.Cancel:
				event.ignore()
				return
			elif response == QMessageBox.Yes:
				self.save_model_button_action()

		event.accept()

	def output(self, identifier):
		'''Generates "terminals" for each identifier and returns
		a function which would insert givent data to that
		terminal

		Args:
			identifier (String): terminal identifier

		Returns:
			func: function to print data
			func: function to show terminal
		'''

		terminal = QtWidgets.QPlainTextEdit()
		terminal.setObjectName("terminal_"+identifier)
		terminal.hide()

		self.centralwidget.layout().insertWidget(1, terminal)

		def out(data):
			terminal.show()
			terminal.insertPlainText(data)

		def show():
			terminal.show()

		return out, show

	def hide_all_terminal(self):
		'''Hides all "terminals" a.k.a. QPlainTextWidgets in MainWindow
		'''

		for terminal in self.centralwidget.findChildren(QtWidgets.QPlainTextEdit):
			terminal.hide()

	def module_bar_switch_action(self, index):
		'''Action called when module_bar tab index changes - active tab is switched

		Args:
			index (int): tab index
		'''

		tab_widget = None
		if index == 0:
			tab_widget = self.firmware_tabs
		elif index == 1:
			tab_widget = self.web_app_tabs
		elif index == 2:
			tab_widget = self.mobile_app_tabs
		elif index == 3:
			tab_widget = self.remote_access_tabs
		elif index == 4:
			tab_widget = self.wireless_tabs

		tab_index = tab_widget.currentIndex()
		if tab_index >= 0:
			self.hide_all_terminal()
			self.show_terminal_func[index][tab_index]()

	def nested_tab_switch_action(self, index):
		'''Action whan tabs are switch between the same tab

		Args:
			index (int): tab index
		'''
		module_bar_index = self.module_bar.currentIndex()
		if index < len(self.show_terminal_func[module_bar_index]):
			self.hide_all_terminal()
			self.show_terminal_func[module_bar_index][index]()


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

		self.init_threat_model(threat_model, self.main.completer)

	def open_model_button_action(self):
		'''Loads a saved ThreatModel instance from a file
		'''

		if not self.threat_model.saved:
			response = QMessageBox.question(self, "Quiting", "Save Threat Model before closing?", QMessageBox.Cancel | QMessageBox.No | QMessageBox.Yes, QMessageBox.No)

			if response == QMessageBox.Cancel:
				return
			elif response == QMessageBox.Yes:
				self.save_model_button_action()

		filepath, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Threat Model", "", filter="Threat Model obj (*" + MainGui.extension + ")")

		if not filepath:
			return

		threat_model = None
		try:
			threat_model = self.main.open_threat_model(filepath)
			self.statusbar.showMessage("Opened: "+filepath)
		except PersistenceException as e:
			Message.print_message(MsgType.ERROR, "Could not open Threat Model " + filepath + ". " + str(e))
			Message.show_message_box(self, MsgType.ERROR, "Could not open Threat Model " + filepath + ". " + str(e))
			return

		self.init_threat_model(threat_model, self.main.completer)

	def save_model_button_action(self):
		'''Try saving to an already used file if not - call save as
		Overwrites previously saved file
		'''

		if self.threat_model.save_file:
			self.general_gui_save(self.threat_model.save_file)
		else:
			self.save_as_model_button_action()


	def save_as_model_button_action(self):
		'''Saves current ThreatModel instance to a file (as user specified file)
		Not overwriting previously saved file
		'''

		filepath, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Threat Model", "", filter="Threat Model obj (*" + MainGui.extension + ")")

		if not filepath:
			return

		filepath += MainGui.extension if not filepath.endswith(MainGui.extension) else ""

		self.general_gui_save(filepath)

	def general_gui_save(self, filepath):
		'''Called by both 'Save' and 'Save as'
		'''

		self.threat_model.saved = True
		try:
			self.main.save_threat_model(filepath, self.threat_model)
			self.threat_model.save_file = filepath
			self.statusbar.showMessage("Saved as: "+filepath)
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

	def export_json_button_action(self):
		'''Exports current threat model as json file
		'''

		json_extension = ".json"
		filepath, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Export Threat Model", "", filter="*.json")

		if not filepath:
			return

		filepath += json_extension if not (filepath.endswith(json_extension)) else ""

		try:
			self.main.export_json(filepath, self.threat_model)
			self.statusbar.showMessage("Threat model exported as: "+filepath)
		except PersistenceException as e:
			Message.print_message(MsgType.ERROR, "Could not export Threat Model as " + filepath + ". " + str(e))
			Message.show_message_box(self, MsgType.ERROR, "Could not export Threat Model as " + filepath + ". " + str(e))
			self.threat_model.saved = False
			return

		Message.show_message_box(self, MsgType.INFO, "Threat Model exported successfully")

	def about_button_action(self):
		'''Open About window
		'''

		Message.show_message_box(self, MsgType.INFO, "Electronics and Computer Science \nUniversity of Southampton \n\nSarunas Iljeitis \n2019 \n\nPart III Individual Project \n\nInternet of Things (IoT) \nPenetration Testing Toolset")

