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
from iotpentool import interface

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

@pytest.mark.parametrize(("interface_file", "content"), [
    ("interface-ls.yml", {"tool":{
        "name":"List items",
        "version":"8.28",
        "command": "ls",
        "flag_iden": "-",
        "flags":{
            "long_format":{
                "flag":"l",
                "has_value":False,
                "description":"print in long format"
                },
            "all_content":{
                "flag":"a",
                "has_value":False,
                "description":"print all content"
                }
            },
        "values":{
            "path":{
                "default_value": ".",
                "description":"path to folder"
                }
            }
        }
    }),
    ("interface-pwd.yml", {"tool":{
        "name":"Print Current Working dir", 
        "version": "1", 
        "command":"pwd", 
        "flag_iden": "-",
        "flags":{
            "help":{
                "flag":"h", 
                "has_value": False,
                "description":"help"
                } 
            }
        } 
    })
    ])
def test_read_interface_file(interface_file, content):
    '''Tests that interface_file is read correctly and json like structure is correct
    
    Args:
        interface_file (String): path to interface file to parse
        content (Set): correct outcome of the run
    '''

    interface_file_path = os.path.join(INTERFACE_DIR, interface_file)

    read_content = interfaceloader.InterfaceLoader.read_interface_file(interface_file_path)

    assert read_content == content


@pytest.mark.parametrize(("interface_data", "name", "version", "command", "flags", "values"), [
    (
        {"tool":{
            "name":"List items",
            "version":"8.28",
            "command": "ls",
            "flag_iden": "-",
            "flags":{
                "long_format":{
                    "flag":"l",
                    "has_value":False,
                    "description":"print in long format"
                    },
                "all_content":{
                    "flag":"a",
                    "has_value":False,
                    "description":"print all content"
                    }
                },
            "values":{
                "path":{
                    "default_value": ".",
                    "description":"path to folder"
                    }
                }
            }
        },
        "List items", 
        "8.28", 
        "ls", 
        [
            ["long_format", "l", False, "print in long format"],
            ["all_content", "a", False, "print all content"]
        ], 
        {"path":{
            "default_value":".",
            "description":"path to folder"
            }
        }
    ),
    (
        {"tool":{
            "name":"Print Current Working dir", 
            "version": "1", 
            "command":"pwd", 
            "flag_iden": "-",
            "flags":{
                "help":{
                    "flag":"h", 
                    "has_value": False,
                    "description":"help"
                    } 
                }
            } 
        }, 
        "Print Current Working dir", 
        "1", 
        "pwd", 
        [
            ["help", "h", False, "help"]
        ], 
        {}
    )
    ])
def test_create_interface(interface_data, name, version, command, flags, values):
    '''Create Interface object by parsing interface_data

    Args:
        interface_data (dict): .yml like dict structure
    '''

    interface_created = interfaceloader.InterfaceLoader.create_interface(interface_data)

    #create flag set from parameter values
    stub_flags = {}
    for flag_data in flags:
      f = interface._Flag(flag_data[0], flag_data[1], flag_data[2], flag_data[3])
      stub_flags[f.iden] = f

    #create values set from parameter values
    stub_values = {}
    for value_data in values:
      v = interface._Value(value_data, values[value_data]["default_value"], values[value_data]['description'])
      stub_values[v.iden] = v

    assert interface_created.name == name
    assert interface_created.version == version
    assert interface_created.command == command
    assert interface_created.flags == stub_flags
    assert interface_created.values == stub_values


def test_execute():
    assert False