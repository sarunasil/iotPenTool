#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
application config loading testing set

By sarunasil
"""

import pytest
import random
import os


from iotpentool import configmanager, mymessage

CONFIG_FILE = 'stub_config.ini'
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_FILE_PATH = os.path.join(CURRENT_DIR, CONFIG_FILE)

@pytest.fixture
def config_manager():
    return configmanager.ConfigManager(CURRENT_DIR)


@pytest.mark.parametrize(("file_path", "overwrite"), [
    ("123.ini", False),
    ("123.ini", True),
    (CONFIG_FILE_PATH, True)
    ])
def test_create_config(config_manager, file_path, overwrite):
    '''create config file
    '''

    result = config_manager.create_config(file_path, overwrite)

    assert result == mymessage.Outcome.SUCCESS
    assert os.path.isfile(file_path)

    #cleanup
    if file_path != CONFIG_FILE_PATH:
        os.remove(file_path)


@pytest.mark.parametrize(("file_path", "overwrite"), [
    (CONFIG_FILE_PATH, False)
    ])
def test_create_config_fail(config_manager, file_path, overwrite):
    '''create config file
    '''

    result = config_manager.create_config(file_path, overwrite)

    assert result == mymessage.Outcome.FAILURE


@pytest.mark.parametrize(("file_path", "outcome"), [
    (CONFIG_FILE_PATH, True),
    ("no_file.ini", False)
    ])
def test_parse_config(config_manager, file_path, outcome):
    '''Test read of config file
    '''

    result = config_manager.parse_config(file_path)

    if outcome:
        assert result == mymessage.Outcome.SUCCESS
        assert config_manager.data_dir == os.path.join(CURRENT_DIR, "../data/")
        assert config_manager.interface_dir == os.path.join(CURRENT_DIR, "../data/interfaces")
    else:
        assert result == mymessage.Outcome.FAILURE

def test_parse_config_default(config_manager):
    '''Test default config file read'''

    result = config_manager.parse_config()

    assert result == mymessage.Outcome.SUCCESS
    assert config_manager.data_dir == os.path.join(CURRENT_DIR, "../data/")
    assert config_manager.interface_dir == os.path.join(CURRENT_DIR, "../data/interfaces")