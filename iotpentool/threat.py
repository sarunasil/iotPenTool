#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
class representing existant or possible IoT system threat/vulnerability

By sarunasil
"""

import os
import uuid

from iotpentool.utils import *


class DreadScore():
	'''Object representation of threat DREAD ranking
	'''

	def __init__(self, scores):

		self.damage = 0
		self.reproducibility = 0
		self.exploitability = 0
		self.affected_users = 0
		self.discoverability = 0
		self.total = 0

		if len(scores) != 5:
			Message.print_message(MsgType.ERROR, "DreadScore provided with corrupted values. Setting all values to 0")
			return

		self.damage = scores[0]
		self.reproducibility = scores[1]
		self.exploitability = scores[2]
		self.affected_users = scores[3]
		self.discoverability = scores[4]

		self.total = self.damage + self.reproducibility +self.exploitability + self.affected_users + self.discoverability


class Threat():
	'''Single discovered or theoretical IoT system threat
	'''

	def __init__(self, description, target, attack_tech, countermeassures, entry_point, technologies, dread, uid=None):
		'''Init
		'''

		self.uid = str(uuid.uuid4()) if not uid else uid
		self.description = description
		self.target = target
		self.attack_tech = attack_tech
		self.countermeassures = countermeassures
		self.entry_point_used = entry_point
		self.technologies_used = technologies
		self.dread = dread
