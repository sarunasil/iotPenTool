#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
class representing technology used in one of the IoT systems assets

By sarunasil
"""

import os


class Technology():
	'''Represents 1 technology used for by IoT asset
	'''
	known_assets = {}

	def __init__(self, name, description, attributes):
		'''Init
		'''

