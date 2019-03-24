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

# @pytest.fixture
# def entry_point():
# 	assets = {}
# 	for i in range(0,4):
# 		a = Asset("stub"+str(i),"stub_desc"+str(i), "stub_path"+str(i), "stub_path2"+str(i))

# 		a.add_technology("tech1","techdesc",{})
# 		a.add_technology("tech2","tech_desc",{"atr":"val"})
# 		a.add_technology("tech"+str(random.randint(0,100)),"tech_desc",{})

# 		assets[a.name] = a

# 	return EntryPoint("stub", "stub", assets)

# @pytest.mark.parametrize(("name","description", "assets"), [("router", "router descr", {})])
# def test_init(name, description, assets):
# 	'''create new EntryPoint
# 	'''
# 	entry_point = EntryPoint(name, description, assets)

# 	assert entry_point
# 	assert entry_point.name == name
# 	assert entry_point.description == description
# 	assert entry_point.assets_in_model == assets
# 	assert isinstance(entry_point.technologies_used, dict)
# 	assert isinstance(entry_point.threats, dict)


# @pytest.mark.parametrize(("name"), [
# 	"tech1", "tech2"
# ])
# def test_add_technology_ref(entry_point, name):
# 	entry_point.add_technology_ref(name)

# 	assert name in entry_point.technologies_used
# 	assert isinstance(entry_point.technologies_used[name], Technology)


# @pytest.mark.parametrize(("name"), [
# 	"tech1"
# ])
# def test_add_technology_ref_duplicate(entry_point, name):
# 	entry_point.add_technology_ref(name)

# 	with pytest.raises(ModellingException):
# 		entry_point.add_technology_ref(name)


# def test_add_technology_ref_non_existant(entry_point):
# 	with pytest.raises(ModellingException):
# 		entry_point.add_technology_ref("tech_non_existant")

