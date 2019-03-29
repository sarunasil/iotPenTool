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
from iotpentool.technology import Technology
from iotpentool.entrypoint import EntryPoint
from iotpentool.threat import Threat
from iotpentool.utils import ModellingException

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
MODEL_DIR = os.path.join(CURRENT_DIR, "stub_model")
@pytest.fixture
def threat_model():
	return ThreatModel("stub","stub", MODEL_DIR)

@pytest.mark.parametrize(("arch_site","dataflow_site"), [("https://www.lucidchart.com", "https://www.lucidchart.com")])
def test_init(arch_site, dataflow_site):
	'''create config file
	'''
	threatmodel = ThreatModel(arch_site, dataflow_site, MODEL_DIR)

	assert threatmodel
	assert threatmodel.id
	assert isinstance(threatmodel.assets, dict)
	assert threatmodel.architectural_diagram_site == arch_site
	assert threatmodel.architectural_diagram == ''
	assert threatmodel.data_flow_diagram_site == dataflow_site
	assert threatmodel.data_flow_diagram == ''
	assert isinstance(threatmodel.entry_points, dict)
	assert threatmodel.model_dir == MODEL_DIR


@pytest.mark.parametrize(("name", "description"), [
	("router", "router description")
	])
def test_add_asset(threat_model, name, description):
	'''adding new asset to model
	'''
	threat_model.add_asset(name, description, cache=False)

	assert name in threat_model.assets
	assert isinstance(threat_model.assets[name], Asset)


@pytest.mark.parametrize(("name", "description"), [
	("router", "router description")
	])
def test_add_asset_duplicate(threat_model, name, description):
	'''adding new asset to model
	'''
	threat_model.add_asset(name, description, cache=False)
	threat_model.add_asset(name, description+"1", cache=False)

	assert len(threat_model.assets) == 1
	assert threat_model.assets[name].description == description+"1"


@pytest.mark.parametrize(("name","description", "attributes", "used_in"), [
	(
		"HTTP", 
		"smth about http", 
		{
			"Header":"Host: net.tutsplus.com User-Agent: Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729) Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
		},
		{"some_name":"Asset_object"}
	)
])
def test_add_technology(threat_model, name, description, attributes, used_in):
	threat_model.add_technology(name, description, attributes, used_in, cache=False);

	assert name in threat_model.technologies
	assert isinstance(threat_model.technologies[name], Technology)


@pytest.mark.parametrize(("name","description", "attributes", "used_in"), [
	(
		"HTTP", 
		"smth about http", 
		{},
		{"some_name":"Asset_object"}
	)
])
def test_add_technology_duplicate(threat_model, name, description, attributes, used_in):
	threat_model.add_technology(name, description, attributes, used_in, cache=False)
	threat_model.add_technology(name, description+"1", attributes, used_in, cache=False)

	assert len(threat_model.technologies) == 1
	assert threat_model.technologies[name].description == description+"1"


@pytest.mark.parametrize(("name","description", "asset_used"), [
	(
		"Firmware",
		"The DVR utilizes firmware to control the device but may only be acquired via vendor technical support (per documentation). The embedded web server utilizes the firmware for managing actions.",
		"stub_ASSET_object"
	)
])
def test_add_entry_point(threat_model, name, description, asset_used):
	threat_model.add_entry_point(name, description, asset_used, cache=False)

	assert name in threat_model.entry_points
	assert isinstance(threat_model.entry_points[name], EntryPoint)


@pytest.mark.parametrize(("name","description","asset_used"), [
	(
		"Firmware", 
		"The DVR utilizes firmware to control the device but may only be acquired via vendor technical support (per documentation). The embedded web server utilizes the firmware for managing actions.",
		"stub_ASSET_object"
	)
])
def test_add_entry_point_duplicate(threat_model, name, description, asset_used):
	'''try adding duplicate entry point to model
	'''

	threat_model.add_entry_point(name, description, asset_used, cache=False)
	threat_model.add_entry_point(name, description+"1", asset_used, cache=False)

	assert len(threat_model.entry_points) == 1
	assert threat_model.entry_points[name].description == description+"1"


@pytest.mark.parametrize(("desc1", "target1", "attack_tech1", "counter1", "entry_point1", "technologies1", "score1", "uid1"), [
		("stub", "stub", "stub", "stub", "stub", "stub", "stub", None),
		("stub1", "stub", "stub", "stub", "stub", "stub", "stub", "123")
])
def test_add_threat(threat_model, desc1, target1, attack_tech1, counter1, entry_point1, technologies1, score1, uid1):
	threat_model.add_threat(desc1, target1, attack_tech1, counter1, entry_point1, technologies1, score1, uid1)

	assert len(threat_model.threats) == 1
	for _, threat in threat_model.threats.items():
		assert isinstance(threat, Threat)


@pytest.mark.parametrize(("desc", "target", "attack_tech", "counter", "entry_point", "technologies", "score", "uid"), [
		("stub", "stub", "stub", "stub", "stub", "stub", "stub", "123")
])
def test_add_threat_duplicate(threat_model, desc, target, attack_tech, counter, entry_point, technologies, score, uid):
	threat_model.add_threat(desc, target, attack_tech, counter, entry_point, technologies, score, uid)
	threat_model.add_threat(desc+"1", target, attack_tech, counter, entry_point, technologies, score, uid)

	assert len(threat_model.threats) == 1
	assert threat_model.threats[uid].description == desc+"1"

def test_clear_assets_cache():
	pass

def test_clear_technologies_cache():
	pass

def test_clear_entry_points_cache():
	pass

