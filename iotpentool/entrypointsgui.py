#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
file to deal with EntryPoints tab gui
cover View and Controller

By sarunasil
"""

import uuid
import os
from collections import OrderedDict
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from iotpentool.utils import *


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
ENTRYPOINT_GUI_FILEPATH = os.path.join(CURRENT_DIR, "gui/entry_points.ui")

Ui_MainWindow, QtBaseClass = uic.loadUiType(ENTRYPOINT_GUI_FILEPATH)

class ComboBox(QtWidgets.QComboBox):
	popupAboutToBeShown = QtCore.pyqtSignal()

	def showPopup(self):
		self.popupAboutToBeShown.emit()
		super(ComboBox, self).showPopup()

class EntryPointsGui(QtWidgets.QWidget, Ui_MainWindow):
	'''Gui for adding system entry points and
	referencing an existing Asset it is present in
	'''

	def __init__(self, controller):
		'''Init
		'''
		QtWidgets.QWidget.__init__(self)

		#Load gui
		Ui_MainWindow.__init__(self)
		self.setupUi(self)


		self.style = ""#TODO
		self.controller = controller

		self.history_combo_box = ComboBox()
		self.history_widget.layout().insertWidget(0, self.history_combo_box)

	def fill_history_combobox(self):
		'''Populate history combobox with Entry Points from history
		'''
		pass

	def fill_from_history(self):
		'''Selecting item from combobox action for adding new entry point from dropdown list in gui
		'''
		pass

	def fill_from_item(self, item):
		'''For editing entered entry point entries

		Args:
			item (QListWidgetItem): selected item
		'''
		pass


	#ENTRY POINT ENTRY

	def add_entry_point_entry(self, entry_point):
		'''Add new entry to gui
		'''
		pass

	def delete_entry_point_entry(self):
		'''Removes EntryPoint from gui
		'''
		pass

	def cleanup(self):
		pass


	#ASSETS COMBOBOX

	def fill_assets_combobox(self, used_assets):
		'''Populate assets combobox
		'''
		pass

class EntryPointsController():
	'''EntryPointsGui action controller
	'''
	def __init__(self, threat_model_controller, entry_points, used_assets):
		'''Init
		'''

		self.threat_model_controller = threat_model_controller
		self.entry_points = entry_points
		self.used_assets = used_assets
		self.entry_points_gui = EntryPointsGui(self)


		# self.add_btn.pressed.connect(self.add_new_asset)

	def add_new_entry_point(self):
		'''Add new EntryPoint to from gui
		'''
		pass

	def delete_entry_point(self, entry_point):
		'''Action called than delete button is clicked, called by View delete method

		Args:
			entry_point (EntryPoint): Entry point to delete
		'''


	def get_history(self):
		'''Get known EntryPoints from cache file

		Returns:
			dict(String:String): entry_point_name : entry_point:desc
		'''

		return None

	def refresh_assets_combobox(self):
		self.entry_points_gui.fill_assets_combobox(self.used_assets)


