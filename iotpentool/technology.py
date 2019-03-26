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

	def __init__(self, name, description, attributes, used_in, tech_filepath):
		'''Init
		'''

		self.name = name
		self.description = description
		self.attributes = attributes
		self.used_in = used_in
		self.tech_filepath = tech_filepath

	def update_known_technologies(self):
		'''writes current technology value to model-technologies.yml file

		Raises:
			ModellingException
		'''

		known_technologies = Technology.fetch_known_technologies(self.tech_filepath)
		known_technologies[self.name] = {
			"name": self.name,
			"description": self.description,
			"attributes": self.attributes
		}

		try:
			with open(self.tech_filepath, 'w') as technologies_file:
				technologies_file.write("technologies:\n")
				for tech_name, tech in known_technologies.items():
					technologies_file.write("  '"+tech_name+"':\n")
					technologies_file.write("    name: '"+tech['name']+"'\n")
					technologies_file.write("    description: '"+tech['description']+"'\n")
					technologies_file.write("    attributes: \n")
					if tech['attributes']:
						for attr_name, attr_value in tech['attributes'].items():
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
			dict(String:dict): technologies from file tech_name:{name:tech_name, description:tech_desc, attributes: {attr1:attr1value, atrrX:attrXvalue, ...} }
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
			for tech, tech_data in content['technologies'].items():
				# technology = Technology(tech_data['name'], tech_data['description'], tech_data['attributes'], tech_filepath)
				known_technologies[tech] = tech_data

		return known_technologies

	@staticmethod
	def create_file(tech_filepath):
		'''Create empty default technologies file if it does not exist

		Args:
			tech_filepath (String): path for empty model_technologies.yml file
		'''
		try:
			with open(tech_filepath, 'w') as technologies_file:
				s = "technologies:\n\n"
				technologies_file.write(s)
		except IOError as e:
			raise ModellingException("Could not create technologies file. "+ e.strerror)
