#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
file to deal with Assets tab gui generation
covers View and Controller

By sarunasil
"""

import uuid
import os
from collections import OrderedDict
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from iotpentool.line import QHLine
from iotpentool.utils import *
from iotpentool.asset import Asset


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
ASSETS_GUI_FILEPATH = os.path.join(CURRENT_DIR, "gui/assets.ui")

Ui_MainWindow, QtBaseClass = uic.loadUiType(ASSETS_GUI_FILEPATH)

class ComboBox(QtWidgets.QComboBox):
    popupAboutToBeShown = QtCore.pyqtSignal()

    def showPopup(self):
        self.popupAboutToBeShown.emit()
        super(ComboBox, self).showPopup()

class AssetsGui(QtWidgets.QWidget, Ui_MainWindow):
	'''Deals with Assets tab which is generated from Assets data
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
		self.asset_widgets = {}

		self.history_combo_box = ComboBox()
		self.history_layout.insertWidget(0, self.history_combo_box)
		self.history_combo_box.popupAboutToBeShown.connect(self.fill_combobox)


	def fill_combobox(self):
		'''Populates history combobox with the content Asset cache file
		'''

		self.history_combo_box.clear()
		for name, descr in self.controller.get_history().items():
			self.history_combo_box.addItem(name, descr)


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
		name_lbl.setObjectName("label_"+asset.name)
		layout.addWidget(name_lbl)

		desc_lbl = QtWidgets.QLabel(asset.description)
		desc_lbl.setObjectName("label_"+asset.description)
		desc_lbl.setWordWrap(True)
		layout.addWidget(desc_lbl)

		btn = QtWidgets.QPushButton()
		btn.setText("Del")
		btn.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
		btn.setObjectName("button_delete_"+asset.name)
		btn.pressed.connect(lambda: self.controller.delete_asset(asset))
		layout.addWidget(btn)

		widget.setLayout(layout)
		# widget.setToolTip(value.description)

		if style:
			widget.setStyleSheet(style)

		self.asset_widgets[asset.name] = widget
		self.display_layout.insertWidget(0, widget)

	def delete_asset_entry(self, asset):
		'''Removes asset entry from gui

		Args:
			asset (Asset):
		'''

		self.display_layout.removeWidget(self.asset_widgets[asset.name])
		self.asset_widgets[asset.name].deleteLater()
		self.asset_widgets[asset.name] = None

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

		self.add_btn.pressed.connect(self.add_new_asset)
		self.assets_gui.history_combo_box.currentTextChanged.connect(self.fill_from_history)

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

			self.assets_gui.add_asset_entry(asset)

			self.assets_gui.name_input_box.clear()
			self.assets_gui.description_input_box.clear()
		except ModellingException as e:
			Message.show_message_box(self.assets_gui, MsgType.INFO, str(e))
			Message.print_message(MsgType.INFO, str(e))

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

	def fill_from_history(self):
		'''add_history_btn action for adding new asset from dropdown list in gui
		'''
		name = self.assets_gui.history_combo_box.currentText()
		desc = self.assets_gui.history_combo_box.currentData()

		if not name or not desc:
			return

		self.assets_gui.name_input_box.setText(name)
		self.assets_gui.description_input_box.setPlainText(desc)

	def delete_asset(self, asset):
		'''Action called when delete button is clicked of a particular asset entry

		Args:
			asset (Asset): Asset to delete
		'''

		self.threat_model_controller.threat_model.delete_asset(asset)
		self.assets_gui.delete_asset_entry(asset)