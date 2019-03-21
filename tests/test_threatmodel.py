#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
application ThreatModel testing set

By sarunasil
"""

import pytest
import random
import os


from iotpentool.threatmodel import ThreatModel
from iotpentool.asset import Asset
from iotpentool.entrypoint import EntryPoint
from iotpentool.utils import ModellingException

@pytest.fixture
def threat_model():
	return ThreatModel("stub","stub", "stub")

@pytest.mark.parametrize(("arch_site","dataflow_site"), [("https://www.lucidchart.com", "https://www.lucidchart.com")])
def test_init(arch_site, dataflow_site):
	'''create config file
	'''
	threatmodel = ThreatModel(arch_site, dataflow_site, "stub")

	assert threatmodel
	assert threatmodel.id
	assert isinstance(threatmodel.assets, dict)
	assert threatmodel.architectural_diagram_site == arch_site
	assert threatmodel.architectural_diagram == ''
	assert threatmodel.data_flow_diagram_site == dataflow_site
	assert threatmodel.data_flow_diagram == ''
	assert isinstance(threatmodel.entry_points, dict)
	assert threatmodel.model_dir == "stub"


@pytest.mark.parametrize(("name", "description"), [
	("router", "router description")
	])
def test_add_asset(threat_model, name, description):
	'''adding new asset to model
	'''
	threat_model.add_asset(name, description)

	assert name in threat_model.assets
	assert isinstance(threat_model.assets[name], Asset)


@pytest.mark.parametrize(("name", "description"), [
	("router", "router description")
	])
def test_add_asset_duplicate(threat_model, name, description):
	'''adding new asset to model
	'''
	threat_model.add_asset(name, description)

	with pytest.raises(ModellingException):
		threat_model.add_asset(name, description)


@pytest.mark.parametrize(("name","description"), [
	(
		"Firmware", 
		"The DVR utilizes firmware to control the device but may only be acquired via vendor technical support (per documentation). The embedded web server utilizes the firmware for managing actions."
	)
])
def test_add_entry_point(threat_model, name, description):
	threat_model.add_entry_point(name, description)

	assert name in threat_model.entry_points
	assert isinstance(threat_model.entry_points[name], EntryPoint)


@pytest.mark.parametrize(("name","description"), [
	(
		"Firmware", 
		"The DVR utilizes firmware to control the device but may only be acquired via vendor technical support (per documentation). The embedded web server utilizes the firmware for managing actions."
	)
])
def test_add_entry_point_duplicate(threat_model, name, description):
	'''try adding duplicate entry point to model
	'''

	threat_model.add_entry_point(name, description)

	with pytest.raises(ModellingException):
		threat_model.add_entry_point(name, description)


# def test_add_threat(threat_model, short_desc, target, countermeasures, entry_point):
# 	size = len(threat_model.threats)

# 	threat_model.add_threat(short_desc, target, countermeasures, entry_point)

# 	assert size + 1 == len(threat_model.threats)
