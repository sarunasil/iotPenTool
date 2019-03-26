#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
file to deal with Threat window gui
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
THREAT_GUI_FILEPATH = os.path.join(CURRENT_DIR, "gui/threat.ui")

Ui_MainWindow, QtBaseClass = uic.loadUiType(THREAT_GUI_FILEPATH)

class ThreatGui(QtWidgets.QMainWindow, Ui_MainWindow):

	def __init__(self, controller, threat):
		'''Init
		'''
		QtWidgets.QMainWindow.__init__(self)

		Ui_MainWindow.__init__(self)
		self.setupUi(self)

		self.style = ""
		self.controller = controller

class ThreatController():
	'''RankingGui action controller
	'''
	def __init__(self, ranking_controller, threat):
		'''Init
		'''

		self.ranking_controller = ranking_controller
		self.threat = threat
		self.threat_gui = ThreatGui(self, self.threat)

		self.threat_gui.show()

		# self.threats_gui.add_threat_button.pressed.connect(self.open_new_threat_window)

	# def open_new_threat_window(self):

	# 	self.threat_details = ThreatDetails(self)
	# 	self.threat_details.show()
