#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
message testing set

By sarunasil
"""

import pytest

from iotpentool import mymessage

@pytest.mark.parametrize("msg_type", [
    mymessage.MsgType.INFO,
    mymessage.MsgType.WARNING,
    mymessage.MsgType.ERROR
    ])
def test_print_message(msg_type):
    '''Test error message
    '''
    msg = "A"
    result = mymessage.Message.print_message(msg_type, msg)

    assert result == msg_type.value+": "+msg

