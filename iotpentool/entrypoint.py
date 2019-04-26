#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
class describing IoT system entry point - interaction that may have a vulnerability

By sarunasil
"""

import os
from ruamel import yaml

from iotpentool.utils import ModellingException


class EntryPoint():
	'''Represents single system interaction and possible exploitation place
	'''

	def __init__(self, name, description, asset_used, entry_points_filepath):
		'''Init
		'''

		self.name = name
		self.description = description
		self.asset_used = asset_used
		self.entry_points_filepath = entry_points_filepath

	def update_known_entry_points(self):
		'''writes current entry_point value to model-entry_points.yml file

		Raises:
			ModellingException
		'''

		known_entry_points = EntryPoint.fetch_known_entry_points(self.entry_points_filepath)
		known_entry_points[self.name] = self.description

		try:
			with open(self.entry_points_filepath, 'w') as entry_points_file:
				yaml.safe_dump({"entry_points":known_entry_points}, entry_points_file)
				# entry_points_file.write("entry_points:\n")
				# for name, desc in known_entry_points.items():
				# 	s = "  '"+name+"': '"+desc+"'\n"
				# 	entry_points_file.write(s)
		except IOError as e:
			raise ModellingException("Could not append EntryPoints file. "+ e.strerror)

	@staticmethod
	def fetch_known_entry_points(entry_points_filepath):
		'''
		reads and returns content of the file used to 'cache' all already used EntryPoints to minimise persons typing

		Args:
			entry_points_filepath (String): path to file of set of used entry_points info

		Raises:
			ModellingException: if a problem arrises report

		Returns:
			dict(String:String): entry_points from file entry_point_name:entry_point_desc
		'''

		known_entry_points = {}

		if not os.path.isfile(entry_points_filepath):
			EntryPoint.create_file(entry_points_filepath)

		content = None
		with open(entry_points_filepath, 'r') as stream:
			try:
				content = yaml.safe_load(stream)
			except yaml.YAMLError as exc:
				raise ModellingException("Could not parse entry_points file "+ entry_points_filepath +". \n"+str(exc))

		if not content or 'entry_points' not in content:
			raise ModellingException("EntryPoint file is corrupt: " + entry_points_filepath)

		if content['entry_points']:
			for name, desc in content['entry_points'].items():
				known_entry_points[name] = desc

		return known_entry_points

	@staticmethod
	def create_file(entry_points_filepath):
		'''Create empty default EntryPoints file if it does not exist

		Args:
			entry_points_filepath (String): path for empty model_entry_points.yml file
		'''
		try:
			with open(entry_points_filepath, 'w') as entry_points_file:
				s = "entry_points:\n\n"
				entry_points_file.write(s)
		except IOError as e:
			raise ModellingException("Could not create entry_points file. "+ e.strerror)

