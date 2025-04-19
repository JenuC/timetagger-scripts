"""Tests for PMT functionality."""

import pytest
from unittest.mock import patch, MagicMock
from pmt_profiler.pmt import start_PMT, stop_PMT, start_cooler
from io import StringIO

@pytest.fixture
def mock_mm():
    """Create a mock MicroManager instance."""
    mock = MagicMock()
    mock.setProperty = MagicMock()
    return mock

def test_start_pmt_with_cooling(mock_mm):
    """Test starting the PMT with cooling."""
    start_PMT(mock_mm, gain=65, channel='C3', cooling_time=5.0)
    # Verify that properties were set correctly
    mock_mm.setProperty.assert_any_call('DCCModule1', 'C3_CoolerVoltage', 2.6)
    mock_mm.setProperty.assert_any_call('DCCModule1', 'C3_Cooling', 'On')
    mock_mm.setProperty.assert_any_call('DCCModule1', 'C3_CoolerCurrentLimit', 1.0)
    mock_mm.setProperty.assert_any_call('DCCModule1', 'C3_GainHV', 65)
    mock_mm.setProperty.assert_any_call('DCCModule1', 'EnableOutputs', 'On')
    mock_mm.setProperty.assert_any_call('DCCModule1', 'C3_Plus12V', 'On')

def test_start_pmt_without_cooling(mock_mm):
    """Test starting the PMT without cooling."""
    with patch('sys.stdout', new=StringIO()) as fake_out:
        start_PMT(mock_mm, gain=65, channel='C3', cooling_time=0)
        output = fake_out.getvalue()
        assert "Warning: PMT cooler is not being used!" in output
        
    # Verify that cooling properties were not set
    cooling_calls = [call for call in mock_mm.setProperty.call_args_list 
                    if any(prop in str(call) for prop in ['Cooling', 'CoolerVoltage', 'CoolerCurrentLimit'])]
    assert len(cooling_calls) == 0
    
    # Verify other properties were set
    mock_mm.setProperty.assert_any_call('DCCModule1', 'C3_GainHV', 65)
    mock_mm.setProperty.assert_any_call('DCCModule1', 'EnableOutputs', 'On')
    mock_mm.setProperty.assert_any_call('DCCModule1', 'C3_Plus12V', 'On')

def test_start_cooler_custom_time(mock_mm):
    """Test starting the cooler with custom cooling time."""
    with patch('time.sleep') as mock_sleep:
        start_cooler(mock_mm, channel='C3', cooling_time=3.0)
        assert mock_sleep.call_count == 3

def test_stop_pmt(mock_mm):
    """Test stopping the PMT."""
    stop_PMT(mock_mm, gain=0, channel='C3')
    # Verify that all properties are set to off/0
    mock_mm.setProperty.assert_any_call('DCCModule1', 'C3_GainHV', 0)
    mock_mm.setProperty.assert_any_call('DCCModule1', 'EnableOutputs', 'Off')
    mock_mm.setProperty.assert_any_call('DCCModule1', 'C3_Plus12V', 'Off')
    mock_mm.setProperty.assert_any_call('DCCModule1', 'C3_Cooling', 'Off') 