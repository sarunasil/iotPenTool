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
	assert asset.name == name
	assert asset.description == description
	assert asset.assets_filepath == filepath



@pytest.mark.parametrize(("content","create"), [
	([], True),
	([], False),
	(["  'assetName1': 'desc_of_asset1'\n"], False),
	(["  'assetName1': 'desc_of_asset1'\n","  'assetName2': 'desc_of_asset2'\n","  'assetName3': 'desc_of_asset3'\n"], False)
])
def test_update_known_assets(asset, content, create):

	#create stub model-assets.yml file
	assets_filepath = os.path.join(MODEL_DIR, "model-assets"+ str(random.randint(1,1001)) +".yml")
	if not create:
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


@pytest.mark.parametrize(("assets_file","outcome","delete"), [
	(
		"model-assets.yml",
		{
			"assetName1":"desc_of_asset1",
			"assetName2":"desc_of_asset2",
			"assetName3":"desc_of_asset3"
		},
		False
	),
	(
		"model-assets_empty.yml",
		{},
		False
	),
	(
		"model-assets_fake.yml",
		{},
		True
	)
])
def test_fetch_known_assets(assets_file, outcome, delete):

	assets_filepath = os.path.join(MODEL_DIR, assets_file)
	known_assets = Asset.fetch_known_assets(assets_filepath)

	assert known_assets == outcome

	if delete:
		os.remove(assets_filepath)


def test_fetch_known_assets_exception():

	#create a corrupted file
	assets_filepath = os.path.join(MODEL_DIR, "model-assets"+ str(random.randint(1,1001)) +".yml")
	try:
		with open(assets_filepath, 'w') as configfile:
			configfile.write("\n")
	except IOError as e:
		print("Could not create assets file. "+ e.strerror)
		assert False

	with pytest.raises(ModellingException):
		known_assets = Asset.fetch_known_assets(assets_filepath)

	#cleanup
	os.remove(assets_filepath)