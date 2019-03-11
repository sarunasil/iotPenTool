#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
Worker object to execute multithreaded code

By sarunasil
"""

import os
import subprocess

from PyQt5.QtCore import QRunnable, pyqtSignal, pyqtSlot, QObject


class WorkerSignals(QObject):
	'''
	Defines the signals available from a running worker thread.

	Supported signals are:

	finished
		No data

	error
		`tuple` (exctype, value, traceback.format_exc() )

	result
		`object` data returned from processing, anything

	progress
		`int` indicating % progress

	'''
	finished = pyqtSignal()
	error = pyqtSignal(tuple)
	result = pyqtSignal(object)
	progress = pyqtSignal(int)


class Worker(QRunnable):
	
	def __init__(self, output):
		super(Worker, self).__init__()

		self.signals = WorkerSignals()
		self.signals.result.connect(output)
		self.command_string = ''

	@pyqtSlot()
	def run(self):
		'''
		Initialise the runner function with passed args, kwargs.
		'''

		cmd_str = self.execute_command(self.command_string)
		print ("This is run: "+cmd_str)

		self.signals.result.emit(cmd_str)
		# # Retrieve args/kwargs here; and fire processing using them
		# try:
		# 	result = self.fn(*self.args, **self.kwargs)
		# except:
		# 	traceback.print_exc()
		# 	exctype, value = sys.exc_info()[:2]
		# 	self.signals.error.emit((exctype, value, traceback.format_exc()))
		# else:
		# 	self.signals.result.emit(result)  # Return the result of the processing
		# finally:
		# 	self.signals.finished.emit()  # Done

	def execute_command(self, command):
		'''Executes cmd command provided to it
		
		Args:
			command (String): command string
		
		Returns:
			[type]: [description] ??? error and exception handling ???
		'''

		process = subprocess.Popen(
			command.split(' ', 1), stdout=subprocess.PIPE, stderr=subprocess.PIPE
			)

		result, error = process.communicate()

		return result.decode()