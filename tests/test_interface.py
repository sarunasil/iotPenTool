#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
application interface testing set

By sarunasil
"""

import os
import pytest
from PyQt5 import QtWidgets


from iotpentool import interface
from iotpentool import interfaceloader
from iotpentool.modulegui import ModuleGui
from iotpentool.manager import Manager

from iotpentool.mymessage import DataException

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
INTERFACE_DIR = os.path.join(CURRENT_DIR, "stub_interfaces")

@pytest.fixture
def application():
	return QtWidgets.QApplication([])

@pytest.fixture
def interface_loader():
	return interfaceloader.InterfaceLoader(INTERFACE_DIR)

@pytest.mark.parametrize(("iden","flag_data","result"), [
	("long_format",
		{"flag":"l",
		"has_value":True,
		"description":"print in long format"
		},
		["long_format", "l", True, "print in long format",0]),
	("all_content",
		{"flag":"a",
		"has_value":False,
		"description":"print all content"
		},
		["all_content", "a", False, "print all content",0]),
	("nested_long",
		{"flag":"l",
		"has_value":True,
		"description":"print in long format",
		"flags":{
			"nested_flag1":{
				"flag":"flag1^2",
				"has_value":True,
				"description":"flag flag description"
				},
			"nested_flag2":{
				"flag": "flag2^2",
				"has_value": False,
				"description": "[flag]"
				}
			}
		},
		["nested_long", "l", True, "print in long format",2])
	])
def test_add_flag(iden, flag_data, result):
	flag = interface._Flag(iden, flag_data)

	assert flag.iden == result[0]
	assert flag.flag == result[1]
	assert flag.has_value == result[2]
	assert flag.description == result[3]
	assert len(flag.flag_flags) == result[4]

@pytest.mark.parametrize(("iden","value_data","result"), [
	(
		"path",
		{"default_value":".","description":"path to folder"},
		["path", ".", "path to folder"]
	),
	(
		"pwd",
		{},
		[]
	)
	])
def test_add_value(iden, value_data, result):
	if not value_data:
		with pytest.raises(DataException):
			value = interface._Value(iden, value_data)
	else:
		value = interface._Value(iden, value_data)

		assert value.iden == result[0]
		assert value.default_value == result[1]
		assert value.description == result[2]

@pytest.mark.parametrize(("interface_command"), ["ls", "pwd"])
def test_generate_gui(application, interface_loader, interface_command):
	'''Test generation of QWidget with all components of a interface

	Args:
		interface_loader (InterfaceLoader): setups interfaces to generate QWidget from
		id (String): Which to use
	'''
	interface = interface_loader.interfaces[interface_command]

	interface.generate_gui(Manager())

	assert isinstance(interface.gui, ModuleGui)

@pytest.mark.parametrize(("interface_command","flags","values","check_command"),
	[
		("ls", {'long_format':'stub', 'all_content':None}, {'path':'.'}, "ls -l stub -a ."),
		("ls", {'all_content':None}, {'path':'.'}, "ls -a ."),
		("ls", {'all_content':None}, {}, "ls -a"),
		("pwd", {'physical':None}, {}, "pwd -P")
	])
def test_build_command(interface_loader, interface_command, flags, values, check_command):

	interface = interface_loader.interfaces[interface_command]

	gen_command = interface.build_command(flags, values)

	assert gen_command == check_command


