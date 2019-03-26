#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
application EntryPoint testing set

By sarunasil
"""

import pytest
import random
import os


from iotpentool.threatmodel import ThreatModel
from iotpentool.entrypoint import EntryPoint
from iotpentool.asset import Asset
from iotpentool.technology import Technology
from iotpentool.utils import ModellingException

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
MODEL_DIR = os.path.join(CURRENT_DIR, "stub_model")

@pytest.fixture
def asset():
	return Asset("stub","stub","stub")

@pytest.fixture
def entry_point():
	return EntryPoint("stub","stub","stub_asset","stub_filepath")

@pytest.mark.parametrize(("name","description", "filepath"), [("web page", "web page descr", "stub_filepath")])
def test_init(name, description, asset, filepath):
	'''create new EntryPoint
	'''

	entry_point = EntryPoint(name, description, asset, filepath)

	assert entry_point
	assert entry_point.name == name
	assert entry_point.description == description
	assert entry_point.asset_used == asset
	assert entry_point.entry_points_filepath == filepath


@pytest.mark.parametrize(("content","create"), [
	([], True),
	([], False),
	(["  'entry_pointName1': 'desc_of_entry_point1'\n"], False),
	(["  'entry_pointName1': 'desc_of_entry_point1'\n","  'entry_pointName2': 'desc_of_entry_point2'\n","  'entry_pointName3': 'desc_of_entry_point3'\n"], False)
])
def test_update_known_entry_points(entry_point, content, create):

	#create stub model-entry_points.yml file
	entry_points_filepath = os.path.join(MODEL_DIR, "model-entry_points"+ str(random.randint(1,1001)) +".yml")
	if not create:
		try:
			with open(entry_points_filepath, 'w') as configfile:
				configfile.write("entry_points:\n")
				configfile.writelines(content)
		except IOError as e:
			print("Could not create entry_points file. "+ e.strerror)
			assert False
	entry_point.entry_points_filepath = entry_points_filepath

	#get prev entry_points
	prev_known_entry_points = EntryPoint.fetch_known_entry_points(entry_points_filepath)

	#update entry_points file
	entry_point.update_known_entry_points()

	#get current entry_points
	current_known_entry_points = EntryPoint.fetch_known_entry_points(entry_points_filepath)

	#delete that file
	os.remove(entry_points_filepath)

	#check that prev_entry_points + added entry_point == current_asssets
	assert { **prev_known_entry_points, **{entry_point.name: entry_point.description} } == current_known_entry_points


@pytest.mark.parametrize(("entry_points_file","outcome","delete"), [
	(
		"model-entry_points_fetch.yml",
		{
			"entry_pointName1":"desc_of_entry_point1",
			"entry_pointName2":"desc_of_entry_point2",
			"entry_pointName3":"desc_of_entry_point3"
		},
		False
	),
	(
		"model-entry_points_empty.yml",
		{},
		False
	),
	(
		"model-entry_points_fake.yml",
		{},
		True
	)
])
def test_fetch_known_entry_points(entry_points_file, outcome, delete):

	entry_points_filepath = os.path.join(MODEL_DIR, entry_points_file)
	known_entry_points = EntryPoint.fetch_known_entry_points(entry_points_filepath)

	assert known_entry_points == outcome

	if delete:
		os.remove(entry_points_filepath)


def test_fetch_known_entry_points_exception():

	#create a corrupted file
	entry_points_filepath = os.path.join(MODEL_DIR, "model-entry_points"+ str(random.randint(1,1001)) +".yml")
	try:
		with open(entry_points_filepath, 'w') as entry_points_file:
			entry_points_file.write("\n")
	except IOError as e:
		print("Could not create entry_points file. "+ e.strerror)
		assert False

	with pytest.raises(ModellingException):
		known_entry_points = EntryPoint.fetch_known_entry_points(entry_points_filepath)

	#cleanup
	os.remove(entry_points_filepath)
