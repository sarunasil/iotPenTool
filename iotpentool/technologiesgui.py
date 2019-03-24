#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
file to deal with Technologies tab gui
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
TECHNOLOGY_GUI_FILEPATH = os.path.join(CURRENT_DIR, "gui/technologies.ui")

Ui_MainWindow, QtBaseClass = uic.loadUiType(TECHNOLOGY_GUI_FILEPATH)

class TechnologiesGui(QtWidgets.QWidget, Ui_MainWindow):
	'''Gui for adding new technologies and adding asssets ref to them
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


class TechnologiesController():
	'''TechnologiesGui action controller
	'''
	def __init__(self, threat_model_controller, technologies, assets):
		'''Init
		'''

		self.threat_model_controller = threat_model_controller
		self.technologies = technologies
		self.technologies_gui = TechnologiesGui(self)


		# self.add_btn.pressed.connect(self.add_new_asset)

	def add_new_asset(self):
		'''add_btn action of adding new Asset from gui
		'''

		name = self.assets_gui.name_input_box.text()
		desc = self.assets_gui.description_input_box.toPlainText()

		if not name or not desc:
			Message.show_message_box(self.assets_gui, MsgType.INFO, "Can not add Asset without name or description")
			return

		try:
			asset = self.threat_model_controller.threat_model.add_asset(name, desc)

			self.assets_gui.add_asset_entry(asset)

			self.assets_gui.name_input_box.clear()
			self.assets_gui.description_input_box.clear()
		except ModellingException as e:
			Message.show_message_box(self.assets_gui, MsgType.INFO, str(e))
			Message.print_message(MsgType.INFO, str(e))

	def get_history(self):
		'''Gets known assets from the cache file

		Returns:
			dict(String:String): asset_name : asset_description
		'''

		file = self.threat_model_controller.threat_model.assets_file
		assets = {}
		try:
			assets = Asset.fetch_known_assets(file)
		except ModellingException as e:
			Message.show_message_box(self.assets_gui, MsgType.ERROR, str(e))
			Message.print_message(MsgType.ERROR, str(e))
		return assets

	def fill_from_history(self):
		'''add_history_btn action for adding new asset from dropdown list in gui
		'''
		name = self.assets_gui.history_combo_box.currentText()
		desc = self.assets_gui.history_combo_box.currentData()

		if not name or not desc:
			return

		self.assets_gui.name_input_box.setText(name)
		self.assets_gui.description_input_box.setPlainText(desc)

	def delete_asset(self, asset):
		'''Action called when delete button is clicked of a particular asset entry

		Args:
			asset (Asset): Asset to delete
		'''

		self.threat_model_controller.threat_model.delete_asset(asset)
		self.assets_gui.delete_asset_entry(asset)
