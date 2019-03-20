#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
message testing set

By sarunasil
"""

import pytest

from iotpentool import utils

@pytest.mark.parametrize("msg_type", [
    utils.MsgType.INFO,
    utils.MsgType.WARNING,
    utils.MsgType.ERROR
    ])
def test_print_message(msg_type):
    '''Test error message
    '''
    msg = "A"
    result = utils.Message.print_message(msg_type, msg)

    assert result == msg_type.value+": "+msg

