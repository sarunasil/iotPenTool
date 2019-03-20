#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
application Asset testing set

By sarunasil
"""

import pytest
import random
import os


from iotpentool.threatmodel import ThreatModel
from iotpentool.asset import Asset
from iotpentool.technology import Technology
from iotpentool.utils import ModellingException

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
MODEL_DIR = os.path.join(CURRENT_DIR, "stub_model")

@pytest.fixture
def asset():
	return Asset("stub","stub","stub")

@pytest.mark.parametrize(("name","description", "filepath"), [("router", "router descr", "stub_filepath")])
def test_init(name, description, filepath):
	'''create new Asset
	'''

	asset = Asset(name, description, filepath)

	assert asset
	assert asset.name
	assert asset.description
	assert isinstance(asset.technologies_present, dict)


@pytest.mark.parametrize(("name","description", "attributes"), [
	(
		"HTTP", 
		"smth about http", 
		{
			"Header":"Host: net.tutsplus.com User-Agent: Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729) Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
		}
	)
])
def test_add_technology(asset, name, description, attributes):
	asset.add_technology(name, description, attributes);

	assert name in asset.technologies_present
	assert isinstance(asset.technologies_present[name], Technology)


@pytest.mark.parametrize(("content"), [
	([]),
	(["  'assetName1': 'desc_of_asset1'\n"]),
	(["  'assetName1': 'desc_of_asset1'\n","  'assetName2': 'desc_of_asset2'\n","  'assetName3': 'desc_of_asset3'\n"])
])
def test_update_known_assets(asset, content):

	#create stub model-assets.yml file

	assets_filepath = os.path.join(MODEL_DIR, "model-assets"+ str(random.randint(1,1001)) +".yml")
	try:
		with open(assets_filepath, 'w') as configfile:
			configfile.write("assets:\n")
			configfile.writelines(content)
	except IOError as e:
		print("Could not create assets file. "+ e.strerror)
		assert False
	asset.assets_filepath = assets_filepath

	#get prev assets
	prev_known_assets = Asset.fetch_known_assets(assets_filepath)

	#update assets file
	asset.update_known_assets()

	#get current assets
	current_known_assets = Asset.fetch_known_assets(assets_filepath)

	#delete that file
	os.remove(assets_filepath)

	#check that prev_assets + added asset == current_asssets
	assert { **prev_known_assets, **{asset.name: asset.description} } == current_known_assets



@pytest.mark.parametrize(("assets_file","outcome"), [
	(
		"model-assets.yml",
		{
			"assetName1":"desc_of_asset1",
			"assetName2":"desc_of_asset2",
			"assetName3":"desc_of_asset3"
		}
	),
	(
		"model-assets_empty.yml",
		{}
	)
])
def test_fetch_known_assets(assets_file, outcome):

	assets_filepath = os.path.join(MODEL_DIR, assets_file)
	known_assets = Asset.fetch_known_assets(assets_filepath)

	assert known_assets == outcome

@pytest.mark.parametrize(("assets_file","outcome"), [
	(
		"model-assets_corrupt.yml",
		{}
	)
])
def test_fetch_known_assets_exception(assets_file, outcome):

	with pytest.raises(ModellingException):
		assets_filepath = os.path.join(MODEL_DIR, assets_file)
		known_assets = Asset.fetch_known_assets(assets_filepath)