#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
class representing Asset of IoT system form modelling
e.g. router, smart bell, etc

By sarunasil
"""

import os
import uuid
import yaml

from iotpentool.technology import Technology
from iotpentool.utils import Message, MsgType, ModellingException


class Asset():
	'''Represents the one Asset of IoT system
	'''

	def __init__(self, name, description, assets_filepath):
		'''Init
		'''

		self.name = name
		self.description = description
		self.technologies_present = {}
		self.assets_filepath = assets_filepath

	def add_technology(self, name, description, attributes):
		if name in self.technologies_present:
			raise ModellingException("Could not add technology: "+ name)

		self.technologies_present[name] = Technology(name, description, attributes)

	def update_known_assets(self):
		'''writes current asset value to model-assets.yml file

		Raises:
			ModellingException: 
		'''

		try:
			with open(self.assets_filepath, 'a') as assets_file:
				s = "  '"+self.name+"': '"+self.description+"'\n"
				assets_file.write(s)
		except IOError as e:
			raise ModellingException("Could not create assets file. "+ e.strerror)

	@staticmethod
	def fetch_known_assets(assets_filepath):
		'''
		reads and returns content of the file used to 'cache' all already used Assets to minimise persons typing

		Args:
			assets_filepath (String): path to file of set of used assets info

		Raises:
			ModellingException: if a problem arrises report

		Returns:
			dict(String:String): assets from file name:description
		'''

		known_assets = {}

		content = None
		with open(assets_filepath, 'r') as stream:
			try:
				content = yaml.safe_load(stream)
			except yaml.YAMLError as exc:
				Message.print_message(MsgType.ERROR, "Could not parse asset file "+ assets_filepath +". \n"+str(exc))

		if not content or 'assets' not in content:
			raise ModellingException("Asset file is corrupt: " + assets_filepath)

		if content['assets']:
			for asset, asset_desc in content['assets'].items():
				known_assets[asset] = asset_desc

		return known_assets


