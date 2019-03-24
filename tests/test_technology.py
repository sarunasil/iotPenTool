#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
application Technology class testing set

By sarunasil
"""

import pytest
import random
import os


from iotpentool.threatmodel import ThreatModel
from iotpentool.technology import Technology
from iotpentool.utils import ModellingException

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
MODEL_DIR = os.path.join(CURRENT_DIR, "stub_model")

@pytest.fixture
def technology():
	return Technology("stub","stub", {"attr1":"value1","stub2":"stub_value2"},"stub")

@pytest.mark.parametrize(("name","description", "attributes", "tech_filepath"), [
	(
		"HTTP",
		"BLABLABLA about HTTP",
		{
			"Header":"Host: net.tutsplus.com User-Agent: Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729) Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
		},
		"stub"
	),
	(
		"HTTP",
		"BLABLABLA about HTTP",
		{
			"Header":"Host: asldkjas",
			"Smth_more":"morevalue"
		},
		"stub1"
	),
	(
		"HTTP",
		"BLABLABLA about HTTP",
		{},
		"stub2"
	)
])
def test_init(name, description, attributes, tech_filepath):
	'''create new Asset
	'''

	technology = Technology(name, description, attributes, tech_filepath)

	assert technology
	assert technology.name == name
	assert technology.description == description
	assert technology.attributes == attributes
	assert technology.tech_filepath == tech_filepath
	assert isinstance(technology.used_in, dict)


@pytest.mark.parametrize(("content","create"), [
	([], True),
	([], False),
	(
		[
			"  'techName1':\n",
			"    name: 'techName1'\n",
			"    description: 'desc_of_tech1'\n",
			"    attributes: \n",
			"      'attribute1Name': 'value1'\n",
			"      'attribute2Name': 'value2'\n"
		],
		False
	),
	(
		[
			"  'techName1':\n",
			"    name: 'techName1'\n",
			"    description: 'desc_of_tech1'\n",
			"    attributes: \n",
			"      'attribute1Name': 'value1'\n",
			"      'attribute2Name': 'value2'\n",
			"  'techName2':\n",
			"    name: 'techName2'\n",
			"    description: 'desc_of_tech2'\n",
			"    attributes: \n",
			"      'attribute22Name': 'value22'\n",
			"      'attribute232Name': 'value33'\n",
		], False
	)
])
def test_update_known_technologies(technology, content, create):
	#create stub model-technologies.yml file
	tech_filepath = os.path.join(MODEL_DIR, "model-technologies"+ str(random.randint(1,1001)) +".yml")
	if not create:
		try:
			with open(tech_filepath, 'w') as configfile:
				configfile.write("technologies:\n")
				configfile.writelines(content)
		except IOError as e:
			print("Could not create technologies file. "+ e.strerror)
			assert False
	technology.tech_filepath = tech_filepath

	#get prev technologies
	prev_known_technologies = Technology.fetch_known_technologies(tech_filepath)

	#update technologies file
	technology.update_known_technologies()

	#get current technologies
	current_known_technologies = Technology.fetch_known_technologies(tech_filepath)

	#delete that file
	os.remove(tech_filepath)

	current_tech = {
		technology.name:{
			"name": technology.name,
			"description": technology.description,
			"attributes": technology.attributes
		}
	}
	#check that prev_technologies + added technology == current_technologies
	assert { **prev_known_technologies, **current_tech } == current_known_technologies


@pytest.mark.parametrize(("tech_file","outcome","delete"), [
	(
		"model-technologies_fetch.yml",
		{
  			"techName1":{
				"name": "techName1",
				"description": "desc_of_tech1",
				"attributes":{
					"attribute1Name": "value1",
					"attribute2Name": "value2"
				}
			},
    		"techName2":{
				"name": "techName2",
				"description": "desc_of_tech2",
				"attributes":{
					"attribute22Name": "value22",
					"attribute232Name": "value33"
				}
			}
		},
		False
	),
	(
		"model-technologies_empty.yml",
		{},
		False
	),
	(
		"model-technologies_fake.yml",
		{},
		True
	)
])
def test_fetch_known_technologies(tech_file, outcome, delete):

	tech_filepath = os.path.join(MODEL_DIR, tech_file)
	known_technologies = Technology.fetch_known_technologies(tech_filepath)

	assert known_technologies == outcome

	if delete:
		os.remove(tech_filepath)


def test_fetch_known_technologies_exception():

	#create a corrupted file
	tech_filepath = os.path.join(MODEL_DIR, "model-technologies"+ str(random.randint(1,1001)) +".yml")
	try:
		with open(tech_filepath, 'w') as tech_file:
			tech_file.write("\n")
	except IOError as e:
		print("Could not create technologies file. "+ e.strerror)
		assert False

	with pytest.raises(ModellingException):
		known_technologies = Technology.fetch_known_technologies(tech_filepath)

	#cleanup
	os.remove(tech_filepath)

