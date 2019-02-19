#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
Useful functions and classes

By sarunasil
"""

import enum

class MsgType(enum.Enum):
    '''Message type enum
    '''

    ERROR = 'ERROR'
    WARNING = 'WARNINIG'
    INFO = 'INFO'


class Message:
    '''Message generation class
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
            raise ValueError("Wrong message type")

        message += ": " + msg

        print(message)
