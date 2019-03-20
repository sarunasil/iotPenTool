#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
class representing technology used in one of the IoT system assets

By sarunasil
"""

import os
import yaml

from iotpentool.utils import ModellingException


class Technology():
	'''Represents 1 technology used by IoT assets
	'''

	def __init__(self, name, description, attributes, tech_filepath):
		'''Init
		'''

		self.name = name
		self.description = description
		self.attributes = attributes
		self.tech_filepath = tech_filepath

	def update_known_technologies(self):
		'''writes current technology value to model-technologies.yml file

		Raises:
			ModellingException
		'''

		try:
			with open(self.tech_filepath, 'a') as technologies_file:
				s = "  '"+self.name+"': '"+self.description+"'\n"
				technologies_file.write("  '"+self.name+"':\n")
				technologies_file.write("    name: '"+self.name+"'\n")
				technologies_file.write("    description: '"+self.description+"'\n")
				technologies_file.write("    attributes: \n")
				for attr_name, attr_value in self.attributes.items():
					technologies_file.write("      '"+attr_name+"': '"+attr_value+"' \n")
		except IOError as e:
			raise ModellingException("Could not append technology file. "+ e.strerror)

	@staticmethod
	def fetch_known_technologies(tech_filepath):
		'''
		reads and returns content of the file used to 'cache' all already used Technologies to minimise persons typing

		Args:
			tech_filepath (String): path to file of set of used technologies info

		Raises:
			ModellingException: if a problem arrises report

		Returns:
			dict(String:String): technologies from file tech_name:{name:tech_name, description:tech_desc, attributes: {attr1:attr1value, atrrX:attrXvalue, ...} }
		'''

		known_technologies = {}

		if not os.path.isfile(tech_filepath):
			Technology.create_file(tech_filepath)

		content = None
		with open(tech_filepath, 'r') as stream:
			try:
				content = yaml.safe_load(stream)
			except yaml.YAMLError as exc:
				raise ModellingException("Could not parse technologies file "+ tech_filepath +". \n"+str(exc))

		if not content or 'technologies' not in content:
			raise ModellingException("Technology file is corrupt: " + tech_filepath)

		if content['technologies']:
			for tech, tech_desc in content['technologies'].items():
				known_technologies[tech] = tech_desc

		return known_technologies

	@staticmethod
	def create_file(tech_filepath):
		'''Create empty default technologies file if it does not exist

		Args:
			tech_filepath (String): path for empty model_technologies.yml file
		'''
		try:
			with open(tech_filepath, 'w') as technologies_file:
				s = "technologies:\n"
				technologies_file.write(s)
		except IOError as e:
			raise ModellingException("Could not create technologies file. "+ e.strerror)
