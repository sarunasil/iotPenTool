#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
special combo box

By sarunasil
"""

import os
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QComboBox

class ComboBox(QComboBox):
	popupAboutToBeShown = pyqtSignal()

	def showPopup(self):
		self.popupAboutToBeShown.emit()
		super(ComboBox, self).showPopup()