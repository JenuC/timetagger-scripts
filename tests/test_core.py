"""Tests for core functionality."""

import pytest
from pmt_profiler.core import MockMicroManager

def test_mock_micro_manager_loaded_devices(mock_mm):
    """Test that the mock Micro-Manager returns the expected loaded devices."""
    devices = mock_mm.getLoadedDevices()
    assert 'DCCHub' in devices
    assert 'DCCModule1' in devices
    assert 'Core' in devices

def test_mock_micro_manager_device_properties(mock_mm):
    """Test that the mock Micro-Manager returns the expected device properties."""
    props = mock_mm.getDevicePropertyNames('DCCHub')
    assert 'SimulateDevice' in props
    assert 'Simulated' in props
    assert 'UseModule1' in props

def test_mock_micro_manager_device_object(mock_mm):
    """Test that the mock Micro-Manager returns a device object with properties."""
    device = mock_mm.getDeviceObject('DCCHub')
    assert hasattr(device, 'properties')
    assert len(device.properties) > 0
    
    # Check that the properties have name and value attributes
    for prop in device.properties:
        assert hasattr(prop, 'name')
        assert hasattr(prop, 'value')
        
    # Check specific property values
    prop_names = [prop.name for prop in device.properties]
    assert 'SimulateDevice' in prop_names
    assert 'Simulated' in prop_names
    assert 'UseModule1' in prop_names 