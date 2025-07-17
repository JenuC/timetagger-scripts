"""Tests for the MDO32 oscilloscope module."""

import os
import pytest
from unittest.mock import MagicMock, patch
from pmt_profiler.mdo32 import (
    connect_to_oscilloscope,
    load_settings,
    capture_waveform,
    export_waveform
)

@pytest.fixture
def mock_scope():
    """Create a mock oscilloscope instance."""
    scope = MagicMock()
    scope.model = "MDO32"
    scope.resource_name = "TCPIP0::192.168.1.100::inst0::INSTR"
    scope.commands = MagicMock()
    return scope

@pytest.fixture
def mock_device_manager():
    """Create a mock device manager."""
    with patch("pmt_profiler.mdo32.DeviceManager") as mock_dm:
        mock_dm_instance = MagicMock()
        mock_dm.return_value = mock_dm_instance
        mock_dm_instance.add_mdo3k.return_value = MagicMock()
        mock_dm_instance.list_devices.return_value = ["TCPIP0::192.168.1.100::inst0::INSTR"]
        yield mock_dm

def test_connect_to_oscilloscope_with_ip(mock_device_manager):
    """Test connecting to oscilloscope with IP address."""
    scope = connect_to_oscilloscope("192.168.1.100")
    assert scope is not None
    mock_device_manager.return_value.add_mdo3k.assert_called_once_with("192.168.1.100")

def test_connect_to_oscilloscope_auto_discover(mock_device_manager):
    """Test connecting to oscilloscope with auto-discovery."""
    scope = connect_to_oscilloscope()
    assert scope is not None
    mock_device_manager.return_value.list_devices.assert_called_once_with(device_type="MDO3K")
    mock_device_manager.return_value.add_mdo3k.assert_called_once_with("TCPIP0::192.168.1.100::inst0::INSTR")

def test_connect_to_oscilloscope_no_devices(mock_device_manager):
    """Test connecting to oscilloscope when no devices are found."""
    mock_device_manager.return_value.list_devices.return_value = []
    with pytest.raises(RuntimeError, match="No MDO3K oscilloscopes found"):
        connect_to_oscilloscope()

def test_load_settings(mock_scope, tmp_path):
    """Test loading settings from a file."""
    # Create a temporary settings file
    settings_file = tmp_path / "test_settings.set"
    settings_file.write_text("dummy settings")
    
    load_settings(mock_scope, str(settings_file))
    mock_scope.commands.recall.setup.write.assert_called_once_with(f'"{str(settings_file)}"')

def test_load_settings_file_not_found(mock_scope):
    """Test loading settings when file doesn't exist."""
    with pytest.raises(FileNotFoundError):
        load_settings(mock_scope, "nonexistent.set")

def test_capture_waveform(mock_scope):
    """Test capturing a waveform."""
    # Mock the acquisition state query to simulate completion
    mock_scope.commands.acquire.state.query.side_effect = ["RUN", "STOP"]
    
    capture_waveform(mock_scope, channel=1)
    
    mock_scope.commands.acquire.state.write.assert_called_once_with("RUN")
    mock_scope.commands.acquire.stopafter.write.assert_called_once_with("SEQUENCE")
    mock_scope.commands.acquire.numacq.write.assert_called_once_with(1)

def test_export_waveform(mock_scope):
    """Test exporting a waveform."""
    filename = "test_waveform.csv"
    
    result = export_waveform(mock_scope, channel=1, filename=filename)
    
    assert result == filename
    mock_scope.commands.data.source.write.assert_called_once_with("CH1")
    mock_scope.commands.data.start.write.assert_called_once_with(1)
    mock_scope.commands.data.stop.write.assert_called_once_with(1000)
    mock_scope.commands.data.encdg.write.assert_called_once_with("ASCII")
    mock_scope.commands.data.filename.write.assert_called_once_with(f'"{filename}"')
    mock_scope.commands.data.export.write.assert_called_once()

def test_export_waveform_default_filename(mock_scope):
    """Test exporting a waveform with default filename."""
    with patch("pmt_profiler.mdo32.datetime") as mock_datetime:
        mock_datetime.now.return_value.strftime.return_value = "20240101_120000"
        result = export_waveform(mock_scope, channel=1)
        
        assert result == "waveform_ch1_20240101_120000.csv" 