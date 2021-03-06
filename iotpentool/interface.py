#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
Interface instance class

By sarunasil
"""

import re

from abc import ABC
from collections import OrderedDict
from iotpentool.interfacegui import InterfaceGuiController
from iotpentool.utils import DataException

#SYMBOL USED TO MARK NESTED FLAGS
NESTED_SYMBOL = "^"

class Argument(ABC):
	'''Abstract argument class to be inherited by _Flag and _Value
	'''

	def __init__(self, iden, data):
		'''Init
		'''

		if "description" not in data:
				raise DataException("Data file is corrupt. Could not find 'description' fields in "+iden)

		self.iden = iden
		self.description = data['description']
		self.keywords = []
		if 'keywords' in data:
			self.keywords = data['keywords']
		self.patterns = []
		if 'patterns' in data:
			self.patterns = data['patterns']
		self.suggestions = []

	def __eq__(self, other):
		'''Overwrite == comparison operation for _Flag objects. != overwritten automatically

		Args:
			other (_Flag): another object to compare with

		Returns:
			Boolean: equal or not
		'''

		return isinstance(other, self.__class__) and self.__dict__ == other.__dict__


class _Flag(Argument):
	'''Object representing command flag instance
	'''

	def __init__(self, iden, data):
		'''Init

		Args:
			data(dict)
		'''

		Argument.__init__(self, iden, data)

		if ("flag" not in data or
			"has_value" not in data):
				raise DataException("Data file is corrupt. Could not find 'flag', 'has_value' fields in "+iden)

		#SYMBOL USED TO MARK NESTED FLAG = ^
		flag_flags = {}
		if 'flags' in data:
			for flag_item in data['flags']:
				for flag_iden, flag_data in flag_item.items():
					nested_flag_iden = iden+NESTED_SYMBOL+flag_iden
					flag_flags[nested_flag_iden] = _Flag(nested_flag_iden, flag_data)

		self.flag = data['flag']
		self.has_value = data['has_value']
		self.flag_flags = flag_flags

class _FlagLabel(_Flag):
	'''Object to add grouping labels between flags
	'''

	def __init__(self, label):
		'''Init

		Args:
			label_value (String): label to display
		'''
		_Flag.__init__(self, label, {"description":"STUB","flag":"STUB","has_value":False})

		self.label = label


class _Value(Argument):
	'''Object representing value taken by the command

		ASSUMING that values are COMPULSORY, if optional - _Flag
	'''

	def __init__(self, iden, data):
		'''Init
		'''
		Argument.__init__(self, iden, data)

		if 'default_value' not in data:
			raise DataException("Data file is corrupt. Could not find 'default_value' field in "+iden)

		self.default_value = data['default_value']


class Interface():
	'''Adapter between main program an the module in use
	module can refer to any program that is callable via an terminal

	Defines all the methods required to interact with the module
	'''

	def __init__(self, category, name, version, command, description, structure):
		'''Init

		Args:
			name (String): print name / identifier
			version (String):
			command (String): terminal command to execute
		'''

		self.category = category
		self.name = name       			#print name
		self.version = version 			#version
		self.command = command 			#terminal call name
		self.description = description	#tool description
		self.flags = OrderedDict()     	#parameters program can take
		self.values = OrderedDict()   	#values provided without a flag e.g. 'ls /dev'
		self.structure = structure 		#defines tool command syntax ls [FLAGS] path
		self.gui_controller = None		#Controller of gui

	def add_flag(self, iden, data):
		'''Add new flag object

		Args:
			iden (String): unique flag identifier
			data (dict): yml like structure with flag data
		'''

		if iden.startswith("GROUP"):
			flag_inst = _FlagLabel(data)
			self.flags[data] = flag_inst
		else:
			flag_inst = _Flag(iden, data)
			self.flags[iden] = flag_inst

	def add_value(self, iden, data):
		'''Add new value to values

		Args:
			iden (String): unique value identifier
			data (dict): yml like structure with value data
		'''

		value_inst = _Value(iden, data)
		self.values[iden] = value_inst

	def generate_gui(self, manager):
		'''Creates a QWidget according to the interface itself.

		Args:
			manager (Manager): reference to Thread Manager
			to execute commands outside main event loop
		'''

		self.gui_controller = InterfaceGuiController(self, manager)

	def build_command(self, flags, values):
		'''Takes dicts of flags and values chosen according to gui and creates one complete command string that can be executed in terminal

		Args:
			flags (list((String,String))): (flag_widget_name, flag_value) - of every selected flag
			values (list((String, String))): (value_widget_name, value_value) - of every selected value

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

				command += self.build_flags(self.flags, flags, item["FLAGS"])

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

		print (command)
		return command.rstrip()

	@staticmethod
	def build_flags(flag_objects, flags, flag_struct):
		'''Builds flag part of the command string

		Args:
			flag_objects (Flag): parent Flag flag objects or self.flags
			flags (dict(String:String|None): checked flags data array
			flag_struct (dict(String)): self.structure['FLAGS']

		Returns:
			String: part of command string with flag data
		'''

		command = ""
		for flag_obj_iden, flag_obj in flag_objects.items():
			if flag_obj_iden in flags:
				symbol = flag_obj.flag
				value = flags[flag_obj_iden] if flags[flag_obj_iden] else ""

				nested_result = ""
				if flag_obj.flag_flags:
					nested_result = Interface.build_flags(flag_obj.flag_flags, flags, flag_struct)

				#follow Interface.structure "FLAGS" pattern to set params
				for flag_item in flag_struct:
					if flag_item == "FLAG":
						command += symbol
					elif flag_item == "NESTED":
						command += nested_result
					elif flag_item == "FLAG_VALUE":
						command += value
					else:
						command += flag_item
		return command

	def build_values(self, values, parent=None):
		pass

