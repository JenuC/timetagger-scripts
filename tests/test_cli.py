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
    """Test that the help message is displayed when no arguments are provided."""
    # Configure the mock to return a MockMicroManager instance
    mock_micro_manager.return_value = MockMicroManager()
    
    with patch('sys.stdout', new=StringIO()) as fake_out:
        with patch('sys.argv', ['pmt_profiler.cli']):
            main()
        output = fake_out.getvalue()
        assert "PMT Profiler Analysis Tool" in output
        assert "--pmt" in output
        assert "--gain" in output
        assert "--channel" in output
        assert "--mock" in output
        assert "--info" in output

@patch('pmt_profiler.core.MicroManager')
def test_cli_start_pmt_mock(mock_micro_manager):
    """Test starting the PMT in mock mode."""
    # Configure the mock to return a MockMicroManager instance
    mock_micro_manager.return_value = MockMicroManager()
    
    with patch('sys.stdout', new=StringIO()) as fake_out:
        with patch('sys.argv', ['pmt_profiler.cli', '--mock', '--pmt', 'start', '--gain', '65', '--channel', 'C3']):
            main()
        output = fake_out.getvalue()
        assert "PMT started on channel C3 with gain 65" in output

@patch('pmt_profiler.core.MicroManager')
def test_cli_stop_pmt_mock(mock_micro_manager):
    """Test stopping the PMT in mock mode."""
    # Configure the mock to return a MockMicroManager instance
    mock_micro_manager.return_value = MockMicroManager()
    
    with patch('sys.stdout', new=StringIO()) as fake_out:
        with patch('sys.argv', ['pmt_profiler.cli', '--mock', '--pmt', 'stop', '--channel', 'C3']):
            main()
        output = fake_out.getvalue()
        assert "PMT stopped on channel C3" in output

@patch('pmt_profiler.core.MicroManager')
def test_cli_info_mock(mock_micro_manager):
    """Test displaying device information in mock mode."""
    # Configure the mock to return a MockMicroManager instance
    mock_micro_manager.return_value = MockMicroManager()
    
    with patch('sys.stdout', new=StringIO()) as fake_out:
        with patch('sys.argv', ['pmt_profiler.cli', '--mock', '--info']):
            main()
        output = fake_out.getvalue()
        assert "Loaded devices:" in output
        assert "DCCHub" in output
        assert "DCCModule1" in output
        assert "Core" in output

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