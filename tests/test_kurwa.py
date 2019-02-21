#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
application config loading testing set

By sarunasil
"""

import unittest
import random
import os


from iotpentool import configmanager

CONFIG_FILE = os.path.join(path.dirname(os.path.realpath(__file__)), 'test_config.ini')

class TestConfig(unittest.TestCase):
    '''config load, read tests
    '''
    def setUp(self):
        '''init
        '''

        self.config_manager = configmanager.ConfigManager()

    # def test_create_config(self):
    #     '''create config file
    #     '''
    #     file_path = str(random.randint(0, 100)) + CONFIG_FILE
    #     configg, successes = self.config_manager.read_config(file_path)

    #     self.assertEqual(successes, list())

    #     result = self.config_manager.create_config(configg)
    #     self.assertEqual(result, 0)

    #     os.remove(file_path)


    def test_read_config(self):
        '''Test read of config file
        '''
        configg, successes = self.config_manager.read_config(CONFIG_FILE)

        print("TEST_CONFIG ",str(configg), str(successes))
        print(os.getcwd())
        l = ["test_config.ini"]
        self.assertTrue(l in successes)

if __name__ == "__main__":
    unittest.main()
