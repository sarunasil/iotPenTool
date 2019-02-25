#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
Startup file

By sarunasil
"""
from os import path


import configmanager
import maingui
import interfaceloader


class Main():
    '''Main class of the application
    Reads configuration file
    Starts InterfaceLoader
    Starts MainGUI
    '''

    def __init__(self):
        '''Init
        '''

        root_dir = path.dirname(path.realpath(__file__))
        config_manager = configmanager.ConfigManager(root_dir)

        result = config_manager.parse_config()
        if result == -1:
            result = config_manager.create_config()

        if result == 0:


        self.interface_loader = interfaceloader.InterfaceLoader(config_manager.interface_dir)

        self.main_gui = maingui.MainGui()


if __name__ == "__main__":
    Main()
