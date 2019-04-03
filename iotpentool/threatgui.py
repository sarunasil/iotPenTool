#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
file to deal with Threat window gui
cover View and Controller

By sarunasil
"""

import os
from collections import OrderedDict
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from iotpentool.utils import *
from iotpentool.combobox import ComboBox


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
THREAT_GUI_FILEPATH = os.path.join(CURRENT_DIR, "gui/threat.ui")

Ui_MainWindow, QtBaseClass = uic.loadUiType(THREAT_GUI_FILEPATH)

class ThreatGui(QtWidgets.QMainWindow, Ui_MainWindow):

	def __init__(self, controller, threat):
		'''Init
		'''
		QtWidgets.QMainWindow.__init__(self, parent = controller.ranking_controller.ranking_gui)

		Ui_MainWindow.__init__(self)
		self.setupUi(self)

		self.style = ""
		self.controller = controller

		self.entry_points_combobox = ComboBox()
		self.details_widget.layout().insertWidget(5, self.entry_points_combobox)
		self.entry_points_combobox.popupAboutToBeShown.connect(self.fill_entry_points_combobox)
		self.entry_points_combobox.currentIndexChanged.connect(self.add_checkable_technologies)

		self.technologies_buttons = {}

		self.damage_spin_box.valueChanged.connect(self.sum_score)
		self.reproducibility_spin_box.valueChanged.connect(self.sum_score)
		self.exploitability_spin_box.valueChanged.connect(self.sum_score)
		self.affected_spin_box.valueChanged.connect(self.sum_score)
		self.discoverability_spin_box.valueChanged.connect(self.sum_score)

		self.save_button.clicked.connect(self.save_threat)

		if threat:
			self.fill(threat)

	def closeEvent(self, event):
		self.controller.delete_ref()
		event.accept()

	def fill(self, threat):
		self.description_text_box.setPlainText(threat.description)
		self.target_text_box.setText(threat.target)
		self.attack_techniques_text_box.setPlainText(threat.attack_tech)
		self.countermeasures_text_box.setPlainText(threat.countermeasures)

		self.fill_entry_points_combobox()
		index = self.entry_points_combobox.findText(threat.entry_point_used.name)
		if index >= 0:
			self.entry_points_combobox.setCurrentIndex(index)
		else:
			Message.show_message_box(self, MsgType.WARNING, "Entry Point with such name does not exist any more, thus can not be loaded.")

		# self.add_checkable_technologies(index)
		self.check_checkable_technologies(threat.technologies_used)

		self.damage_spin_box.setValue(threat.dread.damage)
		self.reproducibility_spin_box.setValue(threat.dread.reproducibility)
		self.exploitability_spin_box.setValue(threat.dread.exploitability)
		self.affected_spin_box.setValue(threat.dread.affected_users)
		self.discoverability_spin_box.setValue(threat.dread.discoverability)



	# DREAD RATING

	def sum_score(self):
		score = self.damage_spin_box.value() + self.reproducibility_spin_box.value() + self.exploitability_spin_box.value() + self.affected_spin_box.value() + self.discoverability_spin_box.value()

		self.rating_score_total_label.setText(str(score))

		self.risk_rating(score)

		return score

	def risk_rating(self, score):
		if score >= 12:
			self.rating_score_label.setText("HIGH")
		elif score >= 8:
			self.rating_score_label.setText("MEDIUM")
		elif score >= 1:
			self.rating_score_label.setText("LOW")
		else:
			self.rating_score_label.setText("")

	# THREAT

	def save_threat(self):
		desc = self.description_text_box.toPlainText()
		target = self.target_text_box.text()
		attack_tech = self.attack_techniques_text_box.toPlainText()
		counter = self.countermeasures_text_box.toPlainText()
		entry_point = self.entry_points_combobox.currentData()
		technologies = self.controller.get_selected_technologies()
		dread_score = [self.damage_spin_box.value(), self.reproducibility_spin_box.value(), self.exploitability_spin_box.value(), self.affected_spin_box.value(), self.discoverability_spin_box.value()]

		if not desc or not entry_point:
			Message.show_message_box(self, MsgType.INFO, "Can not add threat without minimal information: description and entry point.")
			return

		self.controller.save_threat(desc, target, attack_tech, counter, entry_point, technologies, dread_score)


	# ENTRY POINT

	def fill_entry_points_combobox(self):
		'''Fills the EntryPoint selection combobox
		'''
		self.entry_points_combobox.clear()
		for name, entry_point in self.controller.get_entry_points().items():
			self.entry_points_combobox.addItem(name, entry_point)


	# TECHNOLOGIES

	def get_selected_technologies_names(self):
		'''Gathers selected Technologies names from buttons

		Returns:
			list(String): selected buttons names
		'''

		tech_names = []
		for tech_name, btn in self.technologies_buttons.items():
			if btn.isChecked():
				tech_names.append(tech_name)
		return tech_names

	def add_checkable_technologies(self, entry_point_index):
		'''Populate checkable buttons (for Technologies)  widget with checkable buttons.
		3 buttons in each row

		Args:
			entry_point_index (int): index of entry_points_combobox item currently selected
		'''

		entry_point = self.entry_points_combobox.itemData(entry_point_index)
		if not entry_point:
			return


		#clear prev widgets
		for widget in self.technologies_scroll_area_widget.children():
			if not isinstance(widget, QtWidgets.QGridLayout):
				widget.deleteLater()
		self.technologies_buttons.clear()

		possible_technologies = self.controller.get_possible_technologies(entry_point)
		row = 0
		column = 0
		for tech_name in possible_technologies:
			if column >= 3:
				column = 0
				row += 1

			btn = QtWidgets.QPushButton()
			btn.setCheckable(True)
			btn.setText(tech_name)
			btn.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
			self.technologies_scroll_area_widget.layout().addWidget(btn, row, column)

			self.technologies_buttons[tech_name] = btn

			column +=1

	def check_checkable_technologies(self, technologies):
		'''Used or restoring state of the form as it was from saved state

		Args:
			technologies (dict(String:Technology)): Checked technologies
		'''
		self.reset_checkable_technologies()

		if not self.technologies_buttons:
			return

		for button_name, button in self.technologies_buttons.items():
			if button_name in technologies:
				button.setChecked(True)

	def reset_checkable_technologies(self):
		'''Clear buttons
		'''

		for _, btn in self.technologies_buttons.items():
			btn.setChecked(False)


class ThreatController():
	'''RankingGui action controller
	'''
	def __init__(self, ranking_controller, entry_points, technologies, threat=None):
		'''Init
		'''

		self.ranking_controller = ranking_controller
		self.used_entry_points = entry_points
		self.used_technologies = technologies

		self.uid = None if not threat else threat.uid
		self.threat_gui = ThreatGui(self, threat)

		self.threat_gui.show()

		# self.threats_gui.add_threat_button.clicked.connect(self.open_new_threat_window)

	def delete_ref(self):
		'''Delete this ThreatController from ranking_controller list of ThreatControllers
		'''

		self.ranking_controller.delete_threat_controller(self)

	def get_selected_technologies(self):
		'''Gathers selected Technologies objects for this Threat

		Returns:
			dict(String:Technology):
		'''

		technologies = {}
		for tech_name in self.threat_gui.get_selected_technologies_names():
			if tech_name in self.used_technologies:
				technologies[tech_name] = self.used_technologies[tech_name]

		return technologies

	def save_threat(self, desc, target, attack_tech, counter, entry_point, technologies, score):
		'''Try to save threat entry by forwarding data to ranking_controller
		If outcome == SUCCESS - close the window
		else display warning message

		Args:
			desc (String):
			target (String):
			attack_tech (String):
			counter (String):
			entry_point (EntryPoint):
			technologies (dict(String:Technology)):
			score (list[int]): list of all 5 categories in THAT order (as in the book)
		'''

		outcome = self.ranking_controller.add_threat(desc, target, attack_tech, counter, entry_point, technologies, score, self.uid)

		if outcome == Outcome.SUCCESS:
			self.threat_gui.close()
		else:
			Message.show_message_box(self, MsgType.WARNING, "Failed to save threat.")
			Message.print_message(MsgType.WARNING, "Failed to save threat.")

	def get_entry_points(self):
		return self.used_entry_points

	def get_possible_technologies(self, entry_point):
		'''Return only those technologies which are used in the entry_points asset

		Args:
			entry_point (EntryPoint):

		Returns:
			dict(String:Technology):
		'''

		tech = {}
		for tech_name, technology in self.used_technologies.items():
			if entry_point.asset_used.name in technology.used_in:
				tech[tech_name] = technology

		return tech

