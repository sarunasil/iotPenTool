#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
file to deal with Ranking tab gui
cover View and Controller

By sarunasil
"""

import os
from ruamel import yaml
from collections import OrderedDict
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5 import QtCore, Qt

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

		self.display_list_widget.itemActivated.connect(self.edit_threat)
		self.del_threat_button.clicked.connect(self.delete_threat_entry)
		self.investigate_button.clicked.connect(self.investigate_threat)

		#load all assets to gui if any:
		for _, threat in self.controller.threats.items():
			self.add_threat_entry(threat)


	def add_threat_entry(self, threat):
		'''Add new entry to gui
		'''
		style = ""

		widget = QtWidgets.QWidget()
		widget.setObjectName("threat_"+threat.uid)
		layout = QtWidgets.QHBoxLayout()
		layout.setContentsMargins(2,2,2,2)
		layout.setSpacing(10)

		score_lbl = QtWidgets.QLabel(str(threat.dread.total))
		score_lbl.setObjectName("score_"+threat.uid)
		score_lbl.setWordWrap(True)
		layout.addWidget(score_lbl)

		desc_lbl = QtWidgets.QLabel(threat.description)
		desc_lbl.setObjectName("description_"+threat.uid)
		desc_lbl.setWordWrap(True)
		layout.addWidget(desc_lbl)

		widget.setLayout(layout)
		# widget.setToolTip(value.description)

		if style:
			widget.setStyleSheet(style)


		new_item = QtWidgets.QListWidgetItem()
		new_item.setSizeHint(widget.sizeHint())

		#edit existing item
		for index in range(0,self.display_list_widget.count()):
			item = self.display_list_widget.item(index)

			widget_in_list = self.display_list_widget.itemWidget(item)
			if widget.objectName() == widget_in_list.objectName():
				self.display_list_widget.setItemWidget(item, widget)
				self.sort_threats()
				return

		self.display_list_widget.addItem(new_item)
		self.display_list_widget.setItemWidget(new_item, widget)
		self.sort_threats()

	def sort_threats(self):
		'''For some unknown reason qlistwidget can only be sorted by items...
		As I am trying to sort by itemwidget label value, this ugly peace of code
		came to existance.

		What it's doing is actually dumb the whole display_list_widget info
		into a tuple list, clears display_list_widget items,
		sorts it according to score and the recreates the display_list_widget content
		'''

		def get_score(widget):
			labels = widget.findChildren(QtWidgets.QLabel)
			for l in labels:
				if "score_" in l.objectName():
					return int(l.text())
			return 0

		def get_desc(widget):
			labels = widget.findChildren(QtWidgets.QLabel)
			for l in labels:
				if "description_" in l.objectName():
					return l.text()
			return 0

		def recreate(uid, score, desc):
			'''Copy paste from add_threat_entry
			'''

			style = ""

			widget = QtWidgets.QWidget()
			widget.setObjectName("threat_"+uid)
			layout = QtWidgets.QHBoxLayout()
			layout.setContentsMargins(2,2,2,2)
			layout.setSpacing(10)

			score_lbl = QtWidgets.QLabel(str(score))
			score_lbl.setObjectName("score_"+uid)
			score_lbl.setWordWrap(True)
			layout.addWidget(score_lbl)

			desc_lbl = QtWidgets.QLabel(desc)
			desc_lbl.setObjectName("description_"+uid)
			desc_lbl.setWordWrap(True)
			layout.addWidget(desc_lbl)

			widget.setLayout(layout)
			# widget.setToolTip(value.description)

			if style:
				widget.setStyleSheet(style)

			new_item = QtWidgets.QListWidgetItem()
			new_item.setSizeHint(widget.sizeHint())

			self.display_list_widget.addItem(new_item)
			self.display_list_widget.setItemWidget(new_item, widget)

		content = []
		for index in range(0,self.display_list_widget.count()):
			item = self.display_list_widget.item(index)
			widget = self.display_list_widget.itemWidget(item)
			score = get_score(widget)
			desc = get_desc(widget)
			uid = widget.objectName().replace("threat_","",1)

			content.append( (score, desc, uid) )

		self.display_list_widget.clear()
		content = sorted(content, key=lambda tup: tup[0], reverse=True)

		for score, desc, uid in content:
			recreate(uid, score, desc)

	def edit_threat(self, item):
		'''Selects threat to be edited from display_list_widget

		Args:
			item (QListWidgetItem): selected item
		'''

		uid = self.display_list_widget.itemWidget(item).objectName().replace("threat_","",1)
		self.controller.edit_threat(uid)

	def delete_threat_entry(self):
		'''Removes Threat from gui
		'''
		selected_items = self.display_list_widget.selectedItems()
		for item in selected_items:
			threat_uid = self.display_list_widget.itemWidget( self.display_list_widget.currentItem() ).objectName().replace("threat_","",1)
			self.controller.delete_threat( threat_uid )
			self.display_list_widget.takeItem(self.display_list_widget.row(item))

		#clear selection
		self.display_list_widget.clearSelection()

	def investigate_threat(self):
		'''Call completer for selected threat
		'''

		selected_items = self.display_list_widget.selectedItems()
		for item in selected_items:
			threat_uid = self.display_list_widget.itemWidget( self.display_list_widget.currentItem() ).objectName().replace("threat_","",1)

			self.controller.investigate_threat(threat_uid)

			return


class RankingController():
	'''RankingGui action controller
	'''
	def __init__(self, threat_model_controller, threats, technologies, entry_points, completer):
		'''Ranking tab controller

		Args:
			threat_model_controller (ThreatModelController): callback
			threats (dict(String:Threat)): Model threats
			technologies (dict(String:Technology)): Model technologies
			entry_points (dict(String:EntryPoint)): Model entry points
			completer (Completer): Completer object to work on "Investigate button"
		'''


		self.threat_model_controller = threat_model_controller
		self.threats = threats
		self.technologies = technologies
		self.entry_points = entry_points
		self.completer = completer
		self.ranking_gui = RankingGui(self)

		self.threat_controllers = []

		self.ranking_gui.add_threat_button.clicked.connect(self.open_new_threat_window)

	def open_new_threat_window(self):
		self.threat_controllers.append(ThreatController(self, self.entry_points, self.technologies))

	def delete_threat_controller(self, threat_controller):
		self.threat_controllers.remove(threat_controller)

	def add_threat(self, desc, target, attack_tech, counter, entry_point, technologies, score, uid):
		'''Try to new threat object entry

		Args:
			desc (String):
			target (String):
			attack_tech (String):
			counter (String):
			entry_point (EntryPoint):
			technologies (dict(String:Technology)):
			score (list[int]): list of all 5 categories in THAT order (as in the book)
			uid (String): not None if this is a Threat update
		'''

		try:
			threat = self.threat_model_controller.threat_model.add_threat(desc, target, attack_tech, counter, entry_point, technologies, score, uid)
			self.ranking_gui.add_threat_entry(threat)
		except ModellingException as e:
			Message.show_message_box(self.ranking_gui, MsgType.INFO, str(e))
			Message.print_message(MsgType.INFO, str(e))

			return Outcome.FAILURE

		return Outcome.SUCCESS

	def edit_threat(self, uid):
		'''Create ThreatGui window for threat of given uid

		Args:
			uid (int): threat id in threats 
		'''

		self.threat_controllers.append(ThreatController(self, self.entry_points, self.technologies, threat=self.threats[uid]))


	def delete_threat(self, uid):
		'''Action called when delete button is clicked, called by View delete method

		Args:
			uid (String): id of threat to delete
		'''

		self.threat_model_controller.threat_model.delete_threat(self.threats[uid])

	def investigate_threat(self, uid):
		'''Action called when 'Investigate' button is clicked, called by View Investigate method

		Args:
			uid (String): id of threat to investigate
		'''

		self.completer.generateSuggestions(self.threats[uid])
		self.completer.updateCompleters()
