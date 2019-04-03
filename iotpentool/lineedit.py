#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
special lineedit

By sarunasil
"""

import os
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLineEdit, QWidget

class LineEdit(QLineEdit):
	completerSignal = pyqtSignal(QWidget)

	def __init__(self):
		super().__init__()

	def mouseReleaseEvent(self, event):
		self.completerSignal.emit(self)
		super().mouseReleaseEvent(event)

	def focusInEvent(self, event):
		self.completerSignal.emit(self)
		super().focusInEvent(event)