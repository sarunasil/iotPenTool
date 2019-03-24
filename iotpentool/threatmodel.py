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
from iotpentool.entrypoint import EntryPoint
from iotpentool.utils import ModellingException
from iotpentool.threatmodelgui import ThreatModelController
from iotpentool.technology import Technology


class ThreatModel():
	'''Represents the overall threat model
	'''

	def __init__(self, arch_site, dataflow_site, model_dir):
		'''Init
		'''

		self.id = str(uuid.uuid4())
		self.model_dir = model_dir
		self.assets = {}
		self.assets_file = os.path.join(self.model_dir, "model-assets.yml")

		self.architectural_diagram_site = arch_site
		self.architectural_diagram = ""

		self.technologies = {}
		self.technologies_file = os.path.join(self.model_dir, "model-technologies.yml")

		self.data_flow_diagram_site = dataflow_site
		self.data_flow_diagram = ""

		self.entry_points = {}
		self.threats = {}

		self.threat_model_controller = None

	def add_asset(self, name, describtion, cache=True):
		'''add new asset to threat model
		'''
		if name in self.assets:
			raise ModellingException("Could not add duplicate asset: "+name+".")

		self.assets[name] = Asset(name, describtion, self.assets_file)
		if cache:
			self.assets[name].update_known_assets()

		return self.assets[name]

	def delete_asset(self, asset):
		self.assets.pop(asset.name, None)

	def add_technology(self, name, description, attributes):
		if name in self.technologies:
			raise ModellingException("Could not add duplicate technology: "+name+".")

		technologies_file = os.path.join(self.model_dir, "model-technologies.yml")
		self.technologies[name] = Technology(name, description, attributes, technologies_file)

		return self.technologies[name]

	def add_entry_point(self, name, description):
		'''add new entry point to threat model
		'''
		if name in self.entry_points:
			raise ModellingException("Could not add duplicate entry point: "+ name+".")

		self.entry_points[name] =  EntryPoint(name, description, self.assets)


	def add_threat(self):
		pass

	def generate_gui(self):
		self.threat_model_controller = ThreatModelController(self)



