#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing messageet
Interface loader

By sarunasil
"""

import re
from os import listdir, path
import yaml

import interface
from message import Message, MsgType

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

    data_dir = None
    interfaces = {}

    def __init__(self, data_dir):
        '''Init
        '''

        self.data_dir = data_dir

        #get content of the data_dir
        #only select files which:
        #   - start with 'interface-'
        #   - end in .yml or .yaml
        #   - are not interface-example
        content = listdir(self.data_dir)
        regex = re.compile(r"^interface-(?!example)\w+.(yml|yaml)$")
        content = list(filter(regex.search, content))

        #create Interface instances
        for file_name in content:
            full_path = path.join(data_dir, file_name)

            self.create_interface(full_path)
        print(content)

    def create_interface(self, file_path):
        '''Creates an interface from a YML file and returns the new Interface object

        Arguments:
            file_path {String} -- full path to a specific interface file
        '''

        inter = interface.Interface()


        #read file
        content = self.read_interface_file(file_path)

        #parse 'content' and create Interface instance
        if 'tool' in content:
            tool = content.get('tool')

            if ('name' not in tool or
                'version' not in tool or
                'command' not in tool or
                'arguments' not in tool
                ):
                Message.print_message(MsgType.ERROR, file_path+" file is corrupt. Could not find 'name', 'version', command' or arguments' fields")
                return None

            inter.name = tool.get('name')
            inter.version = tool.get('version')
            inter.command = tool.get('command')

            arguments = tool.get('arguments')

            if ('flags' not in arguments or
                'values' not in arguments):
                Message.print_message(MsgType.ERROR, file_path+" file is corrupt. Could not find 'flags or 'values' fields")
                return None

            flags = arguments.get('flags')
            for flag in flags:
                print ("--> ",flag)

                #save every flag separately 


            values = tool.get('values')




    def read_interface_file(self, file_path):
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
