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


# @pytest.mark.parametrize()
def test_add_entry_point():
    '''adding new EntryPoint
    '''
    assert True


# @pytest.mark.parametrize()
def test_add_entry_point_duplicate():
    '''adding new asset to model
    '''
    assert True
