#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
file to deal with Assets tab gui generation
covers View and Controller

By sarunasil
"""

import uuid
import os
from collections import OrderedDict
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from iotpentool.line import QHLine
from iotpentool.utils import *


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
ASSETS_GUI_FILEPATH = os.path.join(CURRENT_DIR, "gui/assets.ui")

Ui_MainWindow, QtBaseClass = uic.loadUiType(ASSETS_GUI_FILEPATH)

class AssetsGui(QtWidgets.QWidget, Ui_MainWindow):
	'''Deals with Assets tab which is generated from Assets data
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


class AssetsController():
	'''AssetsGui action controller
	'''
	def __init__(self, threat_model_controller, assets):
		'''Init
		'''

		self.threat_model_controller = threat_model_controller
		self.assets = assets
		self.assets_gui = AssetsGui(self)

		self.add_btn = self.assets_gui.add_button
		self.add_history_btn = self.assets_gui.add_history_button

		self.add_btn.pressed.connect(self.add_new_asset)
		self.add_history_btn.pressed.connect(self.add_history_asset)

	def add_new_asset(self):
		'''add_btn action of adding new Asset from gui
		'''

		name = self.assets_gui.name_input_box.text()
		desc = self.assets_gui.description_input_box.toPlainText()

		try:
			self.threat_model_controller.threat_model.add_asset(name, desc)

			self.assets_gui.name_input_box.clear()
			self.assets_gui.description_input_box.clear()
		except ModellingException as e:
			Message.show_message_box(self.assets_gui, MsgType.INFO, str(e))
			Message.print_message(MsgType.INFO, str(e))

	def add_history_asset(self):
		'''add_history_btn action for adding new asset from dropdown list in gui
		'''

		pass

	def update_assets_display(self):
		'''Update asset values being displayed
		'''

		pass