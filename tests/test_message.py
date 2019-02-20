#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing messageet
Message testing set

By sarunasil
"""

import unittest

from iotpentool import message

class TestMessage(unittest.TestCase):
    '''Message class tests
    '''

    def test_print_message_error(self):
        '''Test error message
        '''
        msg = "A"
        result = message.Message.print_message(message.MsgType.ERROR, msg)

        self.assertEqual(result, message.MsgType.ERROR.value+": "+msg)

    def test_print_message_warning(self):
        '''Test warning message
        '''
        msg = "A"
        result = message.Message.print_message(message.MsgType.WARNING, msg)

        self.assertEqual(result, message.MsgType.WARNING.value+": "+msg)

    def test_print_message_info(self):
        '''Test info message
        '''
        msg = "A"
        result = message.Message.print_message(message.MsgType.INFO, msg)

        self.assertEqual(result, message.MsgType.INFO.value+": "+msg)

if __name__ == "__main__":
    unittest.main()
