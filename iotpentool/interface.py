#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
Interface instance class

By sarunasil
"""

import re

from abc import ABC
from iotpentool.modulegui import ModuleGui
from iotpentool.mymessage import DataException

class Argument(ABC):
	'''Abstract argument class to be inherited by _Flag and _Value
	'''

	def __init__(self, iden, description):
		'''Init
		'''

		self.iden = iden
		self.description = description

	def __eq__(self, other):
		'''Overwrite == comparison operation for _Flag objects. != overwritten automatically

		Args:
			other (_Flag): another object to compare with

		Returns:
			Boolean: eqaul or not
		'''

		return isinstance(other, self.__class__) and self.__dict__ == other.__dict__


class _Flag(Argument):
	'''Object representing command flag instance 
	'''

	def __init__(self, iden, flag, has_value, description):
		'''Init
		'''
		Argument.__init__(self, iden, description)
		self.has_value = has_value
		self.flag = flag

class _Value(Argument):
	'''Object representing value taken by the command

		ASSUMING that values are COMPULSORY, if optional - _Flag
	'''

	def __init__(self, iden, default_value, description):
		'''Init
		'''
		Argument.__init__(self, iden, description)
		self.default_value = default_value


class Interface():
	'''Adapter between main program an the module in use
	module can refer to any program that is callable via an terminal

	Defines all the methods required to interact with the module
	'''

	def __init__(self, name, version, command, description, structure):
		'''Init

		Args:
			name (String): print name / identifier
			version (String):
			command (String): terminal command to execute
		'''

		self.name = name       #print name
		self.version = version #version
		self.command = command #terminal call name
		self.description = description	#tool description
		self.flags = {}     #parameters program can take
		self.values = {}   #values provided without a flag e.g. 'ls /dev'
		self.structure = structure #defines tool command syntax ls [FLAGS] path
		self.gui = None		#QWidget of the module gui


	def add_flag(self, iden, data):
		'''Add new flag object

		Args:
			iden (String): unique flag identifier
			data (dict): yml like structure with flag data
		'''

		if ("flag" not in data or
				"description" not in data
				):
				raise DataException("Data file is corrupt. Could not find 'flag', 'description' fields in "+iden)

		flag_inst = _Flag(iden, data['flag'], data['has_value'], data['description'])

		self.flags[iden] = flag_inst


	def add_value(self, iden, data):
		'''Add new value to values

		Args:
			iden (String): unique value identifier
			data (dict): yml like structure with value data
		'''

		if ("description" not in data):
				raise DataException("Data file is corrupt. Could not find 'description' fields in "+iden)

		value_inst = _Value(iden, data['default_value'], data['description'])

		self.values[iden] = value_inst

	def generate_gui(self, threadpool, worker):
		'''Creates a QWidget according to the interface itself.
		'''
		self.gui = ModuleGui(self, threadpool, worker)

	def build_command(self, flags, values):
		'''Takes dicts of flags and values chosen according to gui and creates one complete command string that can be executed in terminal

		Args:
			flags (dict(String:String|None)): (flag_iden, value with present) - of every selected flag
			values (dict(String:String)): (value_iden, value) - of every selected value

		Returns:
			String: executable string
		'''
		separator = " "

		command = ""
		for item in self.structure:
			if item == "COMMAND":
				command += self.command + separator
			elif isinstance(item, dict) and "FLAGS" in item:
				#flags building

				#for every checked flag
				for flag_iden, flag_value in flags.items():
					flag_symbol = self.flags[flag_iden].flag

					#follow Interface.structure "FLAGS" pattern to set params
					for flag_item in item["FLAGS"]:
						if flag_item == "FLAG":
							command += flag_symbol
						elif flag_item == "FLAG_VALUE":
							if flag_value:
								command += flag_value
						else:
							command += flag_item

			elif isinstance(item, dict) and "VALUES" in item:
				#values building

				#for every value entered
				for value_iden, value_value in values.items():

					#follow Interface.structure "VALUES" pattern to set params
					for value_item in item["VALUES"]:
						if value_item == "VALUE":
							command += value_value
						else:
							command += value_item

		#clean up string from multiple spaces and trailling spaces
		command = re.sub(' +', ' ', command)
		return command.rstrip()

	def execute(self, param):
		'''Executes a specific module command 
		according to parameters given

		Arguments:
				param {[type]} -- [description]
		'''





