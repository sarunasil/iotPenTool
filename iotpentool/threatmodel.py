#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
class representing whole Threat Model of particular system

By sarunasil
"""

import os
import uuid

from iotpentool.asset import Asset
from iotpentool.utils import ModellingException


class ThreatModel():
	'''Represents the overall threat model
	'''

	def __init__(self, arch_site, dataflow_site, model_dir):
		'''Init
		'''

		self.id = str(uuid.uuid4())
		self.assets = {}

		self.architectural_diagram_site = arch_site
		self.data_flow_diagram_site = dataflow_site
		self.architectural_diagram = ""
		self.data_flow_diagram = ""

		self.entry_points = {}
		self.model_dir = model_dir

	def add_asset(self, name, describtion):
		'''add new asset to threat model
		'''
		if name in self.assets:
			raise ModellingException("Could not add asset: "+ name)

		assets_file = os.path.join(self.model_dir, "/model-assets.yml")
		self.assets[name] = Asset(name, describtion, assets_file)

	def add_entry_point(self):
		'''add new entry point to threat model
		'''

		return 0
	