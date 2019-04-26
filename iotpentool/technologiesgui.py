#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
file to deal with Technologies tab gui
cover View and Controller

By sarunasil
"""

import os
from collections import OrderedDict
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from iotpentool.utils import *
from iotpentool.technology import Technology
from iotpentool.combobox import ComboBox


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
TECHNOLOGY_GUI_FILEPATH = os.path.join(CURRENT_DIR, "gui/technologies.ui")

Ui_MainWindow, QtBaseClass = uic.loadUiType(TECHNOLOGY_GUI_FILEPATH)

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

		self.history_combo_box = ComboBox()
		self.history_widget.layout().insertWidget(0, self.history_combo_box, 1)

		self.asset_buttons = {}
		self.attributes = {}

		self.history_combo_box.popupAboutToBeShown.connect(self.fill_combobox)
		self.history_combo_box.currentTextChanged.connect(self.fill_from_history)
		self.del_button.clicked.connect(self.delete_technology_entry)
		self.display_list_widget.itemActivated.connect(self.fill_from_item)

		self.add_attribute.clicked.connect(self.add_new_attribute)
		self.del_attribute.clicked.connect(self.delete_attribute)
		self.attributes_list.itemActivated.connect(self.fill_attribute_from_item)

		#load all present technologies to gui if any:
		for _, tech in self.controller.technologies.items():
			self.add_technology_entry(tech)


	def fill_combobox(self):
		'''Populates history combobox with the content Technology cache file
		'''
		#clear selection
		self.display_list_widget.clearSelection()

		self.history_combo_box.clear()
		for name, techn in self.controller.get_history().items():
			self.history_combo_box.addItem(name, techn)

	def fill_from_history(self):
		'''selecting item from combobox action for adding new technology from dropdown list in gui
		'''
		name = self.history_combo_box.currentText()
		technology = self.history_combo_box.currentData()

		if not name or not technology:
			return

		self.name_input_box.setText(name)
		self.description_input_box.setPlainText(technology['description'])
		self.populate_attributes(technology['attributes'])

	def fill_from_item(self, item):
		tech_name = self.display_list_widget.itemWidget( item ).objectName().replace("tech_","",1)
		if tech_name not in self.controller.technologies:
			return #problem has accured

		tech = self.controller.technologies[tech_name]
		self.name_input_box.setText(tech.name)
		self.description_input_box.setPlainText(tech.description)
		self.populate_attributes(tech.attributes)
		self.check_checkable_assets(tech.used_in)

	def add_technology_entry(self, technology):
		'''Adds Technology entry in gui

		Args:
			technology (Technology):
		'''

		style = ""

		widget = QtWidgets.QWidget()
		widget.setObjectName("tech_"+technology.name)
		layout = QtWidgets.QHBoxLayout()
		layout.setContentsMargins(2,2,2,2)
		layout.setSpacing(10)

		name_lbl = QtWidgets.QLabel(technology.name)
		name_lbl.setObjectName("name_"+technology.name)
		layout.addWidget(name_lbl)

		desc_lbl = QtWidgets.QLabel(technology.description)
		desc_lbl.setObjectName("description_"+technology.description)
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
				self.cleanup()
				return

		self.display_list_widget.addItem(new_item)
		self.display_list_widget.setItemWidget(new_item, widget)

		#clear
		self.cleanup()

	def delete_technology_entry(self):
		'''Removes selected Technology entry from gui
		'''

		selected_items = self.display_list_widget.selectedItems()
		for item in selected_items:
			tech_name = self.display_list_widget.itemWidget( item ).objectName().replace("tech_","",1)
			self.controller.delete_technology( self.controller.technologies[tech_name] )
			self.display_list_widget.takeItem(self.display_list_widget.row(item))

		#clear selection
		self.display_list_widget.clearSelection()

	def cleanup(self):
		self.name_input_box.clear()
		self.description_input_box.clear()
		self.history_combo_box.clear()
		self.reset_checkable_assets()
		self.attr_key_text_box.clear()
		self.attr_value_text_box.clear()
		self.attributes_list.clear()
		self.attributes = {}

	#ATTRIBUTES

	def add_new_attribute(self, key=None, value=None):
		'''Adds new attribute entry from input boxes
		'''

		if not key or not value:
			key = self.attr_key_text_box.text()
			value = self.attr_value_text_box.text()

		if not key or not value:
			Message.show_message_box(self, MsgType.INFO, "Can not add Technology attribute without key or value")
			return

		self.attributes[key] = value

		widget = QtWidgets.QWidget()
		widget.setObjectName("attr_"+key)
		layout = QtWidgets.QHBoxLayout()
		layout.setContentsMargins(2,2,2,2)
		layout.setSpacing(10)

		key_lbl = QtWidgets.QLabel(key)
		key_lbl.setObjectName("key_"+key)
		layout.addWidget(key_lbl)

		value_lbl = QtWidgets.QLabel(value)
		value_lbl.setObjectName("value_"+value)
		value_lbl.setWordWrap(True)
		layout.addWidget(value_lbl)

		widget.setLayout(layout)
		# widget.setToolTip(value.description)

		new_item = QtWidgets.QListWidgetItem()
		new_item.setSizeHint(widget.sizeHint())

		#edit existing item
		for index in range(0,self.attributes_list.count()):
			item = self.attributes_list.item(index)

			widget_in_list = self.attributes_list.itemWidget(item)
			if widget.objectName() == widget_in_list.objectName():
				self.attributes_list.setItemWidget(item, widget)
				return

		self.attributes_list.addItem(new_item)
		self.attributes_list.setItemWidget(new_item, widget)

		#cleanup
		self.attr_key_text_box.clear()
		self.attr_value_text_box.clear()

	def delete_attribute(self):
		'''deletes selected attribute(s) from qlistwidget
		'''

		selected_items = self.attributes_list.selectedItems()
		for item in selected_items:
			attr_key = self.attributes_list.itemWidget( item ).objectName().replace("attr_","",1)
			self.attributes.pop(attr_key)
			self.attributes_list.takeItem(self.attributes_list.row(item))

		#clear selection
		self.attributes_list.clearSelection()
		self.attr_key_text_box.clear()
		self.attr_value_text_box.clear()

	def populate_attributes(self, attributes):
		'''Populates attributes qlistwidget with technology attritubutes

		Args:
			attributes (dict(String:String)):
		'''
		self.attributes = {}
		self.attributes_list.clear()

		if not attributes:
			return

		for attr_key, attr_value in attributes.items():
			self.add_new_attribute(attr_key, attr_value)

	def fill_attribute_from_item(self, item):
		'''Used for editing attributes that are placed in qlistwidget

		Args:
			item (QListWidgetItem):
		'''

		labels = self.attributes_list.itemWidget( item ).findChildren(QtWidgets.QLabel)

		for l in labels:
			if "key_" in l.objectName():
				self.attr_key_text_box.setText(l.text())
			elif "value_" in l.objectName():
				self.attr_value_text_box.setText(l.text())


	#ASSETS IN WHICH THIS TECH IS USED

	def get_selected_asset_names(self):
		'''Gathers selected Assets names from buttons

		Returns:
			list(String): selected buttons names
		'''

		asset_names = []
		for asset_name, btn in self.asset_buttons.items():
			if btn.isChecked():
				asset_names.append(asset_name)
		return asset_names

	def add_checkable_assets(self, assets):
		'''Populate checkable buttons (for Assets)  widget with checkable buttons.
		3 buttons in each row

		Args:
			assets (dict(String:Asset)): all Assets of the system
		'''

		#clear prev widgets
		for widget in self.assets_scroll_area_widget.children():
			if not isinstance(widget, QtWidgets.QGridLayout):
				widget.deleteLater()

		row = 0
		column = 0
		for asset_name in assets:
			if column >= 3:
				column = 0
				row += 1

			btn = QtWidgets.QPushButton()
			btn.setCheckable(True)
			btn.setText(asset_name)
			btn.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
			self.assets_scroll_area_widget.layout().addWidget(btn, row, column)

			self.asset_buttons[asset_name] = btn

			column +=1

	def check_checkable_assets(self, assets):
		'''Used or restoring state of the form as it was from saved state

		Args:
			assets (dict(String:Asset)): Checked assets
		'''
		self.reset_checkable_assets()

		if not self.asset_buttons:
			return

		for button_name, button in self.asset_buttons.items():
			if button_name in assets:
				button.setChecked(True)

	def reset_checkable_assets(self):
		'''Clear buttons
		'''

		for _, btn in self.asset_buttons.items():
			if btn:
				btn.setChecked(False)

class TechnologiesController():
	'''TechnologiesGui action controller
	'''
	def __init__(self, threat_model_controller, technologies, used_assets):
		'''Init
		'''

		self.threat_model_controller = threat_model_controller
		self.technologies = technologies
		self.used_assets = used_assets	#assets in the system (in total)
		self.technologies_gui = TechnologiesGui(self)
		self.refresh_assets()


		self.technologies_gui.add_button.clicked.connect(self.add_new_technology)

	def get_selected_assets(self):
		'''Gathers selected Assets objects for this TEchnology

		Returns:
			dict(String:Asset):
		'''

		assets = {}
		for asset_name in self.technologies_gui.get_selected_asset_names():
			if asset_name in self.used_assets:
				assets[asset_name] = self.used_assets[asset_name]

		return assets

	def add_new_technology(self):
		'''add_btn action of adding new Asset from gui
		'''

		name = self.technologies_gui.name_input_box.text()
		desc = self.technologies_gui.description_input_box.toPlainText()
		attributes = self.technologies_gui.attributes
		assets = self.get_selected_assets()

		if not name or not desc:
			Message.show_message_box(self.technologies_gui, MsgType.INFO, "Can not add Technology without name or description")
			return

		try:
			technology = self.threat_model_controller.threat_model.add_technology(name, desc, attributes, assets)
			self.technologies_gui.add_technology_entry(technology)
		except ModellingException as e:
			Message.show_message_box(self.technologies_gui, MsgType.INFO, str(e))
			Message.print_message(MsgType.INFO, str(e))

	def delete_technology(self, technology):
		'''Action called when delete button is clicked, called by View delete method

		Args:
			technology (Technology): Technology to delete
		'''

		self.threat_model_controller.threat_model.delete_technology(technology)

	def get_history(self):
		'''Gets known Technologies from the cache file

		Returns:
			dict(String:dict(String)): tech_name : tech_data
		'''

		file = self.threat_model_controller.threat_model.technologies_file
		technologies = {}
		try:
			technologies = Technology.fetch_known_technologies(file)
		except ModellingException as e:
			Message.show_message_box(self.technologies_gui, MsgType.ERROR, str(e))
			Message.print_message(MsgType.ERROR, str(e))
		return technologies

	def refresh_assets(self):
		self.technologies_gui.add_checkable_assets(self.used_assets)