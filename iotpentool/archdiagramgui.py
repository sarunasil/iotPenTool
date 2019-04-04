#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
file to deal with Architectural diagram tab
covers View and Controller

By sarunasil
"""

import os
from collections import OrderedDict
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

from iotpentool.utils import *


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
ARCHDIAGRAM_GUI_FILEPATH = os.path.join(CURRENT_DIR, "gui/arch_diagram.ui")

Ui_MainWindow, QtBaseClass = uic.loadUiType(ARCHDIAGRAM_GUI_FILEPATH)

class ArchDiagramGui(QtWidgets.QWidget, Ui_MainWindow):
	'''Displays link to architectural diagram
	'''

	def __init__(self, controller):
		'''Init
		'''
		QtWidgets.QWidget.__init__(self)

		#Load gui
		Ui_MainWindow.__init__(self)
		self.setupUi(self)

		self.suggested_link_label.setText("<a href='"+controller.architectural_diagram_site+"'>"+controller.architectural_diagram_site+"</a>")

		self.style = ""#TODO
		self.controller = controller

		#set values from loaded threat
		self.link_input_box.setPlainText(controller.architectural_diagram)
		urlLink="<a href='"+controller.architectural_diagram+"'>Link to Architectural diagram</a>"
		self.link_label.setText(urlLink)


		self.link_input_box.textChanged.connect(lambda: controller.save_link(self.link_input_box.toPlainText()))
		self.link_input_box.mousePressEvent = self.add_start

	def add_start(self, event):
		QtWidgets.QPlainTextEdit.mousePressEvent(self.link_input_box, event)

		if self.link_input_box.toPlainText() == "":
			self.link_input_box.setPlainText("https://")
			self.link_input_box.moveCursor(QtGui.QTextCursor.End)


class ArchDiagramController():
	'''ArchDiagramGui action controller
	'''
	def __init__(self, threat_model_controller, architectural_diagram_site, architectural_diagram):
		'''Init
		'''

		self.threat_model_controller = threat_model_controller
		self.architectural_diagram_site = architectural_diagram_site
		self.architectural_diagram = architectural_diagram
		self.arch_diagram_gui = ArchDiagramGui(self)


	def save_link(self, new_link):
		urlLink="<a href='"+new_link+"'>Link to Architectural diagram</a>"
		self.threat_model_controller.threat_model.architectural_diagram = new_link
		self.threat_model_controller.threat_model.saved = False
		self.arch_diagram_gui.link_label.setText(urlLink)

