#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
individual Module gui functionality testing set

By sarunasil
"""

import os
import pytest
from PyQt5 import QtWidgets

from iotpentool.modulegui import ModuleGui
from iotpentool.interface import _Flag, _Value, Interface
from iotpentool.interfaceloader import InterfaceLoader

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
INTERFACE_DIR = os.path.join(CURRENT_DIR, "stub_interfaces")

@pytest.fixture
def interface_loader():
	return InterfaceLoader(INTERFACE_DIR)

@pytest.fixture
def application():
	return QtWidgets.QApplication([])

@pytest.mark.parametrize(("interface_command"), ["ls", "pwd"])
def test_init(application, interface_loader, interface_command):

	interface = interface_loader.interfaces[interface_command]
	widget = ModuleGui(interface)

	assert isinstance(widget, QtWidgets.QWidget)
	assert isinstance(widget.interface, Interface)
	assert widget.styleSheet() == widget.style
	assert widget.objectName() == "widget_interface"
	assert widget.findChild(QtWidgets.QWidget, "widget_general")
	assert widget.findChild(QtWidgets.QWidget, "widget_flags")
	assert widget.findChild(QtWidgets.QWidget, "widget_values")


@pytest.mark.parametrize(("object_name","text","style"), [
	("test", "test text", ""),
	("test2", "another_text", "")
	])
def test__create_label(application, object_name, text, style):

	widget = ModuleGui._create_label(object_name, text, style)

	assert isinstance(widget, QtWidgets.QLabel)
	assert widget.styleSheet() == style
	assert widget.objectName() == "label_"+object_name
	# assert isinstance( widget.layout(), QtWidgets.QHBoxLayout )


@pytest.mark.parametrize(("iden","flag","has_value","description","style"), [
	("long_format", "l", True, "desc", ""),
	("all_content", "a", False, "desc", "")
	])
def test__create_flag(application, iden, flag, has_value, description, style):
	flag = _Flag(iden, flag, has_value, description)

	widget = ModuleGui._create_flag(flag, style)

	assert isinstance(widget, QtWidgets.QWidget)
	assert widget.styleSheet() == style
	assert isinstance( widget.layout(), QtWidgets.QHBoxLayout )
	assert widget.objectName() == "flag_"+iden
	if has_value:
		assert widget.findChild(QtWidgets.QLineEdit, "text_box_"+iden)
	assert widget.findChild(QtWidgets.QCheckBox, "check_box_"+iden)


@pytest.mark.parametrize(("iden","default_value","description","style"), [
	("path", ".", "path to folder",""),
	("other_value", "*", "other description","")
])
def test__create_value(application, iden, default_value, description, style):
	value = _Value(iden, default_value, description)

	widget = ModuleGui._create_value(value, style)

	assert isinstance(widget, QtWidgets.QWidget)
	assert widget.styleSheet() == style
	assert isinstance( widget.layout(), QtWidgets.QHBoxLayout )
	assert widget.objectName() == "value_"+iden
	assert widget.findChild(QtWidgets.QLabel, "label_"+iden)
	assert widget.findChild(QtWidgets.QLineEdit, "text_box_"+iden)


@pytest.mark.parametrize(("name","version","command"), [
	("name_1", "v1", "cmd_1"),
	("name_2", "1", "cmd[?]")
	])
def test__create_general(application, name, version, command):

	interface = Interface(name, version, command)

	widget = ModuleGui._create_general(interface)

	assert isinstance(widget, QtWidgets.QWidget)
	#style = "smth"
	# assert widget.styleSheet() == style  only if common style is used for the whole thing
	assert isinstance( widget.layout(), QtWidgets.QVBoxLayout )
	assert widget.objectName() == "widget_general"
	assert widget.findChild(QtWidgets.QLabel, "label_name")
	assert widget.findChild(QtWidgets.QLabel, "label_version")
	assert widget.findChild(QtWidgets.QLabel, "label_command")


@pytest.mark.parametrize(("flags"),[
	([
		["long_format", "l", False, "print in long format"],
		["all_content", "a", False, "print all content"]
	]),
	([
		["help", "h", False, "help"]
	]),
	])
def test__create_flags(application, flags):

	#create flag set from parameter values
	stub_flags = {}
	for flag_data in flags:
	  f = _Flag(flag_data[0], flag_data[1], flag_data[2], flag_data[3])
	  stub_flags[f.iden] = f

	widget = ModuleGui._create_flags(stub_flags)

	assert isinstance(widget, QtWidgets.QWidget)
	#style = "smth"
	#assert widget.styleSheet() == style
	assert isinstance( widget.layout(), QtWidgets.QVBoxLayout )
	assert widget.objectName() == "widget_flags"
	for flag in stub_flags:
		assert widget.findChild(QtWidgets.QWidget, "flag_"+flag)


@pytest.mark.parametrize(('values'), [
	({"path":{
		"default_value":".",
		"description":"path to folder"
		}
	}),
	({})
	])
def test__create_values(application, values):

	#create values set from parameter values
	stub_values = {}
	for value_data in values:
	  v = _Value(value_data, values[value_data]["default_value"], values[value_data]['description'])
	  stub_values[v.iden] = v

	widget = ModuleGui._create_values(stub_values)

	assert isinstance(widget, QtWidgets.QWidget)
	#style = "smth"
	#assert widget.styleSheet() == style
	assert isinstance( widget.layout(), QtWidgets.QVBoxLayout )
	assert widget.objectName() == "widget_values"
	for value in stub_values:
		assert widget.findChild(QtWidgets.QWidget, "value_"+value)

