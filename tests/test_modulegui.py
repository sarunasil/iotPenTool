#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
individual Module gui functionality testing set

By sarunasil
"""

import os
import pytest
from collections import OrderedDict
from PyQt5 import QtWidgets

from iotpentool.modulegui import ModuleGui, ModuleGuiController
from iotpentool.interface import _Flag, _FlagLabel, _Value, Interface, NESTED_SYMBOL
from iotpentool.interfaceloader import InterfaceLoader
from iotpentool.manager import Manager

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
	controller = ModuleGuiController(interface, None)
	widget = ModuleGui(controller)

	assert isinstance(widget, QtWidgets.QWidget)
	assert isinstance(widget.controller, ModuleGuiController)
	assert widget.styleSheet() == widget.style
	assert widget.objectName() == "widget_interface"
	assert widget.findChild(QtWidgets.QWidget, "widget_general")
	assert widget.findChild(QtWidgets.QWidget, "widget_flags")
	assert widget.findChild(QtWidgets.QWidget, "widget_values")


@pytest.mark.parametrize(("label","object_name","text", "wrap","style"), [
	("Version", "test", "test text", False, ""),
	("Description", "test2", "another_text", True, "")
	])
def test__create_label(application, label, object_name, text, wrap, style):

	widget = ModuleGui._create_label(label, object_name, text, wrap, style)

	assert isinstance(widget, QtWidgets.QWidget)
	assert widget.styleSheet() == style
	assert isinstance( widget.layout(), QtWidgets.QVBoxLayout )
	assert widget.objectName() == "label_"+object_name
	assert widget.findChild(QtWidgets.QLabel, "label_"+label)
	if wrap:
		assert widget.findChild(QtWidgets.QScrollArea, "label_scroll_"+object_name).findChild(QtWidgets.QLabel, "label_value_"+object_name)
	else:
		assert widget.findChild(QtWidgets.QLabel, "label_value_"+object_name)


@pytest.mark.parametrize(("iden","has_value","flag_data","style"), [
	("long_format", True, 
		{"flag":"l",
			"has_value":True,
			"description":"print in long format"
		},
		""
	),
	("all_content", False, 
		{"flag":"a",
		"has_value":False,
		"description":"print all content"
		},
		""
	),
	("nested_long", False,
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
		""
	),
	(
		"GROUP_1",
		False,
		"Test Label Text",
		""
	)
	])
def test__create_flag(application, iden, has_value, flag_data, style):
	if iden.startswith("GROUP"):
		flag = _FlagLabel(flag_data)
	else:
		flag = _Flag(iden, flag_data)

	widget = ModuleGui._create_flag(flag, [], style)

	assert isinstance(widget, QtWidgets.QWidget)
	assert widget.styleSheet() == style
	assert isinstance( widget.layout(), QtWidgets.QVBoxLayout )

	if iden.startswith("GROUP"):
		widget_top = widget.findChild(QtWidgets.QWidget, "widget_top_"+flag_data)
		assert widget.objectName() == "flag_"+flag_data
		assert widget_top.findChild(QtWidgets.QLabel, "label_"+flag_data)
	else:
		widget_top = widget.findChild(QtWidgets.QWidget, "widget_top_"+iden)
		assert widget.objectName() == "flag_"+iden
		if has_value:
			assert widget_top.findChild(QtWidgets.QLineEdit, "text_box_"+iden)
		assert widget_top.findChild(QtWidgets.QCheckBox, "check_box_"+iden)

	if 'flags' in flag_data:
		for flag_iden in flag_data['flags']:
			if not widget.findChild(QtWidgets.QWidget, "flag_"+iden+NESTED_SYMBOL+flag_iden):
				assert False

@pytest.mark.parametrize(("iden","value_data","style"), [
	("path", {"default_value":".","description":"path to folder"},""),
	("other_value", {"default_value":"*","description":"other description"},"")
])
def test__create_value(application, iden, value_data, style):
	value = _Value(iden, value_data)

	widget = ModuleGui._create_value(value, style)

	assert isinstance(widget, QtWidgets.QWidget)
	assert widget.styleSheet() == style
	assert isinstance( widget.layout(), QtWidgets.QHBoxLayout )
	assert widget.objectName() == "value_"+iden
	assert widget.findChild(QtWidgets.QLabel, "label_"+iden)
	assert widget.findChild(QtWidgets.QLineEdit, "text_box_"+iden)


@pytest.mark.parametrize(("name","version","command","description", "structure"), [
	("name_1", "v1", "cmd_1", "description of name_1",
        ["command-sts",{ "FLAGS": [ "_", "FLAG", "<>", "FLAG_VALUE", "?" ] },{ "VALUES": [ "VALUE", " / " ] }]),
	("name_2", "1", "cmd[?]", "description of name_2",
		["lhg", { "VALUES": [ "VALUE", "-" ] }, { "FLAGS": [ "-", "FLAG", "?", "FLAG_VALUE", " == " ] }])
	])
def test__create_general(application, name, version, command, description, structure):

	interface = Interface(name, version, command, description, structure)

	widget = ModuleGui._create_general(interface)

	assert isinstance(widget, QtWidgets.QWidget)
	#style = "smth"
	# assert widget.styleSheet() == style  only if common style is used for the whole thing
	assert isinstance( widget.layout(), QtWidgets.QVBoxLayout )
	assert widget.objectName() == "widget_general"
	assert widget.findChild(QtWidgets.QWidget, "label_name")
	assert widget.findChild(QtWidgets.QWidget, "label_version")
	assert widget.findChild(QtWidgets.QWidget, "label_command")
	assert widget.findChild(QtWidgets.QWidget, "label_description")


@pytest.mark.parametrize(("flags","flag_widgets"),[
	({
		"long_format":{
			"flag":"l",
			"has_value":True,
			"description":"print in long format"
			},
		"all_content":{
			"flag":"a",
			"has_value":False,
			"description":"print all content"
			}
		},
		[]
	),
	({
		"all_content":{
			"flag":"a",
			"has_value":False,
			"description":"print all content"
			}
		}, 
		["stub"]
	),
	(
		{
			"GROUP_3":"group0",
			"all_content":{
				"flag":"a",
				"has_value":False,
				"description":"print all content"
			},
			"GROUP_4":"group1"
		},
		["stub"]
	)
])
def test__create_flags(application, flags, flag_widgets):

	#create flag set from parameter values
	stub_flags = {}
	for flag_iden, flag_data in flags.items():
		if flag_iden.startswith("GROUP"):
			f = _FlagLabel(flag_data)
		else:
			f = _Flag(flag_iden, flag_data)
		stub_flags[f.iden] = f

	flag_widgets_len = len(flag_widgets)
	widget = ModuleGui._create_flags(stub_flags, flag_widgets)
	assert len(flag_widgets) == flag_widgets_len + len(flags)

	assert isinstance(widget, QtWidgets.QWidget)
	#style = "smth"
	#assert widget.styleSheet() == style
	assert isinstance( widget.layout(), QtWidgets.QVBoxLayout )
	assert widget.objectName() == "widget_flags"
	scroll = widget.findChild(QtWidgets.QScrollArea)
	for flag in stub_flags:
		assert scroll.findChild(QtWidgets.QWidget, "flag_"+flag)


@pytest.mark.parametrize(('values', 'value_widgets'), [
	({"path":{
		"default_value":".",
		"description":"path to folder"
		}
	}, []),
	({}, []),
	({"path":{
		"default_value":".",
		"description":"path to folder"
		}
	}, ['stub'])
	])
def test__create_values(application, values, value_widgets):

	#create values set from parameter values
	stub_values = {}
	for value_data in values:
	  v = _Value(value_data, values[value_data])
	  stub_values[v.iden] = v

	value_widgets_len = len(value_widgets)
	widget = ModuleGui._create_values(stub_values, value_widgets)
	assert len(value_widgets) == value_widgets_len + len(values)

	assert isinstance(widget, QtWidgets.QWidget)
	#style = "smth"
	#assert widget.styleSheet() == style
	assert isinstance( widget.layout(), QtWidgets.QVBoxLayout )
	assert widget.objectName() == "widget_values"
	scroll = widget.findChild(QtWidgets.QScrollArea)
	for value in stub_values:
		assert scroll.findChild(QtWidgets.QWidget, "value_"+value)


@pytest.mark.parametrize(('btns_ref'), [
	(OrderedDict()),
	(OrderedDict({'s':'stub'}))
	])
def test__create_footer(application, btns_ref):

	btns_ref_len = len(btns_ref)
	widget = ModuleGui._create_footer(btns_ref)
	assert len(btns_ref) == btns_ref_len + 2

	assert isinstance(widget, QtWidgets.QWidget)
	assert isinstance( widget.layout(), QtWidgets.QHBoxLayout )
	assert widget.objectName() == "widget_footer"
	assert widget.findChild(QtWidgets.QPushButton, "btn_execute")


@pytest.mark.parametrize(("interface_command","flag_states","value_states"), [
	("ls", [('long_format','stub'), ('all_content',None)], [('path','.')]),
	("ls", [('all_content',None)], [('path','.')] ),
	("ls", [('all_content',None)], []),
	("pwd", [('physical',None)], []),
	("group_label", [('physical',None)], [])
	])
def test_gather_params(application, interface_command, flag_states, value_states):
	interface_obj = InterfaceLoader.create_interface(InterfaceLoader.read_interface_file("tests/stub_interfaces/interface-"+interface_command+".yml")) #get single interface object without using InterfaceLoader instance
	controller = ModuleGuiController(interface_obj, None)
	widget = ModuleGui(controller)

	#setup flag values
	#go through each flag_state
	for flag_iden, flag_value in flag_states:
		found = False
		#find qwidget with the right checkbox
		for flag_widget in controller.flag_widgets:
			if flag_widget.objectName() == "flag_"+flag_iden:
				checkbox = flag_widget.findChild(QtWidgets.QCheckBox)
				checkbox.setChecked(True)

				if flag_value:
					textbox = flag_widget.findChild(QtWidgets.QLineEdit)
					textbox.setText(flag_value)

				found = True
				break
		assert found #if widget with right flag_iden not found - error

	#setup value values
	#go through each value_state
	for value_iden, value_value in value_states:
		found = False
		#find qwidget with the right checkbox
		for value_widget in controller.value_widgets:
			if value_widget.objectName() == "value_"+value_iden:
				textbox = value_widget.findChild(QtWidgets.QLineEdit)
				textbox.setText(value_value)

				found = True
				break
		assert found #if widget with right value_iden not found - error


	flags, values = controller.gather_params()
	#flags
	for flag, value in flag_states:
		assert (flag, value) in flags

	#values
	for value_name, value in value_states:
		assert (value_name, value) in values

