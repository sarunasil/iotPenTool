#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
message testing set

By sarunasil
"""

import unittest

from iotpentool import mymessage

class TestMessage(unittest.TestCase):
    '''message class tests
    '''

    def test_print_message_error(self):
        '''Test error message
        '''
        msg = "A"
        result = mymessage.Message.print_message(mymessage.MsgType.ERROR, msg)

        self.assertEqual(result, mymessage.MsgType.ERROR.value+": "+msg)

    def test_print_message_warning(self):
        '''Test warning message
        '''
        msg = "A"
        result = mymessage.Message.print_message(mymessage.MsgType.WARNING, msg)

        self.assertEqual(result, mymessage.MsgType.WARNING.value+": "+msg)

    def test_print_message_info(self):
        '''Test info message
        '''
        msg = "A"
        result = mymessage.Message.print_message(mymessage.MsgType.INFO, msg)

        self.assertEqual(result, mymessage.MsgType.INFO.value+": "+msg)

if __name__ == "__main__":
    unittest.main()
