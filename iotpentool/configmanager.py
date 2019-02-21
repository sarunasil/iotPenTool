#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
Config setup, read, write, default values

By sarunasil
"""

from os import path
import configparser
from iotpentool.mymessage import Message, MsgType

CONFIG_FILE = path.join(path.dirname(path.realpath(__file__)), "../data/config.ini")

class ConfigManager():
    '''Manages config.ini file
    '''

    def __init__(self, root_dir=path.dirname(path.realpath(__file__))+"/"):
        '''init
        '''
        self.data_dir = None
        self.interface_dir = None
        self.root_dir = root_dir

    def read_config(self, file_path=CONFIG_FILE):
        '''Reads the CONFIG_FILE file

        Arguments:
            file_path {string} -- config file path

        Returns:
            ConfigParser, list of successfully parsed files
        '''

        config = configparser.ConfigParser()
        successes = config.read(file_path)
        print (file_path, successes)
        print ("data_dir", self.data_dir)

        return config, successes

    def parse_config(self, config):
        '''Parses hardcoded yaml config file

        Args:
            config (ConfigParser):

        Returns:
            0 - success, -1 - failure
        '''

        corrupt = False

        section = 'General'
        if config.has_section(section):
            if config.has_option(section, 'data_dir'):
                self.data_dir = self.root_dir + config.get(section, 'data_dir')
            else:
                corrupt = True

            if config.has_option(section, 'interface_dir'):
                self.interface_dir = self.root_dir + config.get(section, 'interface_dir')
            else:
                corrupt = True
        else:
            corrupt = True

        if corrupt:
            try:
                self.create_config(config)
                self.read_config(config.file_path)
                return 0
            except:
                Message.print_message(MsgType.ERROR, "Could not create config file")
                return -1
        return 0

    def create_config(self, config_parser):
        '''Creates a new config.ini file

        Arguments:
            config_parser {ConfigParser} -- ConfigParser object

        Returns:
            0 - success, -1 failure
        '''

        Message.print_message(MsgType.WARNING, "config file not found or corrupt. Trying to recreate defaults")

        section = 'General'
        if not config_parser.has_section(section):
            config_parser.add_section('General')
        if not config_parser.has_option(section, 'data_dir'):
            config_parser.set('General', 'data_dir', '../data/')
        if not config_parser.has_option(section, 'defualt_file'):
            config_parser.set('General', 'interface_dir', '../data/interfaces')

        with open(config_parser.file_path, 'w') as configfile:
            config_parser.write(configfile)
            return 0
            #all good
        #if smth went wrong - exception

        return -1
