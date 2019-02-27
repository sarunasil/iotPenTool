#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
Interface instance class

By sarunasil
"""
'''
tool:
  name: tool_name
  version: tool_version
  command: tool_call_name
  flags:
    iden:
      flag: flag
      description: description
    iden:
      description: description
'''

from abc import ABC

class Argument(ABC):
  '''Abstract argument class to be inherited by Flag and Value
  '''

  def __init__(self, iden, description):
    '''Init
    '''

    self.iden = iden
    self.description = description

  def __eq__(self, other):
    '''Overwrite == comparison operation for Flag objects. != overwritten automatically

    Args:
      other (Flag): another object to compare with

    Returns:
      Boolean: eqaul or not
    '''

    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__


class Flag(Argument):
  '''Object representing command flag instance 
  '''

  def __init__(self, iden, flag, description):
    '''Init
    '''
    Argument.__init__(self, iden, description)
    self.flag = flag

class Value(Argument):
  '''Object representing value taken by the command'''

  def __init__(self, iden, description):
    '''Init
    '''
    Argument.__init__(self, iden, description)


class Interface():
  '''Adapter between main program an the module in use
  module can refer to any program that is callable via an terminal

  Defines all the methods required to interact with the module
  '''

  def __init__(self, name, version, command):
    '''Init

    Args:
      name (String): print name / identifier
      version (String):
      command (String): terminal command to execute
    '''

    self.name = name       #print name
    self.version = version #version
    self.command = command #terminal call name
    self.flags = {}     #parameters program can take
    self.values = {}   #values provided without a flag e.g. 'ls /dev'

  def add_flag(self, iden, data):
    '''Add new flag object

    Args:
      iden (String): unique flag identifier
      data (dict): yml like structure with flag data
    '''

    if ("flag" not in data or
        "description" not in data
        ):
        raise DataException("Data file is corrupt. Could not find 'flag', 'description' fields in "+iden)

    flag_inst = Flag(iden, data['flag'], data['description'])

    self.flags[iden] = flag_inst


  def add_value(self, iden, data):
    '''Add new value to values

    Args:
      iden (String): unique value identifier
      data (dict): yml like structure with value data
    '''

    if ("description" not in data):
        raise DataException("Data file is corrupt. Could not find 'description' fields in "+iden)

    value_inst = Value(iden, data['description'])

    self.values[iden] = value_inst

  def execute(self, param):
    '''Executes a specific module command 
    according to parameters given

    Arguments:
        param {[type]} -- [description]
    '''





