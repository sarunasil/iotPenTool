#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
class to deal with Threat Model interface generation and
responsibility separation via Model<->Controller<->View

By sarunasil
"""

import os
from collections import OrderedDict
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from iotpentool.vtabwidget import TabWidget

from iotpentool.assetsgui import AssetsController
from iotpentool.archdiagramgui import ArchDiagramController
from iotpentool.technologiesgui import TechnologiesController
from iotpentool.dataflowdiagramgui import DataFlowDiagramController
from iotpentool.entrypointsgui import EntryPointsController
from iotpentool.rankinggui import RankingController

class ThreatModelGui(QtWidgets.QTabWidget):
	'''Deals with module gui which is generated from ThreatModel data
	'''

	def __init__(self, controller, assets_gui, arch_diagram_gui, technologies_gui, data_flow_diagram_gui, entry_points_gui, ranking_gui):
		'''Init
		'''
		super().__init__()
		self.style = ""#TODO
		self.controller = controller
		self.assets_gui = assets_gui
		self.arch_diagram_gui = arch_diagram_gui
		self.technologies_gui = technologies_gui
		self.data_flow_diagram_gui = data_flow_diagram_gui
		self.entry_points_gui = entry_points_gui
		self.ranking_gui = ranking_gui

		self.initUI()

	def initUI(self):
		'''Function to move GUI creation from __init__
		'''
		self.setMaximumWidth(400)

		if self.style:
			self.setStyleSheet(self.style)

 		#adds generated guis to TabWidget
		self.addTab(self.assets_gui, "Assets")

		architecture_tab = QtWidgets.QTabWidget()#(direction=QtWidgets.QTabWidget.East)
		architecture_tab.addTab(self.arch_diagram_gui, "Architectural Diagram")
		architecture_tab.addTab(self.technologies_gui, "Technologies") 

		self.addTab(architecture_tab, "Architecture")

		decomposition_tab = QtWidgets.QTabWidget()#(direction=QtWidgets.QTabWidget.East)
		decomposition_tab.addTab(self.data_flow_diagram_gui, "Data Flow Diagram")
		decomposition_tab.addTab(self.entry_points_gui, "Entry points")
		self.addTab(decomposition_tab, "Decomposition")
		self.addTab(self.ranking_gui, "Threats")

		#DEV
		self.setCurrentIndex(3)



class ThreatModelController():
	'''ThreatModelGui action controller
	'''
	def __init__(self, threat_model, completer):
		'''Overall threat model controller

		Args:
			threat_model (ThreatModel): threat modelling Model part
			completer (Completer): pass object to RankingController
		'''


		self.assets_controller = AssetsController(self, threat_model.assets)

		self.arch_diagram_controller = ArchDiagramController(self, threat_model.architectural_diagram_site, threat_model.architectural_diagram)

		self.technologies_controller = TechnologiesController(self, threat_model.technologies, threat_model.assets)
		self.assets_controller.assets_gui.assets_updated.connect(self.technologies_controller.refresh_assets)

		self.data_flow_diagram_controller = DataFlowDiagramController(self, threat_model.data_flow_diagram_site, threat_model.data_flow_diagram)

		self.entry_points_controller = EntryPointsController(self, threat_model.entry_points, threat_model.assets)

		self.ranking_controller = RankingController(self, threat_model.threats, threat_model.technologies, threat_model.entry_points, completer)

		self.threat_model = threat_model
		self.threat_model_gui = ThreatModelGui(self,
												self.assets_controller.assets_gui,
												self.arch_diagram_controller.arch_diagram_gui,
												self.technologies_controller.technologies_gui,
												self.data_flow_diagram_controller.data_flow_diagram_gui,
												self.entry_points_controller.entry_points_gui,
												self.ranking_controller.ranking_gui
											)

