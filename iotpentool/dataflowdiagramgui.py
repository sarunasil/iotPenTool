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
ARCHDIAGRAM_GUI_FILEPATH = os.path.join(CURRENT_DIR, "gui/data_flow_diagram.ui")

Ui_MainWindow, QtBaseClass = uic.loadUiType(ARCHDIAGRAM_GUI_FILEPATH)

class DataFlowDiagramGui(QtWidgets.QWidget, Ui_MainWindow):
	'''Gui for adding new technologies and adding asssets ref to them
	'''

	def __init__(self, controller):
		'''Init
		'''
		QtWidgets.QWidget.__init__(self)

		#Load gui
		Ui_MainWindow.__init__(self)
		self.setupUi(self)

		self.suggested_link_label.setText("<a href='"+controller.data_flow_diagram_site+"'>"+controller.data_flow_diagram_site+"</a>")

		self.style = ""#TODO
		self.controller = controller

		self.link_input_box.textChanged.connect(lambda: controller.save_link(self.link_input_box.toPlainText()))
		self.link_input_box.mousePressEvent = self.add_start

	def add_start(self, event):
		QtWidgets.QPlainTextEdit.mousePressEvent(self.link_input_box, event)

		if self.link_input_box.toPlainText() == "":
			self.link_input_box.setPlainText("https://")


class DataFlowDiagramController():
	'''Data Flow Diagram tab action controller
	'''
	def __init__(self, threat_model_controller, data_flow_diagram_site, data_flow_diagram):
		'''Init
		'''

		self.threat_model_controller = threat_model_controller
		self.data_flow_diagram_site = data_flow_diagram_site
		self.data_flow_diagram = data_flow_diagram
		self.data_flow_diagram_gui = DataFlowDiagramGui(self)

	def save_link(self, new_link):
		urlLink="<a href='"+new_link+"'>Link to Data Flow diagram</a>"
		self.threat_model_controller.threat_model.architectural_diagram = new_link
		self.data_flow_diagram_gui.link_label.setText(urlLink)


