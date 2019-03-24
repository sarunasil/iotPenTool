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
		self.assets_filepath = assets_filepath

	def update_known_assets(self):
		'''writes current asset value to model-assets.yml file

		Raises:
			ModellingException: 
		'''

		known_assets = Asset.fetch_known_assets(self.assets_filepath)
		known_assets[self.name] = self.description

		try:
			with open(self.assets_filepath, 'w') as assets_file:
				assets_file.write("assets:\n")
				for name, desc in known_assets.items():
					s = "  '"+name+"': '"+desc+"'\n"
					assets_file.write(s)
		except IOError as e:
			raise ModellingException("Could not append assets file. "+ e.strerror)

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

		if not os.path.isfile(assets_filepath):
			Asset.create_file(assets_filepath)

		content = None
		with open(assets_filepath, 'r') as stream:
			try:
				content = yaml.safe_load(stream)
			except yaml.YAMLError as exc:
				raise ModellingException("Could not parse asset file "+ assets_filepath +". \n"+str(exc))

		if not content or 'assets' not in content:
			raise ModellingException("Asset file is corrupt: " + assets_filepath)

		if content['assets']:
			for asset, asset_desc in content['assets'].items():
				known_assets[asset] = asset_desc

		return known_assets

	@staticmethod
	def create_file(assets_filepath):
		'''Create empty default assets file if it does not exist

		Args:
			assets_filepath (String): path for empty model_assets.yml file
		'''
		try:
			with open(assets_filepath, 'w') as assets_file:
				s = "assets:\n\n"
				assets_file.write(s)
		except IOError as e:
			raise ModellingException("Could not create assets file. "+ e.strerror)
