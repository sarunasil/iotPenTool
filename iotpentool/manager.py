#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
class to manage ThreadPool and worker threads execution

By sarunasil

Some code shamelessly taken from
https://www.mfitzp.com/article/multithreading-pyqt-applications-with-qthreadpool/
"""

import os
import subprocess
from PyQt5.QtCore import QThreadPool
from PyQt5.QtCore import QRunnable, pyqtSignal, pyqtSlot, QObject

from iotpentool import mymessage


class WorkerSignals(QObject):
	'''
	Defines the signals available from a running worker thread.
	Supported signals are:

	finished
		No data
	error
		String
	result
		String
	progress
		`int` indicating % progress
	'''
	finished = pyqtSignal()
	error = pyqtSignal(object)
	result = pyqtSignal(object)
	progress = pyqtSignal(int)


class Worker(QRunnable):
	'''Class that is represents one job
	that has to be executed outside the main event loop
	'''

	def __init__(self, command_string, output_func, callback, cleanup):
		'''Initiates Qt thread wrapper instance
		to do work in another thread

		Args:
			command_string (String): command string to execute
			output_func (func): function to deal with process signals
			callback (Function): job client function to exe after run -> job supplier
			cleanup (Function): manager function to exe after run -> Manager
		'''

		super(Worker, self).__init__()

		self.signals = WorkerSignals()
		self.signals.result.connect(output_func)	#result and
		self.signals.error.connect(output_func)		#error is reported the same way
		self.command_string = command_string

		self.process = None
		self.callback = callback
		self.cleanup = cleanup

	@pyqtSlot()
	def run(self):
		'''
		Execute command_string and report outcome
		'''
		#seems like subprocess does not require a neat string.
		#oh well, split it into command and arguments :(
		command_plus_arg = self.command_string.split(' ')

		result = ""
		error = ""
		try:

			#create subprocess 
			self.process = subprocess.Popen(command_plus_arg, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

			while True:
				output = self.process.stdout.readline().decode()
				if self.process.poll() is not None and output == '':
					break
				if output:
					self.signals.result.emit(output)
					print("result!")
				print ("looping")
			retval = self.process.poll()
			print("Done")

			# #execute subprocess
			# result, error = self.process.communicate()

			# #binary -> ASCII
			# result = result.decode()
			# error = error.decode()

			# if result:
			# 	self.signals.result.emit(self.command_string+"\n---\n"+result)  # Return the result of command
			# else:
			# 	self.signals.error.emit(error)	#return error
		except Exception as e:
			print ("BIG TIME ERROR: Worker.run()")
			self.signals.error.emit(str(e))	#return error
		finally:
			self.signals.finished.emit()  # Done
			self.cleanup()	#Manager function execution
			self.callback()	#Job client function execution

	def terminate(self):
		'''terminate running subprocess
		'''

		if self.process:
			try:
				self.process.terminate()
				return mymessage.Outcome.SUCCESS
			except:
				return mymessage.Outcome.FAILURE

		return mymessage.Outcome.SUCCESS


class Manager():
	'''Manages QThreadPool,
		Starts new workers,
		has a dict of output functions
		to receive worker threads output
		{ interface_iden : output_func }
	'''

	def __init__(self):
		'''Init
		'''

		self.threadpool = QThreadPool()
		self._output_funcs = {} #dict of output functions
		self._workers = {}

	def add_output_func(self, iden, func):
		'''Adds function that deal with thread output
		as dict entry with appropriate identifier

		Args:
			iden (String): interface identifier
			func (function): function to deal with output of 'iden'
		'''
		self._output_funcs[iden] = func

	def run_executor(self, iden, execution_id, command_string, callback):
		'''Run command line tool

		Args:
			iden (String): interface identifier to select output
			execution_id (String): unique identifier for this execution
			command_string (String): command to execute
			callback (Function): function to execute upon task finish
		'''

		def remove_worker(): #to be executed after Worker finishes
			self._workers.pop(execution_id, None)

		output_func = self._output_funcs[iden]
		worker = Worker(command_string, output_func, callback, remove_worker)

		self._workers[execution_id] = worker #remember worker for termination if needed

		self.threadpool.start(worker)

	def terminate_executor(self, executor_id):
		'''Used to cancel running command

		Args:
			executor_id (String): id of the worker
		'''

		if executor_id and executor_id in self._workers:
			result = self._workers[executor_id].terminate()

			if result == mymessage.Outcome.FAILURE:
				mymessage.Message.print_message(mymessage.MsgType.WARNING, "Failed to kill a subprocess with SIGTERM command.")
