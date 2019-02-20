#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing messageet
Startup file file

By sarunasil
"""
import configparser
import sys
from os import getcwd, path, curdir


from message import Message, MsgType
import maingui
import interfaceloader



CONFIG_FILE = path.join(path.dirname(path.realpath(__file__)), "../data/config.ini")

class Main():
    '''Main class of the application
    Reads configuration file
    Starts InterfaceLoader
    Starts MainGUI
    '''

    root_dir = None

    data_dir = None
    interface_dir = None

    interface_loader = None
    main_gui = None

    def __init__(self):
        '''Init
        '''

        self.root_dir = path.dirname(path.realpath(__file__))+"/"
        self.read_config()

        self.interface_loader = interfaceloader.InterfaceLoader(self.interface_dir)

        self.main_gui = maingui.MainGui()


    def read_config(self):
        '''Reads hardcoded yaml config file
        '''
        config = configparser.ConfigParser()
        data = config.read(CONFIG_FILE)

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
                self.read_config()
            except:
                Message.print_message(MsgType.ERROR, "Could not create config file")

        #debug
        print(data)

    @staticmethod
    def create_config(config):
        '''Creates a new config.ini file
        '''

        Message.print_message(MsgType.WARNING, "config file not found or corrupt. Trying to recreate defaults")

        section = 'General'
        if not config.has_section(section):
            config.add_section('General')
        if not config.has_option(section, 'data_dir'):
            config.set('General', 'data_dir', '../data/')
        if not config.has_option(section, 'defualt_file'):
            config.set('General', 'interface_dir', '../data/interfaces')

        with open(CONFIG_FILE, 'w') as configfile:
            config.write(configfile)
            #all good
        #if smth went wrong - exception



if __name__ == "__main__":
    Main()
