#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
class representing whole Threat Model of particular system

By sarunasil
"""

import os
import uuid
from PyQt5 import QtCore

from iotpentool.asset import Asset
from iotpentool.entrypoint import EntryPoint
from iotpentool.utils import ModellingException
from iotpentool.threatmodelgui import ThreatModelController
from iotpentool.technology import Technology
from iotpentool.threat import Threat, DreadScore

class ThreatModel(QtCore.QObject):
	'''Represents the overall threat model
	'''
	assets_updated = QtCore.pyqtSignal()

	def __init__(self, arch_site, dataflow_site, model_dir, DEV=False):
		'''Init
		'''
		super(ThreatModel, self).__init__()

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
		self.entry_points_file = os.path.join(self.model_dir, "model-entry_points.yml")

		self.threats = {}

		self.threat_model_controller = None


		#DEV
		if DEV:
			self.add_asset("123", "bla", cache=False)
			self.add_asset("456", "blabla", cache=False)
			self.add_asset("789", "blablablabla blablablabla", cache=False)

			self.add_technology("tech1", "tech_descr", {"Atrr1":"value1"}, {}, cache=False)
			self.add_technology("tech2", "tech_descrr", {"Atrr1":"value1", "Attr2":"value2"}, {}, cache=False)
			self.add_technology("tech3", "tech_descrrr", {}, {"123":self.assets["123"]}, cache=False)
			self.add_technology("tech4", "tech_descrrrr", {"Atrr1":"value1"}, {"123":self.assets["123"]}, cache=False)
			self.add_technology("tech5", "tech_descrrrrr", {}, {"789":self.assets["789"]}, cache=False)
			self.add_technology("tech6", "tech_descrrrrrr", {"Atrr1":"value1"}, {"789":self.assets["789"]}, cache=False)

			self.add_entry_point("123_login", "bla bla", self.assets["123"])
			self.add_entry_point("123_keyboard", "keyboard qwerty", self.assets["123"])
			self.add_entry_point("456_cable", "bla blaa", self.assets["456"])
			self.add_entry_point("789_tablet", "bla blaaa", self.assets["789"])



	#ASSET

	def add_asset(self, name, describtion, cache=True):
		'''add new asset to threat model
		'''
		#if name already present - override (update that item)
		self.assets[name] = Asset(name, describtion, self.assets_file)
		if cache:
			self.assets[name].update_known_assets()

		self.assets_updated.emit()
		return self.assets[name]

	def delete_asset(self, asset):
		self.assets.pop(asset.name, None)
		self.assets_updated.emit()


	#TECHNOLOGY

	def add_technology(self, name, description, attributes, used_in, cache=True):
		'''Creates and adds new Technology object

		Args:
			name (String): tech name
			description (String): tech desc
			attributes (dict(String:String)): tech attributes
			used_in (dict(String:Asset)): Assets this Technology is used in
			cache (bool, optional): Defaults to True. [description]

		Returns:
			Technology: object created
		'''

		#if name already present - override (update that item)
		self.technologies[name] = Technology(name, description, attributes, used_in, self.technologies_file)
		if cache:
			self.technologies[name].update_known_technologies()

		return self.technologies[name]

	def delete_technology(self, technology):
		self.technologies.pop(technology.name, None)


	#ENTRY POINT

	def add_entry_point(self, name, description, asset_used, cache=True):
		'''add new entry point to threat model

		Args:
			name (String): EntryPoint name
			description (String): EntryPoint desc
			asset_used (Asset): asset where this entry point is present
		'''

		#if name already present - override (update that item)
		self.entry_points[name] =  EntryPoint(name, description, asset_used, self.entry_points_file)
		if cache:
			self.entry_points[name].update_known_entry_points()

		return self.entry_points[name]

	def delete_entry_point(self, entry_point):
		self.entry_points.pop(entry_point.name, None)


	#THREAT

	def add_threat(self, desc, target, attack_tech, counter, entry_point, technologies, score, uid):
		'''Add new threat entry in threat model

		Args:
			desc (String):
			target (String):
			attack_tech (String):
			counter (String):
			entry_point (EntryPoint):
			technologies (dict(String:Technology)):
			score (list[int]): list of all 5 categories in THAT order (as in the book)
			uid (String): not None if this is a Threat update
		'''
		dread = DreadScore(score)

		#if name already present - override (update that item)
		threat = Threat(desc, target, attack_tech, counter, entry_point, technologies, dread, uid)
		self.threats[threat.uid] = threat

		return threat

	def delete_threat(self, threat):
		self.threats.pop(threat.uid, None)

	# THREAT MODEL GUI

	def generate_gui(self):
		self.threat_model_controller = ThreatModelController(self)



