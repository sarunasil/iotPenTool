#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
file to deal with Assets tab gui generation
covers View and Controller

By sarunasil
"""

import os
from collections import OrderedDict
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from iotpentool.line import QHLine
from iotpentool.utils import *
from iotpentool.asset import Asset
from iotpentool.combobox import ComboBox


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
ASSETS_GUI_FILEPATH = os.path.join(CURRENT_DIR, "gui/assets.ui")

Ui_MainWindow, QtBaseClass = uic.loadUiType(ASSETS_GUI_FILEPATH)


class AssetsGui(QtWidgets.QWidget, Ui_MainWindow):
	'''Deals with Assets tab which is generated from Assets data
	'''

	assets_updated = QtCore.pyqtSignal()

	def __init__(self, controller):
		'''Init
		'''
		QtWidgets.QWidget.__init__(self)

		#Load gui
		Ui_MainWindow.__init__(self)
		self.setupUi(self)


		self.style = ""#TODO
		self.controller = controller
		self.asset_widgets = {}

		self.history_combo_box = ComboBox()
		self.history_widget.layout().insertWidget(0, self.history_combo_box, 1)

		self.history_combo_box.popupAboutToBeShown.connect(self.fill_combobox)
		self.history_combo_box.currentTextChanged.connect(self.fill_from_history)
		self.del_button.clicked.connect(self.delete_asset_entry)
		self.display_list_widget.itemActivated.connect(self.fill_from_item)

		#load all present assets to gui if any:
		for _, asset in self.controller.assets.items():
			self.add_asset_entry(asset)


	def fill_combobox(self):
		'''Populates history combobox with the content Asset cache file
		'''

		#clear selection
		self.display_list_widget.clearSelection()

		self.history_combo_box.clear()
		for name, descr in self.controller.get_history().items():
			self.history_combo_box.addItem(name, descr)

	def fill_from_history(self):
		'''selecting item from combobox action for adding new asset from dropdown list in gui
		'''
		name = self.history_combo_box.currentText()
		desc = self.history_combo_box.currentData()

		if not name or not desc:
			return

		self.name_input_box.setText(name)
		self.description_input_box.setPlainText(desc)

	def fill_from_item(self):
		labels = self.display_list_widget.itemWidget( self.display_list_widget.currentItem() ).findChildren(QtWidgets.QLabel)
		for l in labels:
			if "name_" in l.objectName():
				self.name_input_box.setText(l.text())
			elif "description_" in l.objectName():
				self.description_input_box.setPlainText(l.text())


	def add_asset_entry(self, asset):
		'''Adds Asset entry in gui

		Args:
			asset (Asset):
		'''

		style = ""

		widget = QtWidgets.QWidget()
		widget.setObjectName("asset_"+asset.name)
		layout = QtWidgets.QHBoxLayout()
		layout.setContentsMargins(2,2,2,2)
		layout.setSpacing(10)

		name_lbl = QtWidgets.QLabel(asset.name)
		name_lbl.setObjectName("name_"+asset.name)
		layout.addWidget(name_lbl)

		desc_lbl = QtWidgets.QLabel(asset.description)
		desc_lbl.setObjectName("description_"+asset.description)
		desc_lbl.setWordWrap(True)
		layout.addWidget(desc_lbl)

		widget.setLayout(layout)
		# widget.setToolTip(value.description)

		if style:
			widget.setStyleSheet(style)

		self.asset_widgets[asset.name] = widget

		new_item = QtWidgets.QListWidgetItem()
		new_item.setSizeHint(widget.sizeHint())

		#edit existing item
		for index in range(0,self.display_list_widget.count()):
			item = self.display_list_widget.item(index)

			widget_in_list = self.display_list_widget.itemWidget(item)
			if widget.objectName() == widget_in_list.objectName():
				self.display_list_widget.setItemWidget(item, widget)
				self.history_combo_box.clear()
				return

		self.display_list_widget.addItem(new_item)
		self.display_list_widget.setItemWidget(new_item, widget)

		#clear combobox selection
		self.history_combo_box.clear()

	def delete_asset_entry(self):
		'''Removes selected asset entry from gui
		'''
		selected_items = self.display_list_widget.selectedItems()
		for item in selected_items:
			asset_name = self.display_list_widget.itemWidget( self.display_list_widget.currentItem() ).objectName().replace("asset_","",1)
			self.controller.delete_asset( self.controller.assets[asset_name] )
			self.display_list_widget.takeItem(self.display_list_widget.row(item))

		#clear selection
		self.display_list_widget.clearSelection()



class AssetsController():
	'''AssetsGui action controller
	'''
	def __init__(self, threat_model_controller, assets):
		'''Init
		'''

		self.threat_model_controller = threat_model_controller
		self.assets = assets
		self.assets_gui = AssetsGui(self)

		self.add_btn = self.assets_gui.add_button
		self.add_btn.clicked.connect(self.add_new_asset)

	def add_new_asset(self):
		'''add_btn action of adding new Asset from gui
		'''

		name = self.assets_gui.name_input_box.text()
		desc = self.assets_gui.description_input_box.toPlainText()

		if not name or not desc:
			Message.show_message_box(self.assets_gui, MsgType.INFO, "Can not add Asset without name or description")
			return

		try:
			asset = self.threat_model_controller.threat_model.add_asset(name, desc)
			self.assets_gui.assets_updated.emit()

			self.assets_gui.add_asset_entry(asset)

			self.assets_gui.name_input_box.clear()
			self.assets_gui.description_input_box.clear()
		except ModellingException as e:
			Message.show_message_box(self.assets_gui, MsgType.INFO, str(e))
			Message.print_message(MsgType.INFO, str(e))

	def delete_asset(self, asset):
		'''Action called when delete button is clicked of a particular asset entry

		Args:
			asset (Asset): Asset to delete
		'''

		self.threat_model_controller.threat_model.delete_asset(asset)
		self.assets_gui.assets_updated.emit()

	def get_history(self):
		'''Gets known assets from the cache file

		Returns:
			dict(String:String): asset_name : asset_description
		'''

		file = self.threat_model_controller.threat_model.assets_file
		assets = {}
		try:
			assets = Asset.fetch_known_assets(file)
		except ModellingException as e:
			Message.show_message_box(self.assets_gui, MsgType.ERROR, str(e))
			Message.print_message(MsgType.ERROR, str(e))
		return assets