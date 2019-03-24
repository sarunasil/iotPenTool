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
ARCHDIAGRAM_GUI_FILEPATH = os.path.join(CURRENT_DIR, "gui/technologies.ui")

Ui_MainWindow, QtBaseClass = uic.loadUiType(ARCHDIAGRAM_GUI_FILEPATH)

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

