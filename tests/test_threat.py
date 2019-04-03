#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
IoT Penetration testing toolset
application Threat testing set

By sarunasil
"""

import pytest
import random
import os


from iotpentool.threat import *
from iotpentool.entrypoint import EntryPoint
from iotpentool.technology import Technology

@pytest.fixture
def dread_score():
	return DreadScore([
		random.randint(0,4),
		random.randint(0,4),
		random.randint(0,4),
		random.randint(0,4),
		random.randint(0,4)
		])

@pytest.fixture
def entry_point():
	return EntryPoint("stub"+ str(random.randint(1,1001)),"stub","stub_asset","stub_filepath")

@pytest.fixture
def technologies():
	techs = {}
	for i in range(0,3):
		tech_name = "stub"+ str(random.randint(1,1001))
		tech = Technology(tech_name,"stub"+ str(random.randint(1,1001)), {"attr1":"value1","stub2":"stub_value2"}, {},"stub")
		techs[tech_name] = tech

	return techs

@pytest.mark.parametrize(("desc","target", "attack_tech", "countermeasures", "uid"), [
	("some threat bla bla", "all people of the World", "the best ever", "eating nutella", "123:456:789")
])
def test_init(desc,target, attack_tech, countermeasures, uid, entry_point, technologies, dread_score):
	'''create new Threat
	'''

	threat = Threat(desc,target, attack_tech, countermeasures, entry_point, technologies, dread_score, uid)

	assert isinstance(threat, Threat)
	assert threat.description == desc
	assert threat.target == target
	assert threat.attack_tech == attack_tech
	assert threat.countermeasures == countermeasures
	assert threat.entry_point_used == entry_point
	assert isinstance(threat.entry_point_used, EntryPoint)
	assert threat.technologies_used == technologies
	for _, tech in threat.technologies_used.items():
		assert isinstance(tech, Technology)
	assert threat.dread == dread_score
	assert isinstance(threat.dread, DreadScore)


@pytest.mark.parametrize(("damag", "repro", "exploi", "affec", "disco", "total"), [
	(0, 0, 2, 0, 1, 3),
	(0, 0, 3, 0, 4, 0),
	(0, 0, -1, 0, 2, 0)
])
def test_init_dreadscore(damag, repro, exploi, affec, disco, total):
	'''create new DreadScore
	'''

	dread_score = DreadScore([damag, repro, exploi, affec, disco])

	assert dread_score.total == total

