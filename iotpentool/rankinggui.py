#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
file to deal with Ranking tab gui
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
from iotpentool.threatgui import ThreatController


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
RANKING_GUI_FILEPATH = os.path.join(CURRENT_DIR, "gui/ranking.ui")

Ui_MainWindow, QtBaseClass = uic.loadUiType(RANKING_GUI_FILEPATH)

class RankingGui(QtWidgets.QWidget, Ui_MainWindow):
	'''Gui for ranking threats add viewing high level details
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

class RankingController():
	'''RankingGui action controller
	'''
	def __init__(self, threat_model_controller, threats):
		'''Init
		'''

		self.threat_model_controller = threat_model_controller
		self.threats = threats
		self.threats_gui = RankingGui(self)


		self.threats_gui.add_threat_button.pressed.connect(self.open_new_threat_window)

	def open_new_threat_window(self):

		self.threat_controller = ThreatController(self, None)
