#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
Config setup, read, write, default values

By sarunasil
"""

from os import path
import configparser
from iotpentool.mymessage import Message, MsgType, Outcome

CONFIG_FILE = path.join(path.dirname(path.realpath(__file__)), "../data/config.ini")

class ConfigManager():
    '''Manages config.ini file
    '''

    def __init__(self, root_dir):
        '''init
        '''
        self.data_dir = None
        self.interface_dir = None
        self.root_dir = root_dir

        self.config_parser = configparser.ConfigParser()

    def parse_config(self, file_path=CONFIG_FILE):
        '''Parses hardcoded yaml config file

        Arguments:
            file_path {string} -- config file path

        Returns:
            mymessage.Outcome.SUCCESS, mymessage.Outcome.FAILURE
        '''

        successes = self.config_parser.read(file_path)

        if not successes:
            Message.print_message(MsgType.ERROR, "Could not read config file: " + file_path)
            return Outcome.FAILURE

        corrupt = False
        section = 'General'
        if self.config_parser.has_section(section):
            if self.config_parser.has_option(section, 'data_dir'):
                self.data_dir = path.join(self.root_dir,self.config_parser.get(section, 'data_dir'))
            else:
                corrupt = True

            if self.config_parser.has_option(section, 'interface_dir'):
                self.interface_dir = path.join(self.root_dir, self.config_parser.get(section, 'interface_dir'))
            else:
                corrupt = True
        else:
            corrupt = True

        if corrupt:
            return Outcome.FAILURE

        return Outcome.SUCCESS

    def create_config(self, file_path=CONFIG_FILE, overwrite=True):
        '''Creates a new config.ini file

        file_path - file to be created

        Returns:
            mymessage.Outcome.SUCCESS, mymessage.Outcome.FAILURE
        '''
        if path.isfile(file_path) and not overwrite:
            Message.print_message(MsgType.ERROR, "Cannot overwrite existing file.")
            return Outcome.FAILURE

        section = 'General'
        self.config_parser.add_section(section)
        self.config_parser.set(section, 'data_dir', '../data/')
        self.config_parser.set(section, 'interface_dir', '../data/interfaces')


        try:
            with open(file_path, 'w') as configfile:
                self.config_parser.write(configfile)
                return Outcome.SUCCESS
                #all good
            #if smth went wrong - exception
        except e:
            Message.print_message(MsgType.ERROR, "Could not create config file. "+ e.msg)

        return Outcome.FAILURE
