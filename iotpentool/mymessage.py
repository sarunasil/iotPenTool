#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
Useful functions and classes

By sarunasil
"""

import enum

class MsgType(enum.Enum):
    '''message type enum
    '''

    ERROR = 'ERROR'
    WARNING = 'WARNINIG'
    INFO = 'INFO'

class Outcome(enum.Enum):
    '''used to indicate function success, failure, etc
    '''

    SUCCESS = 0
    FAILURE = 1



class Message:
    '''message generation class
    '''

    @staticmethod
    def print_message(typee, msg):
        '''Generates a message of specific type

        Arguments:
            typee {MsgType} -- type of the message
            msg -- message it self
        '''

        message = ""
        if isinstance(typee, MsgType):
            message += typee.value
        else:
            raise DataException("Wrong message type")

        message += ": " + msg

        print (message)
        return message

class DataException(Exception):
    '''Exception for corrupt data 
    '''

    pass