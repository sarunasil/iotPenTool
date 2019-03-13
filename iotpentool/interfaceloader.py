#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
Interface loader

By sarunasil
"""

import re
from os import listdir, path
import yaml

from iotpentool import interface
from iotpentool.mymessage import Message, MsgType, Outcome, DataException

class InterfaceLoader():
    '''Check it's pwd
        Go to ~/interfaces
        Read all files with "interaface_*.[ yml | yaml ]"
        For each file:
        - create an instance of Interface class (interface.py)
        - Validate it: correct format, all fields, executables point to files
        Store them smwh in InterfaceLoader
        Generates preview (basic) information for every interface to be displayed before opening
        Generate list of errors
    '''

    def __init__(self, interface_dir):
        '''Init
        '''

        self.interface_dir = interface_dir
        self.interface_files = set()
        self.interfaces = {}

        self.interface_files = InterfaceLoader.find_interface_files(interface_dir)

        #create Interface instances
        for file_name in self.interface_files:
            file_path = path.join(interface_dir, file_name)

            data = InterfaceLoader.read_interface_file(file_path)

            try:
                interface_instance = InterfaceLoader.create_interface(data)
                command = interface_instance.command

                self.interfaces[command] = interface_instance
            except DataException as de:
                Message.print_message(MsgType.WARNING, file_name+" "+str(de))


    @staticmethod
    def find_interface_files(interface_dir):
        #get content of the interface_dir
        #only select files which:
        #   - start with 'interface-'
        #   - end in .yml or .yaml
        #   - are not interface-example
        content = listdir(interface_dir)
        regex = re.compile(r"^interface-(?!example)\w+.(yml|yaml)$")
        content = set(filter(regex.search, content))

        return content


    @staticmethod
    def read_interface_file(file_path):
        '''Read interaface file, parse yaml content, create nested python dict from it

        Arguments:
            file_path {String} -- full path to a specific interface file
        '''
        content = None
        with open(file_path, 'r') as stream:
            try:
                content = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                Message.print_message(MsgType.ERROR, "Could not parse interface "+ file_path +". \n"+str(exc))

        return content


    @staticmethod
    def create_interface(data):
        '''Creates an interface from a YML file and returns the new Interface object

        Arguments:
            data {dict} -- nested yml like dict structure
        '''

        #parse 'data' and create Interface instance
        if 'tool' not in data:
            raise DataException("Data file is corrupt. Could not find 'tool' field")

        tool = data.get('tool')
        if ('name' not in tool or
            'version' not in tool or
            'command' not in tool or
            'description' not in tool or
            'flags' not in tool or
            'structure' not in tool
            ):
            raise DataException("Data file is corrupt. Could not find 'name', 'version', 'command', 'description' or 'flags' or 'structure' fields")

        #setup Interface instance
        inter = interface.Interface(tool.get('name'), tool.get('version'), tool.get('command'), tool.get('description'), tool.get('structure'))

        #parse Interface flags
        flags = tool.get('flags')
        for flag_name, flag_data in flags.items():
            inter.add_flag(flag_name, flag_data)

        #parse Interface values
        if 'values' in tool:
            values = tool.get('values')
            if values:
                for value_name, value_data in values.items():
                    inter.add_value(value_name, value_data)

        return inter


    def generate_guis(self):
        '''Calls generate_gui() for every interface
        '''

        for key, interface in self.interfaces.items():
            interface.generate_gui()


