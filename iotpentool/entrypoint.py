#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
class describing IoT system entry point - interaction that may have a vulnerability

By sarunasil
"""

import os

from iotpentool.utils import ModellingException


class EntryPoint():
	'''Represents single system interaction and possible exploitation place
	'''

	def __init__(self, name, description, assets_ref):
		'''Init
		'''

		self.name = name
		self.description = description
		self.assets_in_model = assets_ref
		self.asset_used = None
		self.technologies_used = {}

	def add_technology_ref(self, name):
		'''Adds a reference to of the technology used for this entry point

		Args:
			name (String): name of technology

		Raises:
			ModellingException: if couldn't find technology
		'''

		#technologies are globally unique but different instances of
		# Asset can have references to them
		# so there may be multiple ways of getting to the Technology with spec name
		# but all of them point to the same Technology instance
		for _, asset in self.assets_in_model.items():
			if name in asset.technologies_present:
				if name in self.technologies_used:
					raise ModellingException("Could not add duplicate technology: "+name)

				self.technologies_used[name] = asset.technologies_present[name]
				return

		raise ModellingException("Could not find technology of name: "+name)