#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
application interfaceloader testing set

By sarunasil
"""

import pytest
import random
import os


from iotpentool import interfaceloader, mymessage
from iotpentool.interface import Interface

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
INTERFACE_DIR = os.path.join(CURRENT_DIR, "stub_interfaces")

@pytest.fixture
def interface_loader():
    return interfaceloader.InterfaceLoader(INTERFACE_DIR)

@pytest.mark.parametrize(("interface_file"), [
    "interface-ls.yml",
    "interface-pwd.yml"
    ])
def test_find_interface_files(interface_file):
    '''find a list of interface .yml files in interface dir
    '''

    found_files = interfaceloader.InterfaceLoader.find_interface_files(INTERFACE_DIR)

    assert interface_file in found_files

@pytest.mark.parametrize(("interface_file", "name", "version", "command", "arguments"), [
    ("interface-ls.yml","List items", 8.28, "ls", { "flags":{"long_format":{"flag":"l", "description":"print in long format"}, "all_content":{"flag":"a","description":"print all content"}}, "values":["path"] })
    ])
def test_create_interface(interface_file, name, version, command, arguments):
    '''Create Interface object by parsing interface_file

    Args:
        interface_file (String): valid interface .yml file
    '''

    interface = interface.InterfaceLoader.create_interface(interface_file)

    assert interface.name == name
    assert interface.version == version
    assert interface.command == command
    assert interface.arguments == arguments
