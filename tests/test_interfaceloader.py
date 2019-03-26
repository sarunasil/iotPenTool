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
from PyQt5 import QtWidgets



from iotpentool import interfaceloader, utils
from iotpentool import interface

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
INTERFACE_DIR = os.path.join(CURRENT_DIR, "stub_interfaces")

@pytest.fixture
def application():
	return QtWidgets.QApplication([])

@pytest.mark.parametrize(("directory"), [
    INTERFACE_DIR,
    os.path.join(CURRENT_DIR, "empty_dir")
    ])
def test_init(application, directory):
    interface_loader = interfaceloader.InterfaceLoader(directory)
    assert interface_loader.interface_dir == directory
    num = interfaceloader.InterfaceLoader.find_interface_files(directory)
    assert len(interface_loader.interfaces) == len(num)


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
        "category":"WIRELESS",
        "name":"List items",
        "version":"8.28",
        "command": "ls",
        "description":"list items command description",
        "flags":[
            {"long_format":{
                "flag":"l",
                "has_value":True,
                "description":"print in long format"
                },
            },
            {"all_content":{
                "flag":"a",
                "has_value":False,
                "description":"print all content"
                }
            }
        ],
        "values":[
            {
            "path":{
                "default_value": ".",
                "description":"path to folder"
                }
            }
        ],
        "structure": [
            "COMMAND",
            {
            "FLAGS": [
                "-",
                "FLAG",
                " ",
                "FLAG_VALUE",
                " "
                ]
            },
            {
            "VALUES": [
                "VALUE",
                " "
                ]
            }
            ]
        }
    }),
    ("interface-pwd.yml", {"tool":{
        "category":"WIRELESS",
        "name":"Print Current Working dir",
        "version": "1",
        "command":"pwd",
        "description":"Print Current Working dir command description",
        "flags":[
            {"physical":{
                "flag":"P",
                "has_value": False,
                "description": "display physical path"
                }
            }
        ],
        "structure": [
            "COMMAND", 
            {
            "VALUES": [
                "VALUE", 
                " "
            ]
            }, 
            {
            "FLAGS": [
                "-", 
                "FLAG", 
                " ", 
                "FLAG_VALUE", 
                " "
            ]
            }
        ]
        }
    }),
    ("interface-ls_nested.yml", {"tool":{
        "category":"WIRELESS",
        "name":"List items",
        "version":"8.28",
        "command": "ls_nested",
        "description":"list items command description",
        "flags":[
            {"nested_long":{
                "flag":"l",
                "has_value":True,
                "description":"print in long format",
                "flags":[
                    {"nested_flag1":{
                        "flag":"flag1^2",
                        "has_value":True,
                        "description":"flag flag description"
                        }
                    },
                    {"nested_flag2":{
                        "flag": "flag2^2",
                        "has_value": False,
                        "description": "[flag] [flag] description12312 12 flag flag description12312 12flag flag description12312 12"
                        }
                    }
                ]
                }
            },
            {"all_content":{
                "flag":"a",
                "has_value":False,
                "description":"print all content"
                }
            }
        ],
        "structure": [
            "COMMAND",
            {
            "FLAGS": [
                "-",
                "FLAG",
                " ",
                "FLAG_VALUE",
                " "
                ]
            },
            {
            "VALUES": [
                "VALUE",
                " "
                ]
            }
            ]
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


@pytest.mark.parametrize(("interface_data", "category", "name", "version", "command", "description", "flag_count", "value_count", "structure"), [
    (
        {"tool":{
            "category":"WIRELESS",
            "name":"List items",
            "version":"8.28",
            "command": "ls",
            "description":"list items command description",
            "flags":[
                {"long_format":{
                    "flag":"l",
                    "has_value":True,
                    "description":"print in long format"
                    }
                },
                {"all_content":{
                    "flag":"a",
                    "has_value":False,
                    "description":"print all content"
                    }
                }
            ],
            "values":[
                {"path":{
                    "default_value": ".",
                    "description":"path to folder"
                    }
                }
            ],
            "structure": [
                "COMMAND",
                {
                "FLAGS": [
                    "-",
                    "FLAG",
                    " ",
                    "FLAG_VALUE",
                    " "
                    ]
                },
                {
                "VALUES": [
                    "VALUE",
                    " "
                    ]
                }
                ]
            }
        },
        "WIRELESS",
        "List items", 
        "8.28", 
        "ls", 
        "list items command description",
        2, 
        1,
        [
            "COMMAND",
            { "FLAGS": [ "-", "FLAG", " ", "FLAG_VALUE", " " ] },
            { "VALUES": [ "VALUE", " " ] }
        ]
    ),
    (
        {"tool":{
            "category":"MOBILE APP",
            "name":"Print Current Working dir", 
            "version": "1", 
            "command":"pwd", 
            "description":"Print Current Working dir command description",
            "flags":[
                {"physical":{
                    "flag":"P", 
                    "has_value": False,
                    "description": "display physical path"
                    }
                }
            ],
            "structure": [
                "COMMAND", 
                {
                "VALUES": [
                    "VALUE", 
                    " "
                ]
                }, 
                {
                "FLAGS": [
                    "-", 
                    "FLAG", 
                    " ", 
                    "NESTED",
                    " ",
                    "FLAG_VALUE", 
                    " "
                ]
                }
                ]
            }
        }, 
        "MOBILE APP",
        "Print Current Working dir", 
        "1", 
        "pwd", 
        "Print Current Working dir command description",
        1, 
        0,
        [
            "COMMAND", 
            { "VALUES": [ "VALUE", " " ] }, 
            { "FLAGS": [ "-", "FLAG", " ", "NESTED", " ", "FLAG_VALUE", " " ] }
        ]
    ),
    (
        {"tool":{
            "category":"FIRMWARE",
            "name":"List items",
            "version":"8.28",
            "command": "ls_nested",
            "description":"list items command description",
            "flags":[
                {
                "long_format":{
                    "flag":"l",
                    "has_value":True,
                    "description":"print in long format",
                    "flags":[
                        {"nested_flag1":{
                            "flag":"flag1^2",
                            "has_value":True,
                            "description":"flag flag description"
                            }
                        },
                        {"nested_flag2":{
                            "flag": "flag2^2",
                            "has_value": False,
                            "description": "[flag]"
                            }
                        }
                    ]
                    }
                },
                {
                "all_content":{
                    "flag":"a",
                    "has_value":False,
                    "description":"print all content"
                    }
                }
                ],
            "structure": [
                "COMMAND",
                {
                "FLAGS": [
                    "-",
                    "FLAG",
                    " ",
                    "FLAG_VALUE",
                    " "
                    ]
                },
                {
                "VALUES": [
                    "VALUE",
                    " "
                    ]
                }
                ]
            }
        },
        "FIRMWARE",
        "List items", 
        "8.28", 
        "ls_nested", 
        "list items command description",
        2, 
        0,
        [
            "COMMAND",
            { "FLAGS": [ "-", "FLAG", " ", "FLAG_VALUE", " " ] },
            { "VALUES": [ "VALUE", " " ] }
        ]
    )
    ])
def test_create_interface(interface_data, category, name, version, command, description, flag_count, value_count, structure):
    '''Create Interface object by parsing interface_data

    Args:
        interface_data (dict): .yml like dict structure
    '''

    interface_created = interfaceloader.InterfaceLoader.create_interface(interface_data)

    assert interface_created.category == category
    assert interface_created.name == name
    assert interface_created.version == version
    assert interface_created.command == command
    assert interface_created.description == description
    assert interface_created.structure == structure
    assert len(interface_created.flags) == flag_count
    assert len(interface_created.values) == value_count
