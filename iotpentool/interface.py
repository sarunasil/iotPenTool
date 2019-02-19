#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
Interface instance class

By sarunasil
"""
'''
tool:
  - name: tool_name
  - version: tool_version
  - command: tool_call_name
  - arguments:
    - flags:
      - name:
        - flag: flag
        - description: description
    - values:
      - value_without_flag
'''

class Interface():
    '''Adapter between main program an the module in use
    module can refer to any program that is callable via an terminal

    Defines all the methods required to interact with the module
    '''

    name = None     #print name
    version = None  #version
    command = None  #terminal call name
    arguments = {}  #parameters program can take
    value = {}      #value provided without a flag e.g. 'ls /dev'


    def __init__(self):
        '''Init
        '''

    def execute(self, param):
        '''Executes a specific module command 
        according to parameters given

        Arguments:
            param {[type]} -- [description]
        '''





