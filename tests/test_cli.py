"""Tests for CLI functionality."""

import pytest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys
from pmt_profiler.cli import main
from pmt_profiler.core import MockMicroManager

# Mock the MicroManager class to prevent it from trying to load real hardware
@patch('pmt_profiler.core.MicroManager')
def test_cli_help(mock_micro_manager):
    """Test that the help message is displayed correctly."""
    with patch('sys.argv', ['pmt-profiler', '--help']), \
         patch('sys.stdout', new=StringIO()) as fake_out:
        with pytest.raises(SystemExit):
            main()
        output = fake_out.getvalue()
        # Check for key help message components
        assert "PMT Profiler" in output
        assert "usage:" in output.lower()  # Case-insensitive check
        assert "--pmt" in output  # Check for PMT option
        assert "start" in output  # Check for start command
        assert "stop" in output   # Check for stop command
        assert "--info" in output # Check for info option
        assert "Examples:" in output  # Check for examples section

@patch('pmt_profiler.core.MicroManager')
def test_cli_start_pmt_mock(mock_micro_manager):
    """Test starting the PMT in mock mode with default cooling time."""
    # Configure the mock to return a MockMicroManager instance
    mock_micro_manager.return_value = MockMicroManager()
    
    with patch('sys.stdout', new=StringIO()) as fake_out:
        with patch('sys.argv', ['pmt_profiler.cli', '--mock', '--pmt', 'start', '--gain', '65', '--channel', 'C3']):
            main()
        output = fake_out.getvalue()
        assert "PMT started on channel C3 with gain 65" in output

@patch('pmt_profiler.core.MicroManager')
def test_cli_start_pmt_no_cooling(mock_micro_manager):
    """Test starting the PMT in mock mode with no cooling."""
    # Configure the mock to return a MockMicroManager instance
    mock_micro_manager.return_value = MockMicroManager()
    
    with patch('sys.stdout', new=StringIO()) as fake_out:
        with patch('sys.argv', ['pmt_profiler.cli', '--mock', '--pmt', 'start', '--gain', '65', '--channel', 'C3', '--cooling-time', '0']):
            main()
        output = fake_out.getvalue()
        assert "PMT started on channel C3 with gain 65" in output
        assert "Warning: PMT cooler is not being used!" in output
        assert "Starting PMT cooler" not in output

@patch('pmt_profiler.core.MicroManager')
def test_cli_start_pmt_custom_cooling(mock_micro_manager):
    """Test starting the PMT in mock mode with custom cooling time."""
    # Configure the mock to return a MockMicroManager instance
    mock_micro_manager.return_value = MockMicroManager()
    
    with patch('sys.stdout', new=StringIO()) as fake_out:
        with patch('sys.argv', ['pmt_profiler.cli', '--mock', '--pmt', 'start', '--gain', '65', '--channel', 'C3', '--cooling-time', '3']):
            main()
        output = fake_out.getvalue()
        assert "PMT started on channel C3 with gain 65" in output
        assert "Starting PMT cooler" in output

@patch('pmt_profiler.core.MicroManager')
def test_cli_stop_pmt_mock(mock_micro_manager):
    """Test stopping the PMT in mock mode."""
    # Configure the mock to return a MockMicroManager instance
    mock_micro_manager.return_value = MockMicroManager()
    
    with patch('sys.stdout', new=StringIO()) as fake_out:
        with patch('sys.argv', ['pmt_profiler.cli', '--mock', '--pmt', 'stop']):
            main()
        output = fake_out.getvalue()
        assert "PMT stopped on channel C3" in output

@patch('pmt_profiler.core.MicroManager')
def test_cli_info_mock(mock_micro_manager):
    """Test displaying device information in mock mode."""
    # Create a mock MicroManager instance with the necessary methods
    mock_mm = MagicMock()
    
    # Mock getLoadedDevices
    mock_mm.getLoadedDevices.return_value = ['DCCHub', 'DCCModule1', 'Core']
    
    # Mock getDevicePropertyNames
    mock_mm.getDevicePropertyNames.side_effect = lambda device: {
        'DCCHub': ['SimulateDevice', 'Simulated', 'UseModule1', 'UseModule2', 'UseModule3'],
        'DCCModule1': ['EnableOutputs', 'C3_GainHV', 'C3_Plus12V', 'C4_GainHV', 'C4_Plus12V'],
        'Core': ['AutoFocus', 'AutoShutter', 'Camera', 'ChannelGroup', 'Focus', 'Galvo', 'ImageProcessor']
    }.get(device, [])
    
    # Mock getDeviceAdapterNames
    mock_mm.getDeviceAdapterNames.return_value = ['BH_DCC', 'BH_DCC_DCU', 'Core', 'DemoCamera', 'DemoXYStage']
    
    # Mock getProperty
    mock_mm.getProperty.side_effect = lambda device, prop: {
        'DCCHub': {
            'SimulateDevice': 'No',
            'Simulated': 'No',
            'UseModule1': 'Yes',
            'UseModule2': 'No',
            'UseModule3': 'No'
        },
        'DCCModule1': {
            'EnableOutputs': 'Off',
            'C3_GainHV': '0',
            'C3_Plus12V': 'Off',
            'C4_GainHV': '0',
            'C4_Plus12V': 'Off'
        }
    }.get(device, {}).get(prop, 'Unknown')
    
    # Configure the mock to return our custom mock
    mock_micro_manager.return_value = mock_mm
    
    with patch('sys.stdout', new=StringIO()) as fake_out:
        with patch('sys.argv', ['pmt_profiler.cli', '--mock', '--info']):
            main()
        output = fake_out.getvalue()
        
        # Check for key elements in the output without being too strict about formatting
        assert "Device Information" in output
        assert "DCCHub" in output
        assert "DCCModule1" in output
        assert "Core" in output
        
        # Check that property values are being retrieved
        assert "SimulateDevice" in output
        assert "EnableOutputs" in output
        assert "C3_GainHV" in output
        
        # Check that BH devices are NOT shown by default
        assert "BH Devices Available" not in output

@patch('pmt_profiler.core.MicroManager')
def test_cli_info_detailed_mock(mock_micro_manager):
    """Test displaying detailed device information in mock mode."""
    # Create a mock MicroManager instance with the necessary methods
    mock_mm = MagicMock()
    
    # Mock getLoadedDevices
    mock_mm.getLoadedDevices.return_value = ['DCCHub', 'DCCModule1', 'Core']
    
    # Mock getDevicePropertyNames
    mock_mm.getDevicePropertyNames.side_effect = lambda device: {
        'DCCHub': ['SimulateDevice', 'Simulated', 'UseModule1', 'UseModule2', 'UseModule3'],
        'DCCModule1': ['EnableOutputs', 'C3_GainHV', 'C3_Plus12V', 'C4_GainHV', 'C4_Plus12V'],
        'Core': ['AutoFocus', 'AutoShutter', 'Camera', 'ChannelGroup', 'Focus', 'Galvo', 'ImageProcessor']
    }.get(device, [])
    
    # Mock getDeviceAdapterNames
    mock_mm.getDeviceAdapterNames.return_value = ['BH_DCC', 'BH_DCC_DCU', 'Core', 'DemoCamera', 'DemoXYStage']
    
    # Mock getProperty
    mock_mm.getProperty.side_effect = lambda device, prop: {
        'DCCHub': {
            'SimulateDevice': 'No',
            'Simulated': 'No',
            'UseModule1': 'Yes',
            'UseModule2': 'No',
            'UseModule3': 'No'
        },
        'DCCModule1': {
            'EnableOutputs': 'Off',
            'C3_GainHV': '0',
            'C3_Plus12V': 'Off',
            'C4_GainHV': '0',
            'C4_Plus12V': 'Off'
        }
    }.get(device, {}).get(prop, 'Unknown')
    
    # Configure the mock to return our custom mock
    mock_micro_manager.return_value = mock_mm
    
    with patch('sys.stdout', new=StringIO()) as fake_out:
        with patch('sys.argv', ['pmt_profiler.cli', '--mock', '--info', '--detailed']):
            main()
        output = fake_out.getvalue()
        
        # Check for key elements in the output without being too strict about formatting
        assert "Device Information" in output
        assert "DCCHub" in output
        assert "DCCModule1" in output
        assert "Core" in output
        
        # Check that property values are being retrieved
        assert "SimulateDevice" in output
        assert "EnableOutputs" in output
        assert "C3_GainHV" in output
        
        # Check that BH devices ARE shown with --detailed
        assert "BH_DCC" in output
        assert "BH_DCC_DCU" in output

@patch('pmt_profiler.core.MicroManager')
def test_cli_invalid_pmt_option(mock_micro_manager):
    """Test handling of invalid PMT option."""
    # Configure the mock to return a MockMicroManager instance
    mock_micro_manager.return_value = MockMicroManager()
    
    with patch('sys.stderr', new=StringIO()) as fake_err:
        with patch('sys.argv', ['pmt_profiler.cli', '--pmt', 'invalid']):
            with pytest.raises(SystemExit):
                main()
        output = fake_err.getvalue()
        assert "error: argument --pmt: invalid choice: 'invalid'" in output

@patch('pmt_profiler.core.MicroManager')
def test_cli_invalid_gain(mock_micro_manager):
    """Test handling of invalid gain value."""
    # Configure the mock to return a MockMicroManager instance
    mock_micro_manager.return_value = MockMicroManager()
    
    with patch('sys.stderr', new=StringIO()) as fake_err:
        with patch('sys.argv', ['pmt_profiler.cli', '--pmt', 'start', '--gain', 'invalid']):
            with pytest.raises(SystemExit):
                main()
        output = fake_err.getvalue()
        assert "error: argument --gain: invalid int value: 'invalid'" in output 