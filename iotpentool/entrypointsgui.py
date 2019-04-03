#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
file to deal with EntryPoints tab gui
cover View and Controller

By sarunasil
"""

import os
from collections import OrderedDict
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from iotpentool.utils import *
from iotpentool.entrypoint import EntryPoint
from iotpentool.combobox import ComboBox


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
ENTRYPOINT_GUI_FILEPATH = os.path.join(CURRENT_DIR, "gui/entry_points.ui")

Ui_MainWindow, QtBaseClass = uic.loadUiType(ENTRYPOINT_GUI_FILEPATH)

class EntryPointsGui(QtWidgets.QWidget, Ui_MainWindow):
	'''Gui for adding system entry points and
	referencing an existing Asset it is present in
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

		self.assets_combo_box = ComboBox()
		self.assets_widget.layout().insertWidget(0, self.assets_combo_box, 1)
		self.assets_combo_box.popupAboutToBeShown.connect(self.fill_assets_combobox)

		self.history_combo_box.popupAboutToBeShown.connect(self.fill_history_combobox)
		self.history_combo_box.currentTextChanged.connect(self.fill_from_history)
		self.del_button.clicked.connect(self.delete_entry_point_entry)
		self.display_list_widget.itemActivated.connect(self.fill_from_item)

		#load all present entry_points to gui if any:
		for _, entry_point in self.controller.entry_points.items():
			self.add_entry_point_entry(entry_point)


	def fill_history_combobox(self):
		'''Populate history combobox with Entry Points from history
		'''
		#clear selection
		self.display_list_widget.clearSelection()

		self.history_combo_box.clear()
		for name, desc in self.controller.get_history().items():
			self.history_combo_box.addItem(name, desc)

	def fill_from_history(self):
		'''Selecting item from combobox action for adding new entry point from dropdown list in gui
		'''
		name = self.history_combo_box.currentText()
		desc = self.history_combo_box.currentData()

		if not name or not desc:
			return

		self.name_input_box.setText(name)
		self.description_input_box.setPlainText(desc)

	def fill_from_item(self, item):
		'''For editing entered entry point entries

		Args:
			item (QListWidgetItem): selected item
		'''
		labels = self.display_list_widget.itemWidget( item ).findChildren(QtWidgets.QLabel)
		for l in labels:
			if l.objectName().startswith("name_"):
				self.name_input_box.setText(l.text())
			elif l.objectName().startswith("description_"):
				self.description_input_box.setPlainText(l.text())
			elif l.objectName().startswith("asset_"):
				self.fill_assets_combobox()
				index = self.assets_combo_box.findText(l.text())
				if index >= 0:
					self.assets_combo_box.setCurrentIndex(index)
				else:
					Message.show_message_box(self, MsgType.WARNING, "Asset with such name does not exist any more, thus can not be loaded.")


	#ENTRY POINT ENTRY

	def add_entry_point_entry(self, entry_point):
		'''Add new entry to gui
		'''

		style = ""

		widget = QtWidgets.QWidget()
		widget.setObjectName("entry_"+entry_point.name)
		layout = QtWidgets.QHBoxLayout()
		layout.setContentsMargins(2,2,2,2)
		layout.setSpacing(10)

		name_lbl = QtWidgets.QLabel(entry_point.name)
		name_lbl.setObjectName("name_"+entry_point.name)
		name_lbl.setWordWrap(True)
		layout.addWidget(name_lbl)

		asset_lbl = QtWidgets.QLabel(entry_point.asset_used.name)
		asset_lbl.setObjectName("asset_"+entry_point.asset_used.name)
		asset_lbl.setWordWrap(True)
		layout.addWidget(asset_lbl)

		desc_lbl = QtWidgets.QLabel(entry_point.description)
		desc_lbl.setObjectName("description_"+entry_point.description)
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

	def delete_entry_point_entry(self):
		'''Removes EntryPoint from gui
		'''
		selected_items = self.display_list_widget.selectedItems()
		for item in selected_items:
			entry_point_name = self.display_list_widget.itemWidget( self.display_list_widget.currentItem() ).objectName().replace("entry_","",1)
			self.controller.delete_entry_point( self.controller.entry_points[entry_point_name] )
			self.display_list_widget.takeItem(self.display_list_widget.row(item))

		#clear selection
		self.display_list_widget.clearSelection()

	def cleanup(self):
		self.name_input_box.clear()
		self.description_input_box.clear()
		self.history_combo_box.setCurrentIndex(-1)
		self.assets_combo_box.setCurrentIndex(-1)


	#ASSETS COMBOBOX

	def fill_assets_combobox(self):
		'''Populate assets combobox
		'''
		self.assets_combo_box.clear()
		for asset_name, asset in self.controller.used_assets.items():
			self.assets_combo_box.addItem(asset_name, asset)

	def get_asset(self):
		'''Get Asset from combobox
		'''
		index = self.assets_combo_box.currentIndex()
		return self.assets_combo_box.itemData(index)


class EntryPointsController():
	'''EntryPointsGui action controller
	'''
	def __init__(self, threat_model_controller, entry_points, used_assets):
		'''Init
		'''

		self.threat_model_controller = threat_model_controller
		self.entry_points = entry_points
		self.used_assets = used_assets
		self.entry_points_gui = EntryPointsGui(self)


		self.entry_points_gui.add_button.clicked.connect(self.add_new_entry_point)

	def add_new_entry_point(self):
		'''Add new EntryPoint to from gui
		'''
		name = self.entry_points_gui.name_input_box.text()
		desc = self.entry_points_gui.description_input_box.toPlainText()
		asset = self.entry_points_gui.get_asset()

		if not name or not desc or not asset:
			Message.show_message_box(self.entry_points_gui, MsgType.INFO, "Can not add Entry Point without name, description or Asset it is present in.")
			return

		try:
			entry_point = self.threat_model_controller.threat_model.add_entry_point(name, desc, asset)
			self.entry_points_gui.add_entry_point_entry(entry_point)

			self.entry_points_gui.name_input_box.clear()
			self.entry_points_gui.description_input_box.clear()
		except ModellingException as e:
			Message.show_message_box(self.entry_points_gui, MsgType.INFO, str(e))
			Message.print_message(MsgType.INFO, str(e))

	def delete_entry_point(self, entry_point):
		'''Action called than delete button is clicked, called by View delete method

		Args:
			entry_point (EntryPoint): Entry point to delete
		'''
		self.threat_model_controller.threat_model.delete_entry_point(entry_point)

	def get_history(self):
		'''Get known EntryPoints from cache file

		Returns:
			dict(String:String): entry_point_name : entry_point:desc
		'''

		file = self.threat_model_controller.threat_model.entry_points_file
		entry_points = {}
		try:
			entry_points = EntryPoint.fetch_known_entry_points(file)
		except ModellingException as e:
			Message.show_message_box(self.entry_points_gui, MsgType.ERROR, str(e))
			Message.print_message(MsgType.ERROR, str(e))
		return entry_points


