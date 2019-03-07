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

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
INTERFACE_DIR = os.path.join(CURRENT_DIR, "stub_interfaces")

@pytest.fixture
def application():
	return QtWidgets.QApplication([])

@pytest.fixture
def interface_loader():
	return interfaceloader.InterfaceLoader(INTERFACE_DIR)

@pytest.mark.parametrize(("interface_command"), ["ls", "pwd"])
def test_generate_gui(application, interface_loader, interface_command):
	'''Test generation of QWidget with all components of a interface

	Args:
		interface_loader (InterfaceLoader): setups interfaces to generate QWidget from
		id (String): Which to use
	'''

	interface = interface_loader.interfaces[interface_command]

	interface.generate_gui()

	assert isinstance(interface.gui, ModuleGui)
