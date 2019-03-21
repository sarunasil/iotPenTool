#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
class to deal with Threat Model interface generation and
responsibility separation via Model<->Controller<->View

By sarunasil
"""

import uuid
import os
from collections import OrderedDict
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from iotpentool.vtabwidget import TabWidget
from iotpentool.line import QHLine

from iotpentool.assetsgui import AssetsController


class ThreatModelGui(QtWidgets.QTabWidget):
	'''Deals with module gui which is generated from ThreatModel data
	'''

	def __init__(self, controller, assets_gui):
		'''Init
		'''
		super().__init__()
		self.style = ""#TODO
		self.controller = controller
		self.assets_gui = assets_gui
		self.technologies = {}

		self.initUI()

	def initUI(self):
		'''Function to move GUI creation from __init__
		'''
		self.setMaximumWidth(500)

		if self.style:
			self.setStyleSheet(self.style)

		# self.setObjectName("widget_interface")
		# layout = QtWidgets.QVBoxLayout()
		# layout.setContentsMargins(0,0,0,0)
		# layout.setSpacing(0)

		test = QtWidgets.QTabWidget()#(direction=QtWidgets.QTabWidget.East)
		test.addTab(QtWidgets.QWidget(), "Stub1") #adds generated guis to TabWidget
		test.addTab(QtWidgets.QWidget(), "Stub2") 
		test.addTab(QtWidgets.QWidget(), "Stub3") 

 		#adds generated guis to TabWidget
		self.addTab(self.assets_gui, "Assets")
		self.addTab(test, "TEST")
		self.addTab(QtWidgets.QWidget(), "Arch. diagram")
		self.addTab(QtWidgets.QWidget(), "Technologies")
		self.addTab(QtWidgets.QWidget(), "Technologies")

		# self.setLayout(layout)


class ThreatModelController():
	'''ThreatModelGui action controller
	'''
	def __init__(self, threat_model):
		'''Init
		'''
		self.assets_controller = AssetsController(self, threat_model.assets)
		# self.technologies_gui = TechnologiesController(threat_model.technologies)
		# self.entry_points_gui = EntryPointsController(threat_model.entry_points)
		# self.technologies_gui = TechnologiesController(threat_model.technologies)

		self.threat_model = threat_model
		self.threat_model_gui = ThreatModelGui(self, self.assets_controller.assets_gui)

